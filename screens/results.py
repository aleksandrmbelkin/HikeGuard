from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.metrics import dp

# Поиск
from rag.search_engine import *

# Экран Результатов
class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'results'
        self.results = []
        self.current_query = ""

    def show_results(self, query, results_count):
        """Основной метод для отображения результатов"""
        self.current_query = query
        self.results_count = results_count
        
        # Получаем результаты из поискового движка
        search_engine = create_search_engine()
        self.results = search_engine.search(query, top_k=results_count)
        
        # Обновляем интерфейс с новыми результатами
        self.update_results_display()
    
    def update_results_display(self):
        """Обновляет отображение результатов"""
        # Очищаем предыдущий контент
        self.clear_widgets()
        self.create_ui()
    
    def create_ui(self):
        """Создает UI с результатами"""
        # Главный контейнер
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[dp(15), dp(15), dp(15), dp(15)],
            spacing=dp(12)
        )

        # Добавляем фон к главному контейнеру
        with main_layout.canvas.before:
            self.main_bg = Rectangle(
                pos=main_layout.pos,
                size=main_layout.size,
                source='data/assets/background.png'
            )
        main_layout.bind(pos=self.update_main_bg, size=self.update_main_bg)
        
        # Заголовок
        title_label = Label(
            text='Результаты:',
            font_size=dp(32),
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=0.08,
            halign='center'
        )
        main_layout.add_widget(title_label)
        
        # Контейнер для контента
        content_scroll = ScrollView(
            do_scroll_x=False,
            bar_width=dp(8)
        )
        content_layout = BoxLayout(
            size_hint_y=None,
            orientation='vertical',
            spacing=dp(12)
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Добавляем карточки результатов
        for i, result in enumerate(self.results, 1):
            result_card = self.create_result_card(i, result)
            content_layout.add_widget(result_card)

        content_scroll.add_widget(content_layout)
        main_layout.add_widget(content_scroll)

        # Кнопка возврата
        back_button_container = BoxLayout(
            size_hint_y=None,
            height=dp(55),
        )
        
        back_button = Button(
            text='Назад',
            font_size=dp(18),
            bold=True,
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
            background_normal=''
        )
        back_button.bind(on_press=self.go_back)

        # Добавляем фон к контейнеру
        with back_button_container.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.back_button_bg = RoundedRectangle(
                pos=back_button_container.pos,
                size=back_button_container.size,
                radius=[dp(15),]
            )
        back_button_container.bind(pos=self.update_back_button_bg, size=self.update_back_button_bg)
        back_button_container.add_widget(back_button)
        main_layout.add_widget(back_button_container)
        
        self.add_widget(main_layout)
    
    def create_result_card(self, index, result):
        """Создает карточку результата"""
        # Главный контейнер
        result_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(6),
            padding=[dp(8), dp(8)]
        )
        
        # Фон для карточки
        with result_container.canvas.before:
            Color(0.95, 0.95, 0.95, 0.9)
            card_bg = RoundedRectangle(
                pos=result_container.pos,
                size=result_container.size,
                radius=[dp(12),]
            )
        
        # Привязка фона
        result_container.bind(
            pos=lambda instance, value, bg=card_bg: setattr(bg, 'pos', instance.pos),
            size=lambda instance, value, bg=card_bg: setattr(bg, 'size', instance.size)
        )
        
        # Текст результата с номером
        text_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[dp(12), dp(12), dp(12), dp(8)]  # Увеличил верхний отступ
        )
        
        # Текст с жирным номером и отступом
        display_text = f"\n[b]Результат {index}:[/b]\n\n{result['text']}"  # Добавил переносы для отступа
        
        # Лейбл для текста
        result_text = Label(
            text=display_text,
            font_size=dp(14),
            color=(0.2, 0.2, 0.2, 1),
            halign='left',
            valign='top',
            text_size=(text_container.width - dp(24), None),
            size_hint_y=None,
            markup=True
        )
        
        # Функции для обновления размеров
        def update_text_properties(container_instance, size):
            result_text.text_size = (container_instance.width - dp(24), None)
            
        def update_text_height(label_instance, texture_size):
            if texture_size[1] > 0:
                text_height = texture_size[1] + dp(20)
                min_height = dp(80)
                max_height = dp(400)
                calculated_height = max(min_height, min(text_height, max_height))
                label_instance.height = calculated_height
                text_container.height = calculated_height
                result_container.height = text_container.height + dp(40)
        
        # Привязываем обновление размеров
        text_container.bind(size=update_text_properties)
        result_text.bind(texture_size=update_text_height)
        
        text_container.add_widget(result_text)
        result_container.add_widget(text_container)
        
        # Кнопка "Подробнее"
        button_container = BoxLayout(
            size_hint_y=None,
            height=dp(35),
            size_hint_x=0.4,
            pos_hint={'center_x': 0.5}
        )
        
        details_button = Button(
            text='Подробнее',
            font_size=dp(12),
            size_hint=(1, 1),
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1),
            background_normal=''
        )
        
        # Сохраняем всю информацию о результате для кнопки
        details_button.result_data = result
        details_button.bind(on_press=self.show_file)
        
        # Фон для кнопки
        with button_container.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            button_bg = RoundedRectangle(
                pos=button_container.pos,
                size=button_container.size,
                radius=[dp(6),]
            )
        
        button_container.bind(
            pos=lambda instance, value, bg=button_bg: setattr(bg, 'pos', instance.pos),
            size=lambda instance, value, bg=button_bg: setattr(bg, 'size', instance.size)
        )
        
        button_container.add_widget(details_button)
        result_container.add_widget(button_container)
        
        return result_container
    
    def update_main_bg(self, instance, value):
        if hasattr(self, 'main_bg'):
            self.main_bg.pos = instance.pos
            self.main_bg.size = instance.size

    def update_back_button_bg(self, instance, value):
        if hasattr(self, 'back_button_bg'):
            self.back_button_bg.pos = instance.pos
            self.back_button_bg.size = instance.size
    
    def show_file(self, instance):
        result_data = instance.result_data
        file_screen = self.manager.get_screen('file')
        file_screen.show_file(result_data, 'results')
        self.manager.current = 'file'

    def go_back(self, instance):
        self.manager.current = 'search'