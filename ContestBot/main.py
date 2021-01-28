import ContestBot as bot
import config


def main():
    logger = bot.initialize_logger()
    bot.check_config(logger)
    bot.multiply_sleeps(logger)
    api = bot.authenticate(logger)
    search_type = config.search_type
    tweets = bot.get_tweets(logger, api, search_type)
    tweet_num = 0
    success_tweet_num = 0
    total_followed = 0
    total_unfollowed = 0

    while True:
        if tweets:
            for tweet in tweets:
                tweet_num += 1
                logger.info("\n")
                logger.info("--------------------------------------------------")
                logger.info(f'Tweet number: {tweet_num}')
                logger.info(f'Interacted tweets: {success_tweet_num}')
                if success_tweet_num and tweet_num > 1:
                    logger.info(f'Interaction rate: {((success_tweet_num / (tweet_num - 1)) * 100)}%')
                else:
                    logger.info(f'Interaction rate: 0%')
                logger.info(f'Total followed users: {total_followed}')
                logger.info(f'Total unfollowed users: {total_unfollowed}')
                logger.info("--------------------------------------------------")
                tweet_text = bot.check_tweet(logger, api, tweet)
                if tweet_text:
                    actions = bot.find_actions(logger, tweet_text)
                    if actions:
                        completed_actions = bot.perform_actions(logger, api, tweet, actions)
                        if completed_actions:
                            # check if perform_actions just finished _unfollow_mode (returns total_unfollowed int)
                            if isinstance(completed_actions, int) and completed_actions > 0:
                                total_unfollowed = total_unfollowed + completed_actions
                                tweets.clear()
                                continue
                            # perform_actions successfully performed follow action on tweet
                            elif completed_actions.get("follow"):
                                total_followed += 1
                            success_tweet_num += 1
                tweets.remove(tweet)
        else:
            search_type = bot.get_next_search_type(logger, search_type)
            tweets = bot.get_tweets(logger, api, search_type)


if __name__ == '__main__':
    main()
