import ContestBot as bot
import tweepy


def main():
    api = bot.authenticate()
    following = bot.get_following()
    old_times = bot.initialize_times()

    while True:
        tweets = bot.get_tweets()

        for tweet in tweets:
            # check if tweet is a valid (does not contain banned words, banned users, not already liked/retweeted, etc)
            if bot.check_tweet():
                # check tweet and return what actions need to be performed to enter contest
                actions = bot.find_actions(tweet)
                # perform actions and returns updated old_times
                old_times = bot.perform_actions(actions, old_times)




if __name__ == '__main__':
    pass
