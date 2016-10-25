"""Extracts data, charts games by league."""
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


rq = db.execute_sql("""select a.leagues, COUNT(b.hometeam) number, a.sports
                    from leagues a join games b on b.league=a.leagues GROUP BY
                    a.leagues ORDER BY number DESC""")

toPandas = []

for row in rq.fetchall():
    toPush = (row[0], int(row[1]), row[2])
    toPandas.append(toPush)

toPandas = tuple(toPandas)

df = pd.DataFrame([[ij for ij in i] for i in toPandas])
df.rename(columns={0: 'League', 1: 'Games', 2: 'Sport'}, inplace=True)

colors = dict(
    Soccer='#d62728',
    Hockey='#ff7f0e',
    Baseball='#2ca02c',
    Football='#1f77b4',
    Basketball='#9264BC'
)
color = []

for index, row in df.iterrows():
    color.append(colors[row['Sport']])


data = [
    Bar(
        x=df['League'],
        y=df['Games'],
        text=df['Sport'],
        marker=Marker(
            color=color
        )
    )
]
layout = Layout(
    title='Games By League',
    xaxis=XAxis(
        title='League'
    ),
    yaxis=YAxis(
        title='Games Watched'
    )
)

fig = Figure(data=data, layout=layout)
py.iplot(fig, filename='GamesByLeague')
