from twython import Twython
import os

# get emails and password from environment variables
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
VERSION = os.environ.get("VERSION")

twitter = Twython(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)

message = "Nouvelle #Release pour #pypodo : " + VERSION + " . Rendez vous sur http://github.com/thib1984/pypodo ! Ou directement 'pypodo -u' si l'outil est déjà installé sur votre poste. "

twitter.update_status(status=message)

print("Tweeted: %s" % message)
