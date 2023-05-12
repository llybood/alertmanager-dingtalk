#!/usr/local/python381/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/11/1 10:58
# @Author  : llybood

import re
import datetime
import time

def validate_escalation_time(escalation_time):
    pattern = re.compile(r'^[0-9]+(h|hours|s|seconds|m|minutes)*$')
    if not pattern.match(str(escalation_time)):
        raise ValueError("Unsupported alarm escalation time format,Must be an integer followed by the time, minutes or secondsmust be end with h or hours, m or minutes, s or seconds")

def escalation_time_to_seconds(escalation_time):
    """
    升级告警时间统一转换成秒
    :param escalation_time: 升级告警时间
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
    """
    获取给定的UTC时间的时间戳
    :param utc_time: UTC时间
    :return:
    """
    utc_time = time.strptime(utc_time, "%Y-%m-%dT%H:%M:%S.%f%z")
    return int(time.mktime(utc_time))

def get_now_utc_timestamp():
    """
    获取当前时间的UTC时间戳
    :return:
    """
    return int(time.mktime(datetime.datetime.utcnow().utctimetuple()))

def get_diff_timestamp(utc_time):
    """
    获取给定的UTC时间与当前的UTC时间的时间戳之差
    :param utc_time: UTC时间
    :return:
    """
    utc_timestamp = get_utc_timestamp(utc_time)
    now_timestamp = get_now_utc_timestamp()
    return int(now_timestamp - utc_timestamp)

def utc_to_local(utc_time):
    """
    UTC时间转换成本地时间
    :param utc_time: UTC时间
    :return:
    """
    utc_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    utc_time = datetime.datetime.strptime(utc_time, utc_format)
    local_time = utc_time + datetime.timedelta(hours=8)
    return datetime.datetime.strftime(local_time ,'%Y-%m-%d %H:%M:%S')
