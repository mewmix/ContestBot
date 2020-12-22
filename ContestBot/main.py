import ContestBot as bot


def main():
    try:
        api = bot.authenticate()
        tweets = bot.get_tweets(api)

        while True:
            if tweets:
                for tweet in tweets:
                    if bot.check_tweet(tweet):
                        actions = bot.find_actions()
                        if actions:
                            bot.perform_actions(api, tweet, actions)
                    tweets.remove(tweet)
            else:
                tweets = bot.get_tweets(api)
    except Exception as e:
        print(f'main error: {e}')


if __name__ == '__main__':
    main()
