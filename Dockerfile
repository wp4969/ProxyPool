FROM python:3.7-alpine

WORKDIR /app

COPY . .

#替换阿里源
RUN echo "http://mirrors.aliyun.com/alpine/latest-stable/main/" > /etc/apk/repositories && \
    echo "http://mirrors.aliyun.com/alpine/latest-stable/community/" >> /etc/apk/reposi tories

RUN apk add --no-cache libxml2-dev libxslt-dev gcc musl-dev && \
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple&& \
apk del gcc musl-dev libxml2-dev

VOLUME ["/app/proxypool/crawlers/private"]

CMD ["supervisord", "-c", "supervisord.conf"]