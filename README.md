# About

kronos-backend is a simple service to allow get information about locality.
Right now locality only for Russian Federation is supported.

# Parts

kronos-backend consist several tools:
* bootsrap.sh - bash script to install dependencies and necessary software
* run_mysql_in_docker.sh - bash script to run MySQL in docker if you want, script will not install docker itself
* download_fias.py - python script to download FIAS database and extract necessary files
* fias_to_sql.py - convert FIAS database format to SQL
* backend.py - Flask based simple REST API service
* kronos_db.sql.gz - MySQL dump of kronos database to prevent unnecessary parsing FIAS dbf files

# Manual installation

dependencies:
* libunrar5
* python3
* python3-pip
* mysql-server
* wget

```
sudo apt install libunrar5 python3 python3-pip wget mysql-server
```

# Automated installation

run bootstrap.sh script should all work

# How-to run backend server

* check model.py and replace MySQL connection parameters
* execute python3 ./backend.py

Flask will run web-serer on 127.0.0.1:5000.

Right now service provide only one API endpoint: /locality/<locality_name>
Example request:
```
echo -en $(curl "http://127.0.0.1:5000/locality/%D0%A1%D0%B0%D0%BC%D0%B0%D1%80%D0%B0")
```
Example response:
```
[
[
  {
    "Name": "Самара",
    "Type": "д",
    "GUID": "69e8d73c-f252-4183-b7b2-d15343973c51",
    "FedSubjCode": 69,
    "FedSubjType": "обл",
    "FedSubjName": "Тверская",
    "District": "Тверь",
    "MSK_TZ": "msk",
    "UTC_TZ": "utc+3"
  },
  {
    "Name": "Самара",
    "Type": "д",
    "GUID": "d393a779-b266-4d09-9bcd-58e1bdcabcea",
    "FedSubjCode": 62,
    "FedSubjType": "обл",
    "FedSubjName": "Рязанская",
    "District": "Михайловский",
    "MSK_TZ": "msk",
    "UTC_TZ": "utc+3"
  },
  {
    "Name": "Самара",
    "Type": "с",
    "GUID": "4fb7d783-e655-4933-9dac-1ad1af3d4f7a",
    "FedSubjCode": 79,
    "FedSubjType": "Аобл",
    "FedSubjName": "Еврейская",
    "District": "Октябрьский",
    "MSK_TZ": "msk+7",
    "UTC_TZ": "utc+10"
  },
  {
    "Name": "Самара",
    "Type": "г",
    "GUID": "bb035cc3-1dc2-4627-9d25-a1bf2d4b936b",
    "FedSubjCode": 63,
    "FedSubjType": "обл",
    "FedSubjName": "Самарская",
    "District": "Самара",
    "MSK_TZ": "msk+1",
    "UTC_TZ": "utc+4"
  },
  {
    "Name": "Самара",
    "Type": "д",
    "GUID": "553db494-e64b-4bda-b52d-f4ac0dac0462",
    "FedSubjCode": 47,
    "FedSubjType": "обл",
    "FedSubjName": "Ленинградская",
    "District": "Тихвинский",
    "MSK_TZ": "msk",
    "UTC_TZ": "utc+3"
  },
  {
    "Name": "Самара",
    "Type": "с",
    "GUID": "ba879c01-fd34-4dfe-a7a2-7326714de101",
    "FedSubjCode": 38,
    "FedSubjType": "обл",
    "FedSubjName": "Иркутская",
    "District": "Зиминский",
    "MSK_TZ": "msk+5",
    "UTC_TZ": "utc+8"
  }
]
```