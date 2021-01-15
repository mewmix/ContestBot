import ContestBot as bot
import config


def main():
    logger = bot.initialize_logger()
    bot.check_config(logger)
    api = bot.authenticate(logger)
    search_type = config.search_type
    tweets = bot.get_tweets(logger, api, search_type)
    tweet_num = 0

    while True:
        if tweets:
            for tweet in tweets:
                tweet_num += 1
                logger.info("\n")
                logger.info("--------------------------------------------------")
                logger.info(f'Tweet number: {tweet_num}')
                logger.info("--------------------------------------------------")
                tweet_text = bot.check_tweet(logger, api, tweet)
                if tweet_text:
                    actions = bot.find_actions(logger, tweet_text)
                    if actions:
                        completed_actions = bot.perform_actions(logger, api, tweet, actions)
                        if completed_actions == "unfollow_completed":
                            tweets.clear()
                tweets.remove(tweet)
        else:
            search_type = bot.get_next_search_type(logger, search_type)
            tweets = bot.get_tweets(logger, api, search_type)


if __name__ == '__main__':
    main()
