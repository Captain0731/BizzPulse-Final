import os
from flask import render_template, request, jsonify, flash, redirect, url_for, send_from_directory, send_file
from app import app, db
from models import Contact, Newsletter
from forms import ContactForm, NewsletterForm
from sqlalchemy.exc import IntegrityError
from email_service import send_contact_email, send_auto_reply_email
from pdf_generator import PortfolioPDFGenerator  # Import the correct class
import io

# Serve static files
@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files from the static directory"""
    return send_from_directory('static', filename)

# Main routes
@app.route('/')
def index():
    """Serve the main index page"""
    return render_template('index.html')

@app.route('/demo')
def demo():
    """Serve the demo page"""
    return render_template('demo.html')

@app.route('/portfolio-details')
@app.route('/portfolio-details.html')
def portfolio_details():
    """Serve the portfolio details page"""
    return render_template('portfolio-details.html')

@app.route('/service-details')
@app.route('/service-details.html')
def service_details():
    """Serve the service details page"""
    return render_template('service-details.html')

@app.route('/service-details1')
@app.route('/service-details1.html')
def service_details1():
    """Serve the service details 1 page"""
    return render_template('service-details1.html')

@app.route('/service-details2')
@app.route('/service-details2.html')
def service_details2():
    """Serve the service details 2 page"""
    return render_template('service-details2.html')

@app.route('/starter-page')
@app.route('/starter-page.html')
def starter_page():
    """Serve the starter page"""
    return render_template('starter-page.html')

# Contact form handling
@app.route('/contact', methods=['POST'])
def submit_contact():
    """Handle contact form submissions"""
    form = ContactForm()
    
    if form.validate_on_submit():
        try:
            # Prepare contact data from form
            contact_data = {
                'name': form.name.data.strip(),
                'email': form.email.data.strip().lower(),
                'subject': form.subject.data.strip() if form.subject.data else None,
                'message': form.message.data.strip(),
                'phone': form.phone.data.strip() if form.phone.data else None,
                'company': form.company.data.strip() if form.company.data else None
            }
            
            # Check if database is available and save to DB
            database_url = os.environ.get("DATABASE_URL")
            if database_url and not database_url.startswith("sqlite"):
                try:
                    # Create new contact entry
                    contact = Contact(
                        name=contact_data['name'],
                        email=contact_data['email'],
                        subject=contact_data['subject'],
                        message=contact_data['message'],
                        phone=contact_data['phone'],
                        company=contact_data['company']
                    )
                    
                    db.session.add(contact)
                    db.session.commit()
                    app.logger.info(f"New contact submission from {contact.email}")
                except Exception as db_error:
                    app.logger.warning(f"Database save failed, continuing with email: {str(db_error)}")
            else:
                app.logger.warning("Database not configured, skipping DB save")
            
            # Send email notification to admin
            admin_email = os.environ.get('ADMIN_EMAIL', 'harshilgajjar602@gmail.com')
            email_sent, email_result = send_contact_email(contact_data, admin_email)
            
            if email_sent:
                app.logger.info(f"Contact notification email sent to {admin_email}")
                
                # Send auto-reply to customer
                auto_reply_sent, auto_reply_result = send_auto_reply_email(contact_data)
                if auto_reply_sent:
                    app.logger.info(f"Auto-reply sent to {contact_data['email']}")
                else:
                    app.logger.warning(f"Auto-reply failed: {auto_reply_result}")
            else:
                app.logger.error(f"Failed to send contact notification email: {email_result}")
            
            flash('Thank you for your message! We will get back to you soon.', 'success')
            return jsonify({
                'status': 'success',
                'message': 'Thank you for your message! We will get back to you soon.'
            }), 200
            
        except Exception as e:
            try:
                db.session.rollback()
            except:
                pass
            app.logger.error(f"Error saving contact form: {str(e)}")
            
            flash('Sorry, there was an error sending your message. Please try again.', 'error')
            return jsonify({
                'status': 'error',
                'message': 'Sorry, there was an error sending your message. Please try again.'
            }), 500
    
    else:
        # Form validation failed
        errors = []
        for field, field_errors in form.errors.items():
            for error in field_errors:
                errors.append(f"{field.title()}: {error}")
        
        error_message = "Please correct the following errors: " + "; ".join(errors)
        
        flash(error_message, 'error')
        return jsonify({
            'status': 'error',
            'message': error_message,
            'errors': form.errors
        }), 400

# Newsletter subscription
@app.route('/newsletter', methods=['POST'])
def subscribe_newsletter():
    """Handle newsletter subscriptions"""
    form = NewsletterForm()
    
    if form.validate_on_submit():
        try:
            email = form.email.data.strip().lower()
            
            # Check if database is available
            database_url = os.environ.get("DATABASE_URL")
            if not database_url or database_url.startswith("sqlite"):
                # Database not configured, just return success
                app.logger.warning("Database not configured, skipping newsletter subscription")
                return jsonify({
                    'status': 'success',
                    'message': 'Thank you for subscribing to our newsletter!'
                }), 200
            
            # Check if email already exists
            existing_subscription = Newsletter.query.filter_by(email=email).first()
            
            if existing_subscription:
                if existing_subscription.is_active:
                    return jsonify({
                        'status': 'info',
                        'message': 'You are already subscribed to our newsletter!'
                    }), 200
                else:
                    # Reactivate subscription
                    existing_subscription.is_active = True
                    db.session.commit()
                    
                    return jsonify({
                        'status': 'success',
                        'message': 'Welcome back! Your newsletter subscription has been reactivated.'
                    }), 200
            
            # Create new subscription
            subscription = Newsletter(email=email)
            db.session.add(subscription)
            db.session.commit()
            
            app.logger.info(f"New newsletter subscription: {email}")
            
            return jsonify({
                'status': 'success',
                'message': 'Thank you for subscribing to our newsletter!'
            }), 200
            
        except IntegrityError:
            db.session.rollback()
            return jsonify({
                'status': 'info',
                'message': 'You are already subscribed to our newsletter!'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error saving newsletter subscription: {str(e)}")
            
            return jsonify({
                'status': 'error',
                'message': 'Sorry, there was an error processing your subscription. Please try again.'
            }), 500
    
    else:
        # Form validation failed
        errors = []
        for field, field_errors in form.errors.items():
            for error in field_errors:
                errors.append(error)
        
        error_message = "; ".join(errors) if errors else "Invalid email address"
        
        return jsonify({
            'status': 'error',
            'message': error_message,
            'errors': form.errors
        }), 400

# Admin routes for viewing submissions (optional)
@app.route('/admin/contacts')
def admin_contacts():
    """View all contact submissions (admin only)"""
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return jsonify([contact.to_dict() for contact in contacts])

@app.route('/admin/newsletters')
def admin_newsletters():
    """View all newsletter subscriptions (admin only)"""
    subscriptions = Newsletter.query.order_by(Newsletter.subscribed_at.desc()).all()
    return jsonify([sub.to_dict() for sub in subscriptions])

@app.route('/admin/contact/<int:contact_id>/read', methods=['POST'])
def mark_contact_read(contact_id):
    """Mark a contact as read"""
    contact = Contact.query.get_or_404(contact_id)
    contact.is_read = True
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Contact marked as read'
    })

# PDF Generation route
@app.route('/generate-pdf')
def generate_pdf():
    """Generate PDF for the Financial Dashboard project"""
    try:
        # Instantiate the PDF generator
        pdf_generator = PortfolioPDFGenerator()
        
        # Generate a simple PDF with default data
        pdf_buffer = pdf_generator.generate_simple_pdf()
        
        # Send the PDF as a downloadable file
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name='Innovative_Financial_Dashboard_Project.pdf',
            mimetype='application/pdf'
        )
    
    except Exception as e:
        app.logger.error(f"Error generating PDF: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to generate PDF. Please try again.'
        }), 500

# PDF Download route
@app.route('/download-portfolio-pdf')
def download_portfolio_pdf():
    """Generate and download portfolio PDF"""
    try:
        # Instantiate the PDF generator
        pdf_generator = PortfolioPDFGenerator()
        
        # Generate a simple PDF with default data
        pdf_buffer = pdf_generator.generate_simple_pdf()
        
        # Send the PDF as a downloadable file
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name='Innovative_Financial_Dashboard_App.pdf',
            mimetype='application/pdf'
        )
    
    except Exception as e:
        app.logger.error(f"Error downloading portfolio PDF: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to generate PDF. Please try again.'
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500