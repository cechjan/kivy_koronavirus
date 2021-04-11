from modules.database import *
import datetime

db = Database(dbtype='sqlite')

kraj = Kraj()
kraj.zkratka_kraje = 'MSK'
kraj.nazev_kraje = 'Moravskoslezský kraj'
db.create_kraj(kraj)

pes = Pes()
pes.stupen = 1
pes.opatreni = '500 osob venku, 100 osob uvnitř'
db.create_pes(pes)

nakazeni = PocetNakazenychZaDen()
nakazeni.pocet = 2198
nakazeni.umrti = 74
nakazeni.datum = datetime.date(2021, 11, 3)
db.create_nakazeni(nakazeni)
