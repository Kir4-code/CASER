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
    """Класс для генерации PDF документов из данных профиля."""
    
    @staticmethod
    def create_profile_pdf(profile_data, output_path):
        """
        Создает PDF документ из данных профиля.
        
        Args:
            profile_data (dict): Данные профиля
            output_path (str): Путь для сохранения PDF
            
        Returns:
            str: Путь к сохраненному файлу
        """
        try:
            # Создание документа
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                topMargin=2*cm,
                bottomMargin=2*cm,
                leftMargin=2*cm,
                rightMargin=2*cm
            )
            
            # Получение стилей
            styles = getSampleStyleSheet()
            
            # Создание кастомных стилей
            PDFGenerator._setup_custom_styles(styles)
            
            # Сбор элементов документа
            story = []
            
            # Добавление элементов
            PDFGenerator._add_header(story, styles, profile_data)
            PDFGenerator._add_personal_info(story, styles, profile_data)
            PDFGenerator._add_biography(story, styles, profile_data)
            PDFGenerator._add_contacts(story, styles, profile_data)
            PDFGenerator._add_photos(story, styles, profile_data)
            PDFGenerator._add_additional_info(story, styles, profile_data)
            PDFGenerator._add_footer(story, styles, profile_data)
            
            # Сборка документа
            doc.build(story)
            
            logger.info(f"PDF created successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to create PDF: {str(e)}")
            raise
    
    @staticmethod
    def _setup_custom_styles(styles):
        """Настройка кастомных стилей для документа."""
        # Стиль для подзаголовков
        styles.add(ParagraphStyle(
            name='SubTitle',
            parent=styles['Heading2'],
            fontSize=12,
            spaceAfter=12,
            textColor=colors.HexColor('#0055a5')
        ))
        
        # Стиль для метаданных
        styles.add(ParagraphStyle(
            name='Meta',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.gray,
            spaceAfter=3
        ))
    
    @staticmethod
    def _add_header(story, styles, data):
        """Добавление заголовка документа."""
        # Основной заголовок
        title = Paragraph(
            f"<b>PERSONAL PROFILE:</b> {data.get('full_name', 'Unnamed Profile')}",
            styles['Title']
        )
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
    
    # ... остальные методы для добавления секций ...


# Для обратной совместимости
def create_pdf_from_profile(data, output_path):
    """Упрощенная функция для создания PDF."""
    return PDFGenerator.create_profile_pdf(data, output_path)