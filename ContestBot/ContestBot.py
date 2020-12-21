import random
import config
import tweepy


def authenticate(self, consumer_key, consumer_secret, token, token_secret):
    pass


def get_following():
    pass


def get_tweets():
    # count = 1000 of each keyword
    pass


def check_tweet(tweet):
    # if not banned user
    # if not banned words
    pass


def find_actions(tweet):
    actions = {"retweet": False, "like": False, "follow": False, "comment": False, "dm": False}
    # if contains retweet, like, follow, comment, or dm
    pass
    return actions


def perform_actions(tweet, actions):
    if actions.get("retweet"):
        _retweet()
    if actions.get("like"):
        _like()
    if actions.get("follow"):
        _follow()
    if actions.get("comment"):
        _comment()
    if actions.get("dm"):
        _dm()


def _retweet(tweet):
    pass


def _like(tweet):
    pass


def _follow(tweet):
    pass


def _comment(tweet):
    comment = _generate_text()
    pass


def _dm(tweet):
    message = _generate_text()
    pass


def _generate_text():
    reply = random.choice(config.replies) + random.choice(config.punctuation)
    capitalization = random.choice(["original", "upper", "lower"])

    if capitalization == "upper":
        return reply.upper()
    elif capitalization == "lower":
        return reply.lower()
    else:
        return reply
