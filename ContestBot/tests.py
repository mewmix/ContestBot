import pytest
from itertools import product
import ContestBot
import config


def test_generate_reply():
    generated_reply = ContestBot.generate_reply()
    permutations = []

    # generate all possible uppercase, lowercase, and original permutations of config.replies + config.punctuation
    for item in product(config.replies, config.punctuation):
        original_reply = ''.join(item)
        upper_reply = original_reply.upper()
        lower_reply = original_reply.lower()
        permutations.extend([original_reply, upper_reply, lower_reply])

    assert generated_reply in permutations
