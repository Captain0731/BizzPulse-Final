import os
import io
import logging
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from PIL import Image as PILImage

logger = logging.getLogger(__name__)

class PortfolioPDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.custom_styles = self._create_custom_styles()
        
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        styles = {}
        
        styles['CustomTitle'] = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2c5aa0')
        )
        
        styles['CustomSubtitle'] = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#1f4788')
        )
        
        styles['CustomBody'] = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            leading=14
        )
        
        styles['FeatureList'] = ParagraphStyle(
            'FeatureList',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            leftIndent=20,
            bulletIndent=10
        )
        
        return styles
    
    def _add_header_footer(self, canvas, doc):
        """Add header and footer to each page"""
        canvas.saveState()
        
        canvas.setFont('Helvetica-Bold', 12)
        canvas.setFillColor(colors.HexColor('#2c5aa0'))
        canvas.drawString(50, letter[1] - 50, "BizzPulse Portfolio")
        
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.grey)
        canvas.drawString(50, 30, f"Generated on {datetime.now().strftime('%B %d, %Y')}")
        canvas.drawRightString(letter[0] - 50, 30, f"Page {doc.page}")
        
        canvas.restoreState()
    
    def generate_portfolio_pdf(self, portfolio_data):
        """Generate a comprehensive portfolio PDF"""
        buffer = io.BytesIO()
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=50,
            leftMargin=50,
            topMargin=80,
            bottomMargin=50
        )
        
        story = []
        
        story.append(Paragraph("Portfolio Details", self.custom_styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        meta_data = [
            ['Project Type:', portfolio_data.get('project_type', 'UX/UI Design')],
            ['Date:', portfolio_data.get('date', 'September 2024')],
            ['Client:', portfolio_data.get('client', 'DigitalCraft Solutions')],
            ['Website:', portfolio_data.get('website', 'projectwebsite.example.com')]
        ]
        
        meta_table = Table(meta_data, colWidths=[1.5*inch, 4*inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c5aa0')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(meta_table)
        story.append(Spacer(1, 30))
        
        story.append(Paragraph(
            portfolio_data.get('title', 'Innovative Financial Dashboard App'),
            self.custom_styles['CustomTitle']
        ))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("Project Overview", self.custom_styles['CustomSubtitle']))
        overview_text = portfolio_data.get('overview', 
            "This project showcases our expertise in developing modern, user-friendly applications.")
        story.append(Paragraph(overview_text, self.custom_styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("Key Features", self.custom_styles['CustomSubtitle']))
        features = portfolio_data.get('features', [
            "Real-time Data Visualization",
            "User Role Management", 
            "Secure Authentication",
            "Customizable Dashboards"
        ])
        
        for feature in features:
            story.append(Paragraph(f"• {feature}", self.custom_styles['FeatureList']))
        
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("Technology Stack", self.custom_styles['CustomSubtitle']))
        tech_stack = portfolio_data.get('tech_stack', [
            'Python', 'Flask', 'PostgreSQL', 'React', 'AWS'
        ])
        
        tech_text = ", ".join(tech_stack)
        story.append(Paragraph(tech_text, self.custom_styles['CustomBody']))
        
        doc.build(story, onFirstPage=self._add_header_footer, onLaterPages=self._add_header_footer)
        
        buffer.seek(0)
        return buffer

    def generate_simple_pdf(self):
        """Generate a simple portfolio PDF with default data"""
        default_data = {
            'project_type': 'UX/UI Design',
            'date': 'September 2024',
            'client': 'DigitalCraft Solutions',
            'website': 'projectwebsite.example.com',
            'title': 'Innovative Financial Dashboard App',
            'overview': 'A comprehensive financial dashboard designed to provide real-time insights and analytics for modern businesses.',
            'features': [
                'Real-time Data Visualization',
                'User Role Management',
                'Secure Authentication',
                'Customizable Dashboards',
                'Data Export Options',
                'Multi-device Support'
            ],
            'tech_stack': ['Python', 'Flask', 'PostgreSQL', 'React', 'AWS']
        }
        
        return self.generate_portfolio_pdf(default_data)

