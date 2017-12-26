
import sqlite3
import ssl
import re

filename = 'nfl_stats.sqlite'
conn = sqlite3.connect(filename)
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Team;
DROP TABLE IF EXISTS Link;


CREATE TABLE Team (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    team   TEXT UNIQUE

);

CREATE TABLE Link (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    link    TEXT UNIQUE,
    year    INTEGER,
    team_id INTEGER
);

''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

from NFL_team_links import team_urls as teams

# start at 2002
for year in range(len(teams)):
     teams[year][0] = teams[year][0].replace('2014','2002')


for i in (range(2002,2017)):
    new_year = i + 1
    i = str(i)
    new_year = str(new_year)
    for team in range(len(teams)):
        teams[team][0] = teams[team][0].replace(i,new_year)
    i = int(i)
    for t in range(len(teams)):
        team = teams[t][1]
        link = teams[t][0]
        year = new_year

        cur.execute('''INSERT OR IGNORE INTO Team (team)
            VALUES ( ? )''', (team, ) )
        cur.execute('SELECT id FROM Team WHERE team = ? ', (team, ))
        team_id = cur.fetchone()[0]

        cur.execute('''INSERT OR IGNORE INTO Link (year, link, team_id)
            VALUES ( ?, ?, ? )''', ( year, link, team_id ) )

        conn.commit()
