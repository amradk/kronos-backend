BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `tz` (
	`id`	INTEGER,
	`time_offset`	INTEGER,
	`offset_type`	TEXT
);
CREATE TABLE IF NOT EXISTS `locality_type` (
	`id`	INTEGER,
	`name`	TEXT
);
CREATE TABLE IF NOT EXISTS `locality` (
	`id`	INTEGER NOT NULL,
	`name`	TEXT NOT NULL,
	`type`	INTEGER,
	`fedobj`	INTEGER,
	`tz`	INTEGER,
	PRIMARY KEY(`name`)
);
CREATE TABLE IF NOT EXISTS `fedobj` (
	`id`	INTEGER NOT NULL,
	`code`	INTEGER NOT NULL,
	`name`	TEXT,
	PRIMARY KEY(`id`,`name`)
);
CREATE TABLE IF NOT EXISTS `fed_obj_type` (
	`id`	INTEGER NOT NULL,
	`type`	INTEGER
);
COMMIT;
