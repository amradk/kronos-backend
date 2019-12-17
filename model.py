from peewee import *

#sqlite_db = SqliteDatabase('./kronos.db', pragmas={'journal_mode': 'wal'})
db = MySQLDatabase('kronos_db', user='kronos', password='Kr0nos@Time',
                         host='127.0.0.1', port=3306)

class BaseModel(Model):
    class Meta:
        database = db

class FedSubjType(BaseModel):
    type = CharField(max_length=30,unique=True)

class FedSubj(BaseModel):
    guid = CharField(max_length=60,unique=True)
    code = IntegerField(index=True)
    name = CharField(max_length=255,unique=True)
    type = ForeignKeyField(FedSubjType, field='id', backref='fedsubj_type')

class LocalityType(BaseModel):
    type = CharField(max_length=255, unique=True)
    fullname = CharField(max_length=255, unique=True)

class TimeZone(BaseModel):
    utc_tz = CharField(max_length=20)
    msk_tz = CharField(max_length=20)

class District(BaseModel):
    name = CharField(max_length=255)
    guid = CharField(max_length=60,unique=True)
    fedsubj_code = ForeignKeyField(FedSubj, field='code', backref='fedsubj_code_d')
    utc_tz = CharField(max_length=60)
    msk_tz = CharField(max_length=60)

class Locality(BaseModel):
    name = CharField(max_length=255)
    guid = CharField(max_length=60,unique=True)
    type = ForeignKeyField(LocalityType, field='id', backref='locality_type')
    fedsubj_code = ForeignKeyField(FedSubj, field='code', backref='fedsubj_code')
    district = ForeignKeyField(District, backref='district_id')

def create_tables(db):
    with db:
        db.create_tables([FedSubjType, FedSubj, LocalityType, Locality, District])
