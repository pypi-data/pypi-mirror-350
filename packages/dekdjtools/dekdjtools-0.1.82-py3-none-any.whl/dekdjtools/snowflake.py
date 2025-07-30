import time
import logging
import datetime
from django.utils import timezone
from django.conf import settings
from dektools.time import TZ_UTC


class SnowflakeException(Exception):
    pass


class SnowflakeWorkerException(SnowflakeException):
    pass


class SnowflakeBackwardsException(SnowflakeException):
    pass


class SnowflakeGenerator:
    STEP_THRESHOLD_MAX_AMOUNT = 100  # 时钟回拨 个数
    STEP_THRESHOLD_MS = 128 * 2  # 时钟回拨 毫秒 https://docs.ntpsec.org/latest/clock.html
    EPOCH_TIMESTAMP = int(datetime.datetime(2022, 4, 11, 17, 15, 46).replace(tzinfo=TZ_UTC).timestamp() * 1000)
    END_TIMESTAMP = int(datetime.datetime(3022, 4, 11, 17, 15, 46).replace(tzinfo=TZ_UTC).timestamp() * 1000)

    BITS = ['dynamic', 15, 12]
    MAX_VALUE = 2 ** sum(BITS[1:]) - 1 + (END_TIMESTAMP - EPOCH_TIMESTAMP) * 2 ** sum(BITS[1:])
    MAX_VALUE_WORKER = 2 ** BITS[1] - 1

    @classmethod
    def new_instance(cls):
        return cls(int(settings.DEKDJTOOLS_SNOWFLAKE_INSTANCE))

    def __init__(self, worker):
        self.worker = worker & self.MAX_VALUE_WORKER
        if self.worker != worker:
            raise SnowflakeWorkerException('Worker wrong! %d > %d' % (worker, self.MAX_VALUE_WORKER))
        self.last_timestamp = self.EPOCH_TIMESTAMP
        self.sequence = 0
        self.sequence_overload = 0
        self.errors = 0
        self.generated_ids = 0
        self.step_threshold_list = []
        self.step_threshold_map = {}

    def save_step_threshold(self):
        if self.last_timestamp not in self.step_threshold_map:
            index = len(self.step_threshold_list)
            for i, ts in enumerate(reversed(self.step_threshold_list)):
                if self.last_timestamp > ts:
                    index = index - i - 1
                    break
            self.step_threshold_list.insert(index, self.last_timestamp)
        self.step_threshold_map[self.last_timestamp] = max(
            self.step_threshold_map.get(self.last_timestamp, 0),
            self.sequence
        )
        while len(self.step_threshold_list) > self.STEP_THRESHOLD_MAX_AMOUNT:
            if self.last_timestamp - self.step_threshold_list[0] > self.STEP_THRESHOLD_MS:
                ts = self.step_threshold_list.pop(0)
                del self.step_threshold_map[ts]
            else:
                break

    def load_step_threshold(self, curr_time):
        if not self.step_threshold_list:
            return False
        if self.step_threshold_list[0] > curr_time:
            return False
        sequence = self.step_threshold_map.get(curr_time, None)
        self.sequence = sequence if sequence is not None else 0
        self.last_timestamp = curr_time
        return True

    def get_next_id(self):
        curr_time = int(timezone.now().timestamp() * 1000)

        if curr_time < self.last_timestamp:
            if not self.load_step_threshold(curr_time):
                # stop handling requests til we've caught back up
                self.errors += 1
                raise SnowflakeBackwardsException('Clock went backwards! %d < %d' % (curr_time, self.last_timestamp))

        if curr_time > self.last_timestamp:
            self.sequence = 0
            self.last_timestamp = curr_time

        self.sequence += 1

        if self.sequence >= 2 ** self.BITS[2]:
            # the sequence is overload, just wait to next sequence
            logging.warning('The sequence has been overload')
            self.sequence_overload += 1
            time.sleep(0.001)
            return self.get_next_id()

        generated_id = ((curr_time - self.EPOCH_TIMESTAMP) << (self.BITS[1] + self.BITS[2])) \
                       | (self.worker << self.BITS[2]) \
                       | self.sequence

        self.generated_ids += 1
        self.save_step_threshold()
        return generated_id

    @property
    def stats(self):
        return {
            'worker': self.worker,
            'timestamp': int(timezone.now().timestamp() * 1000),  # current timestamp for this worker
            'last_timestamp': self.last_timestamp,  # the last timestamp that generated ID on
            'sequence': self.sequence,  # the sequence number for last timestamp
            'sequence_overload': self.sequence_overload,  # the number of times that the sequence is overflow
            'errors': self.errors,  # the number of times that clock went backward
        }


snowflake_generator = SnowflakeGenerator.new_instance()
