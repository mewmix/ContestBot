import random
import config


def generate_reply():
    reply = random.choice(config.replies) + random.choice(config.punctuation)
    capitalization = random.choice(["original", "upper", "lower"])

    if capitalization == "upper":
        return reply.upper()
    elif capitalization == "lower":
        return reply.lower()
    else:
        return reply
