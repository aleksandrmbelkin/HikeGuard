# Kivy
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.metrics import dp

# Экран Поиска
class SearchScreen(Screen):
    results_count = NumericProperty(1)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'search'
        self.create_ui()
    
    def create_ui(self):
        # Главный контейнер
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[dp(30), dp(20), dp(30), dp(20)],
            spacing=dp(20)
        )
        
        # Добавляем фон к главному контейнеру
        with main_layout.canvas.before:
            Color(1, 1, 1, 1)  # Белый фон чтобы перекрыть затемнение
            self.main_bg = Rectangle(
                pos=main_layout.pos,
                size=main_layout.size,
                source='data/assets/background.png'
            )
        main_layout.bind(pos=self.update_main_bg, size=self.update_main_bg)
        
        # Заголовок приложения
        title = Label(
            text='Hike Guard',
            font_size=dp(52),
            bold=True,
            color=(0.1, 0.1, 0, 1),
            size_hint_y=0.3,
            halign='center',
        )
        main_layout.add_widget(title)

        # Отступ перед поиском
        main_layout.add_widget(Widget(size_hint_y=0.15))
        
        # Контейнер поиска
        search_layout = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(15)
        )
        
        # Поле ввода поиска
        search_input_container = BoxLayout()
        self.search_input = TextInput(
            font_size=dp(18),
            hint_text='Поиск...',
            hint_text_color=(0.3, 0.3, 0.3, 1),
            background_color=(0, 0, 0, 0),
            foreground_color=(0, 0, 0, 1),
            padding=[dp(20), dp(15)],
            multiline=False,
            background_normal='',
            background_active='',
            background_disabled_normal='',
            disabled_foreground_color=(0, 0, 0, 1),
            write_tab=False,
        )
        # Отключаем эффект затемнения при фокусе
        self.search_input.bind(focus=self.on_input_focus)

        # Фон поиска
        with search_input_container.canvas.before:
            Color(1, 1, 1, 1)  # Белый фон
            self.search_input_bg = RoundedRectangle(
                pos=self.search_input.pos,
                size=self.search_input.size,
                radius=[dp(25),]
            )
        search_input_container.bind(pos=self.update_search_input_bg, size=self.update_search_input_bg)
        search_input_container.add_widget(self.search_input)
        search_layout.add_widget(search_input_container)
        
        # Кнопка поиска
        search_button_container = BoxLayout(
            size_hint_x=0.2,
        )
        
        # Создаем виджет вместо кнопки
        search_button = Widget()
        
        # Фон кнопки поиска
        with search_button_container.canvas.before:
            Color(1, 1, 1, 1)  # Белый фон
            self.search_button_bg = Rectangle(
                pos=search_button.pos,
                size=search_button.size,
                source='data/assets/search.png'
            )
        search_button_container.bind(
            pos=self.update_search_button_bg,
            size=self.update_search_button_bg,
        )

        # Обрабатываем нажатие на виджет
        search_button.bind(on_touch_down=self.on_search_button_touch)
        search_button_container.add_widget(search_button)
        search_layout.add_widget(search_button_container)
        main_layout.add_widget(search_layout)
        
        # Контейнер количества результатов
        results_layout = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(0)
        )
        
        # Метка количества ответов
        results_label = Label(
            text='Кол-во ответов:',
            font_size=dp(22),
            color=(0.1, 0.1, 0.1, 1),
            halign='left',
            size_hint_x=0.65
        )
        results_layout.add_widget(results_label)

        # Разделитель количества
        results_separator = Widget(
            size_hint_x=0.01,
        )
        with results_separator.canvas:
            Color(0, 0, 0, 0.6)
            self.results_separator_rect = Rectangle(pos=results_separator.pos, size=results_separator.size)
        results_separator.bind(pos=self.update_results_separator, size=self.update_results_separator)
        results_layout.add_widget(results_separator)
        
        # Поле ввода количества результатов
        self.results_input = TextInput(
            text='1',
            halign='center',
            font_size=dp(18),
            hint_text='1-5',
            hint_text_color=(0.3, 0.3, 0.3, 1),
            background_color=(0.8, 0.8, 0.8, 1),
            foreground_color=(0, 0, 0, 1),
            padding=[dp(10), dp(15)],
            multiline=False,
            background_normal='',
            background_active='',
            input_filter='int',
            size_hint_x=0.2,
            background_disabled_normal='',
            disabled_foreground_color=(0, 0, 0, 1),
            write_tab=False,
        )
        self.results_input.bind(text=self.results_change)
        self.results_input.bind(focus=self.on_input_focus)
        
        # Добавляем фон к контейнеру
        with results_layout.canvas.before:
            Color(1, 1, 1, 1)  # Белый фон
            self.kolvo_bg = RoundedRectangle(
                pos=results_layout.pos,
                size=results_layout.size,
                radius=[dp(5),]
            )
        results_layout.bind(pos=self.update_results_layout_bg, size=self.update_results_layout_bg)
        
        results_layout.add_widget(self.results_input)
        main_layout.add_widget(results_layout)
        
        # Разделитель
        separator = Widget(size_hint_y=None, height=dp(3))
        with separator.canvas:
            Color(1, 1, 1, 0.6)
            self.separator_rect = Rectangle(pos=separator.pos, size=separator.size)
        separator.bind(pos=self.update_separator, size=self.update_separator)
        main_layout.add_widget(separator)
        
        # Отступ перед кнопкой базы данных
        main_layout.add_widget(Widget(size_hint_y=0.4))
        
        # Контейнер для кнопки БД
        database_button_container = BoxLayout(
            size_hint_y=None,
            height=dp(70),
        )
        
        # Кнопка БД - также используем виджет
        database_button = Widget()
        database_button.bind(on_touch_down=self.on_database_button_touch)

        # Добавляем фон к контейнеру
        with database_button_container.canvas.before:
            Color(1, 1, 1, 1)  # Белый фон
            self.database_bg = RoundedRectangle(
                pos=database_button.pos,
                size=database_button.size,
                radius=[dp(20),]
            )
            
            # Текст кнопки БД
            Color(0.2, 0.2, 0.2, 1)
            self.database_bg_color = RoundedRectangle(
                pos=database_button.pos,
                size=database_button.size,
                radius=[dp(20),]
            )
            
            Color(1, 1, 1, 1)
            self.database_label = Label(
                text='База данных',
                font_size=dp(24),
                bold=True,
                pos=database_button.pos,
                size=database_button.size
            )
        database_button_container.bind(
            pos=self.update_database_button_bg, 
            size=self.update_database_button_bg
        )

        database_button_container.add_widget(database_button)
        main_layout.add_widget(database_button_container)
        
        # Отступ внизу
        main_layout.add_widget(Widget(size_hint_y=0.05))
        self.add_widget(main_layout)
    
    def on_input_focus(self, instance, value):
        # Принудительно обновляем цвет фона чтобы избежать затемнения
        if hasattr(instance, 'background_color'):
            instance.background_color = instance.background_color
    
    '''Обновления фонов:'''
    def update_main_bg(self, instance, value):
        self.main_bg.pos = instance.pos
        self.main_bg.size = instance.size
    
    def update_search_input_bg(self, instance, value):
        self.search_input_bg.pos = instance.pos
        self.search_input_bg.size = instance.size

    def update_search_button_bg(self, instance, value):
        self.search_button_bg.pos = instance.pos
        self.search_button_bg.size = instance.size
        
    def update_results_layout_bg(self, instance, value):
        self.kolvo_bg.pos = instance.pos
        self.kolvo_bg.size = instance.size
    
    def update_results_separator(self, instance, value):
        self.results_separator_rect.pos = instance.pos
        self.results_separator_rect.size = instance.size
    
    def update_separator(self, instance, value):
        self.separator_rect.pos = instance.pos
        self.separator_rect.size = instance.size
    
    def update_database_button_bg(self, instance, value):
        self.database_bg.pos = instance.pos
        self.database_bg.size = instance.size
        self.database_bg_color.pos = instance.pos
        self.database_bg_color.size = instance.size
        if hasattr(self, 'database_label'):
            self.database_label.pos = instance.pos
            self.database_label.size = instance.size

    '''Обработчики нажатий на кастомные кнопки'''
    def on_search_button_touch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.search()
            return True
        return False
    
    def on_database_button_touch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.open_database()
            return True
        return False

    '''Обработчики взаимодействий:'''
    def search(self):
        search_text = self.search_input.text
        if search_text:
            # Передаем данные в экран результатов
            results_screen = self.manager.get_screen('results')
            results_screen.show_results(search_text, self.results_count)
            self.manager.current = 'results'

    def results_change(self, instance, value):
        if value and value.isdigit():
            num = int(value)
            if num < 1:
                instance.text = '1'
                self.results_count = 1
            elif num > 5:
                if 1 <= num % 10 <= 5:
                    instance.text = str(num % 10)
                    self.results_count = num % 10
                else:
                    instance.text = str(self.results_count)
            else:
                self.results_count = num
        elif value == '':
            self.results_count = 1
        else:
            instance.text = str(self.results_count)
    
    def results_focus(self, instance, value):
        if not value:
            if not instance.text:
                instance.text = '1'
                self.results_count = 1
    
    def open_database(self):
        self.manager.current = 'database'