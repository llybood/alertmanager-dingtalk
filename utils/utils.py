#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/12 13:58
# @Author  : llybood

import re
import datetime
import time


def validate_escalation_time(escalation_time):
    """
    Check the escalation rule pending time adjustment format

    :param escalation_time: pending in the escalation rule in the global configuration file
    
    """
    pattern = re.compile(r'^[0-9]+(h|hours|s|seconds|m|minutes)*$')
    if not pattern.match(str(escalation_time)):
        raise ValueError("Unsupported escalation time format,Must be an integer followed by the time, minutes or secondsmust be end with h or hours, m or minutes, s or seconds")

def escalation_time_to_seconds(escalation_time):
    """
    Convert the time format in the escalation rule to seconds
    
    :param escalation_time: pending in the escalation rule in the global configuration file
    :return:
    """
    pattern = re.compile(r'^([0-9]+)(h|hours|s|seconds|m|minutes)*$')
    value = pattern.match(str(escalation_time)).group(1)
    unit  = pattern.match(str(escalation_time)).group(2)
    if unit == "s" or unit == "seconds":
       return value
    elif unit == "m" or unit == "minutes":
       return int(int(value) * 60)
    elif unit == "h" or unit == "hours":
       return int(int(value) * 3600)
    else:
       return int(value)
    
def get_utc_timestamp(utc_time):
    utc_time = time.strptime(utc_time, "%Y-%m-%dT%H:%M:%S.%f%z")
    return int(time.mktime(utc_time))

def get_now_utc_timestamp():
    return int(time.mktime(datetime.datetime.utcnow().utctimetuple()))

def get_diff_timestamp(utc_time):
    """
    Get the timestamp difference between the given UTC time and the current UTC time
    """
    utc_timestamp = get_utc_timestamp(utc_time)
    now_timestamp = get_now_utc_timestamp()
    return int(now_timestamp - utc_timestamp)

def utc_to_local(utc_time):
    utc_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    utc_time = datetime.datetime.strptime(utc_time, utc_format)
    local_time = utc_time + datetime.timedelta(hours=8)
    return datetime.datetime.strftime(local_time ,'%Y-%m-%d %H:%M:%S')
