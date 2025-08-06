import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models import EmailCredentials
from app import db

def get_email_credentials():
    """Get the current email credentials from database"""
    return EmailCredentials.query.first()

def send_email(to_email, subject, html_content, text_content=None):
    """Send an email using stored credentials"""
    credentials = get_email_credentials()
    
    if not credentials:
        return False, "No email credentials configured"
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        from_name = getattr(credentials, 'from_name', 'Grand Stage Productions')
        msg['From'] = f"{from_name} <{credentials.email_address}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add text content if provided
        if text_content:
            text_part = MIMEText(text_content, 'plain')
            msg.attach(text_part)
        
        # Add HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Connect to SMTP server with timeout
        server = smtplib.SMTP(credentials.smtp_server, credentials.smtp_port, timeout=30)
        server.starttls()
        server.login(credentials.email_address, credentials.app_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(credentials.email_address, to_email, text)
        server.quit()
        
        return True, "Email sent successfully"
        
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

def send_contact_notification(submission):
    """Send notification emails for contact form submission"""
    credentials = get_email_credentials()
    if not credentials:
        return False, "No email credentials configured"
    
    # Send thank you email to the person who contacted us
    thank_you_subject = "Thank you for contacting Grand Stage Productions"
    thank_you_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 2px solid #722F37; border-radius: 10px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #722F37; font-family: 'Cinzel', serif;">Grand Stage Productions</h1>
                <p style="color: #8B1538; font-style: italic; font-size: 16px;">Bringing stories to life</p>
            </div>
            
            <h2 style="color: #722F37;">Thank you for reaching out!</h2>
            
            <p>Dear {submission.name},</p>
            
            <p>Thank you for contacting Grand Stage Productions. We have received your message and will get back to you as soon as possible.</p>
            
            <div style="background-color: #f8f8f8; padding: 15px; border-left: 4px solid #722F37; margin: 20px 0;">
                <h3 style="color: #722F37; margin-top: 0;">Your Message Summary:</h3>
                <p><strong>Subject:</strong> {submission.subject}</p>
                <p><strong>Message:</strong><br>{submission.message}</p>
            </div>
            
            <p>We appreciate your interest in our theater group and look forward to connecting with you.</p>
            
            <p>Best regards,<br>
            <strong>Grand Stage Productions Team</strong></p>
            
            <hr style="border: none; border-top: 2px solid #722F37; margin: 30px 0;">
            <p style="font-size: 12px; color: #666; text-align: center;">
                This is an automated response. Please do not reply to this email.
            </p>
        </div>
    </body>
    </html>
    """
    
    thank_you_text = f"""
    Thank you for contacting Grand Stage Productions!
    
    Dear {submission.name},
    
    Thank you for reaching out to us. We have received your message about "{submission.subject}" and will get back to you as soon as possible.
    
    Your Message:
    {submission.message}
    
    We appreciate your interest in our theater group and look forward to connecting with you.
    
    Best regards,
    Grand Stage Productions Team
    """
    
    # Send internal notification email
    internal_subject = f"New Contact Form Submission: {submission.subject}"
    internal_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 2px solid #722F37; border-radius: 10px;">
            <h2 style="color: #722F37;">New Contact Form Submission</h2>
            
            <div style="background-color: #f8f8f8; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3 style="color: #722F37; margin-top: 0;">Contact Details:</h3>
                <p><strong>Name:</strong> {submission.name}</p>
                <p><strong>Email:</strong> {submission.email}</p>
                <p><strong>Subject:</strong> {submission.subject}</p>
                <p><strong>Submitted:</strong> {submission.submitted_at.strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
            
            <div style="background-color: #fff; padding: 15px; border-left: 4px solid #722F37; margin: 20px 0;">
                <h3 style="color: #722F37; margin-top: 0;">Message:</h3>
                <p>{submission.message}</p>
            </div>
            
            <p><em>Please respond to this inquiry promptly.</em></p>
        </div>
    </body>
    </html>
    """
    
    # Send both emails
    success_user, msg_user = send_email(submission.email, thank_you_subject, thank_you_html, thank_you_text)
    success_admin, msg_admin = send_email(credentials.email_address, internal_subject, internal_html)
    
    return success_user and success_admin, f"User email: {msg_user}, Admin email: {msg_admin}"