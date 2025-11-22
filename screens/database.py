from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.metrics import dp

# Экран БД
class DatabaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'database'
        
        # Список книг для отображения (позже можно заполнить данными)
        self.books_data = [
            {
                "name": "Полное руководство по выживанию", 
                "chapters": [
                    ("Введение", 8),
                    ("1. Основы", 12),
                    ("2. Стратегия", 50),
                    ("3. Климат и местность", 62),
                    ("4. Пища", 108),
                    ("5. Оборудование лагеря", 244),
                    ("6. Ориентирование", 348),
                    ("7. Передвижение", 372),
                    ("8. Здоровье", 392),
                    ("9. Выживание на море", 480),
                    ("10. Спасательные мероприятия", 504),
                    ("11. Катастрофы", 528),
                    ("Заключение", 572),
                    ("Указатель", 573)
                ]
            }
        ]
        
        self.create_ui()
    
    def create_ui(self):
        # Главный контейнер
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[dp(20), dp(20), dp(20), dp(20)],
            spacing=dp(15)
        )

        # Добавляем основной фон приложения
        with main_layout.canvas.before:
            self.main_bg = Rectangle(
                pos=main_layout.pos,
                size=main_layout.size,
                source='data/assets/background.png'
            )
        main_layout.bind(pos=self.update_main_bg, size=self.update_main_bg)
        
        # Заголовок
        title = Label(
            text='База данных',
            font_size=dp(32),
            bold=True,
            color=(0.2, 0.2, 0.2, 1),  # Темно-серый текст
            size_hint_y=0.1,
            halign='center'
        )
        main_layout.add_widget(title)
        
        # Контейнер для контента
        content_scroll = ScrollView(
            bar_width=dp(8),
            bar_color=(0.5, 0.5, 0.5, 0.5),
            scroll_type=['bars', 'content']
        )
        self.content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(12),
            padding=[dp(5), dp(5), dp(5), dp(5)]
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))

        content_scroll.add_widget(self.content_layout)
        main_layout.add_widget(content_scroll)

        # Контейнер для кнопки возврата
        back_button_container = BoxLayout(
            size_hint_y=None,
            height=dp(55),
        )
        
        # Кнопка возврата с улучшенным дизайном
        back_button = Button(
            text='Назад',
            font_size=dp(18),
            bold=True,
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
            background_normal='',
            size_hint_y=None,
            height=dp(50)
        )
        
        # Добавляем красивый фон для кнопки
        with back_button.canvas.before:
            Color(0.3, 0.3, 0.3, 1)
            self.back_button_bg = RoundedRectangle(
                pos=back_button.pos,
                size=back_button.size,
                radius=[dp(25),]
            )
        back_button.bind(
            pos=self.update_back_button_bg, 
            size=self.update_back_button_bg,
            on_press=self.go_back
        )
        
        back_button_container.add_widget(back_button)
        main_layout.add_widget(back_button_container)
        
        self.add_widget(main_layout)
        
        # Обновляем отображение книг
        self.update_books_display()
    
    def update_books_display(self):
        """Обновляет отображение списка книг"""
        self.content_layout.clear_widgets()
        
        for book in self.books_data:
            book_widget = self.create_book_widget(book)
            self.content_layout.add_widget(book_widget)
    
    def create_book_widget(self, book):
        """Создает виджет для одной книги с использованием Spinner"""
        # Основной контейнер книги
        book_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(55),
            spacing=dp(2),
            padding=[dp(2), dp(2), dp(2), dp(2)]
        )
        
        # Кастомный Spinner с улучшенным дизайном
        book_spinner = Spinner(
            text=book["name"],
            font_size=dp(16),
            bold=True,
            background_color=(0, 0, 0, 0),  # Прозрачный фон кнопки
            color=(0.1, 0.1, 0.1, 1),  # Черный текст
            background_normal='',
            background_down='',
            size_hint_y=None,
            height=dp(50),
            halign='left',
            padding_x=dp(15),
            option_cls=SpinnerOptionCustom  # Используем кастомный класс для опций
        )
        
        # Добавляем красивый фон для Spinner с черной обводкой
        with book_spinner.canvas.before:
            # Черная обводка
            Color(0.1, 0.1, 0.1, 1)  # Черный цвет
            self.spinner_border = RoundedRectangle(
                pos=(book_spinner.pos[0]-dp(1), book_spinner.pos[1]-dp(1)),
                size=(book_spinner.size[0]+dp(2), book_spinner.size[1]+dp(2)),
                radius=[dp(11),]
            )
            # Основной фон
            Color(0.95, 0.95, 0.95, 0.95)  # Светло-серый полупрозрачный
            self.spinner_bg = RoundedRectangle(
                pos=book_spinner.pos,
                size=book_spinner.size,
                radius=[dp(10),]
            )
        book_spinner.bind(pos=self.update_spinner_bg, size=self.update_spinner_bg)
        
        # Добавляем опции в spinner (только главы, без дублирования названия книги)
        spinner_values = []
        for chapter_name, page_number in book["chapters"]:
            spinner_values.append(f"{chapter_name} - стр. {page_number}")
        
        book_spinner.values = spinner_values
        book_spinner.book_data = book
        
        # Привязываем обработчик выбора
        book_spinner.bind(text=self.on_spinner_select)
        
        book_container.add_widget(book_spinner)
        
        return book_container
    
    def on_spinner_select(self, spinner, text):
        """Обработчик выбора в spinner"""
        # Ищем выбранную главу в данных книги
        for chapter_name, page_number in spinner.book_data["chapters"]:
            if text.startswith(chapter_name):
                # Подготавливаем данные для передачи в show_file
                result_data = {
                    "source": spinner.book_data["name"],
                    "page": page_number,
                    "chapter": chapter_name
                }
                self.show_file(result_data)
                # Сбрасываем spinner обратно на название книги
                spinner.text = spinner.book_data["name"]
                break
    
    def show_file(self, result_data):
        """Обработчик нажатия на главу"""
        file_screen = self.manager.get_screen('file')
        file_screen.show_file(result_data, 'database')
        self.manager.current = 'file'
    
    def add_book(self, book_data):
        """Добавляет книгу в список и обновляет отображение"""
        self.books_data.append(book_data)
        self.update_books_display()
    
    def set_books(self, books_list):
        """Устанавливает новый список книг"""
        self.books_data = books_list
        self.update_books_display()
    
    '''Обновления фонов:'''
    def update_main_bg(self, instance, value):
        self.main_bg.pos = instance.pos
        self.main_bg.size = instance.size

    def update_back_button_bg(self, instance, value):
        self.back_button_bg.pos = instance.pos
        self.back_button_bg.size = instance.size

    def update_spinner_bg(self, instance, value):
        # Обновляем позицию и размер фона и обводки
        self.spinner_bg.pos = instance.pos
        self.spinner_bg.size = instance.size
        self.spinner_border.pos = (instance.pos[0]-dp(1), instance.pos[1]-dp(1))
        self.spinner_border.size = (instance.size[0]+dp(2), instance.size[1]+dp(2))

    '''Обработчики взаимодействий:'''
    def go_back(self, instance):
        self.manager.current = 'search'


# Кастомный класс для опций Spinner с улучшенным дизайном
class SpinnerOptionCustom(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.98, 0.98, 0.98, 1)  # Очень светлый серый
        self.color = (0.1, 0.1, 0.1, 1)  # Черный текст
        self.font_size = dp(14)
        self.size_hint_y = None
        self.height = dp(40)
        self.background_normal = ''