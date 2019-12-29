//'use strict';
const path = require('path');
const fs = require('fs');
const YADBF = require('yadbf');

const directoryPath = '/home/manul/Загрузки/fias_dbf';
const sqlite3_db = '/home/manul/Workspace/my/kronos/kronos'
//connect to sqlite3 database
var knex = require('knex')({
    client: 'sqlite3',
    connection: {
      filename: sqlite3_db
    },
    useNullAsDefault: true,
    pool: {
        min: 1,
        max: 1,
        createTimeoutMillis: 30000,
        acquireTimeoutMillis: 300000,
        idleTimeoutMillis: 3000,
        destroyTimeoutMillis: 5000,
        reapIntervalMillis: 1000,
        createRetryIntervalMillis: 50000,
        propagateCreateError: false
    },
  });

let dbf_files = [];


dbf_files = fs.readdirSync(directoryPath);
dbf_files = dbf_files.sort();
dbf_files.forEach(function (file) {
    if (file.search('ADDROB') === 0) {
        //нет данных о субъектк федерации, надо прочитать файл и добавить
        fillDataForFedSubj(directoryPath + '/' + file, knex);
    };
});

function onlyUnique(value, index, self) { 
    return self.indexOf(value) === index;
}

//сравнение "плоских" объектов
function flatObjectsIsEqual(obj1, obj2) {
    let obj1_props = Object.getOwnPropertyNames(obj1);
    let obj2_props = Object.getOwnPropertyNames(obj2);

    //сравниваем кол-во элементов
    if (obj1_props.length != obj2_props.length) {
        return false;
    }

    //сравниваем значения одинаковых элементов
    for (let i = 0; i < obj1_props.length; i++) {
        let propName = obj1_props[i];

        if (obj1[propName] != obj2[propName]) {
            console.log(`OBJ1_Prop: ${obj1[propName]}`);
            console.log(`OBJ2_Prop: ${obj2[propName]}`);
            console.log(`OBJ1_Prop_type: ${typeof(obj1[propName])}`);
            console.log(`OBJ2_Prop_type: ${typeof(obj2[propName])}`);
            return false;
        }
    }

    return true;
}

//функция сравнивает два массива объектов: 
//1 - считан из dbf, 2 - получен запросом из базы
//результат - новый массив объектов (1-2) т.е. 
//остаются те элементы массива1 которые не присутствуют в массиве2 
function filterObjects(aob1, aob2) {
    let diff = [];
    let isPresent = false;
    for (let i = 0; i<aob1.length; i++) {
        for (let j = 0; j<aob2.length; j++) {
            isPresent = flatObjectsIsEqual(aob1[i], aob2[j]);
            if (isPresent == true) break;
        };
        if (isPresent == false) diff.push(aob1[i]);
    };

    console.log(`Diff: ${JSON.stringify(diff)}`);

    return diff;
}

//ищет типы субъектов федерации и вставляет в базу
function insertFedSubjType(fst, db_iface) {
    //надо возвращать promise
    let fst_arr = [];
    let diff = [];
    //трансформируем массив объектов в просто массив
    fst.forEach(function(item, index, array) {
        fst_arr.push(fst[index]['type']);
    });
    //типы субъектов федерации
    if (fst.length > 0) {
        //запрашиваем из базы, которые попадают в
        //массив считанных их базы 
        return db_iface('fedsubj_type').whereIn(
            'type', fst_arr,
        ).select('type')
        .then(function(rows){
            if (rows.length > 0) {
                //собираем типы субъектов федерации
                //нужно отфильтровать значения которые уже присутствуют в базе
                //получаем различие между тем что считати из dbf и тем
                //что уже есть в базе
                diff = filterObjects(fst, rows);
                fst = diff;
            }
        }).then(() => {
            if (fst.length >0 )
                knex.insert(fst).into('fedsubj_type').then(()=>{});
        });
    }
}

function insertFedSubj(fsn, db_iface) {
    //{guid: fed_subj_guid, name: fed_subj_name, code: fed_subj_code, type: fed_subj_type}

    //типы субъектов федерации
    if (fsn.length > 0) {
        let fed_subj_types = {};
        let guids = [];
        let diff = [];
        return db_iface('fedsubj_type')
        .select('id','type')
        .then(function(rows){
            //трансформируем массив объектов в большой объект (hash)
            //вида FedSubjType : ID 
            rows.forEach(function(item, index, array) {
                fed_subj_types[rows[index]['type']] = rows[index]['id'];
            });
            fsn.forEach(function(item, index, array) {
                fsn[index]['type'] = fed_subj_types[fsn[index]['type']];
                guids.push(fsn[index]['guid']);
            });
        }).then(() => {
            //анонимная функция возвращает promise
            db_iface('fedsubj').whereIn(
                'guid', guids,
            ).select('guid','name', 'code', 'type')
            .then(function(rows) {
                if (rows.length > 0) {
                    //собираем типы субъектов федерации
                    //нужно отфильтровать значения которые уже присутствуют в базе
                    diff = filterObjects(fsn, rows);
                    fsn = diff;
                    console.log(`FsnCleared: ${JSON.stringify(fsn)}`);
                }
            })
            .then(() => {
                if ( fsn.length > 0 )
                    return knex.insert(fsn).into('fedsubj').then(()=>{});
            });
        });
    }
}

function insertDataForLocalityType(lt, db_iface) {
    let lt_arr = [];
    let diff = [];
    //трансформируем массив объектов в просто массив
    lt.forEach(function(item, index, array) {
        lt_arr.push(lt[index]['name']);
    });
    //избавляемся от дублей в массиве
    let lt_unique = lt_arr.filter(onlyUnique);
    lt = [];
    lt_unique.forEach(function(item, index, array) {
        lt.push({name: lt_unique[index]});
    });

    console.log(`ULT: ${JSON.stringify(lt)}`);
    //типы населенных пунктов
    if (lt.length > 0) {
        //запрашиваем из базы, которые попадают в
        //массив считанных их базы 
        return db_iface('locality_type').whereIn(
            'name', lt_unique,
        ).select('name')
        .then(function(rows){
            if (rows.length > 0) {
                //получаем различие между тем что считати из dbf и тем
                //что уже есть в базе
                diff = filterObjects(lt, rows);
                lt = diff;
                console.log(`Lt to insert 1: ${JSON.stringify(lt)}`);
                console.log(`Rows: ${JSON.stringify(rows)}`)
                //console.log(`LtCleared: ${JSON.stringify(lt)}`);
            };
        })
        .then(()=>{
            if ( lt.length > 0 ) {
                console.log(`Lt to insert 2: ${JSON.stringify(lt)}`);
                return knex.insert(lt).into('locality_type').then(()=>{});
            };
        });
    }
}

function insertDataChunkForLocalityName(chunk, db_iface) {
    //{guid: aoguid, name: lacality-name, type: locality-type, code: fed_subj_code}
    let locality_types = {};
    db_iface('locality_type')
    .select('id','name')
    .then(function(rows) {
        //трансформируем массив объектов в большой объект (hash)
        //вида LocalityType : ID 
        rows.forEach(function(item, index, array) {
            locality_types[rows[index]['name']] = rows[index]['id'];
        });
        let guids = [];
        chunk.forEach(function(item, index, array) {
            chunk[index]['type'] = locality_types[chunk[index]['type']];
            guids.push(chunk[index]['guid']);
        });
        console.log(`Chunk size: ${chunk.length}`);
        //проверяем есть ли считанные элементы в нашей базе
        db_iface('locality').whereIn(
            'guid', guids,
        ).select('guid', 'name', 'fedsubj', 'type', 'tz')
        .then(function(rows) {
            if (rows.length > 0) {
                console.log(`Rows size: ${rows.length}`);
                //собираем типы субъектов федерации
                //нужно отфильтровать значения которые уже присутствуют в базе
                let diff = filterObjects(chunk, rows);
                chunk = diff;
                console.log(`Diff size: ${diff.length}`);
            }
        });

        //данные подготовлены можно записывать в БД
        knex.transaction(function(trx) {
            knex.insert(chunk).into('locality').then(trx.commit).catch(function(err) {
                console.log(err.stack);
                console.log(`FsnInsrtErr1: ${JSON.stringify(chunk)}`);
                //trx.rollback();
            });
        });
    });
}

function insertDataForLocalityName(ln, db_iface) {
    //{name: lacality-name, type: locality-type, code: fed_subj_code}
    //console.log(`FlnRead: ${ln_arr}`);
    //типы субъектов федерации
    if (ln.length > 0) {
        if ( ln.length > 100) {
            let step = 20;
            let tmp = [];
            for (let i = 0; i < ln.length; i+=step) { 
                tmp = ln.slice(i, i+step);
                insertDataChunkForLocalityName(tmp, db_iface);
            }
        } else {
            insertDataChunkForLocalityName(ln, db_iface);
        }
    }
}

function fillDataForFedSubj(path, db_iface) {
    let fst = [];
    let fsn = [];
    let lt = [];
    let ln = [];
    fs.createReadStream(path)
    .pipe(new YADBF(options = {encoding: 'cp866'}))
    .on('data', record => {
    //99-ый регион это особый случай
        if ( parseInt(record['AOLEVEL'],10) == 1 && parseInt(record['LIVESTATUS'],10) == 1 &&
     (parseInt(record['CURRSTATUS'],10) == 1 || parseInt(record['CURRSTATUS'],10) == 0)) {
            let fed_subj_name = record['OFFNAME'];
            let fed_subj_type = record['SHORTNAME'];
            let fed_subj_code = parseInt(record['REGIONCODE']);
            let fed_subj_guid = record['AOGUID'];
            //собираем типы субъектов федерации
            fst.push({type: fed_subj_type});
            //собираем субъекты федерации
            fsn.push({guid: fed_subj_guid, name: fed_subj_name, code: fed_subj_code, type: fed_subj_type});
        };
        if ( (parseInt(record['AOLEVEL']) == 4 || parseInt(record['AOLEVEL']) == 6) && parseInt(record['LIVESTATUS']) == 1 ) {
            lt.push({name: record['SHORTNAME']});
            ln.push({guid: record['AOGUID'], name: record['OFFNAME'], fedsubj: parseInt(record['REGIONCODE']), type: record['SHORTNAME'], tz: 0});
        }
    })
    //dbf файл обработан, вносим зменения в БД
    .on('end', insert => {
        /*insertFedSubjType(fst, db_iface)
        .then(() => {
            insertFedSubj(fsn, db_iface)
            .then(()=>{
                insertDataForLocalityType(lt, db_iface)
                .then(()=>{
                    insertDataForLocalityName(ln,db_iface);
                });
            });
        });*/
        insertFedSubjType(fst, db_iface)
        .then(() => {
            return insertFedSubj(fsn, db_iface);
        })
        .then(() => {
            return insertDataForLocalityType(lt, db_iface)
        })
        .then(()=>{});
        //insertFedSubj(fsn, db_iface);

        //insertFedSubj(fsn, db_iface);
        //insertDataForLocalityType(lt, db_iface);
        //insertDataForLocalityName(ln,db_iface);
        console.log(`Finish processing DBF: ${path}`);
        }
    )
    .on('error', err => {
      console.error(`an error was thrown: ${err}`);
    });
};

console.log('Finish DBF processing!');
//process.exit(0);