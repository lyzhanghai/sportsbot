"""Extract data, chart by sport."""
import settings
import pandas as pd
import peewee
from peewee import *
import plotly.plotly as py
from plotly.graph_objs import *
# from datetime import date

db = MySQLDatabase(settings.dbname,
                   user=settings.dbuser,
                   passwd=settings.dbpasswd)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class games(BaseModel):
    matchdate = peewee.DateTimeField()
    hometeam = peewee.CharField()
    awayteam = peewee.CharField()
    homescore = peewee.IntegerField()
    awayscore = peewee.IntegerField()
    league = peewee.CharField()
    stage = peewee.CharField()
    view = peewee.CharField()


class leagues(BaseModel):
    leagues = peewee.CharField()
    sports = peewee.CharField()


rq = db.execute_sql("""SELECT COUNT(a.hometeam), sports FROM games a join
                    leagues b on a.league = b.leagues GROUP BY sports""")

toPandas = []

for row in rq.fetchall():
    toPush = (row[0], row[1])
    toPandas.append(toPush)

toPandas = tuple(toPandas)

df = pd.DataFrame([[ij for ij in i] for i in toPandas])
df.rename(columns={0: 'Games', 1: 'Sport'}, inplace=True)

sports = []
for item in df['Sport']:
    sports.append(item)
gameslist = []
for item in df['Games']:
    gameslist.append(item)

fig = {
    'data': [{'labels': sports,
              'values': gameslist,
              'type': 'pie',
              'name': 'Games by Sport'}],
    'layout': {'title': "Games By Sport"}
}

py.iplot(fig, validate=False, filename='GamesPerSport')
