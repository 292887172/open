{% load staticfiles %}
{% load filter %}
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
<style>
    .sign_out a:hover{
        color: #ff6202;
    }
    .sign_out a.user-login{
        background-color: #FF6F37
    }
    .sign_out .user-login:hover{
        color: #fff;
        background-color: #ff6202
    }
    .leftSide{
        margin-bottom:0;
        padding-bottom: 0;
    }
    .h5pro{
            padding-left: 15px;
            padding-bottom: 20px;
            cursor: pointer;
            position: relative;
        }
        .icon-caret-down{
                background: url(/static/image/wiki/arrow_up.png) no-repeat center;
                background-size: 80%;
                width: 15px;
                height: 15px;
                position: absolute;
                margin-left: 82%;
        }
        .icon-caret-right {
            background: url(/static/image/wiki/arrow_down.png) no-repeat center;
            background-size: 80%;
            width: 15px;
            height: 15px;
            position: absolute;
            margin-left: 82%;
        }
        .menuBox ul{
            display: block;
            padding-left: 0px;
            border-top: 1px solid #f5f5f5;
            padding-top: 7px;
        }
        .menuBox ul li {
            height: 55px;
            line-height: 55px;
        }
        .box1 {
            min-height: 0;
        }
        .menuBox {
                border-top: 1px solid #f5f5f5;
                padding: 20px 0px 0 0px;
            }
</style>
<body>
<div class="header">
    <div class="wrapper">
        <h1 class="logo"><a href="{% if user.account_id %}/product/list{% else %}/{% endif %}"><img src="{% static 'image/home/logo-dev1.png' %}" height="40"/></a></h1>
         <ul class="nav">

            {% if user.account_id or user.developer.developer_from == 3%}
                <li><a href="{% url 'product/list' %}">产品管理</a></li>
            {% else %}
                <li><a href="{% url 'home' %}">首页</a></li>
            {% endif %}
            <li><a href="{% url 'product/kitchen' %}">厨电方案</a></li>
            <li><a href="{% url 'wiki' %}">开发指南</a></li>
            <li><a href="{% url 'smartmenu' %}">智能菜谱</a></li>

        </ul>
        <div class="user">
            <div class="sign_out">
                {% if user.account_id %}
                <a href="#" onclick="$('.login_out').width($(this).width()+46);$('.login_out').toggle();"
                       style="text-decoration: none;">账号：{{ user.account_id|cover_user_name:user.account_nickname }}<span class="corner"></span></a>
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
                        <a rel="nofollow" id="modify_pwd_id" href="/contact" onmouseover="$('.login_out').show()" class="login_out" style="width: 120px; cursor: pointer; display: none;">联系客服</a>
                        <a rel="nofollow" id="login_out_id" onclick="location.href='{% url 'logout' %}'" onmouseover="$('.login_out').show()" class="login_out" style="width: 120px; cursor: pointer; display: none;">退出</a>
                    </div>
                {% else %}
                     <a style="min-width: 75px;" class="user-login" href="{% url 'login' %}">登录</a>
                {% endif %}

            </div>
        </div>
    </div>
</div>
{% block content %}

{% endblock %}
<div class="footer">
    <p><a href="http://www.53iq.com/about" target="_blank">关于53iq</a>
        <a href="/contact">联系我们</a>
    </p>

    <p>Copyright©2015 53iq 版权所有</p>
</div>
<script src="{% static 'js/jquery-1.11.0.min.js' %}"></script>
<script src="{% static 'bootstrap/bootstrap.js' %}"></script>
<script>
    function ul_toggle(hobj) {
        $(hobj).children('i').toggleClass('icon-caret-down');
        $(hobj).next('ul').toggle();
        $(".h5pro").css('color', '#000');
        // 解决没有子菜单的菜单点击后再点击别的菜单时焦点颜色不同步的问题
        $(".h5pro").children('a').css('color', '#000');
        if ($(hobj).next('ul').is(":hidden")) {
            $(hobj).css('color', '#000')
        }
        else {
            $(".menuUl").hide();
            $(".menuUl").prev('h5').children('i').removeClass('icon-caret-down');
            $(hobj).next('ul').show();
            $(hobj).children('i').addClass('icon-caret-down');
            $(hobj).css('color', '#ff6202')
        }
    }
</script>
{% block script %}

{% endblock %}
</body>

</html>