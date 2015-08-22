"""Sportsbot."""
import settings
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

hockeym = []
hockeyg = []
baseballm = []
baseballg = []
soccerm = []
soccerg = []
footballm = []
footballg = []


def getHockey():
    rq = db.execute_sql("""SELECT DATE_FORMAT(a.matchdate, %s) GameDate,
                        COUNT(a.hometeam) Games FROM games a JOIN leagues b on
                        a.league = b.leagues WHERE b.sports = %s GROUP BY
                        GameDate, b.sports LIMIT 6""", ('%m/%y', 'hockey'))
    for row in rq.fetchall():
        hockeym.append(row[0])
        hockeyg.append(row[1])


def getBaseball():
    rq = db.execute_sql("""SELECT DATE_FORMAT(a.matchdate, %s) GameDate,
                        COUNT(a.hometeam) Games FROM games a JOIN leagues b on
                        a.league = b.leagues WHERE b.sports = %s GROUP BY
                        GameDate, b.sports LIMIT 6""", ('%m/%y', 'baseball'))
    for row in rq.fetchall():
        baseballm.append(row[0])
        baseballg.append(row[1])


def getSoccer():
    rq = db.execute_sql("""SELECT DATE_FORMAT(a.matchdate, %s) GameDate,
                        COUNT(a.hometeam) Games FROM games a JOIN leagues b on
                        a.league = b.leagues WHERE b.sports = %s GROUP BY
                        GameDate, b.sports LIMIT 6""", ('%m/%y', 'soccer'))
    for row in rq.fetchall():
        soccerm.append(row[0])
        soccerg.append(row[1])


def getFootball():
    rq = db.execute_sql("""SELECT DATE_FORMAT(a.matchdate, %s) GameDate,
                        COUNT(a.hometeam) Games FROM games a JOIN leagues b on
                        a.league = b.leagues WHERE b.sports = %s GROUP BY
                        GameDate, b.sports LIMIT 6""", ('%m/%y', 'football'))
    for row in rq.fetchall():
        footballm.append(row[0])
        footballg.append(row[1])

getFootball()
getSoccer()
getBaseball()
getHockey()

trace1 = Bar(
    x=footballm,
    y=footballg,
    name='Football'
)

trace2 = Bar(
    x=soccerm,
    y=soccerg,
    name='Soccer'
)

trace3 = Bar(
    x=baseballm,
    y=baseballg,
    name='Baseball'
)

trace4 = Bar(
    x=hockeym,
    y=hockeyg,
    name='Hockey'
)

data = Data([trace1, trace2, trace3, trace4])
layout = Layout(
    barmode='stack',
    title='Games Per Month',
    xaxis=XAxis(
        title='Month'
    ),
    yaxis=YAxis(
        title='Games Watched'
    )
)

fig = Figure(data=data, layout=layout)
py.iplot(fig, filename='GamesPerMonth')
