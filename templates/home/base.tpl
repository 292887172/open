{% load staticfiles %}
<!DOCTYPE html>
<html>

<head lang="en">
    <meta charset="UTF-8"/>
    <meta name="viewport"
          content="width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no"/>
    <meta name="Keywords" content="53iq智能，开放平台,超级APP,互联互通,硬件开发，物联开发，物联网，智能硬件开发，智能家居开发，健康设备开发，开发者中心"/>
    <meta name="Description" content="中国物联网与智能硬件行业领先的技术平台，为硬件厂商和开发者提供智能产品接入和推广的快捷通道，智能开发从53iq开始。"/>
    <title>{% block title %}{% endblock %} 厨房智能平台</title>
    <link rel="shortcut icon" href="{% static 'image/53iq.ico' %}"/>
    <link rel="stylesheet" href="{% static 'bootstrap/bootstrap.css' %}"/>
    <link rel="stylesheet" href="{% static 'css/home/main.css' %}"/>
    <link rel="stylesheet" href="{% static 'common/css/simple-line-icons.css' %}"/>
    {% block style %}
        <style>

        </style>
    {% endblock %}
    <script>
        var _hmt = _hmt || [];
        (function () {
            var hm = document.createElement("script");
            hm.src = "//hm.baidu.com/hm.js?9088d602c7fd9fd4bfb8f3472bd734b7";
            var s = document.getElementsByTagName("script")[0];
            s.parentNode.insertBefore(hm, s);
        })();
    </script>

</head>
<body>
<div class="header">
    <div class="wrapper">
        <h1 class="logo"><a href="{% url 'home' %}"><img src="{% static 'image/home/logo-dev.png' %}" height="40"/></a>
        </h1>
        {% block menu %}

        {% endblock %}

        <div class="user" style="position: relative">
            <p style="position: absolute;top: 44px;font-size: 16px;right: 130px;">电话：0571-88868856</p>


        </div>
    <div class="sign_out">
        {% if user.account_id %}
                <!-- 登录 -->
                <a href="#" onclick="$('.login_out').width($(this).width()+46);$('.login_out').toggle();"
                       style="text-decoration: none;">{{ user.account_id }}<span class="corner"></span></a>
                    <div onmouseout="$('.login_out').hide()" style="position: absolute">
                         <a rel="nofollow" href="/center?" class="login_out"
                       onmouseover="$('.login_out').show()" style="width: 120px; cursor: pointer; display: none;">帐号管理</a>
                       {% if user.developer.developer_id %}
                               <a rel="nofollow" onmouseover="$('.login_out').show()" class="login_out" href="/center/checklist"
                           style="width: 120px; cursor: pointer; display: none;">通知</a>
                       {% else %}
                            <a rel="nofollow" onmouseover="$('.login_out').show()" class="login_out" href="#"
                           style="width: 120px; cursor: pointer; display: none;">通知</a>
                        {% endif %}
                        <a rel="nofollow" id="modify_pwd_id" onclick="location.href='{% url 'modify_pwd' %}'"
                       onmouseover="$('.login_out').show()" class="login_out"
                       style="width: 120px; cursor: pointer; display: none;">修改密码</a>
                        <a rel="nofollow" id="login_out_id" onclick="location.href='{% url 'logout' %}'"
                       onmouseover="$('.login_out').show()" class="login_out"
                       style="width: 120px; cursor: pointer; display: none;">退出</a>
                    </div>
            {% else %}
                <!-- 登录 -->


                    <a class="user-login" href="{% url 'login' %}">登录</a>

            {% endif %}
    </div>
    </div>
</div>
{% block content %}
    <div class="wrapper mt20 fn-clear">
        <div class="leftSide">
            <div class="box1">
                <!-- 左侧菜单 begin -->

                <div class="menuBox">
                    <h3>文档中心</h3>
                    <ul>
                        <li class="menu-li"><a href="/wiki" target="_blank"><i
                                class="icon-book-open"></i>开发者文档</a></li>
                    </ul>
                </div>
                <div class="menuBox">
                    <h3>调试工具</h3>
                    <ul>
                        <li class="menu-li"><a href="/debug/debug_interface" target="_blank"><i
                                class="icon-wrench"></i>调试接口</a></li>
                        <li class="menu-li"><a href="/debug/debug_device" target="_blank"><i
                                class="icon-compass"></i>调试设备</a></li>
                    </ul>
                </div>
                <div class="menuBox">
                    <h3>下载中心</h3>
                    <ul>
                        <li class="menu-li" onclick="addHover('/sdk',this)"><a href="#"><i
                                class="icon-cloud-download"></i>下载中心</a></li>
                    </ul>
                </div>
                <div class="menuBox">
                    <h3>联系我们</h3>
                    <ul>
                        <li class="menu-li ui-con" onclick="addHover('/contact',this)"><a href="#"><i
                                class="icon-call-out"></i>联系我们</a></li>
                    </ul>
                </div>
            </div>
        </div>
        {% block right %}
        {% endblock %}
    </div>
{% endblock %}

<div class="footer">
    <p><a href="http://www.53iq.com/about" target="_blank">关于53iq</a>
        <a href="/guide">53iq云</a>
        <a href="/guide#contact" onclick="addHover('contact',this)">联系我们</a>
    </p>

    <p>Copyright©{% now 'Y' %} 53iq 版权所有</p>
</div>
<script src="{% static 'js/jquery-1.11.0.min.js' %}"></script>
<script src="{% static 'bootstrap/bootstrap.js' %}"></script>

{% block script %}

{% endblock %}
</body>

</html>