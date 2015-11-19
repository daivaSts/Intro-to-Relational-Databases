# Udacity.com /ud197 / Intro to Relational Databases
# L5: Final Project Tournament - Implementation of a Swiss-system tournament
# file 1 of 3

# Assignment:
# To writing a Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.
# The game tournament will use the Swiss system for pairing up players in each round: players are not eliminated,
# and each player should be paired with another player with the same number of wins, or as close as possible.
# The project has two parts: defining the database schema (SQL table definitions), and writing the code that will use it.

#!/usr/bin/env python
import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("DELETE FROM draws;")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("DELETE FROM players;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("SELECT count(*) from players;")
    count = cursor.fetchall()[0][0]
    DB.close()
    return count



def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    cursor = DB.cursor()
    content = bleach.clean(name, strip=True).strip()
    cursor.execute("INSERT INTO players (name, wins, matches) VALUES (%s, %s, %s);",(content, 0, 0))
    DB.commit()
    DB.close()



def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list is the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM players order by wins desc;")
    result_table = cursor.fetchall()
    standings = [(int(row[1]), str(row[0]),int(row[2]),int(row[3])) for row in result_table]
    DB.close()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("UPDATE players SET wins = wins + 1, matches = matches + 1 WHERE id = %s;",(str(winner),))
    cursor.execute("UPDATE players SET matches = matches + 1 WHERE id = %s;", (str(loser),))
    DB.commit()
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
    standing = playerStandings()
    pairing = [(standing[i][0], standing[i][1]) for i in range(len(standing))]
    result = []
    for n in range(0,len(pairing),2):
        result.append(pairing[n] +pairing[n+1])
    return result


