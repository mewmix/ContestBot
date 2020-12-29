# AUTHENTICATION SETTINGS
username = ""
consumer_key = ""
consumer_secret = ""
token = ""
token_secret = ""

# LOGGING SETTINGS
level = 1  # 1 for debug, 2 for info, 3 for warning, 4 for error, 5 for critical

# TOGGLE FEATURE SETTINGS
retweet = True
like = True
follow = True
comment = True
dm = False  # suggest leaving this off as you cannot send DMs to users that don't follow you

# GENERAL SETTINGS
search_type = "mixed"  # "mixed", "recent", or "popular". Can also use ContestBot.get_next_search_mode to iterate modes
include_retweets = True  # include in search results. True sometimes results in some duplicate but usually more quality tweets
count = 300  # num of tweets to search for each contest_keyword per iteration of the infinite main loop
max_following = 153  # max number of following before it starts FIFO unfollowing a person before each new follow, 2000 is max value

# SLEEP SETTINGS
sleep_per_action = [20, 40]  # [min, max] sleeps this time after each action on a tweet such as rt, like, follow
sleep_per_tweet = [180, 500]  # [min, max] sleeps this time after all actions have been performed on each tweet

# REPLY SETTINGS
tag_handles = ["pluggrr", "cheapprr", "deallrr"]

replies = ["Entering the giveaway", "I really want to win", "Please pick me", "Please choose me", "Done", "Entered",
           "Finished", "Pls pick me", "Pls choose me", "Me", "Me me", "Me me me", "Pls", "Plss", "Plsss", "Please",
           "Pleasee", "Pleaseee", "Omg pls", "Omg please pick me", "Omg pls pick me", "Omg pls choose me",
           "Omg please choose me", "Ily please choose me", "Ily pls choose me", "Ily please pick me", "Ily pls pick me",
           "Let me win", "Pls let me win", "Omg let me win", "This would change my life", "Pick me", "Pick me pick me",
           "Pick me pick me pick me"]

punctuation = ["", "!", "!!", "!!!", "!!!!", "!!!!!", "!!!!!!", ".", "..", "...", "....", ".....", "......"]

# KEYWORD SETTINGS
contest_keywords = ["giveaway", "contest", "sweepstake"]

retweet_keywords = ["rt", "retweet", "-rt", "#rt", "🔁", "rt,", "rt.", "rt!"]
like_keywords = ["like", "favorite", "fav", "❤️"]
follow_keywords = ["follow", "mbf", "flw"]
comment_keywords = ["reply", "comment"]
tag_keywords = ["tag", "mention", "friend"]
dm_keywords = ["message", "dm"]

banned_user_words = ["bot", "bts", "stan", "kpop"]
banned_words = ["join", "download", "bts", "kpop", "album", "gcash", "subscribe", "answer", "robux"]
