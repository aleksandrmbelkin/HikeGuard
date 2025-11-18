# Kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.uix.screenmanager import FadeTransition

# Экраны
from screens.search import SearchScreen
from screens.database import DatabaseScreen
from screens.results import ResultsScreen
from screens.file import FileScreen 


class HikeGuardApp(App):
    def build(self):
        # Настройка окна
        Window.size = (360, 800)

        self.screen_manager = ScreenManager()
        self.screen_manager.transition = FadeTransition(duration=0.2)
        self.register_screens()
        return self.screen_manager
    
    def register_screens(self):
        '''Регистрация экранов приложения:'''
        # Экран поиска
        search_screen = SearchScreen()
        self.screen_manager.add_widget(search_screen)

        # Экран результатов
        results_screen = ResultsScreen()
        self.screen_manager.add_widget(results_screen)

        # Экран базы данных
        database_screen = DatabaseScreen()
        self.screen_manager.add_widget(database_screen)

        # Экран детальной информации
        details_screen = FileScreen()
        self.screen_manager.add_widget(details_screen)

        self.screen_manager.current = 'search'
    
    def on_stop(self):
        # Закрытие приложения
        print("Приложение закрывается")


if __name__ == '__main__':
    HikeGuardApp().run()
