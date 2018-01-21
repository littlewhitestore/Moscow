# *-* coding:utf-8 *-*

import datetime
import random
import time

xiaobaidian_epoch = 1311557400000L
datacenter_id_bits = 5L
worker_id_bits = 5L
sequence_id_bits = 12L
max_datacenter_id = 1 << datacenter_id_bits
max_worker_id = 1 << worker_id_bits
max_sequence_id = 1 << sequence_id_bits
max_timestamp = 1 << (64L - datacenter_id_bits - worker_id_bits - sequence_id_bits)

def make_snowflake(timestamp_ms, datacenter_id, worker_id, sequence_id, xiaobaidian_epoch=xiaobaidian_epoch):
    sid = ((int(timestamp_ms) - xiaobaidian_epoch) % max_timestamp) << datacenter_id_bits << worker_id_bits << sequence_id_bits
    sid += (datacenter_id % max_datacenter_id) << worker_id_bits << sequence_id_bits
    sid += (worker_id % max_worker_id) << sequence_id_bits
    sid += sequence_id % max_sequence_id
    return sid

def melt(snowflake_id, xiaobaidian_epoch=xiaobaidian_epoch):
    sequence_id = snowflake_id & (max_sequence_id - 1)
    worker_id = (snowflake_id >> sequence_id_bits) & (max_worker_id - 1)
    datacenter_id = (snowflake_id >> sequence_id_bits >> worker_id_bits) & (max_datacenter_id - 1)
    timestamp_ms = snowflake_id >> sequence_id_bits >> worker_id_bits >> datacenter_id_bits
    timestamp_ms += xiaobaidian_epoch
    return (timestamp_ms, int(datacenter_id), int(worker_id), int(sequence_id))

def local_datetime(timestamp_ms):
    return datetime.datetime.fromtimestamp(timestamp_ms / 1000.)

def sn():
    t0 = int(time.time() * 1000)
    p1 = random.randint(1, 32)
    p2 = random.randint(1, 32)
    p3 = random.randint(1, 4096)
    sn = make_snowflake(t0, p1, p2, p3)
    return sn
