-- Crear base de datos (si aún no existe)
CREATE DATABASE IF NOT EXISTS `videos_db`;
USE `videos_db`;

DROP TABLE IF EXISTS `videos`;
DROP TABLE IF EXISTS `timeslots`;
DROP TABLE IF EXISTS `alerts`;
DROP TABLE IF EXISTS `object_counts`;

-- Crear tabla para Video.csv
CREATE EXTERNAL TABLE IF NOT EXISTS `videos` (
    `video_id` STRING,
    `camera_id` STRING,
    `location` STRING,
    `priority` STRING,
    `video_file` STRING,
    `date` DATE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
TBLPROPERTIES ("skip.header.line.count"="1");
LOAD DATA INPATH '/user/hadoop/HIVE/Videos_csv/Video.csv' INTO TABLE `videos`;

-- Crear tabla para Timeslot.csv
CREATE EXTERNAL TABLE IF NOT EXISTS `timeslots` (
    `hour` TIMESTAMP,
    `video_minute` STRING,
    `object_count` INT,
    `video_id` STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
TBLPROPERTIES ("skip.header.line.count"="1");
LOAD DATA INPATH '/user/hadoop/HIVE/Videos_csv/Timeslot.csv' INTO TABLE `timeslots`;

-- Crear tabla para Alert.csv
CREATE EXTERNAL TABLE IF NOT EXISTS `alerts` (
    `type` STRING,
    `timestamp` TIMESTAMP,
    `video_id` STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
TBLPROPERTIES ("skip.header.line.count"="1");
LOAD DATA INPATH '/user/hadoop/HIVE/Videos_csv/Alert.csv' INTO TABLE `alerts`;

-- Crear tabla para ObjectCount.csv
CREATE EXTERNAL TABLE IF NOT EXISTS `object_counts` (
    `hour` TIMESTAMP,
    `video_minute` STRING,
    `object_type` STRING,
    `object_count` INT,
    `video_id` STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
TBLPROPERTIES ("skip.header.line.count"="1");
LOAD DATA INPATH '/user/hadoop/HIVE/Videos_csv/ObjectCount.csv' INTO TABLE `object_counts`;