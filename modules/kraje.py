from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, ImageLeftWidget, IconRightWidget
from kivymd.uix.menu import MDDropdownMenu
from modules.database import Database, Kraj, Pes, PocetNakazenychZaDen
from kivymd.uix.textfield import MDTextField
import datetime


class Content(BoxLayout):
    pass


class NakazeniKrajContent(BoxLayout):
    def menu_kraj(self):
        kraje = app.nakazeni.database.read_kraj()
        menu_items = [{"viewclass": "OneLineListItem", "text": f"{kraj.zkratka_kraje}",
                       "on_release": lambda x=f"{kraj.zkratka_kraje}": self.set_item(x)} for kraj in kraje]

        self.menu_states = MDDropdownMenu(
            caller=self.ids.kraj_dropdown,
            items=menu_items,
            position="auto",
            width_mult=5,
        )
        self.menu_states.open()

    def set_item(self, text_item):
        # Podle textu vybrané položky se nastaví aktuálně vybraný stát
        self.ids.kraj_dropdown.set_item(text_item)
        self.ids.kraj_dropdown.text = text_item
        # Uzavření menu
        self.menu_states.dismiss()

    def menu_pes(self):
        psi = app.nakazeni.database.read_pes()
        menu_items = [{"viewclass": "OneLineListItem", "text": f"{pes.stupen}",
                       "on_release": lambda x=f"{pes.stupen}": self.set_item_pes(x)} for pes in psi]

        self.menu_psi = MDDropdownMenu(
            caller=self.ids.pes_dropdown,
            items=menu_items,
            position="auto",
            width_mult=5,
        )
        self.menu_psi.open()

    def set_item_pes(self, text_item):
        # Podle textu vybrané položky se nastaví aktuálně vybraný stát
        self.ids.pes_dropdown.set_item(text_item)
        self.ids.pes_dropdown.text = text_item
        # Uzavření menu
        self.menu_psi.dismiss()


class PesContent(BoxLayout):
    pass


class NakazeniKrajDialog(MDDialog):
    def __init__(self, id, *args, **kwargs):
        super(NakazeniKrajDialog, self).__init__(
            # Vytvoření objektu s uživatelským obsahem (podle třídy PersonContent)
            type="custom",
            # content_cls=KrajContent(id=id),
            content_cls=NakazeniKrajContent(),
            title='Nový záznam psa',
            # text='Ahoj',
            size_hint=(0.8, 1),
            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )

        self.id = id

    def save_dialog(self, *args):
        nakazeni = {}
        # nakazeni['kraj_id'] = self.content_cls.ids.pes_zkratka_kraje.text
        nakazeni['kraj_id'] = self.content_cls.ids.kraj_dropdown.text
        # print(self.content_cls.ids.kraj_dropdown.text)
        nakazeni['pocet'] = self.content_cls.ids.pes_pocet_nakazenych.text
        # nakazeni['pes_stupen'] = self.content_cls.ids.pes_stupen.text
        nakazeni['pes_stupen'] = self.content_cls.ids.pes_dropdown.text
        nakazeni['umrti'] = self.content_cls.ids.pes_umrti.text
        f = open("ulozeni_data.txt", "r")
        nakazeni['datum'] = f.read()
        # print(nakazeni['datum'], "hhhhh", nakazeni['datum'][0:4], nakazeni['datum'][5:7], nakazeni['datum'][8:])
        nakazeni['datum'] = datetime.date(int(nakazeni['datum'][0:4]), int(nakazeni['datum'][5:7]), int(nakazeni['datum'][8:]))

        if self.id:
            nakazeni["id"] = self.id
            app.nakazeni.update(nakazeni)
        else:
            pocet = PocetNakazenychZaDen()
            # pocet.kraj_id = self.content_cls.ids.pes_zkratka_kraje.text
            pocet.kraj_id = self.content_cls.ids.kraj_dropdown.text
            pocet.pocet = self.content_cls.ids.pes_pocet_nakazenych.text
            # pocet.pes_stupen = self.content_cls.ids.pes_stupen.text
            pocet.pes_stupen = self.content_cls.ids.pes_dropdown.text
            pocet.umrti = self.content_cls.ids.pes_umrti.text
            f = open("ulozeni_data.txt", "r")
            pocet.datum = f.read()
            # print(pocet.datum)
            pocet.datum = datetime.date(int(pocet.datum[0:4]), int(pocet.datum[5:7]),
                                        int(pocet.datum[8:]))

            self.database = Database(dbtype='sqlite', dbname='koronavirus.db')
            self.database.create_nakazeni(pocet)
            app.nakazeni.rewrite_list()

        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()


class PesDialog(MDDialog):
    def __init__(self, id, *args, **kwargs):
        super(PesDialog, self).__init__(
            type="custom",
            content_cls=PesContent(),
            title='Nový záznam psa',
            size_hint=(0.8, 0.3),
            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )
        self.id = id

    def save_dialog(self, *args):
        pes = Pes()
        pes.stupen = self.content_cls.ids.stupen.text
        pes.opatreni = self.content_cls.ids.opatreni.text
        database = Database(dbtype='sqlite', dbname='koronavirus.db')
        database.create_kraj(pes)
        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()


class KrajDialog(MDDialog):
    def __init__(self, id, *args, **kwargs):
        self.label = MDTextField(pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.label2 = MDTextField(pos_hint={'center_x': 0.5, 'center_y': 0.8})
        super(KrajDialog, self).__init__(
            type="custom",
            content_cls=Content(),
            title='Nový záznam kraje',
            # text='Ahoj',
            size_hint=(0.8, 0.3),
            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )
        self.id = id

    def save_dialog(self, *args):
        krajj = {}
        krajj['zkratka_kraje'] = self.content_cls.ids.zkratka_kraje.text
        krajj['nazev_kraje'] = self.content_cls.ids.nazev_kraje.text
        if self.id:
            krajj["id"] = self.id
            app.nakazeni.update(krajj)
        else:
            kraj = Kraj()
            kraj.zkratka_kraje = self.content_cls.ids.zkratka_kraje.text
            kraj.nazev_kraje = self.content_cls.ids.nazev_kraje.text
            self.database = Database(dbtype='sqlite', dbname='koronavirus.db')
            self.database.create_kraj(kraj)
        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()


class MyItem(TwoLineAvatarIconListItem):
    def __init__(self, item, *args, **kwargs):
        super(MyItem, self).__init__()
        self.id = item['id']
        self.database = Database(dbtype='sqlite', dbname='koronavirus.db')

        self.kraj = self.database.read_kraj_by_zkratka(item['kraj_id'])
        self.pes = self.database.read_pes_by_stupen(item['pes_stupen'])
        self.text = f"{item['kraj_id']}, {self.kraj.nazev_kraje}"
        self.secondary_text = f"Nakažených: {item['pocet']}, Úmrtí: {item['umrti']}," \
                              f" Stupeň: {self.pes.stupen}, Dne: {item['datum']}"
        self.icon = IconRightWidget(icon="delete", on_release=self.on_delete)
        self.add_widget(self.icon)

    def on_press(self):
        self.dialog = NakazeniKrajDialog(id=self.id)
        self.dialog.open()

    def on_delete(self, *args):
        yes_button = MDFlatButton(text='Ano', on_release=self.yes_button_release)
        no_button = MDFlatButton(text='Ne', on_release=self.no_button_release)
        self.dialog_confirm = MDDialog(type="confirmation", title='Smazání záznamu', text="Chcete opravdu smazat tento záznam?", buttons=[yes_button, no_button])
        self.dialog_confirm.open()

    def yes_button_release(self, *args):
        self.database = Database(dbtype='sqlite', dbname='koronavirus.db')
        self.database.delete_nakazeni(self.id)
        app.nakazeni.rewrite_list()
        self.dialog_confirm.dismiss()

    def no_button_release(self, *args):
        self.dialog_confirm.dismiss()


class Nakazeni(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(Nakazeni, self).__init__(orientation="vertical")
        global app
        app = App.get_running_app()
        scrollview = ScrollView()
        self.list = MDList()
        self.database = Database(dbtype='sqlite', dbname='koronavirus.db')
        self.rewrite_list()
        scrollview.add_widget(self.list)
        self.add_widget(scrollview)
        button_box = BoxLayout(orientation='horizontal', size_hint_y=0.1)

        new_kraj_btn = MDFillRoundFlatIconButton()
        new_kraj_btn.text = "Nový kraj"
        new_kraj_btn.icon = "plus"
        new_kraj_btn.icon_color = [0.9, 0.9, 0.9, 1]
        new_kraj_btn.text_color = [0.9, 0.9, 0.9, 1]
        new_kraj_btn.md_bg_color = [69/255, 123/255, 157/255, 1]
        new_kraj_btn.font_style = "Button"
        new_kraj_btn.pos_hint = {"center_x": .5, "center_y": .8}
        new_kraj_btn.on_release = self.on_create_kraj
        button_box.add_widget(new_kraj_btn)

        new_pes_btn = MDFillRoundFlatIconButton()
        new_pes_btn.text = "Stupeň psa"
        new_pes_btn.icon = "plus"
        new_pes_btn.icon_color = [0.9, 0.9, 0.9, 1]
        new_pes_btn.text_color = [0.9, 0.9, 0.9, 1]
        new_pes_btn.md_bg_color = [69 / 255, 123 / 255, 157 / 255, 1]
        new_pes_btn.font_style = "Button"
        new_pes_btn.pos_hint = {"center_x": .6, "center_y": .8}
        new_pes_btn.on_release = self.on_create_pes
        button_box.add_widget(new_pes_btn)

        new_nakazeni_btn = MDFillRoundFlatIconButton()
        new_nakazeni_btn.text = "Nakaženi za den"
        new_nakazeni_btn.icon = "plus"
        new_nakazeni_btn.icon_color = [0.9, 0.9, 0.9, 1]
        new_nakazeni_btn.text_color = [0.9, 0.9, 0.9, 1]
        new_nakazeni_btn.md_bg_color = [69/255, 123/255, 157/255, 1]
        new_nakazeni_btn.font_style = "Button"
        new_nakazeni_btn.pos_hint = {"center_x": .6, "center_y": .8}
        new_nakazeni_btn.on_release = self.on_create_nakazeni_za_den
        button_box.add_widget(new_nakazeni_btn)
        self.add_widget(button_box)

    def rewrite_list(self):
        self.list.clear_widgets()
        nakazeni = self.database.read_nakazeni()

        for nakazen in nakazeni:
            # print(vars(nakazen))
            self.list.add_widget(MyItem(item=vars(nakazen)))

    def on_create_kraj(self, *args):
        self.dialog = KrajDialog(id=None)
        self.dialog.open()

    def on_create_pes(self, *args):
        self.dialog = PesDialog(id=None)
        self.dialog.open()

    def on_create_nakazeni_za_den(self, *args):
        self.dialog = NakazeniKrajDialog(id=None)
        self.dialog.open()

    def update(self, nakazeni):
        update_nakazeni = self.database.read_nakazeni_by_id(nakazeni['id'])
        update_nakazeni.kraj_id = nakazeni['kraj_id']
        update_nakazeni.pocet = nakazeni['pocet']
        update_nakazeni.pes_stupen = nakazeni['pes_stupen']
        update_nakazeni.umrti = nakazeni['umrti']
        update_nakazeni.datum = nakazeni['datum']
        self.database.update()
        self.rewrite_list()
