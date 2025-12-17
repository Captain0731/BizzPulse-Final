import os
from flask import Blueprint, render_template, request, jsonify, send_from_directory, send_file
from flask_wtf.csrf import csrf
from app_refactored import db
from models import Contact, Newsletter
from forms import ContactForm, NewsletterForm
from sqlalchemy.exc import IntegrityError
from email_service import send_contact_email, send_auto_reply_email
from pdf_generator import PortfolioPDFGenerator
import logging

logger = logging.getLogger(__name__)

# Blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

# ============ Main Routes ============
@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/demo')
def demo():
    return render_template('demo.html')

@main_bp.route('/portfolio-details')
@main_bp.route('/portfolio-details.html')
def portfolio_details():
    return render_template('portfolio-details.html')

@main_bp.route('/service-details')
@main_bp.route('/service-details.html')
def service_details():
    return render_template('service-details.html')

@main_bp.route('/service-details1')
@main_bp.route('/service-details1.html')
def service_details1():
    return render_template('service-details1.html')

@main_bp.route('/service-details2')
@main_bp.route('/service-details2.html')
def service_details2():
    return render_template('service-details2.html')

@main_bp.route('/starter-page')
@main_bp.route('/starter-page.html')
def starter_page():
    return render_template('starter-page.html')

@main_bp.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# ============ API Routes (CSRF Exempt) ============
@api_bp.route('/contact', methods=['POST'])
@csrf.exempt
def submit_contact():
    """Handle contact form submissions"""
    form = ContactForm(meta={'csrf': False})
    
    if form.validate_on_submit():
        try:
            contact_data = {
                'name': form.name.data.strip(),
                'email': form.email.data.strip().lower(),
                'subject': form.subject.data.strip() if form.subject.data else None,
                'message': form.message.data.strip(),
                'phone': form.phone.data.strip() if form.phone.data else None,
                'company': form.company.data.strip() if form.company.data else None
            }
            
            # Save to database
            try:
                contact = Contact(**contact_data)
                db.session.add(contact)
                db.session.commit()
                logger.info(f"Contact saved: {contact_data['email']}")
            except Exception as db_error:
                logger.error(f"Database save failed: {db_error}")
                db.session.rollback()
            
            # Send emails
            admin_email = os.environ.get('ADMIN_EMAIL', 'harshilgajjar602@gmail.com')
            send_contact_email(contact_data, admin_email)
            send_auto_reply_email(contact_data)
            
            return jsonify({
                'status': 'success',
                'message': 'Thank you for your message! We will get back to you soon.'
            }), 200
            
        except Exception as e:
            logger.error(f"Contact form error: {e}")
            return jsonify({
                'status': 'error',
                'message': 'Sorry, there was an error sending your message. Please try again.'
            }), 500
    
    return jsonify({
        'status': 'error',
        'message': 'Invalid form data',
        'errors': form.errors
    }), 400

@api_bp.route('/newsletter', methods=['POST'])
@csrf.exempt
def subscribe_newsletter():
    """Handle newsletter subscriptions"""
    form = NewsletterForm(meta={'csrf': False})
    
    if form.validate_on_submit():
        try:
            email = form.email.data.strip().lower()
            
            existing = Newsletter.query.filter_by(email=email).first()
            if existing and existing.is_active:
                return jsonify({
                    'status': 'info',
                    'message': 'You are already subscribed to our newsletter!'
                }), 200
            
            if existing:
                existing.is_active = True
            else:
                subscription = Newsletter(email=email)
                db.session.add(subscription)
            
            db.session.commit()
            logger.info(f"Newsletter subscription: {email}")
            
            return jsonify({
                'status': 'success',
                'message': 'Thank you for subscribing to our newsletter!'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Newsletter error: {e}")
            return jsonify({
                'status': 'error',
                'message': 'Sorry, there was an error processing your subscription.'
            }), 500
    
    return jsonify({
        'status': 'error',
        'message': 'Invalid email address',
        'errors': form.errors
    }), 400

@api_bp.route('/generate-pdf')
def generate_pdf():
    """Generate portfolio PDF"""
    try:
        pdf_generator = PortfolioPDFGenerator()
        pdf_buffer = pdf_generator.generate_simple_pdf()
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name='BizzPulse_Portfolio.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        logger.error(f"PDF generation error: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to generate PDF'
        }), 500

# ============ Admin Routes ============
@api_bp.route('/admin/contacts')
def admin_contacts():
    """View all contacts (add authentication in production)"""
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return jsonify([contact.to_dict() for contact in contacts])

@api_bp.route('/admin/newsletters')
def admin_newsletters():
    """View all newsletter subscriptions"""
    subscriptions = Newsletter.query.order_by(Newsletter.subscribed_at.desc()).all()
    return jsonify([sub.to_dict() for sub in subscriptions])

# ============ Health Check ============
@api_bp.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

