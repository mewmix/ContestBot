import random
import time
import tweepy

import config


def authenticate():
    try:
        auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
        auth.set_access_token(config.token, config.token_secret)
        return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    except Exception as e:
        print(f'authenticate error: {e}')


def get_tweets(api):
    try:
        all_tweets = []
        for keyword in config.contest_keywords:
            keyword_tweets = api.search(q=keyword.lower(), count=config.count)
            all_tweets.append(keyword_tweets)
        return all_tweets
    except Exception as e:
        print(f'get_tweets error: {e}')


def check_tweet(tweet):
    try:
        # check if username has any banned user words in it (set in config.banned_user_words)
        if config.banned_user_words:
            if any(banned_user_word.lower() in tweet.user.screen_name.lower() for banned_user_word in
                   config.banned_user_words):
                return False

        # check if tweet text has any banned words in it (set in config.banned_words)
        if config.banned_words:
            if any(banned_word.lower() in tweet.text.lower() for banned_word in config.banned_words):
                return False

        return True
    except Exception as e:
        print(f'check_tweet error: {e}')


def find_actions(tweet):
    try:
        actions = {"retweet": False, "like": False, "follow": False, "comment": False, "tag": False, "dm": False}
        lowercase_tweet_text = tweet.text.lower()

        # check if tweet contains any retweet keywords
        if any(retweet_keyword.lower() in lowercase_tweet_text for retweet_keyword in config.retweet_keywords):
            actions["retweet"] = True
        # check if tweet contains any like keywords
        if any(like_keyword.lower() in lowercase_tweet_text for like_keyword in config.like_keywords):
            actions["like"] = True
        # check if tweet contains any follow keywords
        if any(follow_keyword.lower() in lowercase_tweet_text for follow_keyword in config.follow_keywords):
            actions["follow"] = True
        # check if tweet contains any comment keywords
        if any(comment_keyword.lower() in lowercase_tweet_text for comment_keyword in config.comment_keywords):
            actions["comment"] = True
        # check if tweet contains any tag keywords
        if any(tag_keyword.lower() in lowercase_tweet_text for tag_keyword in config.tag_keywords):
            actions["tag"] = True
        # check if tweet contains any dm keywords
        if any(dm_keyword.lower() in lowercase_tweet_text for dm_keyword in config.dm_keywords):
            actions["dm"] = True

        if any(value for value in actions.values()):
            return actions
        else:
            return False
    except Exception as e:
        print(f'find_actions error: {e}')


def perform_actions(api, tweet, actions):
    try:
        if actions.get("retweet") and config.retweet:
            _retweet(api, tweet)
        if actions.get("like") and config.like:
            _like(api, tweet)
        if actions.get("follow") and config.follow:
            _unfollow_random(api)
            _follow(api, tweet)
        if actions.get("comment") and config.comment and not actions.get("tag"):
            _comment(api, tweet)
        if actions.get("tag") and config.comment:
            _comment(api, tweet, tag=True)
        if actions.get("dm") and config.dm:
            _dm(api, tweet)
    except Exception as e:
        print(f'perform_actions error: {e}')


def _retweet(api, tweet):
    try:
        api.retweet(tweet.id)
        time.sleep(_random_sleep())
    except Exception as e:
        print(f'_retweet error: {e}')


def _like(api, tweet):
    try:
        api.create_favorite(tweet.id)
        time.sleep(_random_sleep())
    except Exception as e:
        print(f'_like error: {e}')


def _follow(api, tweet):
    try:
        username = tweet.user.screen_name
        api.create_friendship(username)
        time.sleep(_random_sleep())
    except Exception as e:
        print(f'_follow error: {e}')


def _comment(api, tweet, tag=False):
    try:
        reply_username = tweet.user.screen_name
        comment = _generate_text()
        if tag:
            tag_username = random.choice(config.tag_handles)
            comment = f'@{reply_username} @{tag_username} {comment}'
        else:
            comment = f'@{reply_username} {comment}'

        api.update_status(status=comment, in_reply_to_status_id=tweet.id)
        time.sleep(_random_sleep())
    except Exception as e:
        print(f'_comment error: {e}')


def _dm(api, tweet):
    try:
        message = _generate_text()
        user_id = api.get_user(tweet.user.screen_name)
        api.send_direct_message(user_id, message)
        time.sleep(_random_sleep())
    except Exception as e:
        print(f'_dm error: {e}')


def _unfollow_random(api):
    try:
        following = api.friends_ids(config.username)
        user_to_unfollow = random.choice(following)
        api.destroy_friendship(user_to_unfollow)
        time.sleep(_random_sleep())
    except Exception as e:
        print(f'_unfollow_random error: {e}')


def _random_sleep():
    try:
        return random.uniform(0, config.sleep_randomizer)
    except Exception as e:
        print(f'_random_sleep error: {e}')


def _generate_text():
    try:
        reply = random.choice(config.replies) + random.choice(config.punctuation)
        capitalization = random.choice(["original", "upper", "lower"])

        if capitalization == "upper":
            return reply.upper()
        elif capitalization == "lower":
            return reply.lower()
        else:
            return reply
    except Exception as e:
        print(f'_generate_text error: {e}')
