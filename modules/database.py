from sqlalchemy import create_engine, Column, ForeignKey, UniqueConstraint, desc
from sqlalchemy.types import Float, String, Integer, TIMESTAMP, Enum, Text, BLOB, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Global Variables

SQLITE = 'sqlite'
MYSQL = 'mysql'

Base = declarative_base()


class Kraj(Base):
    __tablename__ = 'kraje'

    zkratka_kraje = Column(String(3), primary_key=True)
    nazev_kraje = Column(String(50), nullable=False)
    nakazeni = relationship('PocetNakazenychZaDen', backref='kraj')


class Pes(Base):
    __tablename__ = 'pes'

    stupen = Column(Integer, primary_key=True)
    opatreni = Column(Text)
    pes_v_kraji = relationship('PocetNakazenychZaDen', backref='pes')


class PocetNakazenychZaDen(Base):
    __tablename__ = 'pocet_nakazenych_za_den'

    id = Column(Integer, primary_key=True)
    kraj_id = Column(String(3), ForeignKey('kraje.zkratka_kraje'))
    pes_stupen = Column(Integer, ForeignKey('pes.stupen'))
    pocet = Column(Integer, nullable=False)
    umrti = Column(Integer)
    datum = Column(Date)


class Database:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
        MYSQL: 'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@localhost/{DB}'
    }

    def __init__(self, dbtype='sqlite', username='', password='', dbname='../koronavirus.db'):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname, USERNAME=username, PASSWORD=password)
            self.engine = create_engine(engine_url, echo=False)
        else:
            print('DBType is not found in DB_ENGINE')

        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_kraj(self, kraj):
        try:
            self.session.add(kraj)
            self.session.commit()
            return True
        except:
            return False

    def create_pes(self, pes):
        try:
            self.session.add(pes)
            self.session.commit()
            return True
        except:
            return False

    def create_nakazeni(self, nakazeni):
        try:
            self.session.add(nakazeni)
            self.session.commit()
            return True
        except:
            return False

    def read_all(self, order=Kraj.zkratka_kraje):
        try:
            result = self.session.query(Kraj).order_by(order).all()
            return result
        except:
            return False

    def read_kraj(self, order=Kraj.zkratka_kraje):
        try:
            result = self.session.query(Kraj).order_by(order).all()
            return result
        except:
            return False

    def read_kraj_by_zkratka(self, zkratka_kraje):
        try:
            result = self.session.query(Kraj).get(zkratka_kraje)
            return result
        except:
            return False

    def read_pes(self, order=Pes.stupen):
        try:
            result = self.session.query(Pes).order_by(order).all()
            return result
        except:
            return False

    def read_pes_by_stupen(self, stupen):
        try:
            result = self.session.query(Pes).get(stupen)
            return result
        except:
            return False

    def read_nakazeni(self, order=PocetNakazenychZaDen.id):
        try:
            result = self.session.query(PocetNakazenychZaDen).order_by(order).all()
            return result
        except:
            return False

    def read_nakazeni_by_id(self, id):
        try:
            result = self.session.query(PocetNakazenychZaDen).get(id)
            return result
        except:
            return False

    def delete_kraj(self, zkratka_kraje):
        try:
            kraj = self.read_kraj_by_zkratka(zkratka_kraje)
            self.session.delete(kraj)
            self.session.commit()
            return True
        except:
            return False

    def delete_pes(self, stupen_psa):
        try:
            stupen = self.read_pes_by_stupen(stupen_psa)
            self.session.delete(stupen)
            self.session.commit()
            return True
        except:
            return False

    def delete_nakazeni(self, id):
        try:
            nakazeni = self.read_nakazeni_by_id(id)
            self.session.delete(nakazeni)
            self.session.commit()
            return True
        except:
            return False

    def update(self):
        try:
            self.session.commit()
            return True
        except:
            return False
