import os
import sys
import logging
import argparse
from peewee import *
from dbfread import DBF
from model import *
from ru_tz import *

#путь к файлам базы fias dbf, нужны ADDROBJ
fias_dir = './fias_dbf'

def usage():
    print("usage:", os.path.basename(__file__), " -d -c -e")
    print("  -c      client name or adm or pwd or all, default value is all")
    print("  -t      date for which check the backup, default - yesterday")
    print("Example: check_db_backups.py -d njc -c cbsi")
    sys.exit()

def create_args_parser():
#    arg_parser = argparse.ArgumentParser()
#    arg_parser.add_argument('-c', action='store', help='client name to test database for, \
#        also pwd or adm values are available', required=True)
#    arg_parser.add_argument('-t', action='store', help='date',
#        default=(date.today() - timedelta(days=1)).strftime('%Y-%m-%d'))
#    arg_parser.add_argument('-e', action='append', help='exclude db from checking')
#
#    return arg_parser
    pass

# преобразует массив кортежей в словарь
# т.к. DBF по умолчанию выдает записи как массив кортежей
def dbf_record_to_dict(items):
    rec = dict()
    for (name, value) in items:
            rec[name] = value
    return rec

def check_if_obj_present(arr_of_obj, obj):
    for o in arr_of_obj:
        if o == obj:
            return True
    return False

def find_district_for_locality(areacode, districts):
    for d in districts:
        if d['areacode'] == areacode:
            return d
    return None 

def process_dbf_in_mem(dbf_file_path):
    table = DBF(dbf_file_path, load=True)
    fst = {}
    fed_s = {}
    fs_districts = []
    lt = []
    locality = []

    for record in table:
        # субъект федерации
        if (
            (record['AOLEVEL'] == 1) and (record['LIVESTATUS'] == 1) and 
            ((record['CURRSTATUS'] == 1) or (record['CURRSTATUS'] == 0))
        ):
            fst['type'] = record['SHORTNAME']
            fed_s = {
                'guid':record['AOGUID'],
                'code':record['REGIONCODE'],
                'name':record['OFFNAME'],
                'type':record['SHORTNAME']
            }

        # район
        if (
            # город является центром райнона
            ((record['AOLEVEL'] == 4) and 
            ((record['CENTSTATUS'] == 2) or (record['CENTSTATUS'] == 3)) and
            (record['LIVESTATUS'] == 1)) or
            #район
            ((record['AOLEVEL'] == 3) and (record['LIVESTATUS'] == 1))
        ):
            fs_districts.append(
                {
                    'guid':record['AOGUID'],
                    'name':record['OFFNAME'],
                    'fedsubj_code':record['REGIONCODE'],
                    'tz':'',
                    'areacode':record['AREACODE']
                }
            )

        #город или населенный пункт
        # костыль для Москвы
        if (
            (int(record['REGIONCODE']) == 77) and (record['OFFNAME'] == 'Москва') and 
            (record['LIVESTATUS'] == 1)
        ):
            fs_districts.append(
                {
                    'guid':fed_s['guid'],
                    'name':fed_s['name'],
                    'fedsubj_code':record['REGIONCODE'],
                    'tz':'',
                    'areacode':'000'
                }
            )
            locality.append(
                {
                    'guid':record['AOGUID'],
                    'type':record['SHORTNAME'],
                    'name':record['OFFNAME'],
                    'fedsubj_code':record['REGIONCODE'],
                    'district':record['AREACODE']
                }
            )

        # костыль для Пензы
        if (
            (int(record['REGIONCODE']) == 58) and (record['OFFNAME'] == 'Пенза') and 
            (record['LIVESTATUS'] == 1)
        ):
            fs_districts.append(
                {
                    'guid':fed_s['guid'],
                    'name':fed_s['name'],
                    'fedsubj_code':record['REGIONCODE'],
                    'tz':'',
                    'areacode':'000'
                }
            )
            locality.append(
                {
                    'guid':record['AOGUID'],
                    'type':record['SHORTNAME'],
                    'name':record['OFFNAME'],
                    'fedsubj_code':record['REGIONCODE'],
                    'district':record['AREACODE']
                }
            )

        # костыль для Крыма
        if (
            (int(record['REGIONCODE']) == 91) and (record['OFFNAME'] == 'Крым') and 
            (record['LIVESTATUS'] == 1)
        ):
            fs_districts.append(
                {
                    'guid':fed_s['guid'],
                    'name':fed_s['name'],
                    'fedsubj_code':record['REGIONCODE'],
                    'tz':'',
                    'areacode':'000'
                }
            )
            locality.append(
                {
                    'guid':record['AOGUID'],
                    'type':'г',
                    'name':record['OFFNAME'],
                    'fedsubj_code':record['REGIONCODE'],
                    'district':record['AREACODE']
                }
            )

        # костыль для Байконура
        if (
            (int(record['REGIONCODE']) == 99) and (record['OFFNAME'] == 'Байконур') and 
            (record['LIVESTATUS'] == 1)
        ):
            fs_districts.append(
                {
                    'guid':fed_s['guid'],
                    'name':fed_s['name'],
                    'fedsubj_code':record['REGIONCODE'],
                    'tz':'',
                    'areacode':'000'
                }
            )
            locality.append(
                {
                    'guid':record['AOGUID'],
                    'type':record['SHORTNAME'],
                    'name':record['OFFNAME'],
                    'fedsubj_code':record['REGIONCODE'],
                    'district':record['AREACODE']
                }
            )

        # костыль для Санк-Петербурга
        if (
            (int(record['REGIONCODE']) == 78) and (record['OFFNAME'] == 'Санкт-Петербург') and
            (record['LIVESTATUS'] == 1)
        ):  
            fs_districts.append(
                {
                    'guid':fed_s['guid'],
                    'name':fed_s['name'],
                    'fedsubj_code':record['REGIONCODE'],
                    'tz':'',
                    'areacode':'000'
                }
            )
            locality.append(
                {
                    'guid':record['AOGUID'],
                    'type':record['SHORTNAME'],
                    'name':record['OFFNAME'],
                    'fedsubj_code':record['REGIONCODE'],
                    'district':record['AREACODE']
                }
            )
        # костыль для Севастополя
        if (
            (int(record['REGIONCODE']) == 92) and (record['OFFNAME'] == 'Севастополь') and
            (record['LIVESTATUS'] == 1)
        ):  
            fs_districts.append(
                {
                    'guid':fed_s['guid'],
                    'name':fed_s['name'],
                    'fedsubj_code':record['REGIONCODE'],
                    'tz':'',
                    'areacode':'000'
                }
            )
            locality.append(
                {
                    'guid':record['AOGUID'],
                    'type':record['SHORTNAME'],
                    'name':record['OFFNAME'],
                    'fedsubj_code':record['REGIONCODE'],
                    'district':record['AREACODE']
                }
            )

        #город или населенный пункт
        if (
            ((record['AOLEVEL'] == 4) or (record['AOLEVEL'] == 6)) and
            (record['LIVESTATUS'] == 1)
        ):
            list(filter(lambda t: t['type'] != record['SHORTNAME'], lt))
            if not check_if_obj_present(lt, {'type':record['SHORTNAME']}):
                lt.append({'type':record['SHORTNAME']})
            locality.append(
                {
                    'guid':record['AOGUID'],
                    'type':record['SHORTNAME'],
                    'name':record['OFFNAME'],
                    'fedsubj_code':record['REGIONCODE'],
                    'district':record['AREACODE']
                }
            )

            # костыль для Тюмени
            if ((int(record['REGIONCODE'])) == 72 and (record['OFFNAME'] == 'Тюмень')):
                fs_districts.append(
                    {
                        'guid':record['AOGUID'],
                        'name':record['OFFNAME'],
                        'fedsubj_code':record['REGIONCODE'],
                        'tz':'',
                        'areacode':record['AREACODE']
                    }
                )

            # костыль для Тюмени
            if ((int(record['REGIONCODE'])) == 99 and (record['OFFNAME'] == 'Тюмень')):
                fs_districts.append(
                    {
                        'guid':record['AOGUID'],
                        'name':record['OFFNAME'],
                        'fedsubj_code':record['REGIONCODE'],
                        'tz':'',
                        'areacode':record['AREACODE']
                    }
                )

    #а теперь записываем в базу
    # тип субъекта и субъект федерации
    try:
        fed_subj_type = FedSubjType.get(FedSubjType.type == fst['type'])
    except FedSubjType.DoesNotExist:
        fed_subj_type = FedSubjType.create(type=fst['type'])

    try:
        fed_subj = FedSubj.get(FedSubj.guid == fed_s['guid'])
    except: 
        fed_subj = FedSubj.create(type=fed_subj_type, guid=fed_s['guid'], 
        code=fed_s['code'], name=fed_s['name'])

    #районы
    d_guids = []
    # костыль для Московской области
    if (int(record['REGIONCODE']) == 50):  
        fs_districts.append(
            {
                'guid':fed_s['guid'],
                'name':fed_s['name'],
                'fedsubj_code':record['REGIONCODE'],
                'tz':'',
                'areacode':'000'
            }
        )
    # костыль для Ленинградской области
    if (int(record['REGIONCODE']) == 47):  
        fs_districts.append(
            {
                'guid':fed_s['guid'],
                'name':fed_s['name'],
                'fedsubj_code':record['REGIONCODE'],
                'tz':'',
                'areacode':'000'
            }
        )
    for d in fs_districts:
        d_guids.append(d['guid'])
    d_guids_from_base = list(District.select(District.guid).where(District.guid << d_guids))
    # для вставки в базу оставляем только те районы которых в базе еще нет
    d_guids_to_insert = list(set(d_guids) - set(d_guids_from_base))
    fs_districts_to_insert = filter(lambda e: e['guid'] in d_guids_to_insert, fs_districts)
    for district in fs_districts_to_insert:
        try:
            District.get(District.guid == district['guid'])
        except:
            District.create(guid=district['guid'], name=district['name'],
            fedsubj_code=fed_subj, tz='')

    #типы нас. пункты
    for t in lt:
        try:
            LocalityType.get(LocalityType.type == t['type'])
        except:
            LocalityType.create(type=t['type'])

    #нас. пункты
    #сие есть говнокод ибо надо сделать bulk insert только того чего нет
    #в базе
    for l in locality:
        try:
            Locality.get(Locality.guid == l['guid'])
        except:
            district = find_district_for_locality(l['district'], fs_districts)
            if district is not None:
                l_district = District.get(District.guid == district['guid'])
                l_type = LocalityType.get(LocalityType.type == l['type'])
                Locality.create(type=l_type, district=l_district, guid=l['guid'], 
                    name=l['name'], fedsubj_code=fed_subj)
            else:
                print('Something goes wrong!')
                print('Cant find district For locality:', l)
                sys.exit(1)


def add_tz(tz_map, msk_tz_map):
    for k in tz_map.keys():
        for fsubj in tz_map[k]:
            try:
                fs = FedSubj.get(FedSubj.code == fsubj['code'])
            except:
                print('Cant fill tz info for FedSubj with region code: ' + str(fsubj['code']) 
                    + '. FedSubj does not exists!')
                continue
            if len(fsubj['districts']) > 0:
                continue
            else:
                query = District.update(msk_tz = k, utc_tz = msk_tz_map[k]).where(
                    District.fedsubj_code == fsubj['code'])
                query.execute()

create_tables(db)

#with os.scandir(fias_dir) as entries:
#    for entry in entries:
#        if entry.name.startswith('ADDROB'):
#            print('Process file: ' + fias_dir + '/' + entry.name)
            #process_dbf(fias_dir + '/' + entry.name)
#            process_dbf_in_mem(fias_dir + '/' + entry.name)

add_tz(fedsubj_tz_map, msk_to_utc_tz_map)

