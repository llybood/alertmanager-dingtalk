#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/12 10:58
# @Author  : llybood

import collections
from jinja2 import Environment, FileSystemLoader

from utils.utils import get_diff_timestamp
from utils.utils import get_utc_timestamp
from utils.utils import escalation_time_to_seconds
from utils.utils import utc_to_local
 

class AlertManagerMessage:
    
    def __init__(self, alerts):
        self.start_time = None
        self.alerts = alerts

    def get_alerts_start_time(self):
        """
        获取alerts的最早触发时间
        一组alerts可能会有多条告警,获取最早的触发时间
        """
        start_time_dict = {}
        for alert in self.alerts.get("alerts"):
            start_time = alert.get("startsAt")
            start_timestamp = get_utc_timestamp(start_time)
            start_time_dict[start_time] = start_timestamp
        order_start_time = sorted(start_time_dict.items(), key=lambda x:x[1])
        return order_start_time[0][0]

    def get_alerts_duration_time(self):
        """
        获取alerts的持续时间
        """
        return get_diff_timestamp(self.get_alerts_start_time())

    def get_alerts_escalation_rule(self, escalation_rule):
        """
        获取alerts告警升级规则,为空则返回None
        """
        alerts_escalation_status = collections.OrderedDict()
        alerts_escalation_status["alerts"] = self.get_alerts_duration_time()
        for k,v in escalation_rule.items():
            alerts_escalation_status[k] = escalation_time_to_seconds(v["pending"])
        alerts_escalation_status = dict(sorted(alerts_escalation_status.items(), key=lambda x:x[1]))
        alerts_escalation_list = []
        for k,v in alerts_escalation_status.items():
            alerts_escalation_list.append(k)
        alerts_index = alerts_escalation_list.index("alerts")
        if alerts_index == 0:
            return None
        else:
            alerts_rule_index = int(alerts_index - 1)
            alerts_rule = alerts_escalation_list[alerts_rule_index]
        return escalation_rule[alerts_rule]

    def format_alerts_to_markdown(self):
        """
        alerts转换成markdown格式
        """
        file_loader = FileSystemLoader('config')
        env = Environment(loader=file_loader)
        env.filters['utc_to_local'] = utc_to_local
        template = env.get_template('template.tmpl')
        return template.render(alerts=self.alerts)
