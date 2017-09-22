{% load staticfiles %}
<!DOCTYPE html>
<!--[if lt IE 7]>      <html lang="en" ng-app="Product" class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html lang="en" ng-app="Product" class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html lang="en" ng-app="Product" class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html lang="en" ng-app="Product" class="no-js"> <!--<![endif]-->


<head lang="en">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no"/>
    <meta name="Keywords" content="53iq智能，开放平台,超级APP,互联互通,硬件开发，物联开发，物联网，智能硬件开发，智能家居开发，健康设备开发，开发者中心"/>
    <meta name="Description" content="中国物联网与智能硬件行业领先的技术平台，为硬件厂商和开发者提供智能产品接入和推广的快捷通道，智能开发从53iq开始。"/>
    <title>{% block title %}{% endblock %} - 厨房智能平台</title>
    <link rel="shortcut icon" href="{% static 'image/53iq.ico' %}"/>
    <link rel="stylesheet" href="{% static 'bootstrap/bootstrap.css' %}"/>
    <link rel="stylesheet" href="{% static 'css/base/main.css' %}"/>
    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
    <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
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
        <h1 class="logo"><a href="{% url 'home' %}"><img src="{% static 'image/home/logo-dev.png' %}" height="40"></a></h1>
        <ul class="nav">
            {% block menu %}

            {% endblock %}
        </ul>

    <div class="sign_out">
         {% if user.account_id %}
                <!-- 登录 -->
                <a onclick="$('.login_out').width($(this).width()+46);$('.login_out').toggle();"
                       style="text-decoration: none;">{{ user.account_id }}<span class="corner"></span></a>
                    <div onmouseout="$('.login_out').hide()" style="position: absolute;background: #F1F4F9; box-shadow: 0 1px 6px rgba(0,0,0,.2);">

                       {% if user.developer.developer_id %}
                               <a rel="nofollow" onmouseover="$('.login_out').show()" class="login_out" href="/center/checklist"
                           style="width: 120px; cursor: pointer; display: none;">通知</a>
                       {% else %}
                            <a rel="nofollow" onmouseover="$('.login_out').show()" class="login_out" href="#"
                           style="width: 120px; cursor: pointer; display: none;">通知</a>
                        {% endif %}


                    <a rel="nofollow" href="/center?" class="login_out"
                       onmouseover="$('.login_out').show()" style="width: 120px; cursor: pointer; display: none;">帐号管理</a>
                    <a rel="nofollow" id="modify_pwd_id" onclick="location.href='{% url 'modify_pwd' %}'"
                       onmouseover="$('.login_out').show()" class="login_out"
                       style="width: 120px; cursor: pointer; display: none;">修改密码</a>
                        <a rel="nofollow" id="modify_pwd_id" href="/guide#" onclick="addHover('/contact',this)" onmouseover="$('.login_out').show()" class="login_out" style="width: 120px; cursor: pointer; display: none;">联系客服</a>
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

{% endblock %}

<div class="footer">
    <p><a href="http://www.53iq.com/about" target="_blank">关于53iq</a>
        <a href="/guide#contact" onclick="addHover('contact',this)">联系我们</a>
    </p>

    <p>Copyright©{% now 'Y' %} 53iq 版权所有</p>
</div>
<script src="{% static 'js/jquery-1.11.0.min.js' %}"></script>
<script src="http://apps.bdimg.com/libs/bootstrap/3.3.4/js/bootstrap.min.js"></script>
{% block end_fixed_script %}{% endblock %}
{% block end_script %}{% endblock %}
</body>

</html>