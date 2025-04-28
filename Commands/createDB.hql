-- Crear base de datos (si aún no existe)
CREATE DATABASE IF NOT EXISTS `videos_db`;
USE `videos_db`;

-- Eliminar tablas si existen
DROP TABLE IF EXISTS `videos`;
DROP TABLE IF EXISTS `timeslots`;
DROP TABLE IF EXISTS `alerts`;
DROP TABLE IF EXISTS `object_counts`;
DROP TABLE IF EXISTS `alert_types`;
DROP TABLE IF EXISTS `locations`;
DROP TABLE IF EXISTS `priorities`;

-- Crear tabla alert_types como tabla interna
CREATE TABLE IF NOT EXISTS `alert_types` (
    `alert_type` STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',';

-- Crear tabla locations como tabla interna
CREATE TABLE IF NOT EXISTS `locations` (
    `location` STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',';

-- Crear tabla priorities como tabla interna
CREATE TABLE IF NOT EXISTS `priorities` (
    `priority` STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',';

-- Insertar datos en alert_types
INSERT INTO TABLE alert_types VALUES
  ('presence_out_of_hours'),
  ('suspicious_movement'),
  ('abandoned_object'),
  ('intrusion'),
  ('camera_failure'),
  ('unrecognized_vehicle'),
  ('high_traffic_volume'),
  ('unauthorized_access'),
  ('not_found_alert');

-- Insertar datos en locations
INSERT INTO TABLE locations VALUES
  ('Entrada_A'),
  ('Entrada_B'),
  ('Entrada_C'),
  ('Estacionamiento_A'),
  ('Estacionamiento_B'),
  ('Estacionamiento_C'),
  ('Estacionamiento_D'),
  ('Estacionamiento_E'),
  ('Pasaje_A'),
  ('Pasaje_B'),
  ('Pasaje_C'),
  ('Patio'),
  ('Patio_de_comidas_A'),
  ('Patio_de_comidas_B');

-- Insertar datos en priorities
INSERT INTO TABLE priorities VALUES
  ('very_low'),
  ('low'),
  ('medium'),
  ('high'),
  ('very_high');

-- Crear tabla videos
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

-- Eliminar datos previos y cargar nuevos datos en la tabla videos
LOAD DATA INPATH '/user/hadoop/Videos_csv/Video.csv' INTO TABLE `videos`;

-- Crear tabla timeslots
CREATE EXTERNAL TABLE IF NOT EXISTS `timeslots` (
    `hour` TIMESTAMP,
    `video_minute` STRING,
    `object_count` INT,
    `video_id` STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
TBLPROPERTIES ("skip.header.line.count"="1");

-- Eliminar datos previos y cargar nuevos datos en la tabla timeslots
LOAD DATA INPATH '/user/hadoop/Videos_csv/Timeslot.csv' INTO TABLE `timeslots`;

-- Crear tabla alerts
CREATE EXTERNAL TABLE IF NOT EXISTS `alerts` (
    `type` STRING,
    `timestamp` TIMESTAMP,
    `video_id` STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
TBLPROPERTIES ("skip.header.line.count"="1");

-- Eliminar datos previos y cargar nuevos datos en la tabla alerts
LOAD DATA INPATH '/user/hadoop/Videos_csv/Alert.csv' INTO TABLE `alerts`;

-- Crear tabla object_counts
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

-- Eliminar datos previos y cargar nuevos datos en la tabla object_counts
LOAD DATA INPATH '/user/hadoop/Videos_csv/ObjectCount.csv' INTO TABLE `object_counts`;
