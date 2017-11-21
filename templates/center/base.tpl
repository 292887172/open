{% load staticfiles %}
{% load filter %}
<!DOCTYPE html>
<html ng-app>

<head lang="en">
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no"/>
    <meta name="Keywords" content="53iq智能，开放平台,超级APP,互联互通,硬件开发，物联开发，物联网，智能硬件开发，智能家居开发，健康设备开发，开发者中心"/>
    <meta name="Description" content="中国物联网与智能硬件行业领先的技术平台，为硬件厂商和开发者提供智能产品接入和推广的快捷通道，智能开发从53iq开始。"/>
    <title>{% block title %}{% endblock %} 厨房智能平台</title>
    <link rel="shortcut icon" href="{% static 'image/53iq.ico' %}"/>
    <link rel="stylesheet" href="{% static 'bootstrap/bootstrap.css' %}"/>
    <link rel="stylesheet" href="{% static 'css/base/main.css' %}"/>
    <link rel="stylesheet" href="{% static 'css/center/dev.css' %}"/>

    <style>
        #header .cnt .menu li a .corner{display:inline-block; width:6px; height:4px; margin:0 0 0 10px; background:url({% static 'image/sanjiao.png' %}) center center no-repeat; vertical-align:middle;}
    .nav-current{
            text-decoration:none; border-bottom: 3px solid #ff6202;height: 35px;
        }
    </style>
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
<style>
   .sign_out a:hover{
        color: #ff6202;
    }
    .sign_out .user-login:hover{
        color: #fff;
    }
</style>
<body>
<div id="header">
    <div class="cnt">
        <h1>
            <a href="{% url 'home' %}"><img src="{% static 'image/home/logo-dev1.png' %}" height="40"
                                            title="53iq云智能云"></a>
        </h1>
        <ul class="nav">
           <li><a href="{% url 'home' %}">首页</a></li>
            {% if user.developer.developer_id and user.developer.developer_check_status == 1 or user.developer.developer_from == 3%}
                <li><a href="{% url 'product/list' %}">产品管理</a></li>
            {% endif %}
            <li><a href="{% url 'home/guide' %}">开发指南</a></li>
            <li><a href="/wiki/"  >开发文档</a></li>
        </ul>
        <div class="sign_out">
            {% if user.account_id %}
                <a href="#" onclick="$('.login_out').width($(this).width()+46);$('.login_out').toggle();"
                       style="text-decoration: none;">我的账号：{{ user.account_id|cover_user_name:user.account_nickname }}<span class="corner"></span></a>
                    <div onmouseout="$('.login_out').hide()" style="position: absolute;background: #F1F4F9; box-shadow: 0 1px 6px rgba(0,0,0,.2);">
                       {% if user.developer.developer_id %}
                               <a rel="nofollow" onmouseover="$('.login_out').show()" class="login_out" href="/center/checklist"
                           style="width: 120px; cursor: pointer; display: none;">通知</a>
                       {% else %}
                            <a rel="nofollow" onmouseover="$('.login_out').show()" class="login_out" href="/center/checklist"
                           style="width: 120px; cursor: pointer; display: none;">通知</a>
                        {% endif %}

                        <a rel="nofollow" href="/center?" class="login_out" onmouseover="$('.login_out').show()" style="width: 120px; cursor: pointer; display: none;">帐号管理</a>
                        {% if not user.account_nicknam %}
                            <a rel="nofollow" id="modify_pwd_id" onclick="location.href='{% url 'modify_pwd' %}'" onmouseover="$('.login_out').show()" class="login_out" style="width: 120px; cursor: pointer; display: none;">修改密码</a>
                        {% endif %}

                        <a rel="nofollow" id="modify_pwd_id" href="/guide#contact" onclick="addHover('/contact',this)" onmouseover="$('.login_out').show()" class="login_out" style="width: 120px; cursor: pointer; display: none;">联系客服</a>
                        <a rel="nofollow" id="login_out_id" onclick="location.href='{% url 'logout' %}'" onmouseover="$('.login_out').show()" class="login_out" style="width: 120px; cursor: pointer; display: none;">退出</a>
                    </div>
            {% endif %}

        </div>
</div>
<div class="container">
{% if user.developer.developer_check_remarks and user.developer.developer_check_status == -1 %}
    <div class="wrapper">
        <div class="alert alert-danger">
            <button type="button" class="close" data-dismiss="alert">×</button>
            <i class="fa fa-bell-o"></i>&nbsp;&nbsp;[审核未通过原因]&nbsp;&nbsp;<span>{{ user.developer.developer_check_remarks }}</span>
        </div>
    </div>
{% endif %}
</div>
{% block content %}

{% endblock %}
<div class="footer">
    <ul>
        <li><a href="http://www.53iq.com/about" target="_blank" rel="nofollow">关于53iq</a></li>
        <li>|</li>
        <li><a href="/guide#contact"  rel="nofollow">联系我们</a></li>

    </ul>
    <p>Copyright©{% now 'Y' %} 53iq 版权所有</p>
</div>
<script src="{% static 'js/jquery-1.11.0.min.js' %}"></script>
<script src="{% static 'bootstrap/bootstrap.js' %}"></script>
<script src="{% static 'js/center/bootbox.js' %}"></script>
{% block script %}

{% endblock %}
</body>

</html>