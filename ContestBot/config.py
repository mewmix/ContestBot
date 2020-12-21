# LOGIN
consumer_key = ""
consumer_secret = ""
token = ""
token_secret = ""

# SLEEP SETTINGS
sleep_minimum = 0  # lower bound of sleep after each action
sleep_maximum = 0  # upper bound of sleep after each action

# REPLY SETTINGS
tag_handles = ["pluggrr", "cheapprr", "deallrr"]

replies = ["Entering the giveaway", "I really want to win", "Please pick me", "Please choose me", "Done", "Entered",
           "Finished", "Pls pick me", "Pls choose me", "Me", "Me me", "Me me me", "Pls", "Plss", "Plsss", "Please",
           "Pleasee", "Pleaseee", "Omg pls", "Omg please pick me", "Omg pls pick me", "Omg pls choose me",
           "Omg please choose me", "Ily please choose me", "Ily pls choose me", "Ily please pick me", "Ily pls pick me",
           "Let me win", "Pls let me win", "Omg let me win", "This would change my life", "Pick me", "Pick me pick me",
           "Pick me pick me pick me"]

punctuation = ["", "!", "!!", "!!!", "!!!!", "!!!!!", "!!!!!!", ".", "..", "...", "....", ".....", "......"]

# RATE LIMIT SLEEPS (only value that should be changed is SLEEP_RANDOMIZER, unless twitter rate limits change)
MAX_FOLLOWING = 2000
SLEEP_RANDOMIZER = 5   # max limit of random time that will be added to each sleep, set to 0 for no randomization
STATUS_SLEEP = 36  # 300 comments/retweets per 3 hours
LIKE_SLEEP = 86.4  # 1000 likes per 24 hours
FOLLOW_SLEEP = 216  # 400 follows per 24 hours
DM_SLEEP = 86.4  # 1000 dms per 24 hours

# KEYWORDS
contest_keywords = ["giveaway", "contest", "sweepstakes", "to win"]
retweet_keywords = ["rt", "retweet", "share"]
like_keywords = ["like", "favorite", "fav"]
follow_keywords = ["follow"]
comment_keywords = ["reply", "comment"]
tag_keywords = ["tag", "mention"]
dm_keywords = ["message", "dm"]
banned_users = []
banned_words = ["join", "download"]
