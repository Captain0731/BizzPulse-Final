import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import logging
from flask import Flask, render_template, request, jsonify, send_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__, 
            template_folder=os.path.join(parent_dir, 'templates'),
            static_folder=os.path.join(parent_dir, 'static'))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'vercel-secret-key')

# Import helper functions
try:
    from email_service_vercel import send_contact_email, send_auto_reply_email
    from pdf_generator_vercel import PortfolioPDFGenerator
    EMAIL_AVAILABLE = True
    PDF_AVAILABLE = True
except Exception as e:
    logger.warning(f"Import error: {e}")
    EMAIL_AVAILABLE = False
    PDF_AVAILABLE = False

# ============ Routes ============
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Index error: {e}")
        return f"<h1>BizzPulse</h1><p>Welcome! Error: {str(e)}</p>", 200

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
    return jsonify({
        'status': 'healthy',
        'platform': 'vercel',
        'email_available': EMAIL_AVAILABLE,
        'pdf_available': PDF_AVAILABLE
    }), 200

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
        
        if not contact_data['name'] or not contact_data['email'] or not contact_data['message']:
            return jsonify({
                'status': 'error',
                'message': 'Name, email, and message are required'
            }), 400
        
        if EMAIL_AVAILABLE:
            admin_email = os.environ.get('ADMIN_EMAIL', 'harshilgajjar602@gmail.com')
            send_contact_email(contact_data, admin_email)
            send_auto_reply_email(contact_data)
        
        logger.info(f"Contact: {contact_data['email']}")
        
        return jsonify({
            'status': 'success',
            'message': 'Thank you for your message! We will get back to you soon.'
        }), 200
        
    except Exception as e:
        logger.error(f"Contact error: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
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
        
        logger.info(f"Newsletter: {email}")
        
        return jsonify({
            'status': 'success',
            'message': 'Thank you for subscribing!'
        }), 200
        
    except Exception as e:
        logger.error(f"Newsletter error: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/generate-pdf')
def generate_pdf():
    try:
        if not PDF_AVAILABLE:
            return jsonify({
                'status': 'error',
                'message': 'PDF generation not available'
            }), 503
        
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
            'message': str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    return jsonify({'error': str(e)}), 500
