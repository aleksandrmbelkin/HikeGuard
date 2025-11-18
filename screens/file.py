from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.core.image import Image as CoreImage
from kivy.metrics import dp
from io import BytesIO
import os, fitz

DOCUMENTS = {
    'osnovi.txt': 'Polnoe_rukovodstvo_po_vizivaniyu.pdf'
}

class FileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'file'
        self.current_result = None
        self.current_page = 0
        self.pdf_document = None
        self.total_pages = 0
        self.fullscreen_mode = False
        
    def show_file(self, result_data):
        self.current_result = result_data
        self.current_page = result_data.get('page', 1) - 1
        self.fullscreen_mode = False
        self.create_ui()
    
    def create_ui(self):
        self.clear_widgets()
        
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[dp(5), dp(5), dp(5), dp(5)],
            spacing=dp(8)
        )

        with main_layout.canvas.before:
            self.main_bg = Rectangle(
                pos=main_layout.pos,
                size=main_layout.size,
                source='data/assets/background.png'
            )
        main_layout.bind(pos=self.update_main_bg, size=self.update_main_bg)
        
        # Контейнер для PDF изображения
        pdf_container = BoxLayout(
            orientation='vertical',
            size_hint_y=0.82,
            spacing=dp(5),
            padding=[dp(2), dp(2)]
        )
        
        # Изображение страницы PDF
        self.pdf_image = Image(
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=True
        )
        
        # Добавляем обработчик двойного тапа для полноэкранного режима
        self.pdf_image.bind(on_touch_down=self.on_image_touch)
        self.last_touch_time = 0
        
        pdf_container.add_widget(self.pdf_image)
        main_layout.add_widget(pdf_container)
        
        # Контейнер для кнопок навигации (скрывается в полноэкранном режиме)
        self.nav_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.1,
            spacing=dp(40),
            padding=[dp(15), dp(2)]
        )
        
        # Кнопка "Влево"
        left_button = Button(
            size_hint=(0.35, 1),
            background_normal='data/assets/buttons/left.png',
            background_color=(1, 1, 1, 1),
            background_down='data/assets/buttons/left.png'
        )
        left_button.bind(on_press=self.previous_page)
        
        self.page_label = Label(
            text='Загрузка...',
            font_size=dp(22),
            bold=True,
            color=(1, 1, 1, 1),
            halign='center',
            size_hint=(0.3, 1)
        )
        
        # Кнопка "Вправо"
        right_button = Button(
            size_hint=(0.35, 1),
            background_normal='data/assets/buttons/right.png',
            background_color=(1, 1, 1, 1),
            background_down='data/assets/buttons/right.png'
        )
        right_button.bind(on_press=self.next_page)
        
        self.nav_container.add_widget(left_button)
        self.nav_container.add_widget(self.page_label)
        self.nav_container.add_widget(right_button)
        main_layout.add_widget(self.nav_container)
        
        # Контейнер для кнопки возврата (скрывается в полноэкранном режиме)
        self.back_button_container = BoxLayout(
            size_hint_y=0.08,
        )
        
        # Кнопка "Назад"
        back_button = Button(
            text='Назад',
            font_size=dp(16),
            bold=True,
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
            background_normal='',
            background_down=''
        )
        back_button.bind(on_press=self.go_back)

        with self.back_button_container.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.back_button_bg = RoundedRectangle(
                pos=self.back_button_container.pos,
                size=self.back_button_container.size,
                radius=[dp(12),]
            )
        self.back_button_container.bind(pos=self.update_back_button_bg, size=self.update_back_button_bg)
        self.back_button_container.add_widget(back_button)
        main_layout.add_widget(self.back_button_container)
        
        self.add_widget(main_layout)
        self.load_pdf_page()
    
    def on_image_touch(self, instance, touch):
        """Обработчик касания изображения для полноэкранного режима"""
        if instance.collide_point(*touch.pos):
            current_time = touch.time_start
            # Проверяем двойное касание (в пределах 0.3 секунды)
            if current_time - self.last_touch_time < 0.3:
                self.toggle_fullscreen()
                return True
            self.last_touch_time = current_time
        return False
    
    def toggle_fullscreen(self):
        """Переключает полноэкранный режим"""
        self.fullscreen_mode = not self.fullscreen_mode
        
        if self.fullscreen_mode:
            # Входим в полноэкранный режим - скрываем элементы управления
            self.nav_container.opacity = 0
            self.nav_container.disabled = True
            self.back_button_container.opacity = 0
            self.back_button_container.disabled = True
            
            # Увеличиваем область изображения
            self.pdf_image.parent.size_hint_y = 0.95
        else:
            # Выходим из полноэкранного режима - показываем элементы управления
            self.nav_container.opacity = 1
            self.nav_container.disabled = False
            self.back_button_container.opacity = 1
            self.back_button_container.disabled = False
            
            # Возвращаем нормальный размер изображения
            self.pdf_image.parent.size_hint_y = 0.82
    
    def load_pdf_page(self):
        try:
            source_file = self.current_result.get('source')
            pdf_path = os.path.join('data/documents/pdf', DOCUMENTS[source_file])
            
            if os.path.exists(pdf_path):
                if self.pdf_document:
                    self.pdf_document.close()
                
                self.pdf_document = fitz.open(pdf_path)
                self.total_pages = len(self.pdf_document)
                
                if self.current_page >= self.total_pages:
                    self.current_page = self.total_pages - 1
                if self.current_page < 0:
                    self.current_page = 0
                
                page = self.pdf_document[self.current_page]
                mat = fitz.Matrix(2.0, 2.0)
                pix = page.get_pixmap(matrix=mat)
                
                # Конвертируем Pixmap в данные PNG в памяти
                img_data = pix.tobytes("png")
                
                # Создаем текстуру из данных в памяти
                texture = CoreImage(BytesIO(img_data), ext='png').texture
                
                # Устанавливаем текстуру для изображения
                self.pdf_image.texture = texture
                
                self.page_label.text = f'{self.current_page + 1}/{self.total_pages}'
                
            else:
                self.show_error("PDF файл не найден")
                
        except Exception as e:
            self.show_error(f"Ошибка загрузки PDF: {str(e)}")
    
    def previous_page(self, instance):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_pdf_page()
    
    def next_page(self, instance):
        if self.pdf_document and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.load_pdf_page()
    
    def show_error(self, message):
        self.pdf_image.source = ''
        self.page_label.text = message
        print(f"Ошибка: {message}")
    
    def update_main_bg(self, instance, value):
        self.main_bg.pos = instance.pos
        self.main_bg.size = instance.size

    def update_back_button_bg(self, instance, value):
        self.back_button_bg.pos = instance.pos
        self.back_button_bg.size = instance.size
    
    def go_back(self, instance):
        if self.pdf_document:
            self.pdf_document.close()
            self.pdf_document = None
        self.manager.current = 'results'
    
    def on_leave(self):
        if self.pdf_document:
            self.pdf_document.close()
            self.pdf_document = None