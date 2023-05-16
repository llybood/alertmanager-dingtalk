#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/12 10:58
# @Author  : llybood

import collections

from utils.utils import get_diff_timestamp
from utils.utils import get_utc_timestamp
from utils.utils import escalation_time_to_seconds
from utils.utils import utc_to_local
from template.template import MessageTemplate
 

class AlertManagerMessage:
    """Handle alert information in alertmanager format."""
    
    def __init__(self, alerts):
        """
        :param alerts: Alert information in alertmanager format
        """
        self.alerts = alerts

    def get_alerts_start_time(self):
        """
        Get the trigger time of alerts.
        a group of alerts may have multiple alarms, get the earliest trigger time
        """
        start_time_dict = {}
        for alert in self.alerts.get("alerts"):
            start_time = alert.get("startsAt")
            start_timestamp = get_utc_timestamp(start_time)
            start_time_dict[start_time] = start_timestamp
        order_start_time = sorted(start_time_dict.items(), key=lambda x:x[1])
        alerts_start_time = order_start_time[0][0]
        return alerts_start_time

    def get_alerts_duration_time(self):
        """ Get the alerts duration in seconds """
        return get_diff_timestamp(self.get_alerts_start_time())

    def get_alerts_escalation_rule(self, escalation_rule):
        """
        Get the alerts escalation rules, return None if it is empty

        The alerts, alerts duration time and the name of the rule in the global escalation rule,pending form an ordered dictionary.
        Then sorted according to pending. The previous one of the alerts is the triggered escalation rule. 
        If the subscript of the alerts index is 0, it means that it has not been triggered any escalation rules.

        """
        alerts_escalation_status = collections.OrderedDict()
        alerts_escalation_status["alerts"] = self.get_alerts_duration_time()
        for k,v in escalation_rule.items():
            alerts_escalation_status[k] = escalation_time_to_seconds(v["pending"])
        alerts_escalation_status = dict(sorted(alerts_escalation_status.items(), key=lambda x:x[1]))
        alerts_with_escalation_list = []
        for k,v in alerts_escalation_status.items():
            alerts_with_escalation_list.append(k)
        alerts_index = alerts_with_escalation_list.index("alerts")
        if alerts_index == 0:
            return None
        else:
            alerts_escalation_rule_index = int(alerts_index - 1)
            alerts_escalation_rule = alerts_with_escalation_list[alerts_escalation_rule_index]
        return alerts_escalation_rule

    def format_alerts_to_markdown(self):
        template = MessageTemplate("template").get_template()
        return template.render(alerts=self.alerts)
