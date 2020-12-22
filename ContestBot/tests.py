import pytest
import tweepy
from itertools import product
import ContestBot
import config

# tweet a variety of test tweets on an account and use them for tests

def test_config():
    assert config.username
    assert config.consumer_key and config.consumer_key != ""
    assert config.consumer_secret and config.consumer_secret != ""
    assert config.token and config.token != ""
    assert config.token_secret and config.token_secret != ""
    assert type(config.retweet) == bool
    assert type(config.like) == bool
    assert type(config.follow) == bool
    assert type(config.comment) == bool
    assert type(config.dm) == bool
    assert config.count >= 0
    assert config.sleep_randomizer >= 0
    assert config.tag_handles
    assert config.replies
    assert config.punctuation
    assert config.contest_keywords
    assert config.retweet_keywords
    assert config.like_keywords
    assert config.follow_keywords
    assert config.comment_keywords
    assert config.tag_keywords
    assert config.dm_keywords


@pytest.fixture()
def api():
    return ContestBot.authenticate()


# def test_authenticate():
#     api = ContestBot.authenticate()
#     assert api.verify_credentials()


def test_get_tweets(api):
    tweets = ContestBot.get_tweets(api)
    assert type(tweets) is tweepy.SearchResults
    assert len(tweets) > 0


def test_check_tweet():
    valid_tweet = "This is a test sweepstakes tweet. Like/rt this tweet. Follow and mention 5 friends to enter."
    invalid_tweet = "Download this app."
    assert ContestBot.check_tweet(valid_tweet)
    assert not ContestBot.check_tweet(invalid_tweet)


def test_find_actions():
    all_actions_tweet = "This is a test sweepstakes tweet. Like/rt this tweet. Follow and mention 5 friends to enter. Dm to win."
    some_actions_tweet = "Like and follow to enter contest."
    no_actions_tweet = "Hello World"
    assert ContestBot._find_actions(all_actions_tweet) == {"retweet": True, "like": True, "follow": True,
                                                           "comment": True, "tag": True, "dm": True}
    assert ContestBot._find_actions(some_actions_tweet) == {"retweet": False, "like": True, "follow": True,
                                                            "comment": False, "tag": True, "dm": False}
    assert ContestBot._find_actions(no_actions_tweet) == {"retweet": False, "like": False, "follow": False,
                                                          "comment": False, "tag": False, "dm": False}


# def test_perform_actions(api):
#     # finish this once I find a test tweet to hard code.
#     assert ContestBot.perform_actions(api, tweet,
#                                       {"retweet": True, "like": True, "follow": True, "comment": True, "tag": True,
#                                        "dm": True})


def test_random_sleep():
    assert 0 <= ContestBot._random_sleep() <= config.sleep_randomizer


def test_generate_text():
    generated_reply = ContestBot.generate_text()
    permutations = []

    # generate all possible uppercase, lowercase, and original permutations of config.replies + config.punctuation
    for item in product(config.replies, config.punctuation):
        original_reply = ''.join(item)
        upper_reply = original_reply.upper()
        lower_reply = original_reply.lower()
        permutations.extend([original_reply, upper_reply, lower_reply])

    assert generated_reply in permutations
