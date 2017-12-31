

# Get teams

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re

import ssl





ctx = ssl.create_default_context()
ctx.check_hostname=False
ctx.verify_mode = ssl.CERT_NONE




# Get list of teams
url = 'https://www.pro-football-reference.com/years/2014/'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')




# Tables are split between AFC and NFC
table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="AFC")
table.append(soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="NFC"))





teams = table.findAll('a')
team_links = []
for i in range(len(teams)):
    team_links.append([re.findall('="(.+)"',str(teams[i]))[0],
                      re.findall('>(.+)<',str(teams[i]))[0]])

print(team_links)





# Get new urls

url.replace('/years/2014/',team_links[0][0])



team_urls = []
for i in range(len(team_links)):
    team_urls.append([url.replace('/years/2014/',team_links[i][0]),team_links[i][1]])
