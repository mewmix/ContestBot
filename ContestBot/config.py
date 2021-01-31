# ========================AUTHENTICATION SETTINGS========================
username = ""
consumer_key = ""
consumer_secret = ""
token = ""
token_secret = ""


# ========================TOGGLE FEATURE SETTINGS========================
retweet = True
like = True
follow = True
comment = False  # suggest leaving this off as it triggers an app write limitation fairly quickly
dm = False  # suggest leaving this off as you cannot send DMs to users that don't follow you


# ========================ACTION SETTINGS========================
retweet_keywords = ["rt", "retweet", "-rt", "#rt", "🔁", "rt,", "rt.", "rt!", "rt+", "rt&", "rt-"]
like_keywords = ["like", "favorite", "fav", "❤️"]
follow_keywords = ["follow", "mbf", "flw"]
comment_keywords = ["reply", "comment"]
tag_keywords = ["tag", "mention", "friend"]
dm_keywords = ["message", "dm"]


# ========================SLEEP SETTINGS========================
sleep_multiplier = 1   # multiply all sleeps by this amount, suggested 2 for a week then 1.5, 1
sleep_per_tweet = [180, 240]  # [min, max] random sleeps this time after all actions have been performed on each tweet
sleep_per_action = [45, 60]  # [min, max] random sleeps this time after each action on a tweet such as rt, like, follow
sleep_per_unfollow = [200, 300]  # [min, max] random sleeps this time after each unfollow in ContestBot._unfollow()
sleep_unfollow_mode = [10800, 14400]  # [min, max] random sleeps this time at start and finish of ContestBot._unfollow_mode()


# ========================SEARCH SETTINGS========================
count = 200  # num of tweets to search for each search_keyword per iteration of the infinite main loop
search_type = "mixed"  # "mixed", "recent", or "popular". Can also use ContestBot.get_next_search_mode() to iterate modes
search_keywords = ["giveaway", "contest", "sweepstake"]
banned_username_words = ["bot", "bts", "stan", "kpop"]
banned_tweet_words = ["join", "download", "bts", "kpop", "album", "gcash", "subscribe", "answer", "robux", "indonesia", "kyoongcon"]
include_retweets = True  # include in search results. True sometimes results in some duplicate but usually more quality tweets
include_replies = False  # include in search results. Replies are often times NOT contests/giveaways


# ========================FOLLOW/UNFOLLOW SETTINGS========================
max_following = [1900, 1999]  # [min, max] random choice of max_following before ContestBot._unfollow_mode() is triggered, must be less than 2000
unfollow_range = [100, 200]  # [min, max] random choice of users to unfollow in total for a run of ContestBot._unfollow_mode()


# ========================COMMENT SETTINGS========================
include_hashtags = True   # toggle adding all hashtags found in tweet to your comment
tag_friends = ["pluggrr", "cheapprr", "deallrr"]
comments = ["Entering the giveaway", "I really want to win", "Please pick me", "Please choose me", "Done", "Entered",
           "Finished", "Pls pick me", "Pls choose me", "Me", "Me me", "Me me me", "Pls", "Plss", "Plsss", "Please",
           "Pleasee", "Pleaseee", "Omg pls", "Omg please pick me", "Omg pls pick me", "Omg pls choose me",
           "Omg please choose me", "Ily please choose me", "Ily pls choose me", "Ily please pick me", "Ily pls pick me",
           "Let me win", "Pls let me win", "Omg let me win", "This would change my life", "Pick me", "Pick me pick me",
           "Pick me pick me pick me"]
comment_punctuation = ["", "!", "!!", "!!!", "!!!!", "!!!!!", "!!!!!!", ".", "..", "...", "....", ".....", "......"]


# ========================LOGGING SETTINGS========================
level = 2  # 1 for debug, 2 for info, 3 for warning, 4 for error, 5 for critical
file_logs = True  # toggle file logs on/off
