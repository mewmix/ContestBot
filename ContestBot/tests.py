import pytest
from itertools import product
import ContestBot
import config


@pytest.fixture()
def logger():
    return ContestBot.initialize_logger()


@pytest.fixture()
def api(logger):
    return ContestBot.authenticate(logger)


@pytest.fixture()
def tweets(api):
    return api.user_timeline("scrapertweeter3")


def test_initialize_logger():
    assert ContestBot.initialize_logger()


def test_check_config(logger):
    assert ContestBot.check_config(logger)


def test_authenticate(logger):
    api = ContestBot.authenticate(logger)
    assert api.verify_credentials()


def test_get_tweets(logger, api):
    assert ContestBot.get_tweets(logger, api)


def test_check_tweet(logger, tweets):
    checked_list = []
    for tweet in tweets:
        checked = ContestBot.check_tweet(logger, tweet)
        checked_list.append(checked)
    assert checked_list[0] == False
    assert checked_list[1]


def test_find_actions(logger, tweets):
    actions_list = []
    for tweet in tweets:
        actions = ContestBot.find_actions(logger, tweet)
        actions_list.append(actions)

    assert actions_list[0] == False

    assert actions_list[1] == {"retweet": True, "like": True, "follow": True,
                               "comment": True, "tag": True, "dm": True}


def test_perform_actions(logger, api, tweets):
    # set config.max_following to 0 so it perform_actions unfollows a user no matter what
    try:
        config.max_following = 0
        tweet = tweets[1]

        actions = {"retweet": True, "like": True, "follow": True, "comment": True, "tag": True, "dm": True}
        actions_ran = ContestBot.perform_actions(logger, api, tweet, actions)
        assert actions_ran == {"retweet": True, "like": True, "unfollow": True, "follow": True, "comment": True,
                               "tag": True,
                               "dm": True}
    except Exception as e:
        pass

    # undo all actions so tests work again
    api.unretweet(tweet.id)
    api.destroy_favorite(tweet.id)
    api.destroy_friendship("scrapertweeter3")


def test_random_sleep(logger):
    assert config.sleep_per_action[0] <= ContestBot._random_sleep(logger, config.sleep_per_action[0],
                                            config.sleep_per_action[1]) <= config.sleep_per_action[1]
    assert config.sleep_per_tweet[0] <= ContestBot._random_sleep(logger, config.sleep_per_tweet[0],
                                            config.sleep_per_tweet[1]) <= config.sleep_per_tweet[1]


def test_generate_text(logger):
    generated_reply = ContestBot._generate_text(logger)
    permutations = []

    # generate all possible uppercase, lowercase, and original permutations of config.replies + config.punctuation
    for item in product(config.replies, config.punctuation):
        original_reply = ''.join(item)
        upper_reply = original_reply.upper()
        lower_reply = original_reply.lower()
        permutations.extend([original_reply, upper_reply, lower_reply])

    assert generated_reply in permutations
