{% load staticfiles %}
<!DOCTYPE html>
<!--[if lt IE 7]>      <html lang="en" class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html lang="en" class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html lang="en" class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html lang="en" class="no-js"> <!--<![endif]-->

<head lang="en">
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no"/>
    <meta name="Keywords" content="53iq智能，开放平台,超级APP,互联互通,硬件开发，物联开发，物联网，智能硬件开发，智能家居开发，健康设备开发，开发者中心"/>
    <meta name="Description" content="中国物联网与智能硬件行业领先的技术平台，为硬件厂商和开发者提供智能产品接入和推广的快捷通道，智能开发从53iq开始。"/>
    <title>{% block title %}{% endblock %} 智能厨房电器方案提供商</title>
    <link rel="shortcut icon" href="{% static 'image/53iq.ico' %}"/>
    <link rel="stylesheet" href="{% static 'bootstrap/bootstrap.css' %}"/>
    <link rel="stylesheet" href="{% static 'css/base/main.css' %}"/>
    {% block style %}
    {% endblock %}
<script>
var _hmt = _hmt || [];
(function() {
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
        <h1 class="logo"><a href="{% url 'home' %}"><img src="{% static 'image/home/logo-dev.png' %}" height="40"/></a></h1>
        <ul class="nav">
            {% block menu %}

            {% endblock %}
        </ul>
        <div class="user">
            {% if user.username %}
                <!-- 登录 -->
                <div class="sign_out">
                    <a href="{% url 'center' %}">管理中心</a>
                </div>
            {% else %}
                <!-- 登录 -->
                <div class="sign_out">
                    <a href="{% url 'login' %}">登录</a>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% block content %}

{% endblock %}
<div class="footer">
    <p><a href="http://www.53iq.com/about" target="_blank">关于53iq</a>
        <a href="/guide#contact">联系我们</a>
    </p>

    <p>Copyright©2015 53iq 版权所有</p>
</div>
<script src="{% static 'js/jquery-1.11.0.min.js' %}"></script>
<script src="{% static 'bootstrap/bootstrap.js' %}"></script>
{% block script %}

{% endblock %}
</body>

</html>