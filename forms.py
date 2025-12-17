from wtforms import StringField, TextAreaField, validators
from wtforms.validators import DataRequired, Email, Length, Optional

class ContactForm:
    """Simplified form for serverless"""
    def __init__(self, data=None):
        self.data = data or {}
        self.name = StringField('Name', validators=[DataRequired()])
        self.email = StringField('Email', validators=[DataRequired(), Email()])
        self.subject = StringField('Subject', validators=[Optional()])
        self.message = TextAreaField('Message', validators=[DataRequired()])
        self.phone = StringField('Phone', validators=[Optional()])
        self.company = StringField('Company', validators=[Optional()])

class NewsletterForm:
    """Simplified newsletter form"""
    def __init__(self, data=None):
        self.data = data or {}
        self.email = StringField('Email', validators=[DataRequired(), Email()])
