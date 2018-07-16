FROM python:3.4.1

COPY requirements.txt /tmp/requirements.txt

RUN apt-get update \
    && apt-get autoremove -y \
    && apt-get purge -y --auto-remove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' >/etc/timezone

RUN pip install -r /tmp/requirements.txt

CMD /bin/bash
