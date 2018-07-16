部署
====


域名
-----

* http://open.53iq.com

uwsgi配置文件
-------------

::

    [uwsgi]
    #v1.0
    chdir=/home/project/open
    module=open.wsgi
    env DJANGO_SETTINGS_MODULE=open.settings
    master=True
    pidfile=/tmp/open-master.pid
    socket=0.0.0.0:8003
    # 开启的进程数，推荐值=cpu核心数*2，因为有个叫超线程的东西
    processes=8
    vacuum=True
    max-requests=5000
    daemonize=/var/log/uwsgi-open.log
    # 开启的线程数，在每个进程中再开启的线程，一般2个即可
    threads=2
    # 让uwsgi使用virtualenv运行
    virtualenv=/root/.pythonbrew/venvs/Python-3.4.1/openenv


nginx配置
---------

::

    # 开放平台管理
    server {
    listen 80;
    server_name open.53iq.com;
    access_log /var/log/nginx/open-access.log;
    error_log /var/log/nginx/open-error.log;
    location / {
            uwsgi_pass 127.0.0.1:8003;
            include uwsgi_params;
          }
        location ~ ^/static/ {
                root /home/project/open/;
                #设置缓存过期时间为1天
                expires 24h;
                access_log   off;
             }
        location ~ ^/tcp {
            proxy_pass http://127.0.0.1:9000;
            proxy_redirect off;
         }
    }


运行
----

::

    /root/.pythonbrew/venvs/Python-3.4.1/openenv/bin/uwsgi --emperor /home/project/uwsgi-config/ --daemonize /var/log/uwsgi.log

