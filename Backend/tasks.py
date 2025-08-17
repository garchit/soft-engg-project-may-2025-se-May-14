

import os
import re
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import func
from celery import group

from celery_worker import celery

from factory import create_app
from extension import db
from models.teacher import Teacher
from models.user_teacher import UserTeacher
from models.user import User
from models.unit import Unit as Course
from models.user_course import UserCourse
from models.badges import Badge, badge_user
from email_utils import send_mail
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()


app = create_app()



def validate_email(email):
    if not email or not isinstance(email, str): return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None

def calculate_student_rank(student_data, all_students_data):
    def performance_score(s):
        return (s['completion_rate'] * 0.4 + s['avg_marks'] * 0.3 + s['engagement_score'] * 0.3)
    sorted_students = sorted(all_students_data, key=performance_score, reverse=True)
    student_id = student_data['student'].id
    for rank, student in enumerate(sorted_students, 1):
        if student['student'].id == student_id:
            return rank
    return len(all_students_data)

def get_student_badges_info(student_id):
    badges_data = (db.session.query(Badge.name, Badge.points, Badge.description)
                   .join(badge_user, badge_user.c.badge_id == Badge.id)
                   .filter(badge_user.c.user_id == student_id).all())
    return {
        'badge_count': len(badges_data),
        'total_badge_points': sum(badge.points for badge in badges_data)
    }

def generate_teacher_student_summary(teacher_id):
    students = (db.session.query(User)
                .join(UserTeacher, UserTeacher.user_id == User.id)
                .filter(UserTeacher.teacher_id == teacher_id).all())
    if not students:
        return None, f"No students found for teacher ID {teacher_id}"

    total_courses = Course.query.count()
    student_data = []
    for student in students:
        completed_courses = db.session.query(Course, UserCourse.marks_scored).join(UserCourse).filter(UserCourse.user_id == student.id).all()
        completion_rate = (len(completed_courses) / total_courses * 100) if total_courses > 0 else 0
        marks_data = [c.marks_scored for c in completed_courses if c.marks_scored is not None]
        avg_marks = sum(marks_data) / len(marks_data) if marks_data else 0
        badge_info = get_student_badges_info(student.id)

        engagement_score = 0
        if student.latest_timestamp:
            days_since_last_activity = (datetime.now() - student.latest_timestamp).days
            if days_since_last_activity <= 1: engagement_score += 40
            elif days_since_last_activity <= 3: engagement_score += 25
            elif days_since_last_activity <= 7: engagement_score += 10
        engagement_score += min(30, (student.rewards or 0) / 10)
        engagement_score = min(100, engagement_score)

        student_data.append({
            'student': student,
            'completion_rate': completion_rate,
            'avg_marks': avg_marks,
            'badges_info': badge_info,
            'engagement_score': engagement_score
        })

    for student in student_data:
        student['class_rank'] = calculate_student_rank(student, student_data)

    total_students = len(student_data)
    def performance_score(s):
        return (s['completion_rate'] * 0.4 + s['avg_marks'] * 0.3 + s['engagement_score'] * 0.3)
    sorted_students = sorted(student_data, key=performance_score, reverse=True)
    
    return {
        'total_students': total_students,
        'avg_completion': sum(s['completion_rate'] for s in student_data) / total_students,
        'avg_engagement': sum(s['engagement_score'] for s in student_data) / total_students,
        'top_performers': sorted_students[:3],
        'needs_attention': [s for s in student_data if s['engagement_score'] < 40][:3],
    }, None

def setup_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

def generate_ai_report_for_teacher(client, teacher, summary_data):
    if client and summary_data:
        try:
            prompt = (f"Write a brief, encouraging report for Teacher {teacher.name}. Key stats for your {summary_data['total_students']} students: {summary_data['avg_completion']:.0f}% avg course completion, {summary_data['avg_engagement']:.0f}/100 avg engagement. Top performers: {', '.join([s['student'].full_name for s in summary_data['top_performers']])}. Students needing support: {len(summary_data['needs_attention'])}. Keep it 3-4 sentences max, positive and actionable.")
            response = client.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"AI generation error for teacher {teacher.name}: {e}")
    return "Your students are making steady progress. Keep an eye on engagement levels."

def create_attractive_teacher_email_html(teacher, summary_data, ai_summary, month_year):
    top_performers_html = "".join([f"<li style='margin-bottom: 5px;'>#{s['class_rank']} <strong>{s['student'].full_name}</strong> ({s['avg_marks']:.0f} avg)</li>" for s in summary_data['top_performers']])
    needs_attention_html = "".join([f"<li style='margin-bottom: 5px;'>#{s['class_rank']} <strong>{s['student'].full_name}</strong> ({s['engagement_score']:.0f}/100)</li>" for s in summary_data['needs_attention']])
    return f"""
    <!DOCTYPE html><html><head><link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet"></head><body style="font-family: 'Poppins', sans-serif; margin: 0; padding: 20px; background-color: #f4f7f9;"><div style="max-width: 680px; margin: auto; background: rgba(255, 255, 255, 0.7); border-radius: 16px; border: 1px solid #e5e7eb; overflow: hidden; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);"><div style="padding: 30px 25px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center;"><h1 style="margin: 0; font-size: 2rem; font-weight: 600;">Monthly Student Report</h1><p style="margin: 5px 0 0; font-size: 1rem; opacity: 0.9;">{month_year} Summary for {teacher.name}</p></div><div style="padding: 30px;"><div style="background: rgba(255, 255, 255, 0.5); padding: 20px; border-radius: 12px; margin-bottom: 25px; border-left: 4px solid #667eea;"><h3 style="margin:0 0 10px 0; color: #1a202c; font-weight: 600;">💡 AI Insights</h3><p style="margin:0; line-height: 1.6; color: #4a5568;">{ai_summary}</p></div><div style="display: flex; gap: 20px; flex-wrap: wrap; text-align: center; justify-content: space-around; margin-bottom: 30px; padding: 20px; background: rgba(243, 244, 246, 0.7); border-radius: 12px;"><div><div style="font-size: 28px; font-weight: 700; color: #111827;">{summary_data['total_students']}</div><div style="font-size: 12px; color: #6b7280; text-transform: uppercase; font-weight: 500;">Students</div></div><div><div style="font-size: 28px; font-weight: 700; color: #111827;">{summary_data['avg_completion']:.0f}%</div><div style="font-size: 12px; color: #6b7280; text-transform: uppercase; font-weight: 500;">Avg. Completion</div></div><div><div style="font-size: 28px; font-weight: 700; color: #111827;">{summary_data['avg_engagement']:.0f}</div><div style="font-size: 12px; color: #6b7280; text-transform: uppercase; font-weight: 500;">Avg. Engagement</div></div></div><div style="display: flex; gap: 20px; flex-wrap: wrap;"><div style="flex: 1; min-width: 200px;"><h3 style="color: #166534; font-weight: 600;">🏆 Top Performers</h3><ul style="padding-left: 20px; margin: 0; color: #374151; list-style-type: none;">{top_performers_html}</ul></div><div style="flex: 1; min-width: 200px;"><h3 style="color: #b45309; font-weight: 600;">⚡ Needs Support</h3><ul style="padding-left: 20px; margin: 0; color: #374151; list-style-type: none;">{needs_attention_html}</ul></div></div></div></div></body></html>
    """

def get_student_progress_for_parent(student_id):
    student = db.session.get(User, student_id)
    if not student: return None
    rank_subquery = db.session.query(User.id, func.rank().over(order_by=User.rewards.desc()).label('rank')).subquery()
    user_rank_data = db.session.query(rank_subquery.c.rank).filter(rank_subquery.c.id == student_id).first()
    overall_rank = user_rank_data[0] if user_rank_data else "N/A"
    courses_completed = db.session.query(Course.title, UserCourse.marks_scored).join(UserCourse).filter(UserCourse.user_id == student_id).all()
    if not courses_completed: return None
    avg_score = sum(c.marks_scored for c in courses_completed) / len(courses_completed)
    strongest_area = max(courses_completed, key=lambda item: item[1])
    weakest_area = min(courses_completed, key=lambda item: item[1])
    return {"student_name": student.full_name, "parent_email": student.parents_email, "average_score": f"{avg_score:.1f}", "strongest_area": f"{strongest_area[0]} ({strongest_area[1]}%)", "area_for_improvement": f"{weakest_area[0]} ({weakest_area[1]}%)", "overall_rank": overall_rank, "streak": student.streak or 0, "rewards": student.rewards or 0}

def generate_ai_report_for_parent(client, progress_data):
    if not client or not progress_data: return None
    try:
        parent_name = progress_data['parent_email'].split('@')[0].replace('.', ' ').title()
        student_name = progress_data['student_name']
        prompt = (f"Write a friendly, encouraging progress report for {student_name}'s parent, {parent_name}, in 3 short paragraphs. Start with 'Hi {parent_name},'. First, celebrate their effort. Second, highlight these achievements: average score is **{progress_data['average_score']}%**, strongest subject is **{progress_data['strongest_area']}**, and they have a **{progress_data['streak']} day** learning streak. Third, gently mention '{progress_data['area_for_improvement']}' as an opportunity for growth and end on a positive note. Keep it under 120 words.")
        response = client.generate_content(prompt)
        return response.text.strip().replace("\n", "<br>")
    except Exception as e:
        print(f"AI generation error for parent of {progress_data.get('student_name', 'Unknown')}: {e}")
        return "We're currently compiling the latest progress data for your child. Thank you for your continued support!"

def create_parent_email_html(progress_data, ai_body):
    student_name = progress_data['student_name']
    return f"""
    <!DOCTYPE html><html><head><link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet"></head><body style="font-family: 'Poppins', sans-serif; margin: 0; padding: 20px; background-color: #f4f7f9;"><div style="max-width: 600px; margin: auto; background: rgba(255, 255, 255, 0.7); border-radius: 16px; border: 1px solid #e5e7eb; overflow: hidden; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);"><div style="padding: 30px; text-align:center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;"><h1 style="margin:0; font-size:2rem; font-weight: 600;">✨ Progress Report</h1><p style="margin:5px 0 0; font-size: 1rem; opacity: 0.9;">For {student_name}</p></div><div style="padding: 30px; color:#374151; line-height:1.7;">{ai_body}</div><div style="display:flex; justify-content:space-around; text-align:center; padding: 25px 20px; background-color: rgba(243, 244, 246, 0.7); border-top: 1px solid #e5e7eb;"><div><div style="font-size:2rem; font-weight: 700; color:#111827;">#{progress_data['overall_rank']}</div><div style="font-size:0.8rem; color:#6b7280; text-transform: uppercase; font-weight: 500;">Overall Rank</div></div><div><div style="font-size:2rem; font-weight: 700; color:#111827;">{progress_data['average_score']}%</div><div style="font-size:0.8rem; color:#6b7280; text-transform: uppercase; font-weight: 500;">Average Score</div></div><div><div style="font-size:2rem; font-weight: 700; color:#111827;">🔥 {progress_data['streak']}</div><div style="font-size:0.8rem; color:#6b7280; text-transform: uppercase; font-weight: 500;">Day Streak</div></div></div></div></body></html>
    """



@celery.task(name='tasks.send_monthly_class_reports_to_teachers')
def send_monthly_class_reports_to_teachers():
    print("Starting monthly student reports task for teachers...")
    gemini_client = None
    try:
        gemini_client = setup_gemini_client()
    except ValueError as e:
        print(f"Teacher reports: Gemini setup failed - {e}")

    teachers = Teacher.query.filter(Teacher.email.isnot(None), Teacher.email != '').all()
    if not teachers:
        return {'status': 'success', 'message': 'No teachers found', 'processed': 0}

    processed = 0
    month_year = datetime.now().strftime("%B %Y")
    for teacher in teachers:
        summary_data, error_msg = generate_teacher_student_summary(teacher.id)
        if not summary_data:
            print(f"Skipping teacher {teacher.name}: {error_msg}")
            continue

        ai_summary = generate_ai_report_for_teacher(gemini_client, teacher, summary_data)
        html_body = create_attractive_teacher_email_html(teacher, summary_data, ai_summary, month_year)
        subject = f"📊 Your Student Performance Report - {month_year}"

        send_mail(to_email=teacher.email.strip(), subject=subject, body_html=html_body)
        print(f"✅ Sent student report to teacher {teacher.name} ({teacher.email})")
        processed += 1
    return {'status': 'success', 'processed': processed, 'total': len(teachers)}


@celery.task(name='tasks.send_progress_report_to_parent')
def send_progress_report_to_parent(student_id):
    print(f"Starting parent report for student ID: {student_id}")
    gemini_client = None
    try:
        gemini_client = setup_gemini_client()
    except ValueError as e:
        print(f"Parent reports: Gemini setup failed - {e}")

    progress_data = get_student_progress_for_parent(student_id)
    if not progress_data:
        print(f"No valid data for student {student_id}. Skipping parent report.")
        return
    ai_body = generate_ai_report_for_parent(gemini_client, progress_data)
    html_content = create_parent_email_html(progress_data, ai_body)
    subject = f"✨ Progress Report for {progress_data['student_name']}"
    send_mail(to_email=progress_data['parent_email'], subject=subject, body_html=html_content)
    print(f"✅ Successfully sent parent report for student {student_id} to {progress_data['parent_email']}")


@celery.task(name='tasks.schedule_all_parent_reports')
def schedule_all_parent_reports():
    print("🗓️ Scheduling weekly parent progress reports...")
    student_ids = [student.id for student in db.session.query(User.id).filter(User.parents_email.isnot(None), User.parents_email != '').all()]
    if not student_ids:
        print("No students with parent emails found.")
        return
    task_group = group(send_progress_report_to_parent.s(sid) for sid in student_ids)
    task_group.apply_async()
    print(f"📨 Queued parent reports for {len(student_ids)} students.")