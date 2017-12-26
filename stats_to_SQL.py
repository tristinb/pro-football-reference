
import sqlite3
import ssl
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re


# Now read the SQL table


conn = sqlite3.connect('nfl_stats.sqlite')
cur = conn.cursor()


cur.executescript(''' DROP TABLE IF EXISTS Stats;

CREATE TABLE Stats(
id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
team_id INTEGER,
link_id INTEGER,
opp_id  INTEGER,
Week INTEGER,
Year  INTEGER,
Day  TEXT,
Win  INTEGER,
Tot_Wins  INTEGER,
Tot_Loss INTEGER,
Home  INTEGER,
Points_off  INTEGER,
Points_def  INTEGER,
Yards_off  INTEGER,
Pass_Yards_off  INTEGER,
Rush_Yards_off  INTEGER,
Yards_def  INTEGER,
Pass_Yards_def  INTEGER,
Rush_Yards_def  INTEGER,
TO_off  INTEGER,
TO_def  INTEGER
);
''')


cur.execute('SELECT * FROM Link')

teams2 = []
for row in cur:
    teams2.append(row)


for link in range(len(teams2)):
    url = teams2[link][1]
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="games")
    bods = table.find('tbody')
    tab = bods.findAll('tr')


    for i in range(len(tab)):
        th = tab[i].findAll('th') # This is to get week number
        week = re.findall('>(.*)<', str(th))[0]
        td = tab[i].findAll('td')
        stats = [] # This will be reset after each week (row in table)
        for j in range(len(td)):
            stats.append([re.findall('data-stat="(.+?)">', str(td[j]))[0],
            re.findall('>(.*)<', str(td[j]))[0] ])
        opp = re.findall('>(.*)<',str(stats[8][1])) #get rid of op url

        if len(opp)>0 and opp[0]!='Bye Week':
            cur.execute('SELECT id FROM Team WHERE team = ? ', (opp[0], ))
            opp_id = cur.fetchone()[0]
            if stats[4][1] =='W': # Make W, L into dummy var
                win = 1
            else:
                win = 0
            # Note: above and below ignore ties
            record = stats[6][1].split('-')
            tot_wins = int(record[0]) # split wins, losses
            tot_loss = int(record[1])
            print(tot_wins, tot_loss)
            if stats[7][1] =='@': # turn at into dummy
                home = 0
            else:
                home = 1

        cur.execute('''INSERT OR IGNORE INTO Stats (team_id, link_id,opp_id,Week, Year, Day,Win,
        Tot_Wins, Tot_Loss, Home, Points_off, Points_def,Yards_off,Pass_Yards_off,Rush_Yards_off,Yards_def,Pass_Yards_def,Rush_Yards_def,TO_off,TO_def)
        Values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(teams2[link][3],
            teams2[link][0],opp_id, week,
            teams2[link][2],stats[1][1],win,tot_wins,tot_loss,home,stats[9][1],stats[10][1],stats[12][1],stats[13][1],
            stats[14][1],stats[17][1],stats[18][1],stats[19][1],stats[15][1],stats[20][1]) )
        conn.commit()
