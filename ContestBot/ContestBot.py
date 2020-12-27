import random
import time
import tweepy
import logging
import sys

import config


def initialize_logger():
    try:
        levels = {0: logging.NOTSET, 1: logging.DEBUG, 2: logging.INFO, 3: logging.WARNING, 4: logging.ERROR,
                  5: logging.CRITICAL}
        level = levels.get(config.level)

        logger = logging.getLogger("ContestBot")

        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(levelname)-s - %(message)s', datefmt="%H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
        logger.info("Logger initialized successfully.")
        return logger
    except Exception as e:
        print(f'initialize_logger error: {e}')
        raise Exception("Logger error. Fix logger.")


def check_config(logger):
    """
    Checks if the config.py file exists and all variables are provided and valid depending what features are turned on.
    Call this function first in your main function so the program fails early if config.py is invalid.
    Warning: This is not an exhaustive check and edge cases could not be caught by this function.

    :return: raises Exception is errors detected.
    """
    valid = True
    try:
        # check authentication settings
        if config.follow and not config.username:
            valid = False
            logger.error("config.follow feature ON requires you to supply a config.username.")

        authentication_settings = [config.consumer_key, config.consumer_secret, config.token, config.token_secret]
        if any(not setting for setting in authentication_settings):
            valid = False
            logger.error("Missing authentication setting(s) in config.py.")

        # check logging settings
        if 1 > config.level > 5:
            valid = False
            logger.error("config.level must be a value between 1 and 5")

        # check toggle feature settings
        toggle_settings = [config.retweet, config.like, config.follow, config.comment, config.dm]
        if any(type(setting) is not bool for setting in toggle_settings):
            valid = False
            logger.error("Missing toggle setting(s) in config.py.")

        # check general settings
        if config.count <= 0:
            valid = False
            logger.error("Invalid config.count setting. Must be greater than 0.")

        if config.follow and 0 >= config.max_following > 2000:
            valid = False
            logger.error("config.follow feature ON requires you to supply config.max_following greater than 0 and "
                         "less than 2000.")

        # check sleep settings
        if (config.sleep_per_action[0] < 0) or (config.sleep_per_action[0] > config.sleep_per_action[1]) or (
                config.sleep_per_action[1] < 0):
            valid = False
            logger.error(
                "Invalid config.sleep_per_action setting. Each value must be 0 or greater and second value cannot be "
                "larger than first.")

        if (config.sleep_per_tweet[0] < 0) or (config.sleep_per_tweet[0] > config.sleep_per_tweet[1]) or (
                config.sleep_per_tweet[1] < 0):
            valid = False
            logger.error(
                "Invalid config.sleep_per_tweet setting. Each value must be 0 or greater and second value cannot be "
                "larger than first.")

        # check reply settings
        if config.comment and not all([config.tag_handles, config.replies, config.punctuation]):
            valid = False
            logger.error("config.comment feature ON requires you to supply config.tag_handles, config.replies, "
                         "and config.punctuation.")

        # check keyword settings
        if not config.contest_keywords:
            valid = False
            logger.error("Missing config.contest_keywords.")

        if config.retweet and not config.retweet_keywords:
            valid = False
            logger.error("config.retweet feature ON requires you to supply config.retweet_keywords.")

        if config.like and not config.like_keywords:
            valid = False
            logger.error("config.like feature ON requires you to supply config.like_keywords.")

        if config.follow and not config.follow_keywords:
            valid = False
            logger.error("config.follow feature ON requires you to supply config.follow_keywords.")

        if config.comment and not all([config.comment_keywords, config.tag_keywords]):
            valid = False
            logger.error("config.comment feature ON requires you to supply config.comment_keywords and "
                         "config.tag_keywords.")

        if config.dm and not config.dm_keywords:
            valid = False
            logger.error("config.dm feature ON requires you to supply config.dm_keywords.")

    except Exception as e:
        valid = False
        logger.error(f'check_config error: {e}')

    if not valid:
        logger.critical("There is a critical error with your config.py file. Please fix errors.")
        raise Exception("Invalid config.py file.")

    logger.info("Config file passed check.")
    logger.info('------------Settings------------')
    logger.info(f'retweet: {config.retweet}')
    logger.info(f'like: {config.like}')
    logger.info(f'follow: {config.follow}')
    logger.info(f'comment: {config.comment}')
    logger.info(f'dm: {config.dm}')
    logger.info('--------------------------------')
    return True


def authenticate(logger):
    try:
        auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
        auth.set_access_token(config.token, config.token_secret)
        logger.info("Authentication successful.")
        return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    except tweepy.TweepError as e:
        _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'authenticate error: {e}')
        raise Exception("Authentication unsuccessful.")


def get_tweets(logger, api):
    try:
        keyword_tweets = []
        all_tweets = []
        logger.info("Searching for tweets...")
        for keyword in config.contest_keywords:
            logger.debug(f'Searching for "{keyword}" keyword.')
            for status in tweepy.Cursor(api.search, lang="en", tweet_mode="extended", q=keyword.lower()).items(
                    config.count):
                # status is a retweet
                try:
                    tweet = status.retweeted_status.full_text
                # status is not a retweet
                except AttributeError:
                    tweet = status.full_text
                keyword_tweets.append(tweet)
            logger.debug(f'Found {len(keyword_tweets)} tweets for {keyword}. Appending to list...')
            all_tweets.extend(keyword_tweets)
            sleep = _random_sleep(logger, config.sleep_per_action[0], config.sleep_per_action[1])
            logger.info(f'Sleeping for {sleep}s')
            time.sleep(sleep)
        logger.info(f'Scraped {len(all_tweets)} total tweets successfully.')
        return all_tweets
    except tweepy.TweepError as e:
        _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'get_tweets error: {e}')
        return False


def check_tweet(logger, tweet):
    try:
        # check if username has any banned user words in it (set in config.banned_user_words)
        if config.banned_user_words:
            if any(banned_user_word.lower() in tweet.user.screen_name.lower() for banned_user_word in
                   config.banned_user_words):
                logger.debug("Banned user word found in username. Tweet invalid.")
                return False
        # check if tweet text has any banned words in it (set in config.banned_words)
        if config.banned_words:
            if any(banned_word.lower() in tweet.full_text.lower() for banned_word in config.banned_words):
                logger.debug("Banned word found in tweet. Tweet invalid.")
                return False
        logger.info("Found tweet that does not contain banned users or words.")
        return True
    except tweepy.TweepError as e:
        _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'check_tweet error: {e}')
        return False


def find_actions(logger, tweet):
    try:
        actions = {"retweet": False, "like": False, "follow": False, "comment": False, "tag": False, "dm": False}
        lowercase_tweet_text = tweet.full_text.lower()

        # check if tweet contains any retweet keywords
        if any(retweet_keyword.lower() in lowercase_tweet_text for retweet_keyword in config.retweet_keywords):
            logger.debug("Retweet keyword found in tweet.")
            actions["retweet"] = True
        # check if tweet contains any like keywords
        if any(like_keyword.lower() in lowercase_tweet_text for like_keyword in config.like_keywords):
            logger.debug("Like keyword found in tweet.")
            actions["like"] = True
        # check if tweet contains any follow keywords
        if any(follow_keyword.lower() in lowercase_tweet_text for follow_keyword in config.follow_keywords):
            logger.debug("Follow keyword found in tweet.")
            actions["follow"] = True
        # check if tweet contains any comment keywords
        if any(comment_keyword.lower() in lowercase_tweet_text for comment_keyword in config.comment_keywords):
            logger.debug("Comment keyword found in tweet.")
            actions["comment"] = True
        # check if tweet contains any tag keywords
        if any(tag_keyword.lower() in lowercase_tweet_text for tag_keyword in config.tag_keywords):
            logger.debug("Tag keyword found in tweet.")
            actions["tag"] = True
        # check if tweet contains any dm keywords
        if any(dm_keyword.lower() in lowercase_tweet_text for dm_keyword in config.dm_keywords):
            logger.debug("Dm keyword found in tweet.")
            actions["dm"] = True

        if any(value for value in actions.values()):
            logger.info("Action(s) found in tweet.")
            return actions
        else:
            logger.debug("No actions found in tweet.")
            return False
    except Exception as e:
        logger.error(f'find_actions error: {e}')
        return False


def perform_actions(logger, api, tweet, actions):
    actions_ran = {"retweet": False, "like": False, "unfollow": False, "follow": False, "comment": False, "tag": False,
                   "dm": False}
    try:
        if actions.get("retweet") and config.retweet:
            retweet = _retweet(logger, api, tweet)
            actions_ran["retweet"] = retweet
            if not retweet:
                logger.warning("Problem retweeting. Skipping tweet.")
                return False
        if actions.get("like") and config.like:
            like = _like(logger, api, tweet)
            actions_ran["like"] = like
            if not like:
                logger.warning("Problem liking. Skipping tweet.")
                return False
        if actions.get("follow") and config.follow:
            following = _get_following(logger, api)
            if len(following) >= config.max_following:
                unfollow = _unfollow(logger, api, following[0])
                actions_ran["unfollow"] = unfollow
                if not unfollow:
                    logger.warning("Problem unfollowing. Skipping tweet.")
                    return False
            follow = _follow(logger, api, tweet)
            actions_ran["follow"] = follow
            if not follow:
                logger.warning("Problem following. Skipping tweet.")
                return False
        if actions.get("comment") and config.comment and not actions.get("tag"):
            comment = _comment(logger, api, tweet)
            actions_ran["comment"] = comment
            if not comment:
                logger.wanring("Problem commenting. Skipping tweet.")
                return False
        if actions.get("tag") and config.comment:
            tag = _comment(logger, api, tweet, tag=True)
            actions_ran["tag"] = tag
            if not tag:
                logger.warning("Problem tagging. Skipping tweet.")
                return False
        if actions.get("dm") and config.dm:
            dm = _dm(logger, api, tweet)
            actions_ran["dm"] = dm
            if not dm:
                logger.warning("Problem dming. Skipping tweet.")
                return False
        logger.info("All detected actions were performed on tweet.")
        sleep = _random_sleep(logger, config.sleep_per_tweet[0], config.sleep_per_tweet[1])
        logger.info(f'Sleeping for {sleep}s')
        time.sleep(sleep)
        return actions_ran
    except tweepy.TweepError as e:
        _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'perform_actions error: {e}')
        return False


def _retweet(logger, api, tweet):
    try:
        api.retweet(tweet.id)
        logger.info("Tweet retweeted successfully.")
        sleep = _random_sleep(logger, config.sleep_per_action[0], config.sleep_per_action[1])
        logger.info(f'Sleeping for {sleep}s')
        time.sleep(sleep)
        return True
    except tweepy.TweepError as e:
        return _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'_retweet error: {e}')
        return False


def _like(logger, api, tweet):
    try:
        api.create_favorite(tweet.id)
        logger.info("Tweet liked successfully.")
        sleep = _random_sleep(logger, config.sleep_per_action[0], config.sleep_per_action[1])
        logger.info(f'Sleeping for {sleep}s')
        time.sleep(sleep)
        return True
    except tweepy.TweepError as e:
        return _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'_like error: {e}')
        return False


def _follow(logger, api, tweet):
    try:
        username = tweet.user.screen_name
        api.create_friendship(username)
        logger.info("Tweet author followed successfully.")
        sleep = _random_sleep(logger, config.sleep_per_action[0], config.sleep_per_action[1])
        logger.info(f'Sleeping for {sleep}s')
        time.sleep(sleep)
        return True
    except tweepy.TweepError as e:
        return _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'_follow error: {e}')
        return False


def _comment(logger, api, tweet, tag=False):
    try:
        reply_username = tweet.user.screen_name
        comment = _generate_text(logger)
        if tag:
            tag_username = random.choice(config.tag_handles)
            comment = f'@{reply_username} @{tag_username} {comment}'
        else:
            comment = f'@{reply_username} {comment}'

        api.update_status(status=comment, in_reply_to_status_id=tweet.id)
        logger.info("Tweet commented successfully.")
        sleep = _random_sleep(logger, config.sleep_per_action[0], config.sleep_per_action[1])
        logger.info(f'Sleeping for {sleep}s')
        time.sleep(sleep)
        return True
    except tweepy.TweepError as e:
        return _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'_comment error: {e}')
        return False


def _dm(logger, api, tweet):
    try:
        message = _generate_text(logger)
        api.send_direct_message(tweet.user.id, message)
        logger.info("Tweet author dm'd successfully.")
        sleep = _random_sleep(logger, config.sleep_per_action[0], config.sleep_per_action[1])
        logger.info(f'Sleeping for {sleep}s')
        time.sleep(sleep)
        return True
    except tweepy.TweepError as e:
        return _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'_dm error: {e}')
        return False


def _get_following(logger, api):
    try:
        following = api.friends_ids(config.username)
        logger.info(f'User following checked. Current following: {len(following)}')
        sleep = _random_sleep(logger, config.sleep_per_action[0], config.sleep_per_action[1])
        logger.info(f'Sleeping for {sleep}s')
        time.sleep(sleep)
        return following
    except tweepy.TweepError as e:
        return _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'_get_following error: {e}')
        return False


def _unfollow(logger, api, user_id):
    try:
        api.destroy_friendship(user_id)
        logger.info("Oldest followed account unfollowed successfully.")
        sleep = _random_sleep(logger, config.sleep_per_action[0], config.sleep_per_action[1])
        logger.info(f'Sleeping for {sleep}s')
        time.sleep(sleep)
        return True
    except tweepy.TweepError as e:
        return _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'_unfollow error: {e}')
        return False


def _random_sleep(logger, minimum, maximum):
    try:
        random_time = random.uniform(minimum, maximum)
        logger.debug("Random sleep generated successfully.")
        return random_time
    except Exception as e:
        logger.error(f'_random_sleep error: {e}')
        return 0


def _generate_text(logger):
    try:
        reply = random.choice(config.replies) + random.choice(config.punctuation)
        capitalization = random.choice(["original", "upper", "lower"])

        if capitalization == "upper":
            reply = reply.upper()
        elif capitalization == "lower":
            reply = reply.lower()
        logger.info(f'Message generated successfully: {reply}')
        return reply
    except Exception as e:
        logger.error(f'_generate_text error: {e}')
        return False


def _tweepy_error_handler(logger, tweep_error):
    # raises exception if critical error, returns False if recoverable error, returns True if ignorable error
    if tweep_error.api_code == 326:
        logger.critical(f'tweepy_error_handler caught {tweep_error}')
        raise Exception(f'tweepy_error_handler terminated ContestBot because: {tweep_error}')
    elif tweep_error.api_code == 327:
        logger.warning(f'tweepy_error_handler caught {tweep_error}')
        return False
    else:
        logger.warning(f'tweepy_error_handler caught and ignored: {tweep_error}')
        return True
