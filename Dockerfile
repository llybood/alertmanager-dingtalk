FROM python:3.11.0-alpine
COPY . /app/alertmanager-dingtalk/
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk update && apk add --no-cache tzdata bash bash-completion && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone
WORKDIR /app/alertmanager-dingtalk
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt 
CMD ["python","server.py"]
EXPOSE 8111
