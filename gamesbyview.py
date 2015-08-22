"""Extract data, chart by view."""
import settings
import pandas as pd
import peewee
from peewee import *
import plotly.plotly as py
from plotly.graph_objs import *

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


rq = db.execute_sql("""SELECT COUNT(hometeam), view FROM games a
                    GROUP BY view""")

toPandas = []

for row in rq.fetchall():
    toPush = (row[0], row[1])
    toPandas.append(toPush)

print toPandas
toPandas = tuple(toPandas)
print toPandas


df = pd.DataFrame([[ij for ij in i] for i in toPandas])
df.rename(columns={0: 'Games', 1: 'View'}, inplace=True)

sports = []
for item in df['View']:
    sports.append(item)
gameslist = []
for item in df['Games']:
    gameslist.append(item)

fig = {
    'data': [{'labels': sports,
              'values': gameslist,
              'type': 'pie',
              'name': 'Games by View'}],
    'layout': {'title': "Games By View"}
}

py.iplot(fig, validate=False, filename='Gamesbyview')
