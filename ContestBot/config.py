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

# RATE LIMIT CONSTANTS (ONLY CHANGE THESE IF TWITTER ADJUSTS THEIR RATE LIMITS)
MAX_FOLLOWING = 2000
TOTAL_ACTIONS_LIMIT_PER_HOUR = 0
RETWEET_LIMIT_PER_HOUR = 0
LIKE_LIMIT_PER_HOUR = 0
FOLLOW_LIMIT_PER_HOUR = 0
COMMENT_LIMIT_PER_HOUR = 0
UNFOLLOW_LIMIT_PER_HOUR = 0
DM_LIMIT_PER_HOUR = 0

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