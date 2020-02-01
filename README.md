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
Example response:
```
[
    {
        "Name": "\u0421\u0430\u043c\u0430\u0440\u0430",
        "Type": "\u0434",
        "GUID": "69e8d73c-f252-4183-b7b2-d15343973c51",
        "FedSubjCode": 69,
        "FedSubjType": "\u043e\u0431\u043b",
        "FedSubjName": "\u0422\u0432\u0435\u0440\u0441\u043a\u0430\u044f",
        "District": "\u0422\u0432\u0435\u0440\u044c",
        "MSK_TZ": "msk",
        "UTC_TZ": "utc+3"
    },
    {
        "Name": "\u0421\u0430\u043c\u0430\u0440\u0430",
        "Type": "\u0434",
        "GUID": "d393a779-b266-4d09-9bcd-58e1bdcabcea",
        "FedSubjCode": 62,
        "FedSubjType": "\u043e\u0431\u043b",
        "FedSubjName": "\u0420\u044f\u0437\u0430\u043d\u0441\u043a\u0430\u044f",
        "District": "\u041c\u0438\u0445\u0430\u0439\u043b\u043e\u0432\u0441\u043a\u0438\u0439",
        "MSK_TZ": "msk",
        "UTC_TZ": "utc+3"
    },
    {
        "Name": "\u0421\u0430\u043c\u0430\u0440\u0430",
        "Type": "\u0441",
        "GUID": "4fb7d783-e655-4933-9dac-1ad1af3d4f7a",
        "FedSubjCode": 79,
        "FedSubjType": "\u0410\u043e\u0431\u043b",
        "FedSubjName": "\u0415\u0432\u0440\u0435\u0439\u0441\u043a\u0430\u044f",
        "District": "\u041e\u043a\u0442\u044f\u0431\u0440\u044c\u0441\u043a\u0438\u0439",
        "MSK_TZ": "msk+7",
        "UTC_TZ": "utc+10"
    },
    {
        "Name": "\u0421\u0430\u043c\u0430\u0440\u0430",
        "Type": "\u0433",
        "GUID": "bb035cc3-1dc2-4627-9d25-a1bf2d4b936b",
        "FedSubjCode": 63,
        "FedSubjType": "\u043e\u0431\u043b",
        "FedSubjName": "\u0421\u0430\u043c\u0430\u0440\u0441\u043a\u0430\u044f",
        "District": "\u0421\u0430\u043c\u0430\u0440\u0430",
        "MSK_TZ": "msk+1",
        "UTC_TZ": "utc+4"
    },
    {
        "Name": "\u0421\u0430\u043c\u0430\u0440\u0430",
        "Type": "\u0434",
        "GUID": "553db494-e64b-4bda-b52d-f4ac0dac0462",
        "FedSubjCode": 47,
        "FedSubjType": "\u043e\u0431\u043b",
        "FedSubjName": "\u041b\u0435\u043d\u0438\u043d\u0433\u0440\u0430\u0434\u0441\u043a\u0430\u044f",
        "District": "\u0422\u0438\u0445\u0432\u0438\u043d\u0441\u043a\u0438\u0439",
        "MSK_TZ": "msk",
        "UTC_TZ": "utc+3"
    },
    {
        "Name": "\u0421\u0430\u043c\u0430\u0440\u0430",
        "Type": "\u0441",
        "GUID": "ba879c01-fd34-4dfe-a7a2-7326714de101",
        "FedSubjCode": 38,
        "FedSubjType": "\u043e\u0431\u043b",
        "FedSubjName": "\u0418\u0440\u043a\u0443\u0442\u0441\u043a\u0430\u044f",
        "District": "\u0417\u0438\u043c\u0438\u043d\u0441\u043a\u0438\u0439",
        "MSK_TZ": "msk+5",
        "UTC_TZ": "utc+8"
    }
]
```