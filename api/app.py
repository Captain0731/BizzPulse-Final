import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import io

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'vercel-secret-key')
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for serverless

CORS(app)

# Import models and forms without DB initialization
try:
    from forms import ContactForm, NewsletterForm
    from email_service import send_contact_email, send_auto_reply_email
    from pdf_generator import PortfolioPDFGenerator
except ImportError as e:
    logger.warning(f"Import warning: {e}")

# ============ Routes ============
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/portfolio-details')
@app.route('/portfolio-details.html')
def portfolio_details():
    return render_template('portfolio-details.html')

@app.route('/service-details')
@app.route('/service-details.html')
def service_details():
    return render_template('service-details.html')

@app.route('/service-details1')
@app.route('/service-details1.html')
def service_details1():
    return render_template('service-details1.html')

@app.route('/service-details2')
@app.route('/service-details2.html')
def service_details2():
    return render_template('service-details2.html')

@app.route('/starter-page')
@app.route('/starter-page.html')
def starter_page():
    return render_template('starter-page.html')

# ============ API Routes ============
@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'platform': 'vercel'}), 200

@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json() or request.form.to_dict()
        
        contact_data = {
            'name': data.get('name', '').strip(),
            'email': data.get('email', '').strip().lower(),
            'subject': data.get('subject', '').strip(),
            'message': data.get('message', '').strip(),
            'phone': data.get('phone', '').strip(),
            'company': data.get('company', '').strip()
        }
        
        # Validate
        if not contact_data['name'] or not contact_data['email'] or not contact_data['message']:
            return jsonify({
                'status': 'error',
                'message': 'Name, email, and message are required'
            }), 400
        
        # Send emails
        admin_email = os.environ.get('ADMIN_EMAIL', 'harshilgajjar602@gmail.com')
        send_contact_email(contact_data, admin_email)
        send_auto_reply_email(contact_data)
        
        logger.info(f"Contact form submitted: {contact_data['email']}")
        
        return jsonify({
            'status': 'success',
            'message': 'Thank you for your message! We will get back to you soon.'
        }), 200
        
    except Exception as e:
        logger.error(f"Contact error: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Sorry, there was an error. Please try again.'
        }), 500

@app.route('/api/newsletter', methods=['POST'])
def newsletter():
    try:
        data = request.get_json() or request.form.to_dict()
        email = data.get('email', '').strip().lower()
        
        if not email or '@' not in email:
            return jsonify({
                'status': 'error',
                'message': 'Valid email is required'
            }), 400
        
        logger.info(f"Newsletter subscription: {email}")
        
        return jsonify({
            'status': 'success',
            'message': 'Thank you for subscribing to our newsletter!'
        }), 200
        
    except Exception as e:
        logger.error(f"Newsletter error: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Sorry, there was an error.'
        }), 500

@app.route('/api/generate-pdf')
def generate_pdf():
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
        logger.error(f"PDF error: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to generate PDF'
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    return jsonify({'error': 'Internal server error'}), 500

