#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from math import log

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete from match")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete from players")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("select count(*) from players")
    result = c.fetchone()[0]
    DB.close()
    return result
    
def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    try:
    	
    	c.execute("insert into players(name) values(%s)",(name,))
    	
    	DB.commit()
    except psycopg2.Error as e:
        print "An error occurred:", e.args[0]
    	DB.rollback()
    DB.close()
    
def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute("select id,name,won,matches from players order by won")
    result = c.fetchall()
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    try:
	c.execute("update PLAYERS set won = won+1 , matches = matches+1 where ID = %s " , [winner])
	c.execute("update PLAYERS set  matches = matches+1 where ID = %s " , [loser])
	DB.commit()
    except psycopg2.Error as e:
        print "An error occurred:", e.args[0]
	DB.rollback()
    DB.close()
    
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB = connect()
    c = DB.cursor()
    c.execute("select max(ROUNDID) from match")
    data = c.fetchone()
    max = 0
    if data == '':
    	max = data[0]
     
    if max < log(countPlayers(),2) :
    	c.execute("select id from PLAYERS where id%2=0 order by won")
    	even = c.fetchall();
    	c.execute("select id from PLAYERS where id%2=1 order by won")
    	odd = c.fetchall()
    	match = 1
    	max = max+1
    	for rec1,rec2 in even,odd:
    		c.execute("insert into match(ROUNDID,MATCHID,PLAYER1,PLAYER2) values(%s,%s,%s,%s)", (max,match,rec1[0],rec2[0]))
    		match = match+1
    		DB.commit()
    
    c.execute("select PLAYER1,p1.name,PLAYER2,p2.name from match m, players p1, players p2 where m.PLAYER1 = p1.id and m.PLAYER2 = p2.id and ROUNDID = %s", [max])
    result = c.fetchall()
    return result
    

