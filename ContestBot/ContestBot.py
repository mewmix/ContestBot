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
        logger.debug("Logger initialized.")
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
        if any(type(setting) != bool for setting in toggle_settings):
            valid = False
            logger.error("Missing toggle setting(s) in config.py.")

        # check general settings
        if config.search_type not in ("mixed", "recent", "popular"):
            valid = False
            logger.error(f'config.search_type must be "mixed", "recent", or "popular".')

        if not type(config.include_retweets) == bool:
            valid = False
            logger.error("config.include_retweets must be True or False.")

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


def get_tweets(logger, api, search_type=config.search_type):
    """
    Searches tweets on twitter. Relevant settings in config.py: contest_keywords, count, search_type
    You can use the return from ContestBot.get_next_search_type() to iterate through search types and pass it to the
    search_type parameter in this function call.
    :param logger: logger instance.
    :param api: tweepy api instance.
    :param search_type: Valid: "mixed", "recent", "popular". Defaults to the value set in config.search_type. Can use
    ContestBot.get_next_search_type() to iterate through search types.
    :return: list that contains all status(tweets) objects scraped from twitter search.
    """
    try:
        all_tweets = []
        logger.info("Searching for tweets...")
        logger.info(f'Search type: {search_type}')
        for keyword in config.contest_keywords:
            if not config.include_retweets:
                logger.debug("Not including retweeted statuses.")
                search_keyword = f'{keyword.lower()} -filter:retweets'
            else:
                logger.debug("Including retweeted statuses.")
                search_keyword = keyword.lower()
            logger.info(f'Gathering {config.count} tweets with "{search_keyword}" keyword.')
            for status in tweepy.Cursor(api.search, lang="en", result_type=search_type,
                                        tweet_mode="extended", q=search_keyword).items(config.count):
                all_tweets.append(status)
            logger.info("Done.")
            logger.debug(
                f'Finished finding tweets for "{search_keyword}". Tweet list now contains {len(all_tweets)} tweets.')
            _random_sleep(logger, config.sleep_per_action[0], config.sleep_per_action[1])
        logger.info(f'Scraped {len(all_tweets)} total tweets.')
        return all_tweets
    except tweepy.TweepError as e:
        _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'get_tweets error: {e}')
        return False


def check_tweet(logger, tweet):
    try:
        lowercase_tweet_text = _get_tweet_text(logger, tweet)
        # check if username has any banned user words in it (set in config.banned_user_words)
        if config.banned_user_words:
            if any(banned_user_word.lower() in tweet.user.screen_name.lower() for banned_user_word in
                   config.banned_user_words):
                logger.info("Banned user word found in username. Skipping tweet.")
                return False
        # check if tweet text has any banned words in it (set in config.banned_words)
        if config.banned_words:
            if any(banned_word.lower() in lowercase_tweet_text for banned_word in config.banned_words):
                logger.info("Banned word found in tweet. Skipping tweet.")
                return False
        logger.debug("Found tweet that does not contain banned users or words.")
        return lowercase_tweet_text
    except Exception as e:
        logger.error(f'check_tweet error: {e}')
        return False


def find_actions(logger, tweet_text):
    try:
        actions = {"retweet": False, "like": False, "follow": False, "comment": False, "tag": False, "dm": False}
        lowercase_tweet_text = tweet_text
        split_text = lowercase_tweet_text.split()
        logger.debug(f'lowercase_tweet_text: {lowercase_tweet_text}')
        logger.info("Searching tweet for ON features keywords...")

        # check if tweet contains any retweet keywords, special case for "rt" since it was returning false positives
        if config.retweet:
            for retweet_keyword in config.retweet_keywords:
                lowercase_retweet_keyword = retweet_keyword.lower()
                if lowercase_retweet_keyword == "rt":
                    logger.debug(f'Searching split text for keyword "rt".')
                    for word in split_text:
                        if word == "rt":
                            logger.debug(f'Found "rt" in split text.')
                            actions["retweet"] = True
                else:
                    if lowercase_retweet_keyword in lowercase_tweet_text:
                        actions["retweet"] = True
            if actions.get("retweet"):
                logger.info("Retweet keyword found in tweet.")
        # check if tweet contains any like keywords
        if any(like_keyword.lower() in lowercase_tweet_text for like_keyword in config.like_keywords) and config.like:
            logger.info("Like keyword found in tweet.")
            actions["like"] = True
        # check if tweet contains any follow keywords
        if any(follow_keyword.lower() in lowercase_tweet_text for follow_keyword in
               config.follow_keywords) and config.follow:
            logger.info("Follow keyword found in tweet.")
            actions["follow"] = True
        # check if tweet contains any comment keywords
        if any(comment_keyword.lower() in lowercase_tweet_text for comment_keyword in
               config.comment_keywords) and config.comment:
            logger.info("Comment keyword found in tweet.")
            actions["comment"] = True
        # check if tweet contains any tag keywords
        if any(tag_keyword.lower() in lowercase_tweet_text for tag_keyword in config.tag_keywords) and config.comment:
            logger.info("Tag keyword found in tweet.")
            actions["tag"] = True
        # check if tweet contains any dm keywords
        if any(dm_keyword.lower() in lowercase_tweet_text for dm_keyword in config.dm_keywords) and config.dm:
            logger.info("Dm keyword found in tweet.")
            actions["dm"] = True
        # if any actions detected
        if any(value for value in actions.values()):
            # if only follow action detected
            if actions.get("follow") and not (
                    actions.get("retweet") or actions.get("like") or actions.get("comment") or actions.get(
                "tag") or actions.get("dm")):
                logger.info("Only follow action found. Skipping tweet.")
                return False
            else:
                return actions
        else:
            logger.info("No actions found in tweet. Skipping tweet.")
            return False
    except Exception as e:
        logger.error(f'find_actions error: {e}')
        return False


def perform_actions(logger, api, tweet, actions):
    actions_ran = {"retweet": False, "like": False, "unfollow": False, "follow": False, "comment": False, "tag": False,
                   "dm": False}
    try:
        if actions.get("retweet"):
            retweet = _retweet(logger, api, tweet)
            actions_ran["retweet"] = retweet
            if not retweet:
                logger.warning("Problem retweeting. Skipping tweet.")
                return False
        if actions.get("like"):
            like = _like(logger, api, tweet)
            actions_ran["like"] = like
            if not like:
                logger.warning("Problem liking. Skipping tweet.")
                return False
        if actions.get("follow"):
            following = _get_following(logger, api)
            while len(following) >= config.max_following:
                unfollow = _unfollow(logger, api, following[0])
                actions_ran["unfollow"] = unfollow
                if not unfollow:
                    logger.warning("Problem unfollowing.")
            follow = _follow(logger, api, tweet)
            actions_ran["follow"] = follow
            if not follow:
                logger.warning("Problem following.")
        if actions.get("comment") and not actions.get("tag"):
            comment = _comment(logger, api, tweet)
            actions_ran["comment"] = comment
            if not comment:
                logger.warning("Problem commenting. Skipping tweet.")
                return False
        if actions.get("tag"):
            tag = _comment(logger, api, tweet, tag=True)
            actions_ran["tag"] = tag
            if not tag:
                logger.warning("Problem tagging. Skipping tweet.")
                return False
        if actions.get("dm"):
            dm = _dm(logger, api, tweet)
            actions_ran["dm"] = dm
            if not dm:
                logger.warning("Problem dming. Skipping tweet.")
                return False
        logger.info("All detected actions were performed on tweet.")
        _random_sleep(logger, config.sleep_per_tweet[0], config.sleep_per_tweet[1])
        return actions_ran
    except tweepy.TweepError as e:
        _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'perform_actions error: {e}')
        return False


def get_next_search_type(logger, current_search_type):
    if current_search_type == "mixed":
        new_search_type = "recent"
    elif current_search_type == "recent":
        new_search_type = "popular"
    elif current_search_type == "popular":
        new_search_type = "mixed"
    else:
        logger.warning(f'Invalid search type parameter. Defaulting new search type to "mixed".')
        new_search_type = "mixed"
    logger.debug(f'Old search type: {current_search_type}')
    logger.debug(f'New search type: {new_search_type}')
    return new_search_type


def _get_tweet_text(logger, tweet):
    # status is a retweet
    try:
        text = tweet.retweeted_status.full_text
        logger.debug("Tweet text extracted successfully. Tweet is a retweet.")
    # status is not a retweet
    except AttributeError:
        text = tweet.full_text
        logger.debug("Tweet text extracted successfully. Tweet is not a retweet.")
    return text.lower()


def _get_tweet_author(logger, tweet):
    # status is a retweet
    try:
        author = tweet.retweeted_status.user.screen_name
        logger.debug(f'Tweet is a retweet. Original author is @{author}.')
    # status is not a retweet
    except:
        author = tweet.user.screen_name
        logger.debug(f'Tweet is not a retweet. Author is @{author}.')
    return author


def _retweet(logger, api, tweet):
    try:
        api.retweet(tweet.id)
        logger.info("Tweet retweeted.")
        _random_sleep(logger, config.sleep_per_action[0], config.sleep_per_action[1])
        return True
    except tweepy.TweepError as e:
        return _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'_retweet error: {e}')
        return False


def _like(logger, api, tweet):
    try:
        api.create_favorite(tweet.id)
        logger.info("Tweet liked.")
        _random_sleep(logger, config.sleep_per_action[0], config.sleep_per_action[1])
        return True
    except tweepy.TweepError as e:
        return _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'_like error: {e}')
        return False


def _follow(logger, api, tweet):
    try:
        username = _get_tweet_author(logger, tweet)
        api.create_friendship(username)
        logger.info(f'Followed: @{username}')
        _random_sleep(logger, config.sleep_per_action[0], config.sleep_per_action[1])
        return True
    except tweepy.TweepError as e:
        return _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'_follow error: {e}')
        return False


def _comment(logger, api, tweet, tag=False):
    try:
        comment = _generate_text(logger)
        if tag:
            tag_username = random.choice(config.tag_handles)
            comment = f'@{tag_username} {comment}'

        api.update_status(status=comment, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
        logger.info("Tweet commented.")
        _random_sleep(logger, config.sleep_per_action[0], config.sleep_per_action[1])
        return True
    except tweepy.TweepError as e:
        return _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'_comment error: {e}')
        return False


def _dm(logger, api, tweet):
    try:
        username = _get_tweet_author(logger, tweet)
        message = _generate_text(logger)
        api.send_direct_message(username, message)
        logger.info(f'Direct messaged @{username}')
        _random_sleep(logger, config.sleep_per_action[0], config.sleep_per_action[1])
        return True
    except tweepy.TweepError as e:
        return _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'_dm error: {e}')
        return False


def _get_following(logger, api):
    try:
        following = api.friends_ids(config.username)
        logger.info(f'Current following: {len(following)}')
        _random_sleep(logger, config.sleep_per_action[0], config.sleep_per_action[1])
        return following
    except tweepy.TweepError as e:
        return _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'_get_following error: {e}')
        return False


def _unfollow(logger, api, user_id):
    try:
        api.destroy_friendship(user_id)
        logger.info("Oldest following account unfollowed.")
        _random_sleep(logger, config.sleep_per_action[0], config.sleep_per_action[1])
        return True
    except tweepy.TweepError as e:
        return _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'_unfollow error: {e}')
        return False


def _random_sleep(logger, minimum, maximum):
    try:
        random_time = random.uniform(minimum, maximum)
        logger.info(f'Sleeping for {random_time}s.')
        time.sleep(random_time)
        return True
    except Exception as e:
        logger.error(f'_random_sleep error: {e}')
        return False


def _generate_text(logger):
    try:
        reply = random.choice(config.replies) + random.choice(config.punctuation)
        capitalization = random.choice(["original", "upper", "lower"])

        if capitalization == "upper":
            reply = reply.upper()
        elif capitalization == "lower":
            reply = reply.lower()
        logger.info(f'Text generated: {reply}')
        return reply
    except Exception as e:
        logger.error(f'_generate_text error: {e}')
        return False


def _tweepy_error_handler(logger, tweep_error):
    """
    :param logger: logger instance
    :param tweep_error: pass the caught exception from caller
    :return: raises exception if critical error, returns False if recoverable error
    """
    logger.warning(f'_tweepy_error_handler caught {tweep_error}')
    # account has been locked
    if tweep_error.api_code == 326:
        raise Exception(f'_tweepy_error_handler terminated ContestBot because: {tweep_error}')
    return False
