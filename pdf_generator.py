"""
PDF Generator module for CASER Profile Builder.
Separates PDF creation logic from the main application.
"""

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus.flowables import KeepTogether
from PIL import Image as PilImage
import os
import tempfile
import logging

logger = logging.getLogger(__name__)


class PDFGenerator:
    """Class for generating PDF documents from profile data."""
    
    @staticmethod
    def create_profile_pdf(profile_data, output_path):
        """
        Creates PDF document from profile data.
        
        Args:
            profile_data (dict): Profile data
            output_path (str): Path to save PDF
            
        Returns:
            str: Path to saved file
        """
        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                topMargin=2*cm,
                bottomMargin=2*cm,
                leftMargin=2*cm,
                rightMargin=2*cm
            )
            
            styles = getSampleStyleSheet()
            PDFGenerator._setup_custom_styles(styles)
            
            story = []
            PDFGenerator._add_header(story, styles, profile_data)
            PDFGenerator._add_personal_info(story, styles, profile_data)
            PDFGenerator._add_biography(story, styles, profile_data)
            PDFGenerator._add_contacts(story, styles, profile_data)
            PDFGenerator._add_photos(story, styles, profile_data)
            PDFGenerator._add_additional_info(story, styles, profile_data)
            PDFGenerator._add_footer(story, styles, profile_data)
            
            doc.build(story)
            logger.info(f"PDF created successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to create PDF: {str(e)}")
            raise
    
    @staticmethod
    def _setup_custom_styles(styles):
        """Setup custom styles for document."""
        styles.add(ParagraphStyle(
            name='SubTitle',
            parent=styles['Heading2'],
            fontSize=12,
            spaceAfter=12,
            textColor=colors.HexColor('#0055a5')
        ))
        
        styles.add(ParagraphStyle(
            name='Meta',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.gray,
            spaceAfter=3
        ))
    
    @staticmethod
    def _add_header(story, styles, data):
        """Add document header."""
        title = Paragraph(
            f"<b>PERSONAL PROFILE:</b> {data.get('full_name', 'Unnamed Profile')}",
            styles['Title']
        )
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
    
    @staticmethod
    def _add_personal_info(story, styles, data):
        """Add personal information section."""
        info_fields = [
            ("Date of Birth", data.get("date_of_birth", "")),
            ("Position", data.get("position", "")),
            ("Tags", data.get("tags", "")),
            ("Created", data.get("created_at", "")),
        ]
        
        for label, value in info_fields:
            if value:
                story.append(Paragraph(f"<b>{label}:</b> {value}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
    
    @staticmethod
    def _add_biography(story, styles, data):
        """Add biography section."""
        bio = data.get("biography", "")
        if bio:
            story.append(Paragraph("<b>Biography:</b>", styles['Heading2']))
            story.append(Paragraph(bio, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
    
    @staticmethod
    def _add_contacts(story, styles, data):
        """Add contacts section."""
        contacts = data.get("contacts", [])
        if contacts:
            story.append(Paragraph("<b>Contacts:</b>", styles['Heading2']))
            for contact in contacts:
                story.append(Paragraph(f"• {contact}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
    
    @staticmethod
    def _add_photos(story, styles, data):
        """Add photos section."""
        photos = data.get("photos", [])
        if photos:
            story.append(Paragraph("<b>Photos:</b>", styles['Heading2']))
            temp_files = []
            
            for photo_path in photos:
                if os.path.exists(photo_path):
                    try:
                        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                            img = PilImage.open(photo_path)
                            img.save(temp_file.name, 'JPEG', quality=85)
                            temp_files.append(temp_file.name)
                            
                            story.append(Image(temp_file.name, width=2*inch, height=2.5*inch))
                            story.append(Spacer(1, 0.1*inch))
                    except Exception as e:
                        logger.error(f"Failed to add photo: {e}")
            
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file)
                except:
                    pass
    
    @staticmethod
    def _add_additional_info(story, styles, data):
        """Add additional information section."""
        additional = data.get("additional_info", "")
        if additional:
            story.append(Paragraph("<b>Additional Information:</b>", styles['Heading2']))
            story.append(Paragraph(additional, styles['Normal']))
    
    @staticmethod
    def _add_footer(story, styles, data):
        """Add document footer."""
        story.append(Spacer(1, 0.5*inch))
        footer = Paragraph(
            f"<i>Generated by CASER Profile Builder v{data.get('app_version', '1.0')}</i>",
            styles['Italic']
        )
        story.append(footer)


def create_pdf_from_profile(data, output_path):
    """Simplified function for creating PDF."""
    return PDFGenerator.create_profile_pdf(data, output_path)
```

