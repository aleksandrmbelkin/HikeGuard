# Kivy
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.properties import StringProperty, NumericProperty
from kivy.metrics import dp

# Бэкенд
from rag.search_engine import *

# Экран Результатов
class ResultsScreen(Screen):
    results = [{'text': 'Перелом, вывих: 1. Сначала смотрим. Особенно, если пострадавший без сознания или упал с высоты на спину и область головы. При риске смещения обломков, вероятном переломе позвонков, костей таза двигать человека категорически нельзя. Первая помощь оказывается на месте. При незначительных травмах, например, растяжении, можно наложить тугую повязку, а дальнейшую помощь оказать в более удобном месте или вернуться для этого в лагерь. 2. Обезболивание. В аптечке первой помощи ПИКа есть нимесил, кетанов', 'score': 0.8382720947265625, 'index': 20, 'source': 'first_aid_1.txt', 'para_id': 6, 'chunk_id': 0}, {'text': 'версального рецепта тут нет. Главное - обездвижить кость плотной повязкой и шиной в двух местах - выше и ниже перелома. Ноги можно прибинтовать друг к другу, руки к туловищу или повесить в “косынку”, одетую на шею, использовать импровизированные шины из веток дерева, лыжных палок, лыж. При переломах позвоночника, ребер и костей таза пострадавший с минимумом движений укладывается на широкую плоскую шину (доска, фанера, сноуборд без креплений и т.п.) и фиксируется для исключения смещения отломков.', 'score': 0.8312132358551025, 'index': 22, 'source': 'first_aid_1.txt', 'para_id': 6, 'chunk_id': 2}, {'text': 'овании по маршруту принимать в зависимости от состояния больного.', 'score': 0.7951524257659912, 'index': 7, 'source': 'first_aid_1.txt', 'para_id': 0, 'chunk_id': 1}]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'results'
        self.create_ui()

    def request(self, query, results_count):
        search_engine = create_search_engine()
        self.results = search_engine.search(query, top_k=results_count)
    
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
            text='Результаты:',
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
            size_hint_y=None,
            orientation='vertical',
            spacing=dp(15),
            padding=[dp(5), dp(5), dp(5), dp(5)]
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Результаты
        for i, result in enumerate(self.results, 1):
            # Создаем карточку результата с автоматической высотой
            result_card = self.create_result_card(i, result)
            content_layout.add_widget(result_card)

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
                pos=back_button_container.pos,
                size=back_button_container.size,
                radius=[dp(20),]
            )
        back_button_container.bind(pos=self.update_back_button_bg, size=self.update_back_button_bg)
        back_button_container.add_widget(back_button)
        main_layout.add_widget(back_button_container)
        
        self.add_widget(main_layout)
    
    def create_result_card(self, index, result):
        """Создает карточку результата с автоматической высотой"""
        # Главный контейнер для одного результата
        result_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(8),
            padding=[dp(10), dp(10)]
        )
        
        # Рассчитываем высоту на основе длины текста
        text_length = len(result['text'])
        if text_length < 150:
            container_height = dp(140)
        elif text_length < 300:
            container_height = dp(180)
        else:
            container_height = dp(220)
        
        result_container.height = container_height
        
        # Фон для всей карточки
        with result_container.canvas.before:
            Color(0.95, 0.95, 0.95, 0.9)  # Светло-серый фон с прозрачностью
            card_bg = RoundedRectangle(
                pos=result_container.pos,
                size=result_container.size,
                radius=[dp(15),]
            )
        
        # Привязка фона карточки
        result_container.bind(
            pos=lambda instance, value, bg=card_bg: setattr(bg, 'pos', instance.pos),
            size=lambda instance, value, bg=card_bg: setattr(bg, 'size', instance.size)
        )
        
        # Заголовок результата
        header_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.2,
            spacing=dp(10)
        )
        
        result_title = Label(
            text=f"[b]Результат {index}:[/b]",
            font_size=dp(18),
            color=(0.1, 0.1, 0.1, 1),
            halign='left',
            markup=True,
            size_hint_x=0.7
        )
        
        score_label = Label(
            text=f"Совпадение: {result['score']:.1%}",
            font_size=dp(14),
            color=(0.4, 0.4, 0.4, 1),
            halign='right',
            size_hint_x=0.3
        )
        
        header_layout.add_widget(result_title)
        header_layout.add_widget(score_label)
        result_container.add_widget(header_layout)
        
        # Текст результата
        text_container = BoxLayout(
            orientation='vertical',
            size_hint_y=0.65
        )
        
        # Обрезаем текст если слишком длинный
        display_text = result['text']
        if len(display_text) > 250:
            display_text = display_text[:250] + "..."
        
        result_text = Label(
            text=display_text,
            font_size=dp(16),
            color=(0.2, 0.2, 0.2, 1),
            halign='left',
            valign='top',
            text_size=(text_container.width - dp(20), None),
            size_hint_y=1.0
        )
        
        # Обновляем text_size при изменении размера
        def update_text_size(container, size):
            result_text.text_size = (container.width - dp(20), None)
        
        text_container.bind(size=update_text_size)
        text_container.add_widget(result_text)
        result_container.add_widget(text_container)
        
        # Контейнер для кнопки "подробнее"
        button_container = BoxLayout(
            size_hint_y=0.15,
            size_hint_x=0.35,
            pos_hint={'center_x': 0.5}
        )
        
        # Кнопка "подробнее"
        details_button = Button(
            text='подробнее',
            font_size=dp(14),
            size_hint=(1, 1),
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1),
            background_normal=''
        )
        
        # Привязываем кнопку к текущему результату
        details_button.result_index = index - 1
        details_button.bind(on_press=self.show_details)
        
        # Фон для кнопки
        with button_container.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            button_bg = RoundedRectangle(
                pos=button_container.pos,
                size=button_container.size,
                radius=[dp(8),]
            )
        
        # Привязка фона кнопки
        button_container.bind(
            pos=lambda instance, value, bg=button_bg: setattr(bg, 'pos', instance.pos),
            size=lambda instance, value, bg=button_bg: setattr(bg, 'size', instance.size)
        )
        
        button_container.add_widget(details_button)
        result_container.add_widget(button_container)
        
        return result_container
    
    '''Обновления фонов:'''
    def update_main_bg(self, instance, value):
        self.main_bg.pos = instance.pos
        self.main_bg.size = instance.size

    def update_back_button_bg(self, instance, value):
        self.back_button_bg.pos = instance.pos
        self.back_button_bg.size = instance.size
    
    def show_details(self, instance):
        result_index = instance.result_index
        if 0 <= result_index < len(self.results):
            selected_result = self.results[result_index]
            print(f"Подробнее для результата {result_index + 1}:")
            print(f"Текст: {selected_result['text']}")
            print(f"Источник: {selected_result['source']}")
            print(f"Совпадение: {selected_result['score']:.1%}")
            # Здесь можно добавить переход на экран с детальной информацией

    '''Обработчики взаимодействий:'''
    def go_back(self, instance):
        self.manager.current = 'search'