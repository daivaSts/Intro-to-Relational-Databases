-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.

CREATE TABLE players (
    id				SERIAL primary key,
    name			TEXT,
    wins         	INT,
    matches         INT
);

CREATE TABLE  draws(
    id				SERIAL primary key,
    name_1			TEXT,
    name_2      	TEXT
);
