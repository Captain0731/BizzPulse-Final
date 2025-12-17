import os
import resend
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Configure Resend
resend.api_key = os.environ.get("RESEND_API_KEY")

def send_contact_email(contact_data, admin_email="harshilgajjar602@gmail.com"):
    """Send contact form submission to admin email via Resend"""
    try:
        email_subject = f"🔔 New Contact Form Submission - {contact_data['name']}"
        
        email_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background-color: #2c5282; color: white; padding: 20px; border-radius: 8px 8px 0 0; text-align: center;">
                    <h1 style="margin: 0; font-size: 24px;">BizzPulse Admin Notification</h1>
                    <p style="margin: 10px 0 0 0; font-size: 16px;">New Contact Form Submission</p>
                </div>
                
                <div style="background-color: #f8f9fa; padding: 20px; border: 1px solid #e2e8f0;">
                    <h2 style="color: #2c5282; margin-top: 0;">Someone is interested in your services!</h2>
                    <p style="color: #4a5568; font-size: 16px; margin-bottom: 20px;">
                        A potential client has submitted a contact form. Here are the details:
                    </p>
                </div>
                
                <div style="background-color: #f7fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #2d3748;">Contact Information</h3>
                    
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold; width: 120px;">Name:</td>
                            <td style="padding: 8px 0;">{contact_data['name']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold;">Email:</td>
                            <td style="padding: 8px 0;">
                                <a href="mailto:{contact_data['email']}" style="color: #3182ce; text-decoration: none;">
                                    {contact_data['email']}
                                </a>
                            </td>
                        </tr>
                        {f'''<tr>
                            <td style="padding: 8px 0; font-weight: bold;">Phone:</td>
                            <td style="padding: 8px 0;">{contact_data['phone']}</td>
                        </tr>''' if contact_data.get('phone') else ''}
                        {f'''<tr>
                            <td style="padding: 8px 0; font-weight: bold;">Company:</td>
                            <td style="padding: 8px 0;">{contact_data['company']}</td>
                        </tr>''' if contact_data.get('company') else ''}
                        {f'''<tr>
                            <td style="padding: 8px 0; font-weight: bold;">Subject:</td>
                            <td style="padding: 8px 0;">{contact_data['subject']}</td>
                        </tr>''' if contact_data.get('subject') else ''}
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold;">Submitted:</td>
                            <td style="padding: 8px 0;">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</td>
                        </tr>
                    </table>
                </div>
                
                <div style="background-color: #ffffff; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px;">
                    <h3 style="margin-top: 0; color: #2d3748;">Message</h3>
                    <div style="background-color: #f7fafc; padding: 15px; border-radius: 4px; border-left: 4px solid #3182ce;">
                        {contact_data['message'].replace(chr(10), '<br>')}
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        email_text = f"""
BIZZPULSE ADMIN NOTIFICATION
New Contact Form Submission

POTENTIAL CLIENT DETAILS:
- Name: {contact_data['name']}
- Email: {contact_data['email']}
{f"- Phone: {contact_data['phone']}" if contact_data.get('phone') else ''}
{f"- Company: {contact_data['company']}" if contact_data.get('company') else ''}
{f"- Subject: {contact_data['subject']}" if contact_data.get('subject') else ''}
- Submitted: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

CLIENT MESSAGE:
{contact_data['message']}
        """
        
        params = {
           "from": "BizzPulse <onboarding@resend.dev>",
           "to": [admin_email],
           "reply_to": contact_data['email'],
           "subject": email_subject,
           "html": email_html,
           "text": email_text,
        }
        
        response = resend.Emails.send(params)
        
        if hasattr(response, 'get') and response.get('id'):
            logger.info(f"Contact email sent successfully. ID: {response.get('id')}")
            return True, response
        else:
            logger.error(f"Resend API error: {response}")
            return False, f"API Error: {response}"
        
    except Exception as e:
        logger.error(f"Failed to send contact email: {str(e)}")
        return False, str(e)

def send_auto_reply_email(contact_data):
    """Send automatic reply to the person who submitted the contact form"""
    try:
        email_subject = "Thank you for contacting BizzPulse"
        
        email_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #2c5282; margin-bottom: 10px;">BizzPulse</h1>
                    <p style="color: #4a5568; font-size: 18px; margin: 0;">Business Consulting Excellence</p>
                </div>
                
                <h2 style="color: #2d3748; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px;">
                    Thank You for Your Message
                </h2>
                
                <p>Dear {contact_data['name']},</p>
                
                <p>Thank you for reaching out to BizzPulse. We have received your message and appreciate your interest in our services.</p>
                
                <div style="background-color: #f7fafc; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3182ce;">
                    <h3 style="margin-top: 0; color: #2d3748;">What happens next?</h3>
                    <ul style="margin-bottom: 0;">
                        <li>Our team will review your message within 24 hours</li>
                        <li>We'll reach out to you via email or phone to discuss your needs</li>
                        <li>If urgent, feel free to call us directly at +1 (555) 123-4567</li>
                    </ul>
                </div>
                
                <div style="background-color: #ffffff; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #2d3748;">Your Message Summary</h3>
                    <p><strong>Subject:</strong> {contact_data.get('subject', 'General Inquiry')}</p>
                    <p><strong>Submitted:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                </div>
                
                <p>Best regards,<br>
                <strong>The BizzPulse Team</strong></p>
                
                <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;">
                
                <div style="font-size: 14px; color: #4a5568; text-align: center;">
                    <p>BizzPulse - Elevating Business Performance Through Innovation</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        email_text = f"""
Dear {contact_data['name']},

Thank you for reaching out to BizzPulse. We have received your message and appreciate your interest in our services.

What happens next?
- Our team will review your message within 24 hours
- We'll reach out to you via email or phone to discuss your needs
- If urgent, feel free to call us directly at +1 (555) 123-4567

Your Message Summary:
Subject: {contact_data.get('subject', 'General Inquiry')}
Submitted: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

Best regards,
The BizzPulse Team
        """
        
        params = {
            "from": "BizzPulse <onboarding@resend.dev>",
            "to": [contact_data['email']],
            "subject": email_subject,
            "html": email_html,
            "text": email_text,
        }
        
        response = resend.Emails.send(params)
        
        if hasattr(response, 'get') and response.get('id'):
            logger.info(f"Auto-reply sent to {contact_data['email']}. ID: {response.get('id')}")
            return True, response
        else:
            logger.error(f"Auto-reply API error: {response}")
            return False, f"API Error: {response}"
        
    except Exception as e:
        logger.error(f"Failed to send auto-reply: {str(e)}")
        return False, str(e)

