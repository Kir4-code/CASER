"""
CASER Profile Builder v1.0
Desktop application for creating person profiles with PDF export.
Author: glp
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from PIL import Image as PilImage
import os
import tempfile
import logging
from datetime import datetime
import sys


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("caser.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Константы приложения
APP_NAME = "CASER Profile Builder"
VERSION = "1.0.0"
WINDOW_SIZE = "950x850"
THEME_MODE = "dark"
COLOR_THEME = "dark-blue"


class App(ctk.CTk):
    """Главное окно приложения CASER."""
    
    def __init__(self):
        """Инициализация приложения."""
        super().__init__()
        
        # Конфигурация окна
        self.title(f"{APP_NAME} v{VERSION}")
        self.geometry(WINDOW_SIZE)

        try:
            self.iconbitmap("icon.ico")
        except:
            pass
        
        # Настройка темы
        ctk.set_appearance_mode(THEME_MODE)
        ctk.set_default_color_theme(COLOR_THEME)
        
        # Установка иконки
        self._set_window_icon()
        
        # Инициализация данных
        self.contacts = []
        self.photos = []
        self.temp_files = []  # Для временных файлов
        
        # Построение интерфейса
        self._setup_ui()
        
        # Центрирование окна
        self._center_window()
        
        # Обработка закрытия окна
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        logger.info(f"{APP_NAME} v{VERSION} initialized")
    
    def _set_window_icon(self):
        """Устанавливает иконку окна."""
        icon_paths = [
            "icon.ico",                                # В корне
            os.path.join("icons", "icon.ico"),         # В папке icons
            os.path.join(os.path.dirname(__file__), "..", "icon.ico"),  # На уровень выше
            os.path.join(os.path.dirname(__file__), "icon.ico"),        # Рядом с main.py
        ]
        
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                try:
                    self.iconbitmap(icon_path)
                    logger.info(f"Icon loaded from: {icon_path}")
                    break
                except Exception as e:
                    logger.warning(f"Failed to load icon from {icon_path}: {e}")
                    continue
    
    def _center_window(self):
        """Центрирует окно на экране."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def _setup_ui(self):
        """Настраивает пользовательский интерфейс."""
        # Хедер
        self._create_header()
        
        # Основная форма
        self._create_main_form()
    
    def _create_header(self):
        """Создает верхнюю панель."""
        header = ctk.CTkFrame(self, height=80, corner_radius=0, fg_color="#1a1a1a")
        header.pack(fill="x", pady=(0, 10))
        header.pack_propagate(False)
        
        # Логотип
        logo_frame = ctk.CTkFrame(header, fg_color="transparent")
        logo_frame.pack(side="left", padx=25, pady=25)
        
        ctk.CTkLabel(
            logo_frame,
            text="📄",
            font=ctk.CTkFont(size=28)
        ).pack(side="left")
        
        ctk.CTkLabel(
            logo_frame,
            text="CASER",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(side="left", padx=(10, 5))
        
        ctk.CTkLabel(
            logo_frame,
            text=f"v{VERSION}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(side="left")
        
        # Кнопка сохранения
        self.save_btn = ctk.CTkButton(
            header,
            text="💾 SAVE PDF",
            font=ctk.CTkFont(size=18, weight="bold"),
            height=55,
            fg_color="#0055a5",
            hover_color="#004080",
            width=220,
            command=self._save_profile
        )
        self.save_btn.pack(side="right", padx=25, pady=17)
    
    def _create_main_form(self):
        """Создает основную форму для ввода данных."""
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            width=900,
            corner_radius=10,
            fg_color="#2b2b2b"
        )
        self.scroll_frame.pack(padx=25, pady=10, fill="both", expand=True)
        
        # Словарь для полей ввода
        self.entries = {}
        
        # Создание всех секций
        self._create_personal_info_section()
        self._create_contacts_section()
        self._create_photos_section()
        self._create_custom_section()
    
    def _create_personal_info_section(self):
        """Создает секцию персональной информации."""
        # Заголовок секции
        ctk.CTkLabel(
            self.scroll_frame,
            text="👤 PERSONAL INFORMATION",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 15))
        
        # Поля ввода
        fields = [
            ("Full Name", "John Smith"),
            ("Date of Birth", "01.01.1990"),
            ("Position", "Software Developer"),
            ("Tags", "#python #developer #backend")
        ]
        
        for label, placeholder in fields:
            ctk.CTkLabel(
                self.scroll_frame,
                text=f"{label}:",
                font=ctk.CTkFont(size=13)
            ).pack(anchor="w", padx=20, pady=(5, 5))
            
            entry = ctk.CTkEntry(
                self.scroll_frame,
                width=850,
                height=45,
                placeholder_text=placeholder,
                font=ctk.CTkFont(size=14),
                corner_radius=8,
                border_width=2,
                fg_color="#3a3a3a",
                border_color="#4a4a4a"
            )
            entry.pack(padx=20, fill="x", pady=(0, 10))
            
            key = label.lower().replace(" ", "_")
            self.entries[key] = entry
        
        # Биография
        ctk.CTkLabel(
            self.scroll_frame,
            text="📖 Biography:",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        self.bio_text = ctk.CTkTextbox(
            self.scroll_frame,
            width=850,
            height=120,
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            border_width=2,
            fg_color="#3a3a3a",
            border_color="#4a4a4a"
        )
        self.bio_text.pack(padx=20, fill="x", pady=(0, 15))
        
        # Заметки
        ctk.CTkLabel(
            self.scroll_frame,
            text="📝 Notes:",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", padx=20, pady=(5, 5))
        
        self.notes_text = ctk.CTkTextbox(
            self.scroll_frame,
            width=850,
            height=90,
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            border_width=2,
            fg_color="#3a3a3a",
            border_color="#4a4a4a"
        )
        self.notes_text.pack(padx=20, fill="x", pady=(0, 20))
    
    def _create_contacts_section(self):
        """Создает секцию контактов."""
        ctk.CTkLabel(
            self.scroll_frame,
            text="📞 CONTACTS",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 15))
        
        # Фрейм для управления контактами
        contacts_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="#3a3a3a",
            corner_radius=8
        )
        contacts_frame.pack(padx=20, fill="x")
        
        # Поле ввода нового контакта
        self.contact_entry = ctk.CTkEntry(
            contacts_frame,
            placeholder_text="Phone / Email / Social Media / Website",
            height=45,
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            border_width=2,
            fg_color="#4a4a4a",
            border_color="#5a5a5a"
        )
        self.contact_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        
        # Кнопка добавления
        ctk.CTkButton(
            contacts_frame,
            text="➕ Add",
            width=100,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#0055a5",
            hover_color="#004080",
            command=self._add_contact
        ).pack(side="right", padx=10, pady=10)
        
        # Список контактов
        self.contacts_list = ctk.CTkTextbox(
            self.scroll_frame,
            width=850,
            height=100,
            state="disabled",
            font=ctk.CTkFont(size=13),
            corner_radius=8,
            border_width=2,
            fg_color="#3a3a3a",
            border_color="#4a4a4a"
        )
        self.contacts_list.pack(padx=20, pady=(10, 20), fill="x")
    
    def _create_photos_section(self):
        """Создает секцию фотографий."""
        ctk.CTkLabel(
            self.scroll_frame,
            text="🖼️ PHOTOS",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 15))
        
        # Фрейм для управления фотографиями
        photos_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="#3a3a3a",
            corner_radius=8
        )
        photos_frame.pack(padx=20, fill="x")
        
        # Список фотографий
        self.photos_list = ctk.CTkTextbox(
            photos_frame,
            height=100,
            state="disabled",
            font=ctk.CTkFont(size=13),
            corner_radius=8,
            border_width=2,
            fg_color="#4a4a4a",
            border_color="#5a5a5a"
        )
        self.photos_list.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Кнопки управления
        btn_frame = ctk.CTkFrame(photos_frame, fg_color="transparent")
        btn_frame.pack(side="right", padx=10, pady=10, fill="y")
        
        ctk.CTkButton(
            btn_frame,
            text="📁 Add Photo",
            width=120,
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color="#0055a5",
            hover_color="#004080",
            command=self._add_photo
        ).pack(pady=(0, 5))
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Clear All",
            width=120,
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color="#d9534f",
            hover_color="#c9302c",
            command=self._clear_photos
        ).pack()
    
    def _create_custom_section(self):
        """Создает кастомную секцию."""
        ctk.CTkLabel(
            self.scroll_frame,
            text="✨ ADDITIONAL INFORMATION",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 15))
        
        self.custom_text = ctk.CTkTextbox(
            self.scroll_frame,
            width=850,
            height=160,
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            border_width=2,
            fg_color="#3a3a3a",
            border_color="#4a4a4a"
        )
        self.custom_text.pack(padx=20, fill="x", pady=(0, 30))
    
    def _add_contact(self):
        """Добавляет новый контакт."""
        contact = self.contact_entry.get().strip()
        
        if not contact:
            messagebox.showwarning("Empty Field", "Please enter a contact before adding.")
            return
        
        if contact in self.contacts:
            messagebox.showinfo("Duplicate", "This contact is already in the list.")
            return
        
        self.contacts.append(contact)
        self._update_contacts_list()
        self.contact_entry.delete(0, "end")
        
        logger.info(f"Added contact: {contact}")
    
    def _update_contacts_list(self):
        """Обновляет отображение списка контактов."""
        self.contacts_list.configure(state="normal")
        self.contacts_list.delete("1.0", "end")
        
        if not self.contacts:
            self.contacts_list.insert("end", "No contacts added yet...")
        else:
            for i, contact in enumerate(self.contacts, 1):
                self.contacts_list.insert("end", f"{i}. {contact}\n")
        
        self.contacts_list.configure(state="disabled")
    
    def _add_photo(self):
        """Добавляет фотографию."""
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
        
        photo_path = filedialog.askopenfilename(
            title="Select Photo",
            filetypes=filetypes
        )
        
        if not photo_path:
            return
        
        if not os.path.exists(photo_path):
            messagebox.showerror("Error", "Selected file does not exist.")
            return
        
        if photo_path in self.photos:
            messagebox.showinfo("Duplicate", "This photo is already added.")
            return
        
        # Проверяем размер файла (макс 10MB)
        file_size = os.path.getsize(photo_path) / (1024 * 1024)
        if file_size > 10:
            if not messagebox.askyesno("Large File", 
                                      f"File size is {file_size:.1f}MB (max 10MB).\nContinue anyway?"):
                return
        
        self.photos.append(photo_path)
        self._update_photos_list()
        
        logger.info(f"Added photo: {os.path.basename(photo_path)} ({file_size:.1f}MB)")
    
    def _update_photos_list(self):
        """Обновляет отображение списка фотографий."""
        self.photos_list.configure(state="normal")
        self.photos_list.delete("1.0", "end")
        
        if not self.photos:
            self.photos_list.insert("end", "No photos added yet...")
        else:
            for i, photo_path in enumerate(self.photos, 1):
                filename = os.path.basename(photo_path)
                file_size = os.path.getsize(photo_path) / 1024  # KB
                self.photos_list.insert("end", f"{i}. {filename} ({file_size:.0f} KB)\n")
        
        self.photos_list.configure(state="disabled")
    
    def _clear_photos(self):
        """Очищает список фотографий."""
        if not self.photos:
            return
        
        if messagebox.askyesno(
            "Clear All Photos",
            f"Are you sure you want to remove all {len(self.photos)} photos?"
        ):
            self.photos.clear()
            self._update_photos_list()
            logger.info("All photos cleared")
    
    def _collect_profile_data(self):
        """Собирает все данные профиля."""
        data = {
            "full_name": self.entries["full_name"].get().strip(),
            "date_of_birth": self.entries["date_of_birth"].get().strip(),
            "position": self.entries["position"].get().strip(),
            "tags": self.entries["tags"].get().strip(),
            "biography": self.bio_text.get("1.0", "end-1c").strip(),
            "notes": self.notes_text.get("1.0", "end-1c").strip(),
            "contacts": self.contacts.copy(),
            "photos": self.photos.copy(),
            "additional_info": self.custom_text.get("1.0", "end-1c").strip(),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "app_version": VERSION
        }
        
        return data
    
    def _generate_filename(self, full_name):
        """Генерирует имя файла на основе ФИО."""
        if not full_name:
            return f"profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Берем первую часть как фамилию
        name_parts = full_name.split()
        surname = name_parts[0] if name_parts else full_name
        
        # Убираем запрещенные символы
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            surname = surname.replace(char, '_')
        
        timestamp = datetime.now().strftime("%Y%m%d")
        return f"{surname}_case_{timestamp}.pdf"
    
    def _save_profile(self):
        """Сохраняет профиль в PDF."""
        try:
            # Сбор данных
            data = self._collect_profile_data()
            
            # Проверка обязательных полей
            if not data["full_name"]:
                messagebox.showwarning(
                    "Missing Information",
                    "Please enter Full Name before saving.\nThis will be used as the filename."
                )
                self.entries["full_name"].focus_set()
                return
            
            # Генерация имени файла
            default_filename = self._generate_filename(data["full_name"])
            
            # Диалог сохранения
            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                initialfile=default_filename,
                filetypes=[
                    ("PDF Documents", "*.pdf"),
                    ("All Files", "*.*")
                ],
                title="Save Profile As"
            )
            
            if not save_path:
                return  # Пользователь отменил
            
            # Создание PDF
            self._create_pdf_document(data, save_path)
            
            # Успешное сохранение
            messagebox.showinfo(
                "Success!",
                f"✅ Profile saved successfully!\n\n"
                f"📄 File: {os.path.basename(save_path)}\n"
                f"📁 Location: {os.path.dirname(save_path)}\n\n"
                f"Total pages generated with {len(data['photos'])} photos."
            )
            
            logger.info(f"Profile saved to: {save_path}")
            
        except Exception as e:
            logger.error(f"Error saving profile: {str(e)}", exc_info=True)
            messagebox.showerror(
                "Error",
                f"Failed to save profile:\n\n{str(e)}\n\n"
                "Please check the log file for details."
            )
    
    def _create_pdf_document(self, data, save_path):
        """Создает PDF документ из данных."""
        doc = SimpleDocTemplate(save_path, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Заголовок
        title = Paragraph(
            f"<b>PERSONAL PROFILE:</b> {data['full_name']}",
            styles['Title']
        )
        story.append(title)
        story.append(Spacer(1, 0.3 * inch))
        
        # Основная информация
        info_fields = [
            ("Date of Birth", data["date_of_birth"]),
            ("Position", data["position"]),
            ("Tags", data["tags"]),
            ("Created", data["created_at"]),
            ("App Version", data["app_version"])
        ]
        
        for label, value in info_fields:
            if value:
                text = f"<b>{label}:</b> {value}"
                story.append(Paragraph(text, styles['Normal']))
                story.append(Spacer(1, 0.1 * inch))
        
        story.append(Spacer(1, 0.3 * inch))
        
        # Биография
        if data["biography"]:
            story.append(Paragraph("<b>Biography:</b>", styles['Heading2']))
            story.append(Paragraph(data["biography"], styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))
        
        # Заметки
        if data["notes"]:
            story.append(Paragraph("<b>Notes:</b>", styles['Heading2']))
            story.append(Paragraph(data["notes"], styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))
        
        # Контакты
        if data["contacts"]:
            story.append(Paragraph("<b>Contacts:</b>", styles['Heading2']))
            for contact in data["contacts"]:
                story.append(Paragraph(f"• {contact}", styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))
        
        # Фотографии
        if data["photos"]:
            story.append(Paragraph("<b>Photos:</b>", styles['Heading2']))
            
            for photo_path in data["photos"]:
                if os.path.exists(photo_path):
                    try:
                        # Создание временной копии для ReportLab
                        with tempfile.NamedTemporaryFile(
                            suffix='.jpg',
                            delete=False
                        ) as temp_file:
                            img = PilImage.open(photo_path)
                            # Конвертируем в RGB если нужно
                            if img.mode in ('RGBA', 'LA', 'P'):
                                img = img.convert('RGB')
                            img.save(temp_file.name, 'JPEG', quality=85)
                            self.temp_files.append(temp_file.name)
                            
                            # Добавление изображения в PDF
                            story.append(
                                Image(
                                    temp_file.name,
                                    width=2.5 * inch,
                                    height=3 * inch
                                )
                            )
                            story.append(
                                Paragraph(
                                    f"<i>{os.path.basename(photo_path)}</i>",
                                    styles['Italic']
                                )
                            )
                            story.append(Spacer(1, 0.1 * inch))
                    except Exception as img_error:
                        logger.error(f"Failed to add photo {photo_path}: {img_error}")
                        story.append(
                            Paragraph(
                                f"[Photo: {os.path.basename(photo_path)} - Error: {str(img_error)}]",
                                styles['Italic']
                            )
                        )
        
        # Дополнительная информация
        if data["additional_info"]:
            story.append(Paragraph("<b>Additional Information:</b>", styles['Heading2']))
            story.append(Paragraph(data["additional_info"], styles['Normal']))
        
        # Сборка документа
        doc.build(story)
        
        # Очистка временных файлов
        self._cleanup_temp_files()
    
    def _cleanup_temp_files(self):
        """Очищает временные файлы."""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except:
                pass
        self.temp_files.clear()
    
    def _on_closing(self):
        """Обработчик закрытия окна."""
        self._cleanup_temp_files()
        logger.info("Application closed")
        self.destroy()


def main():
    """Точка входа в приложение."""
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        logger.critical(f"Application crashed: {str(e)}", exc_info=True)
        messagebox.showerror(
            "Fatal Error",
            f"The application encountered a critical error:\n\n{str(e)}\n\n"
            "Please check the caser.log file for details."
        )
        raise


if __name__ == "__main__":
    main()