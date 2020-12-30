import random
import time
import tweepy
import logging
import sys

import config


def initialize_logger():
    try:
        # get logger level
        levels = {0: logging.NOTSET, 1: logging.DEBUG, 2: logging.INFO, 3: logging.WARNING, 4: logging.ERROR,
                  5: logging.CRITICAL}
        level = levels.get(config.level)
        # create logger instance
        logger = logging.getLogger("ContestBot")
        # create logger formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)-s - %(message)s', datefmt="%H:%M:%S")
        # console logs
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        # file logs
        if config.file_logs:
            file_handler = logging.FileHandler('ContestBot.log')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        # set logger level
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

        # check toggle feature settings
        toggle_settings = [config.retweet, config.like, config.follow, config.comment, config.dm]
        if any(type(setting) != bool for setting in toggle_settings):
            valid = False
            logger.error("Missing toggle feature setting(s) in config.py.")

        # check action settings
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

        # check sleep settings
        if (config.sleep_per_tweet[0] < 0) or (config.sleep_per_tweet[0] > config.sleep_per_tweet[1]) or (
                config.sleep_per_tweet[1] < 0):
            valid = False
            logger.error(
                "Invalid config.sleep_per_tweet setting. Each value must be 0 or greater and second value cannot be "
                "larger than first.")
        if (config.sleep_per_action[0] < 0) or (config.sleep_per_action[0] > config.sleep_per_action[1]) or (
                config.sleep_per_action[1] < 0):
            valid = False
            logger.error(
                "Invalid config.sleep_per_action setting. Each value must be 0 or greater and second value cannot be "
                "larger than first.")
        if config.follow and (
                (config.sleep_per_unfollow[0] < 0) or (config.sleep_per_unfollow[0] > config.sleep_per_unfollow[1]) or (
                config.sleep_per_unfollow[1] < 0)):
            valid = False
            logger.error(
                "Invalid config.sleep_per_unfollow setting. Each value must be 0 or greater and second value cannot be "
                "larger than first.")
        if config.follow and ((config.sleep_unfollow_mode[0] < 0) or (
                config.sleep_unfollow_mode[0] > config.sleep_unfollow_mode[1]) or (
                                      config.sleep_unfollow_mode[1] < 0)):
            valid = False
            logger.error(
                "Invalid config.sleep_unfollow_mode setting. Each value must be 0 or greater and second value cannot be "
                "larger than first.")

        # check search settings
        if config.count <= 0:
            valid = False
            logger.error("Invalid config.count setting. Must be greater than 0.")
        if config.search_type not in ("mixed", "recent", "popular"):
            valid = False
            logger.error(f'config.search_type must be "mixed", "recent", or "popular".')
        if not config.search_keywords:
            valid = False
            logger.error("Missing config.search_keywords.")
        if not type(config.include_retweets) == bool:
            valid = False
            logger.error("config.include_retweets must be True or False.")
        if not type(config.include_replies) == bool:
            valid = False
            logger.error("config.include_replies must be True or False.")

        # check follow/unfollow settings
        if config.follow and (config.max_following[0] > config.max_following[1] or config.max_following[0] < 0 or
                              config.max_following[1] > 2000 or config.max_following[1]) < 0:
            valid = False
            logger.error("config.follow feature ON requires you to supply config.max_following. Min must be > 0, "
                         "Max must be < 2000 and > Min.")
        if config.follow and (config.unfollow_range[0] > config.unfollow_range[1] or config.unfollow_range[0] < 0 or
                              config.unfollow_range[1] < 0):
            valid = False
            logger.error(
                "config.follow feature ON requires you to supply config.unfollow_range greater than 0. Min should be "
                "< Max and both should be > 0.")

        # check comment settings
        if not type(config.include_hashtags) == bool:
            valid = False
            logger.error("config.include_hashtags must be True or False.")
        if config.comment and not all([config.tag_friends, config.comments, config.comment_punctuation]):
            valid = False
            logger.error("config.comment feature ON requires you to supply config.tag_friends, config.comments, "
                         "and config.comment_punctuation.")

        # check logging settings
        if 1 > config.level > 5:
            valid = False
            logger.error("config.level must be a value between 1 and 5")
        if not type(config.file_logs) == bool:
            valid = False
            logger.error("config.file_logs must be True or False.")

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
        for keyword in config.search_keywords:
            search_keyword = keyword.lower()
            if not config.include_retweets and not config.include_replies:
                logger.debug("Not including retweets or replies.")
                search_keyword = f'{search_keyword} -filter:retweets AND -filter:replies'
            elif not config.include_retweets and config.include_replies:
                logger.debug("Not including retweets.")
                search_keyword = f'{search_keyword} -filter:retweets'
            elif not config.include_replies and config.include_retweets:
                logger.debug("Not including replies.")
                search_keyword = f'{search_keyword} -filter:replies'
            else:
                logger.debug("No retweet or reply filters added to search keyword.")
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


def check_tweet(logger, api, tweet):
    try:
        lowercase_tweet_text = _get_tweet_text(logger, tweet)
        # check if username has any banned user words in it (set in config.banned_user_words)
        if config.banned_username_words:
            if any(banned_user_word.lower() in tweet.user.screen_name.lower() for banned_user_word in
                   config.banned_username_words):
                logger.info("Banned user word found in username. Skipping tweet.")
                return False
        # check if tweet text has any banned words in it (set in config.banned_words)
        if config.banned_tweet_words:
            if any(banned_word.lower() in lowercase_tweet_text for banned_word in config.banned_tweet_words):
                logger.info("Banned word found in tweet. Skipping tweet.")
                return False
        # workaround to check if tweet has already been retweeted or liked
        # placed this code block after banned username/tweet words to save an api call if banned words found first
        status = api.get_status(tweet.id)
        # check if tweet has already been liked
        if status.favorited:
            logger.info("Tweet already liked. Skipping tweet.")
            return False
        # check if tweet has already been retweeted
        if status.retweeted:
            logger.info("Tweet already retweeted. Skipping tweet.")
            return False
        logger.debug("Found tweet that does not contain banned users, banned words, or already liked/retweeted.")
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
    actions_ran = {"retweet": False, "like": False, "follow": False, "comment": False, "tag": False,
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
            max_following = _get_random_max_following(logger)
            if len(following) > max_following:
                _unfollow_mode(logger, api, following)
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


def _get_random_max_following(logger):
    random_max_following = random.randint(config.max_following[0], config.max_following[1])
    logger.debug(f'Random max following: {random_max_following}')
    return random_max_following


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


def _get_tweet_hashtags(logger, tweet):
    hashtags = set()
    lowercase_tweet_text = _get_tweet_text(logger, tweet)
    for word in lowercase_tweet_text.split():
        if word.startswith("#"):
            hashtags.add(word)
    if hashtags:
        hashtags_string = ' '.join(hashtags)
        logger.debug(f'Hashtags found in tweet: {hashtags_string}')
        return hashtags_string
    else:
        logger.debug("No hashtags found in tweet.")
        return False


def _unfollow_mode(logger, api, following):
    try:
        total_to_unfollow = random.randint(config.unfollow_range[0], config.unfollow_range[1])
        target_following = len(following) - total_to_unfollow
        logger.info("--------------------------------------------------")
        logger.info("Starting unfollow mode...")
        logger.info(f'Unfollowing {total_to_unfollow} users.')
        logger.info("--------------------------------------------------")
        _random_sleep(logger, config.sleep_unfollow_mode[0], config.sleep_unfollow_mode[1])
        while len(following) > target_following:
            unfollow = _unfollow(logger, api, following.pop())
            if not unfollow:
                logger.warning("Problem unfollowing. Skipping user.")
            following = _get_following(logger, api)
            unfollow_remaining = len(following) - total_to_unfollow
            logger.info(f'{unfollow_remaining} user(s) remaining to unfollow.')
        logger.info("Unfollow mode completed.")
        _random_sleep(logger, config.sleep_unfollow_mode[0], config.sleep_unfollow_mode[1])
    except Exception as e:
        logger.warning(f'_unfollow_mode_error: {e}')
        logger.warning(f'Exiting unfollow mode.')
        return False


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
        # generate and build comment based off config.py settings
        comment = _generate_text(logger)
        if config.include_hashtags:
            hashtags = _get_tweet_hashtags(logger, tweet)
            if hashtags:
                comment = f'{comment} {hashtags}'
        if tag:
            tag_username = random.choice(config.tag_friends)
            comment = f'@{tag_username} {comment}'

        api.update_status(status=comment, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
        logger.info(f'Commented: {comment}')
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
        follower_ids = []
        for user in tweepy.Cursor(api.friends_ids, screen_name=config.username, count=5000).items():
            follower_ids.append(user)
        logger.info(f'Current following: {len(follower_ids)}')
        _random_sleep(logger, config.sleep_per_action[0], config.sleep_per_action[1])
        return follower_ids
    except tweepy.TweepError as e:
        return _tweepy_error_handler(logger, e)
    except Exception as e:
        logger.error(f'_get_following error: {e}')
        return False


def _unfollow(logger, api, user_id):
    try:
        username = api.get_user(user_id).screen_name
        api.destroy_friendship(username)
        logger.info(f'Unfollowed: @{username}')
        _random_sleep(logger, config.sleep_per_unfollow[0], config.sleep_per_unfollow[1])
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
        reply = random.choice(config.comments) + random.choice(config.comment_punctuation)
        capitalization = random.choice(["original", "upper", "lower"])

        if capitalization == "upper":
            reply = reply.upper()
        elif capitalization == "lower":
            reply = reply.lower()
        logger.debug(f'Text generated: {reply}')
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
        raise Exception(f'Terminated because account is probably banned or limited.')
    elif tweep_error.api_code == 261:
        raise Exception(f'Terminated because app is probably limited.')
    return False
