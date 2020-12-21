import time
import random
import tweepy

import config


def authenticate(consumer_key, consumer_secret, token, token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(token, token_secret)
    return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_following(api):
    pass


def get_tweets(api):
    # count = 200 of each keyword
    pass


def check_tweet(api, tweet):
    # if not banned user
    # if not banned words
    # if not already liked/retweeted/etc
    pass


def find_actions(tweet):
    actions = {"retweet": False, "like": False, "follow": False, "comment": False, "dm": False}
    # if contains retweet, like, follow, comment, or dm
    pass
    return actions


def perform_actions(api, tweet, actions, old_times):
    status_time = old_times.get("status")
    like_time = old_times.get("like")
    follow_time = old_times.get("follow")
    dm_time = old_times.get("dm")

    if actions.get("retweet"):
        _sleep_handler(status_time, config.STATUS_SLEEP)
        _retweet(tweet)
        status_time = time.perf_counter()
    if actions.get("like"):
        _sleep_handler(like_time, config.LIKE_SLEEP)
        _like(tweet)
        like_time = time.perf_counter()
    if actions.get("follow"):
        _sleep_handler(follow_time, config.FOLLOW_SLEEP)
        _follow(tweet)
        follow_time = time.perf_counter()
    if actions.get("comment"):
        _sleep_handler(status_time, config.STATUS_SLEEP)
        _comment(tweet)
        status_time = time.perf_counter()
    if actions.get("dm"):
        _sleep_handler(dm_time, config.DM_SLEEP)
        _dm(tweet)
        dm_time = time.perf_counter()

    return {"status": status_time, "like": like_time, "follow": follow_time, "dm": dm_time}


def initialize_times():
    return {"status": 0, "like": 0, "follow": 0, "dm": 0}


def _sleep_handler(old_time, action_sleep):
    new_time = time.perf_counter()
    time_since_last_action = new_time - old_time

    if time_since_last_action < action_sleep:
        return time.sleep((action_sleep-time_since_last_action)+_random_sleep())


def _random_sleep():
    return random.uniform(0, config.SLEEP_RANDOMIZER)


def _retweet(api, tweet):
    pass


def _like(api, tweet):
    pass


def _follow(api, tweet):
    pass


def _comment(api, tweet):
    comment = _generate_text()
    pass


def _dm(api, tweet):
    message = _generate_text()
    pass


def _unfollow(api):
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
