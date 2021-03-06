{% load staticfiles %}
{% load filter %}
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
    <title>{% block title %}{% endblock %} - 厨电开发平台</title>
    <link rel="shortcut icon" href="{% static 'image/53iq.ico' %}"/>
     <link rel="stylesheet" href="{% static 'assets/css/bootstrap.min.css'%}" />
    <link rel="stylesheet" href="{% static 'css/base/main.css' %}"/>
    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
    <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
    {% block style %}

    {% endblock %}
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
            .header{
                position: fixed;
                top: 0;
                width: 100%;

            }
            .footer{
                position: relative;
                padding: 20px;
                z-index: 0;
            }
            .footer > p {
                margin-top: 0;
                display:block;
            }
        .nav{
            margin-top: 30px;
        }

    </style>
</head>
<body>
<div class="header" style="background: #F1F4F9;">
    <div class="wrapper">
        {% block image %}
            <h1 class="logo"><a href="{% if user.account_id %}/product/list{% else %}/{% endif %}"><img src="{% static 'image/home/logo-dev1.png' %}" ></a></h1>
        {% endblock %}


        {% block menu %}

        {% endblock %}

    <div class="sign_out">
         {% if user.account_id %}
                <!-- 登录 -->
                <a role="button" class="account" onclick="$('.login_out').width($(this).width()+46);$('.login_out').toggle();"
                       style="text-decoration: none;">账号：{{ user.account_id|cover_user_name:user.account_nickname }}<span class="corner"></span></a>
                    <div onmouseout="$('.login_out').hide()" style="position: absolute;background: #F1F4F9; box-shadow: 0 1px 6px rgba(0,0,0,.2);">
                       <!--
                       {% if user.developer.developer_id %}
                               <a rel="nofollow" onmouseover="$('.login_out').show()" class="login_out" href="/center/checklist"
                           style="width: 120px; cursor: pointer; display: none;">通知</a>
                       {% else %}
                            <a rel="nofollow" onmouseover="$('.login_out').show()" class="login_out" href="/center/checklist"
                           style="width: 120px; cursor: pointer; display: none;">通知</a>
                        {% endif %}
                        -->

                    <a rel="nofollow" href="/center?" class="login_out"
                       onmouseover="$('.login_out').show()" style="width: 120px; cursor: pointer; display: none;">账户中心</a>


                        <a rel="nofollow" id="modify_pwd_id" href="/contact" onmouseover="$('.login_out').show()" class="login_out" style="width: 120px; cursor: pointer; display: none;">联系客服</a>
                     <a rel="nofollow" id="login_out_id" onclick="location.href='{% url 'logout' %}'"
                       onmouseover="$('.login_out').show()" class="login_out"
                       style="width: 120px; cursor: pointer; display: none;">退出</a>
                    </div>
            {% else %}
                <!-- 登录 -->


                    <a style="min-width: 75px;" class="user-login" href="{% url 'login' %}">登录</a>

            {% endif %}
    </div>
    </div>
</div>
{% block content %}

{% endblock %}

<div class="footer">
    <p><a href="http://www.53iq.com/about" target="_blank">关于53iq</a>
        <a href="/contact">联系我们</a>
    </p>

    <p>Copyright©{% now 'Y' %} 53iq 版权所有</p>
</div>
<script src="{% static 'js/jquery-1.11.0.min.js' %}"></script>
<script src="/static/assets/js/bootstrap.min.js"></script>
<script src="/static/js/check-ie.js"></script>
<script>
    if(lessIE9()){
        $.ajax({
            type: "get",
            url: '/error',
            data: "",
            success: function (msg) {
                $("body").html(msg)
            },
            error: function () {
            }
        })
    }
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "//hm.baidu.com/hm.js?9088d602c7fd9fd4bfb8f3472bd734b7";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();
</script>
{% block end_fixed_script %}{% endblock %}
{% block end_script %}{% endblock %}
</body>

</html>