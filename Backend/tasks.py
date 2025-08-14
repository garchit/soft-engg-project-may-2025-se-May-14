import os
import re
from celery_worker import celery
from factory import create_app
from models import db
from models.teacher import Teacher
from models.user_teacher import UserTeacher
from models.user import User
from models.unit import Unit as Course
from models.user_course import UserCourse
from models.streaklog import StreakLog
from models.badges import Badge, badge_user
from email_utils import send_mail
import google.generativeai as genai
from datetime import date, datetime, timedelta
from sqlalchemy import func

# Create Flask app instance
app = create_app()


def validate_email(email):
    """Simple email validation."""
    if not email or not isinstance(email, str):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None


def get_teacher_classes(teacher_id):
    """Get all classes associated with a teacher."""
    class_names = (
        db.session.query(User.user_class)
        .join(UserTeacher, UserTeacher.user_id == User.id)
        .filter(UserTeacher.teacher_id == teacher_id)
        .filter(User.user_class.is_not(None))
        .filter(User.user_class != '')
        .distinct()
        .all()
    )
    return [cls[0] for cls in class_names if cls[0]]


def calculate_student_rank(student_data, all_students_data):
    """Calculate student rank based on performance score."""
    def performance_score(s):
        return (s['completion_rate'] * 0.4 + s['avg_marks'] * 0.3 + s['engagement_score'] * 0.3)
    
    sorted_students = sorted(all_students_data, key=performance_score, reverse=True)
    student_id = student_data['student'].id
    for rank, student in enumerate(sorted_students, 1):
        if student['student'].id == student_id:
            return rank
    return len(all_students_data)


def get_student_badges_info(student_id):
    """Get detailed badge information for a student."""
    badges_data = (
        db.session.query(Badge.name, Badge.points, Badge.description)
        .join(badge_user, badge_user.c.badge_id == Badge.id)
        .filter(badge_user.c.user_id == student_id)
        .all()
    )
    
    return {
        'badge_count': len(badges_data),
        'total_badge_points': sum(badge.points for badge in badges_data)
    }


def generate_class_summary_for_teacher(teacher_id, class_name):
    """Generate comprehensive class summary for a specific teacher and class."""
    students = (
        db.session.query(User)
        .join(UserTeacher, UserTeacher.user_id == User.id)
        .filter(UserTeacher.teacher_id == teacher_id)
        .filter(User.user_class == class_name)
        .all()
    )
    
    if not students:
        return None, f"No students found for teacher in class {class_name}"

    total_courses = Course.query.count()
    student_data = []
    
    for student in students:
        completed_courses_query = (
            db.session.query(Course, UserCourse.marks_scored)
            .join(UserCourse, UserCourse.course_id == Course.id)
            .filter(UserCourse.user_id == student.id)
        )
        completed_courses = completed_courses_query.all()
        completion_rate = (len(completed_courses) / total_courses * 100) if total_courses > 0 else 0

        marks_data = [c.marks_scored for c in completed_courses if c.marks_scored is not None]
        avg_marks = sum(marks_data) / len(marks_data) if marks_data else 0
        current_streak = student.streak or 0
        
        recent_activity = (
            db.session.query(StreakLog)
            .filter_by(user_id=student.id)
            .filter(StreakLog.checkin_date >= date.today() - timedelta(days=7))
            .count()
        )

        badge_info = get_student_badges_info(student.id)

        # Engagement score calculation
        engagement_score = 0
        if student.latest_timestamp:
            days_since_last_activity = (datetime.now() - student.latest_timestamp).days
            if days_since_last_activity <= 1:
                engagement_score += 40
            elif days_since_last_activity <= 3:
                engagement_score += 25
            elif days_since_last_activity <= 7:
                engagement_score += 10
        
        engagement_score += min(30, recent_activity * 5)
        engagement_score += min(30, (student.rewards or 0) / 10)
        engagement_score = min(100, engagement_score)

        student_data.append({
            'student': student,
            'completion_rate': completion_rate,
            'avg_marks': avg_marks,
            'current_streak': current_streak,
            'recent_activity': recent_activity,
            'badges_earned': badge_info['badge_count'],
            'badge_info': badge_info,
            'engagement_score': engagement_score,
            'courses_completed': len(completed_courses),
            'rewards': student.rewards or 0
        })

    # Calculate ranks for all students
    for student in student_data:
        student['class_rank'] = calculate_student_rank(student, student_data)

    # Calculate class statistics
    total_students = len(student_data)
    avg_completion = sum(s['completion_rate'] for s in student_data) / total_students
    avg_marks = sum(s['avg_marks'] for s in student_data) / total_students
    avg_engagement = sum(s['engagement_score'] for s in student_data) / total_students
    avg_badges = sum(s['badges_earned'] for s in student_data) / total_students
    total_badge_points = sum(s['badge_info']['total_badge_points'] for s in student_data)
    highly_engaged = len([s for s in student_data if s['engagement_score'] >= 80])
    low_engagement = len([s for s in student_data if s['engagement_score'] < 40])
    
    def performance_score(s):
        return (s['completion_rate'] * 0.4 + s['avg_marks'] * 0.3 + s['engagement_score'] * 0.3)
    
    sorted_students = sorted(student_data, key=performance_score, reverse=True)
    top_performers = sorted_students[:3]
    needs_attention = [s for s in student_data if s['engagement_score'] < 40][:3]
    top_badge_earners = sorted(student_data, key=lambda x: x['badge_info']['total_badge_points'], reverse=True)[:3]
    
    return class_name, {
        'class_name': class_name,
        'total_students': total_students,
        'avg_completion': avg_completion,
        'avg_marks': avg_marks,
        'avg_engagement': avg_engagement,
        'avg_badges': avg_badges,
        'total_badge_points': total_badge_points,
        'highly_engaged': highly_engaged,
        'low_engagement': low_engagement,
        'top_performers': top_performers,
        'needs_attention': needs_attention,
        'top_badge_earners': top_badge_earners
    }


def setup_gemini_client():
    """Setup Gemini AI client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')


def generate_ai_report_for_teacher(client, teacher, class_data):
    """Generate short AI report for teacher using Gemini."""
    if client and class_data:
        try:
            class_name = class_data['class_name']
            prompt = (
                f"Write a brief, encouraging class report for Teacher {teacher.name} for Class {class_name}. "
                f"Key stats: {class_data['total_students']} students, {class_data['avg_completion']:.0f}% completion, "
                f"{class_data['avg_engagement']:.0f}/100 engagement, {class_data['avg_badges']:.1f} avg badges earned, "
                f"{class_data['total_badge_points']} total badge points. {class_data['highly_engaged']} highly engaged, "
                f"{class_data['low_engagement']} need attention. "
                f"Top performers: {', '.join([s['student'].full_name for s in class_data['top_performers']])}. "
                f"Top badge earners: {', '.join([s['student'].full_name for s in class_data['top_badge_earners']])}. "
                "Keep it to 3-4 sentences max, positive and actionable."
            )
            
            response = client.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=150,
                    temperature=0.7,
                ),
            )
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"AI generation error for teacher {teacher.name}: {e}")
    
    # Fallback short report
    if class_data:
        return (f"Class {class_data['class_name']} shows good progress with "
                f"{class_data['avg_completion']:.0f}% average completion and {class_data['avg_badges']:.1f} badges per student. "
                f"{class_data['highly_engaged']} students are highly engaged. "
                f"Keep supporting the {class_data['low_engagement']} students who need attention.")
    
    return "Class performance data is being updated."


def create_attractive_email_html(teacher, class_reports_data, month_year):
    """Create attractive HTML email template with rank and badges information."""
    
    class_cards_html = ""
    for class_data, ai_summary in class_reports_data:
        # Determine class health status
        avg_engagement = class_data['avg_engagement']
        if avg_engagement >= 80:
            health_color, health_status, health_icon = "#28a745", "Excellent", "🌟"
        elif avg_engagement >= 60:
            health_color, health_status, health_icon = "#ffc107", "Good", "👍"
        else:
            health_color, health_status, health_icon = "#dc3545", "Needs Focus", "⚠️"
        
        class_cards_html += f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 15px; padding: 25px; margin: 20px 0; 
                    box-shadow: 0 8px 25px rgba(0,0,0,0.15); color: white;">
            <h2 style="margin: 0 0 15px 0; font-size: 24px; font-weight: 600;">
                📚 Class {class_data['class_name']}
            </h2>
            
            <div style="display: flex; flex-wrap: wrap; gap: 15px; margin: 20px 0;">
                <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; 
                           backdrop-filter: blur(10px); min-width: 120px; text-align: center;">
                    <div style="font-size: 28px; font-weight: bold; margin-bottom: 5px;">
                        {class_data['total_students']}
                    </div>
                    <div style="font-size: 12px; opacity: 0.9;">Students</div>
                </div>
                
                <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; 
                           backdrop-filter: blur(10px); min-width: 120px; text-align: center;">
                    <div style="font-size: 28px; font-weight: bold; margin-bottom: 5px;">
                        {class_data['avg_completion']:.0f}%
                    </div>
                    <div style="font-size: 12px; opacity: 0.9;">Completion</div>
                </div>
                
                <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; 
                           backdrop-filter: blur(10px); min-width: 120px; text-align: center;">
                    <div style="font-size: 28px; font-weight: bold; margin-bottom: 5px;">
                        {class_data['avg_marks']:.0f}
                    </div>
                    <div style="font-size: 12px; opacity: 0.9;">Avg Score</div>
                </div>
                
                <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; 
                           backdrop-filter: blur(10px); min-width: 120px; text-align: center;">
                    <div style="font-size: 28px; font-weight: bold; margin-bottom: 5px;">
                        🏆 {class_data['avg_badges']:.1f}
                    </div>
                    <div style="font-size: 12px; opacity: 0.9;">Avg Badges</div>
                </div>
                
                <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; 
                           backdrop-filter: blur(10px); min-width: 120px; text-align: center;">
                    <div style="font-size: 28px; font-weight: bold; margin-bottom: 5px;">
                        🎖️ {class_data['total_badge_points']}
                    </div>
                    <div style="font-size: 12px; opacity: 0.9;">Badge Points</div>
                </div>
                
                <div style="background: {health_color}; padding: 15px; border-radius: 10px; 
                           min-width: 120px; text-align: center; border: 2px solid white;">
                    <div style="font-size: 20px; margin-bottom: 5px;">
                        {health_icon} {health_status}
                    </div>
                    <div style="font-size: 12px; opacity: 0.9;">{class_data['avg_engagement']:.0f}/100</div>
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.15); padding: 20px; border-radius: 12px; 
                       border-left: 4px solid #00ff88; margin: 15px 0;">
                <h4 style="margin: 0 0 10px 0; color: #00ff88; font-size: 16px;">
                    💡 AI Insights
                </h4>
                <p style="margin: 0; font-size: 15px; line-height: 1.6;">
                    {ai_summary}
                </p>
            </div>
            
            <div style="display: flex; gap: 20px; margin-top: 20px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 200px;">
                    <h4 style="margin: 0 0 10px 0; font-size: 14px; color: #00ff88;">🏆 Top Performers (by Rank)</h4>
                    <ul style="margin: 0; padding-left: 20px; font-size: 13px;">
                        {chr(10).join([f"<li>#{s['class_rank']} {s['student'].full_name} ({s['avg_marks']:.0f} avg)</li>" for s in class_data['top_performers']])}
                    </ul>
                </div>
                
                <div style="flex: 1; min-width: 200px;">
                    <h4 style="margin: 0 0 10px 0; font-size: 14px; color: #ffd700;">🎖️ Badge Champions</h4>
                    <ul style="margin: 0; padding-left: 20px; font-size: 13px;">
                        {chr(10).join([f"<li>{s['student'].full_name} ({s['badge_info']['total_badge_points']} pts, {s['badges_earned']} badges)</li>" for s in class_data['top_badge_earners']])}
                    </ul>
                </div>
                
                {f'''<div style="flex: 1; min-width: 200px;">
                    <h4 style="margin: 0 0 10px 0; font-size: 14px; color: #ffaa00;">⚡ Needs Support</h4>
                    <ul style="margin: 0; padding-left: 20px; font-size: 13px;">
                        {chr(10).join([f"<li>#{s['class_rank']} {s['student'].full_name} ({s['engagement_score']:.0f}/100)</li>" for s in class_data['needs_attention']])}
                    </ul>
                </div>''' if class_data['needs_attention'] else ''}
            </div>
        </div>
        """
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Monthly Class Report</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        </style>
    </head>
    <body style="margin: 0; padding: 0; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        
        <div style="max-width: 700px; margin: 0 auto; background: white; 
                   border-radius: 20px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.1);">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       padding: 40px 30px; text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 32px; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                    📊 Monthly Class Reports
                </h1>
                <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.9;">
                    {month_year} Performance Summary
                </p>
                <div style="background: rgba(255,255,255,0.2); padding: 15px; margin: 20px auto; 
                           border-radius: 50px; max-width: 300px; backdrop-filter: blur(10px);">
                    <p style="margin: 0; font-size: 16px; font-weight: 500;">
                        Dear {teacher.name} 👋
                    </p>
                </div>
            </div>
            
            <!-- Content -->
            <div style="padding: 30px;">
                <div style="background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%); 
                           padding: 20px; border-radius: 12px; margin-bottom: 25px;">
                    <p style="margin: 0; color: white; font-size: 16px; text-align: center; font-weight: 500;">
                        ✨ Here's how your {len(class_reports_data)} class{'es' if len(class_reports_data) > 1 else ''} 
                        performed this month with ranks and badges!
                    </p>
                </div>
                
                {class_cards_html}
                
                <!-- Footer -->
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                           padding: 25px; border-radius: 15px; margin-top: 30px; text-align: center; color: white;">
                    <h3 style="margin: 0 0 10px 0; font-size: 20px; font-weight: 600;">
                        🚀 Keep Up the Great Work!
                    </h3>
                    <p style="margin: 0; font-size: 14px; opacity: 0.95; line-height: 1.5;">
                        Your dedication to student success makes a real difference. 
                        Continue inspiring and guiding your students to achieve their best ranks and earn more badges!
                    </p>
                </div>
                
                <div style="text-align: center; margin-top: 25px; padding: 20px; 
                           border-top: 2px solid #f0f0f0;">
                    <p style="margin: 0; color: #666; font-size: 14px;">
                        <strong>Best regards,</strong><br>
                        <span style="color: #667eea; font-weight: 600;">The Savvy Team</span>
                    </p>
                </div>
            </div>
        </div>
        
        <!-- Mobile responsiveness -->
        <style>
            @media only screen and (max-width: 600px) {{
                .container {{ width: 100% !important; }}
                .card {{ margin: 10px !important; padding: 20px !important; }}
                .stats-grid {{ flex-direction: column !important; }}
            }}
        </style>
    </body>
    </html>
    """


@celery.task(name='tasks.send_monthly_class_reports_to_teachers')
def send_monthly_class_reports_to_teachers():
    """Send monthly class reports to teachers using Gemini AI with attractive design."""
    print("Starting enhanced monthly class reports task for teachers with ranks and badges...")
    
    gemini_client = None
    try:
        gemini_client = setup_gemini_client()
        print("Gemini client ready")
    except Exception as e:
        print(f"Gemini setup failed, using fallback reports: {e}")
    
    with app.app_context():
        try:
            teachers = (
                Teacher.query
                .filter(Teacher.email.isnot(None))
                .filter(Teacher.email != '')
                .all()
            )
            
            if not teachers:
                return {'status': 'success', 'message': 'No teachers found', 'processed': 0}
            
            processed = 0
            errors = 0
            month_year = datetime.now().strftime("%B %Y")
            
            for teacher in teachers:
                try:
                    if not validate_email(teacher.email):
                        print(f"Invalid email for teacher {teacher.name}: {teacher.email}")
                        errors += 1
                        continue
                    
                    teacher_classes = get_teacher_classes(teacher.id)
                    if not teacher_classes:
                        print(f"No classes found for teacher {teacher.name}")
                        continue
                    
                    class_reports_data = []
                    for class_name in teacher_classes:
                        class_obj, class_data = generate_class_summary_for_teacher(teacher.id, class_name)
                        if class_obj and class_data:
                            ai_summary = generate_ai_report_for_teacher(gemini_client, teacher, class_data)
                            class_reports_data.append((class_data, ai_summary))
                    
                    if not class_reports_data:
                        print(f"No class data found for teacher {teacher.name}")
                        errors += 1
                        continue
                    
                    html_body = create_attractive_email_html(teacher, class_reports_data, month_year)
                    subject = f"📊 Your Monthly Class Reports - {month_year}"
                    
                    send_mail(
                        to_email=teacher.email.strip(),
                        subject=subject,
                        body_html=html_body
                    )
                    
                    print(f"✅ Sent enhanced class reports to teacher {teacher.name} ({teacher.email}) for {len(teacher_classes)} classes")
                    processed += 1
                    
                except Exception as e:
                    print(f"❌ Failed to send email to teacher {teacher.email}: {e}")
                    errors += 1
            
            return {
                'status': 'success',
                'message': 'Enhanced monthly class reports with ranks and badges completed',
                'processed': processed,
                'errors': errors,
                'total': len(teachers)
            }
            
        except Exception as e:
            print(f"Critical error: {e}")
            return {'status': 'error', 'message': str(e)}
        
        finally:
            db.session.close()


def test_class_reports():
    """Test the monthly class reports task."""
    try:
        result = send_monthly_class_reports_to_teachers.delay()
        print(f"Enhanced class reports task queued: {result.id}")
        return result
    except Exception as e:
        print(f"Failed to queue class reports task: {e}")
        return None