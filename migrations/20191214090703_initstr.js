
exports.up = function(knex) {
    return knex.schema
    .createTable('tz', function (table) {
       table.increments('id');
       table.integer('time_offset').notNullable();
       table.string('offset_type', 255).notNullable();
    })
    .createTable('locality_type', function (table) {
       table.increments('id');
       table.string('name', 120).notNullable();
    })
    .createTable('locality', function (table) {
       table.increments('id');
       table.string('guid');
       table.string('name', 255).notNullable();
       table.integer('type');
       table.integer('fedsubj');
       table.integer('tz');    
    })
    .createTable('fedsubj', function (table) {
        table.increments('id');
        table.string('guid');
        table.integer('code').notNullable();
        table.string('name', 255);
        table.integer('type');
    })
    .createTable('fedsubj_type', function (table) {
        table.increments('id');
        table.string('type', 255).notNullable();
    })
    .alterTable('fedsubj_type', function(table) {
        table.unique('type')
    })
    .alterTable('fedsubj', function(table) {
        table.unique('name')
    })
    ;
};

exports.down = function(knex) {
  
};
