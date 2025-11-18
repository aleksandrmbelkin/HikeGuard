from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.metrics import dp

# Экран БД
class DatabaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'database'
        self.create_ui()
    
    def create_ui(self):
        # Главный контейнер
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[dp(20), dp(20), dp(20), dp(20)],
            spacing=dp(15)
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
        title = Label(
            text='База данных',
            font_size=dp(38),
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=0.1,
            halign='center'
        )
        main_layout.add_widget(title)
        
        # Контейнер для контента
        content_scroll = ScrollView()
        content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(30)
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))

        for _ in range(10):
            content_layout.add_widget(Label(
                text='12345',
                size_hint_x=0,
                size_hint_y=0,
                halign='left',
                text_size=(None, None)
                ))
        
        content_scroll.add_widget(content_layout)
        main_layout.add_widget(content_scroll)

        # Контейнер для кнопки возврата
        back_button_container = BoxLayout(
            size_hint_y=None,
            height=dp(60),
        )
        
        # Кнопка возврата
        back_button = Button(
            text='Назад',
            font_size=dp(20),
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
                pos=back_button.pos,
                size=back_button.size,
                radius=[dp(20),]
            )
        back_button_container.bind(pos=self.update_back_button_bg, size=self.update_back_button_bg)
        back_button_container.add_widget(back_button)
        main_layout.add_widget(back_button_container)
        
        self.add_widget(main_layout)
    
    '''Обновления фонов:'''
    def update_main_bg(self, instance, value): # Обновление главного фона
        self.main_bg.pos = instance.pos
        self.main_bg.size = instance.size

    def update_back_button_bg(self, instance, value): # Обновление кнопки возврата
        self.back_button_bg.pos = instance.pos
        self.back_button_bg.size = instance.size

    '''Обработчики взаимодействий:'''
    def go_back(self, instance): # Назад
        self.manager.current = 'search'
