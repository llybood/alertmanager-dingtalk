# alertmanager-dingtalk
## 简介
该项目是基于高性能python框架sanic实现的alertmanager告警组件.目前发现网上很多基于alertmanager的告警组件都不支持告警通知升级功能,所以基于python开发了本项目。目前支持以下功能
* 钉钉告警多通道配置
* 告警通知升级
* 自定义消息模板

## 快速开始
### 直接部署
1. 运行环境
> 需要安装Python3,建议Python版本在3.8及以上。

2. 项目代码克隆
```
git clone https://github.com/llybood/alertmanager-dingtalk.git
```
> 或在**Release**直接手动下载源码。

3. 安装依赖
```
cd alertmanager-dingtalk/
pip3 install -r requirements.txt
```
4. 启动服务
```
python3 server.py
# 后台启动
nohup python3 server.py &
```
### docker-compose部署
1. 项目代码克隆
```
git clone https://github.com/llybood/alertmanager-dingtalk.git
```
> 或在**Release**直接下载源码。
2. 启动服务
```
docker-compose up -d
```
### 消息发送url
```
# 发送钉钉告警
http://IP:8111/media/dingtalk/{告警通道名称}/send
#示例:
http://192.168.229.121:8111/media/dingtalk/webhook1/send
# 发送钉钉告警,并使用告警通知升级规则
http://IP:8111/media/dingtalk/{告警通道名称}/send?escalation={告警升级规则名称}
#示例:
http://192.168.229.121:8111/media/dingtalk/webhook1/send?escalation=test
```
## 配置
> 项目配置文件为项目根目录下的config/config.yaml
### 服务端配置
```
server:
  listen: 0.0.0.0   # 服务监听地址,默认为0.0.0.0
  port: 8111        # 服务监听端口,默认为8111
  workers: 2        # 服务工作进程数量,默认为2
  access_log: False # 是否开启访问日志,默认关闭,不建议打开,因为默认会记录告警日志
```
### 告警通道配置
```
media: 
  dingtalk:
    channels:
      # 告警通道配置
      webhook:      # 告警通道名称,名称可以自定义修改
        url: https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx   # 钉钉机器人的webhook地址
      webhook1:
        url: https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        secret: SECxxxxxxxxxxxxxxxxxxxxxxxx         # 钉钉机器人的加签信息
      webhook2:
        url: https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        secret: SECxxxxxxxxxxxxxxxxxxxxxxxx         
        at_mobiles: ["XXXXXXXXXXX","XXXXXXXXXXX"]   # 需要@群成员的手机号码
      webhook3: 
        url: https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        secret: SECxxxxxxxxxxxxxxxxxxxxxxxx         
        is_at_all: True                             # 是否@所有人
```
> 以上内容可以根据自己的情况进行配置,需要几个通道就配置几个通道,其他不使用通道可以删除。
### 告警升级规则配置
```
rules:
  # 告警升级规则
  escalation:
    test:                  # 告警升级规则名称,可以自定义修改
      step_1:              # 告警升级规则步骤名称,可以自定义修改
        media: dingtalk    # 告警媒介,目前只支持dingtalk,必填
        channel: webhook1  # 告警通道,这里需要填写告警通道中的告警通道名称,必填
        pending: 1h        # 告警通知升级触发时间,目前支持s/seconds,m/minutes,h/hours写法,比如15m/15minutes,3600s/3600seconds等,告警持续时间大于等于该时间,触发该规则,必填
      step_2:
        media: dingtalk
        channel: webhook2
        pending: 2h
      step_3:
        media: dingtalk
        channel: webhook3
        pending: 3h
```
> 以上内容是配置的test告警通知升级规则中的3个步骤。可以根据情况配置多个告警规则,以不同的告警升级规则名称命名即可,告警升级规则下最低需要1个步骤。
### 消息模板配置
> 模板配置文件为项目根目录下的template/template.tmpl
```
{% set alertNum = alerts.alerts|selectattr("status", "equalto", "firing") | list | length %}
{% if alertNum != 0 %}
### **<font color=red>故障告警通知</font>**
{% if alerts.escalation %}
**<font color=red>告警持续时间过长,触发升级策略,通知相关负责人,请及时处理</font>**
{% endif %}
{% endif %}
{% for alert in alerts.alerts|selectattr("status", "equalto", "firing") %}
{% if alertNum != 1 %}
* **<font color=blue>告警{{ loop.index }}</font>**
{% endif %}
**故障名称**: {{ alert.labels.alertname }}

**故障级别**: {{ alert.labels.severity }}

**故障时间**: {{ alert.startsAt | utc_to_local }}

**故障描述**: {{ alert.annotations.description }}
{% endfor %}

{% set resolvedNum = alerts.alerts|selectattr("status", "equalto", "resolved") | list | length %}
{% if resolvedNum != 0 %}
### **<font color=green>故障恢复通知</font>**
{% endif %}
{% for alert in alerts.alerts|selectattr("status", "equalto", "resolved") %}
{% if resolvedNum != 1 %}
* **<font color=blue>恢复详情{{ loop.index }}</font>**
{% endif %}
**故障类型**: {{ alert.labels.alertname }}

**故障级别**: {{ alert.labels.severity }}

**故障时间**: {{ alert.startsAt | utc_to_local }}

**恢复时间**: {{ alert.endsAt | utc_to_local }}

**故障描述**: {{ alert.annotations.description }}
{% endfor %}

```
> 模板文件使用jinja2模板,可以根据自己的情况进行模板的修改,其中alerts为传入的alertmanager格式的字典对象,alerts.alerts为告警消息列表.
如果该消息触发了告警升级规则,则注入alerts.escalation键值对,以便于进行告警消息模板的格式化输出显示。

* alertmanager格式的字典对象格式如下
```
{
	"receiver": "webhook",
	"status": "firing",
	"alerts": [{
		"status": "firing",
		"labels": {
			"alertname": "KubeSchedulerDown",
			"endpoint": "https-metrics",
			"instance": "192.168.229.131:10259",
			"job": "kube-scheduler",
			"namespace": "kube-system",
			"prometheus": "monitoring/k8s",
			"service": "kube-scheduler",
			"severity": "critical"
		},
		"annotations": {
			"description": "KubeScheduler has disappeared from Prometheus target discovery.",
			"runbook_url": "https://github.com/prometheus-operator/kube-prometheus/wiki/kubeschedulerdown",
			"summary": "Target disappeared from Prometheus target discovery."
		},
		"startsAt": "2023-05-16T02:31:03.323Z",
		"endsAt": "0001-01-01T00:00:00Z",
		"generatorURL": "http://prometheus-k8s-0:9090/graph?g0.expr=up%7Bjob%3D%22kube-scheduler%22%7D+%3D%3D+0&g0.tab=1",
		"fingerprint": "07be849af6320674"
	}, {
		"status": "firing",
		"labels": {
			"alertname": "KubeSchedulerDown",
			"endpoint": "https-metrics",
			"instance": "192.168.229.132:10259",
			"job": "kube-scheduler",
			"namespace": "kube-system",
			"prometheus": "monitoring/k8s",
			"service": "kube-scheduler",
			"severity": "critical"
		},
		"annotations": {
			"description": "KubeScheduler has disappeared from Prometheus target discovery.",
			"runbook_url": "https://github.com/prometheus-operator/kube-prometheus/wiki/kubeschedulerdown",
			"summary": "Target disappeared from Prometheus target discovery."
		},
		"startsAt": "2023-05-16T02:31:03.323Z",
		"endsAt": "0001-01-01T00:00:00Z",
		"generatorURL": "http://prometheus-k8s-0:9090/graph?g0.expr=up%7Bjob%3D%22kube-scheduler%22%7D+%3D%3D+0&g0.tab=1",
		"fingerprint": "585228d2499f0ae3"
	}, {
		"status": "firing",
		"labels": {
			"alertname": "KubeSchedulerDown",
			"endpoint": "https-metrics",
			"instance": "192.168.229.133:10259",
			"job": "kube-scheduler",
			"namespace": "kube-system",
			"prometheus": "monitoring/k8s",
			"service": "kube-scheduler",
			"severity": "critical"
		},
		"annotations": {
			"description": "KubeScheduler has disappeared from Prometheus target discovery.",
			"runbook_url": "https://github.com/prometheus-operator/kube-prometheus/wiki/kubeschedulerdown",
			"summary": "Target disappeared from Prometheus target discovery."
		},
		"startsAt": "2023-05-16T02:31:03.323Z",
		"endsAt": "0001-01-01T00:00:00Z",
		"generatorURL": "http://prometheus-k8s-0:9090/graph?g0.expr=up%7Bjob%3D%22kube-scheduler%22%7D+%3D%3D+0&g0.tab=1",
		"fingerprint": "dde611e6d29cd8c2"
	}],
	"groupLabels": {
		"alertname": "KubeSchedulerDown",
		"job": "kube-scheduler"
	},
	"commonLabels": {
		"alertname": "KubeSchedulerDown",
		"endpoint": "https-metrics",
		"job": "kube-scheduler",
		"namespace": "kube-system",
		"prometheus": "monitoring/k8s",
		"service": "kube-scheduler",
		"severity": "critical"
	},
	"commonAnnotations": {
		"description": "KubeScheduler has disappeared from Prometheus target discovery.",
		"runbook_url": "https://github.com/prometheus-operator/kube-prometheus/wiki/kubeschedulerdown",
		"summary": "Target disappeared from Prometheus target discovery."
	},
	"externalURL": "http://alertmanager-main-0:9093",
	"version": "4",
	"groupKey": "{}/{severity='critical'}:{alertname='KubeSchedulerDown', job='kube-scheduler'}",
	"truncatedAlerts": 0
}
```



