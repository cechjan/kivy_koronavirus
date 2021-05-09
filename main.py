from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.lang import Builder
# from modules.kraje import Kraje
from modules.kraje import Nakazeni
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.picker import MDDatePicker
import datetime


class DatabaseScreen(Screen):
    pass


class Test(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Amber"
        builder = Builder.load_file('main.kv')
        # self.kraje = Kraje()
        self.nakazeni = Nakazeni()
        builder.ids.navigation.ids.tab_manager.screens[0].add_widget(self.nakazeni)
        return builder

    def show_datepicker(self):
        picker = MDDatePicker()
        picker.bind(on_save=self.get_date)
        picker.open()

    def get_date(self, the_date, *args):
        datum = the_date._current_selected_date

        f = open("ulozeni_data.txt", "w")
        f.write(f"{datetime.date(datum[2], datum[1], datum[0])}")
        f.close()


Test().run()
