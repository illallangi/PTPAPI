from math import ceil, floor
from time import sleep, time

from loguru import logger


# https://gist.github.com/drocco007/6155452
class TokenBucket(object):
    def __init__(self, capacity, fill_rate):
        """capacity is the maximum tokens in the bucket. fill_rate is the
        rate in tokens/second that the bucket will be refilled."""
        self.capacity = float(capacity)
        self._tokens = 1
        self.fill_rate = float(fill_rate)
        self.timestamp = time()

    def consume(self, block=True):
        """Consume a token from the bucket.
        If there are not enough tokens, sleeps until the
        bucket is replenished.
        """

        if self.tokens < 1:
            deficit = 1 - self._tokens
            delay = ceil(deficit / self.fill_rate)

            logger.info('Sleeping {} seconds', delay)
            sleep(delay)

        logger.trace('Have {} tokens', floor(self._tokens))
        self._tokens -= 1

    @property
    def tokens(self):
        if self._tokens < self.capacity:
            now = time()
            delta = self.fill_rate * (now - self.timestamp)
            self._tokens = min(self.capacity, self._tokens + delta)
            self.timestamp = now
        return self._tokens
