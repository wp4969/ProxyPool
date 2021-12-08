FROM python:3.7-alpine

WORKDIR /

COPY ../ProxyPool .

#替换阿里源
RUN echo "http://mirrors.aliyun.com/alpine/latest-stable/main/" > /etc/apk/repositories && \
    echo "http://mirrors.aliyun.com/alpine/latest-stable/community/" >> /etc/apk/reposi tories

#依赖包
RUN apk add --no-cache python3 python3-dev gcc openssl-dev openssl  libc-dev linux-headers libffi-dev libxml2-dev libxml2 libxslt-dev openssh-client

RUN pip3 install --default-timeout=100 --no-cache-dir --upgrade pip Scrapy

#-r requirements.txt
#ENTRYPOINT ["python"]