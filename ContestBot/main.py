import ContestBot as bot


def main():
    logger = bot.initialize_logger()
    bot.check_config(logger)
    api = bot.authenticate(logger)
    tweets = bot.get_tweets(logger, api)

    while True:
        try:
            if tweets:
                for tweet in tweets:
                    if bot.check_tweet(logger, tweet):
                        actions = bot.find_actions(logger, tweet)
                        if actions:
                            bot.perform_actions(logger, api, tweet, actions)
                    tweets.remove(tweet)
            else:
                tweets = bot.get_tweets(logger, api)
        except Exception as e:
            print(f'main error: {e}')


if __name__ == '__main__':
    main()
