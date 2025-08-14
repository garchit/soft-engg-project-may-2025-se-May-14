import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from flask import render_template
import pdfkit
from config import Config

def send_mail(to_email, subject, body_html):
    msg = MIMEMultipart()
    msg['From'] = Config.FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body_html, 'html'))

    with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
        server.send_message(msg)

    print(f"✅ Email sent to {to_email}")

def generate_pdf_from_html(template_name, context):
    rendered = render_template(template_name, **context)
    return pdfkit.from_string(rendered, False)

def send_mail_with_pdf(to_email, subject, html_body, pdf):
    msg = MIMEMultipart()
    msg['From'] = Config.FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(html_body, 'html'))
    msg.attach(MIMEApplication(pdf, _subtype='pdf', Name='monthly_report.pdf'))

    with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
        server.send_message(msg)

    print(f"✅ Email with PDF sent to {to_email}")
