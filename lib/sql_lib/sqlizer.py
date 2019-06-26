import sqlite3
from sqlite3 import Error
import lib.sql_lib.commands as sql_cmd
 
 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_player(conn, name, Player):
    """
    Create a new player into the players table
    :param conn - SQL Connection:
    :param name - Player's name:
    :param Player - Player class:
    :return: player name
    """
    age = int(Player.age)
    height = Player.height.split('-')
    height = (int(height[0])*12) + int(height[1])
    weight = ''.join(x for x in Player.weight if x.isdigit())
    awards = ', '.join(Player.awards)

    inp = (name, Player.profile_link, age, height, weight, Player.position[0], Player.shoots, Player.team, Player.born, Player.college, Player.high_school, Player.recruiting_rank, Player.draft, Player.nba_debut, Player.experience, awards)
    cur = conn.cursor()
    cur.execute(sql_cmd.PLAYERS_REPLACE, inp)
    return Player.name


def create_stat(conn, name, stat):
    """
    Create a new stat
    :param conn:
    :param stat:
    :return:
    """
    hash_name = (name + "-" + stat[0] + '-stats').replace(' ', '-')


    inp = (hash_name, name) + tuple(stat)
    cur = conn.cursor()
    cur.execute(sql_cmd.STATS_REPLACE, inp)
    return cur.lastrowid

def create_play_by_play(conn, name, stat):
    """
    Create a new play by play
    :param conn - SQL Connection:
    :param stat - Play-by-Play stat:
    :return:
    """
    hash_name = (name + "-" + stat[0] + '-stats').replace(' ', '-')
    inp = (hash_name, name) + tuple(stat)
    cur = conn.cursor()
    cur.execute(sql_cmd.PBP_REPLACE, inp)
    return cur.lastrowid

def create_all_tables(conn):
    if conn is not None:
        create_table(conn, sql_cmd.PLAYERS_CREATE)
        create_table(conn, sql_cmd.STATS_CREATE)
        create_table(conn, sql_cmd.PBP_CREATE)
        return True
    else:
        print("Error: cannot create the database connection.")
        return False
