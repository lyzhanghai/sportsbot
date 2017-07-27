"""A bot to tweet sports scores to Tim, then add to db."""
import settings
import peewee  # against standards, but specified in peewee docs?
from peewee import *  # against standards, but specified in peewee docs?
from twython import Twython
from datetime import date
import re

db = MySQLDatabase(settings.dbname,
                   user=settings.dbuser,
                   passwd=settings.dbpasswd)
db.connect()


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


APP_KEY = settings.APP_KEY
APP_SECRET = settings.APP_SECRET

OAUTH_TOKEN = settings.OAUTH_TOKEN
OAUTH_TOKEN_SECRET = settings.OAUTH_TOKEN_SECRET

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

lastTweet = ''


def getLast():
    """Determine where to start."""
    homeFeed = twitter.get_user_timeline(user_id=settings.bot, count=100)
    global lastTweet
    for tweet in homeFeed:
        if ((tweet['text'][:15] == "@NAME added") |
           (tweet['text'][:15] == "@NAME no")):
            lastTweet = int(tweet['id'])
            break


def intake():
    """Grab all tweets from Tim since the last."""
    mentions = twitter.get_mentions_timeline(user_id=settings.bot, count=100)
    tweetsToProcess = []
    for tweet in mentions:
        if ((tweet['user']['id'] == 22884755) & (tweet['id'] > lastTweet)):
            tweetsToProcess.append(tweet)
    return tweetsToProcess


def manual(tweet):
    """
    Administer manual tweets.

    Manual format should be:
    @NAMESports manual [Home, Away, Homescore, AwayScore, League,
                            Stage, View]
    """
    tweetText = tweet['text'][23:]
    tweetArray = [x.strip() for x in tweetText.split(',')]
    print tweetArray
    new = games()
    new.matchdate = date.today()
    new.hometeam = tweetArray[0]
    new.awayteam = tweetArray[1]
    new.homescore = tweetArray[2]
    new.awayscore = tweetArray[3]
    new.league = tweetArray[4]
    new.stage = tweetArray[5]
    new.view = tweetArray[6]
    new.save()
    newTweet = "@NAME added {}.".format(tweetArray)
    twitter.update_status(status=newTweet,
                          in_reply_to_status_id=int(tweet['id']))


def normal(tweet):
    """Administer normal tweets.

    Format should be:
    @NAMESports yes, League, Stage, View
    """
    tweetText = tweet['text']
    replyTweet = tweet['in_reply_to_status_id']
    originalTweet = twitter.show_status(id=replyTweet)

    print originalTweet['text'][:31]

    if originalTweet['text'][:31] == '@NAME Did you watch? Final:':
        tweetArray = [x.strip() for x in tweetText.split(',')]
        originalText = originalTweet['text'][32:-7]
        s = ' '
        originalArray = re.split('\.', originalText)[0]
        home = re.split('(?<=\d)\s', originalArray)[0]
        print home
        away = re.split('(?<=\d)\s', originalArray)[1]
        hscore = home[-1]
        ascore = away[-1]
        hteam = s.join(home[:-len(hscore)].split(' ')).strip()
        ateam = s.join(away[:-len(ascore)].split(' ')).strip()

        new = games()
        new.league = tweetArray[1]
        new.stage = tweetArray[2]
        new.view = tweetArray[3]
        new.hometeam = hteam
        new.awayteam = ateam
        new.homescore = hscore
        new.awayscore = ascore
        new.matchdate = date.today()
        new.save()

        newTweet = "@NAME added {} - {}.".format(hteam, ateam)
        twitter.update_status(status=newTweet,
                              in_reply_to_status_id=int(tweet['id']))

    elif originalTweet['text'][:29] == '@NAME Did you watch? FT -':
        tweetArray = [x.strip() for x in tweetText.split(',')]
        s = " "
        originalText = originalTweet['text'][30:-7]
        originalArray = originalText.split('-')
        home = originalArray[0].split(' ')
        away = originalArray[1].split(' ')
        hscore = home[-1]
        ascore = away[0]
        hteam = s.join(home[:-len(hscore)]).strip()
        ateam = s.join(away[len(ascore):]).strip()

        new = games()
        new.league = tweetArray[1]
        new.stage = tweetArray[2]
        new.view = tweetArray[3]
        new.hometeam = hteam
        new.awayteam = ateam
        new.homescore = hscore
        new.awayscore = ascore
        new.matchdate = date.today()
        new.save()

        newTweet = "@NAME added {} - {}.".format(hteam, ateam)
        twitter.update_status(status=newTweet,
                              in_reply_to_status_id=int(tweet['id']))


def process(tweets):
    """Process tweets from Tim."""

    for tweet in tweets:
        if tweet['text'][:19] == "@NAMESports yes":
            normal(tweet)
        elif tweet['text'][:22] == "@NAMESports manual":
            manual(tweet)

getLast()
process(intake())
