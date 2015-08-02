-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--create database tournament;
create table players
(
ID SERIAL PRIMARY KEY,
NAME TEXT NOT NULL,
MATCHES INTEGER DEFAULT 0,
WON REAL  DEFAULT 0
);

create table match
(
ROUNDID INTEGER  DEFAULT 0,
MATCHID INTEGER  DEFAULT 0,
PLAYER1 INTEGER references PLAYERS(ID),
PLAYER2 INTEGER references PLAYERS(ID),
PRIMARY KEY(ROUNDID,MATCHID)
);


