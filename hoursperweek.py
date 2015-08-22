"""Extract data, chart by hours watched per week.."""
import settings
import peewee
from peewee import *
import plotly.plotly as py
from plotly.graph_objs import *
import datetime

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


class gametime(BaseModel):
    sport = peewee.CharField()
    gtime = peewee.IntegerField()

hockeym = []
hockeyg = []
baseballm = []
baseballg = []
soccerm = []
soccerg = []
footballm = []
footballg = []


def get_week_days(year, week):
    d = datetime.datetime(year, 1, 1)
    if(d.weekday() > 3):
        d = d+datetime.timedelta(7-d.weekday())
    else:
        d = d - datetime.timedelta(d.weekday())
    dlt = datetime.timedelta(days=((week) * 7) - 1)
    return (datetime.datetime.strftime(d + dlt, '%m/%d') + '-' +
            datetime.datetime.strftime(d + dlt + datetime.timedelta(days=6),
            '%m/%d'))


def getBaseball():
    rq = db.execute_sql("""SELECT a.matchdate thedate, SUM(b.gtime) GameTime
                        FROM games a JOIN leagues c ON a.league = c.leagues
                        JOIN gametime b ON c.sports = b.sport WHERE b.sport =
                        'baseball' GROUP BY DATE_FORMAT(thedate, %s) ORDER BY
                        thedate ASC LIMIT 4""", ('%U/%Y'))
    for row in rq.fetchall():
        baseballm.append(get_week_days(int(row[0].strftime('%Y')),
                         int(row[0].strftime('%U'))))
        baseballg.append(int(row[1]))

getBaseball()


def gethockey():
    rq = db.execute_sql("""SELECT a.matchdate thedate, SUM(b.gtime) GameTime
                        FROM games a JOIN leagues c ON a.league = c.leagues
                        JOIN gametime b ON c.sports = b.sport WHERE b.sport =
                        'hockey' GROUP BY DATE_FORMAT(thedate, %s) ORDER BY
                        thedate ASC LIMIT 4""", ('%U/%Y'))
    for row in rq.fetchall():
        hockeym.append(get_week_days(int(row[0].strftime('%Y')),
                       int(row[0].strftime('%U'))))
        hockeyg.append(int(row[1]))

gethockey()


def getsoccer():
    rq = db.execute_sql("""SELECT a.matchdate thedate, SUM(b.gtime) GameTime
                        FROM games a JOIN leagues c ON a.league = c.leagues
                        JOIN gametime b ON c.sports = b.sport WHERE b.sport =
                        'soccer' GROUP BY DATE_FORMAT(thedate, %s) ORDER BY
                        thedate ASC LIMIT 4""", ('%U/%Y'))
    for row in rq.fetchall():
        soccerm.append(get_week_days(int(row[0].strftime('%Y')),
                       int(row[0].strftime('%U'))))
        soccerg.append(int(row[1]))

getsoccer()


def getfootball():
    rq = db.execute_sql("""SELECT a.matchdate thedate, SUM(b.gtime) GameTime
                        FROM games a JOIN leagues c ON a.league = c.leagues
                        JOIN gametime b ON c.sports = b.sport WHERE b.sport =
                        'football' GROUP BY DATE_FORMAT(thedate, %s) ORDER BY
                        thedate ASC LIMIT 4""", ('%U/%Y'))
    for row in rq.fetchall():
        footballm.append(get_week_days(int(row[0].strftime('%Y')),
                         int(row[0].strftime('%U'))))
        footballg.append(int(row[1]))

getfootball()


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
    title='Hours Per Week',
    xaxis=XAxis(
        title='Week'
    ),
    yaxis=YAxis(
        title='Hours'
    )
)

fig = Figure(data=data, layout=layout)
py.iplot(fig, filename='Hoursperweek')
