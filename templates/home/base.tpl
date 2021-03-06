{% load staticfiles %}
{% load filter %}
<!DOCTYPE html>
<html>

<head lang="en">
    <meta charset="UTF-8"/>

    <meta name="viewport"
          content="width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no"/>
    <meta name="Keywords" content="53iq智能，开放平台,超级APP,互联互通,硬件开发，物联开发，物联网，智能硬件开发，智能家居开发，健康设备开发，开发者中心"/>
    <meta name="Description" content="中国物联网与智能硬件行业领先的技术平台，为硬件厂商和开发者提供智能产品接入和推广的快捷通道，智能开发从53iq开始。"/>
    <title>{% block title %}{% endblock %} 厨电开发平台</title>
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
<style>
     .image_ss{
         position: absolute;
         top: 35px;
         left: 0;
         max-width: 130px;
         z-index:1
     }
    .sign_out a:hover{
        color: #ff0000 !import;
    }
    .sign_out a.user-login{
        background-color: #FF6F37
    }
    .sign_out .user-login:hover{
        color: #fff;
        background-color: #ff6202
    }
    .footer{
        position: relative;
        padding: 20px;
    }
    .header{
        position: fixed;
        width: 100%;
        top: 0;
    }
     .footer > p {
            margin-top: 0;
            display:block;
        }
    .nav{
        margin-top: 30px;
    }
</style>
<body>
<div class="header">
    <div class="wrapper">
        <h1 class="logo"><a href="{% if user.account_id %}/product/list{% else %}/{% endif %}"><img src="{% static 'image/home/logo-dev1.png' %}" /></a>
        </h1>
        {% block menu %}

        {% endblock %}
    <div class="sign_out">
        {% if user.account_id %}
                <!-- 登录 -->
                <a href="#" onclick="$('.login_out').width($(this).width()+46);$('.login_out').toggle();"
                       style="text-decoration: none;">账号：{{ user.account_id|cover_user_name:user.account_nickname }}<span class="corner"></span></a>
                    <div onmouseout="$('.login_out').hide()" style="position: absolute;background: #F1F4F9; box-shadow: 0 1px 6px rgba(0,0,0,.2);">
                    <!----
                       {% if user.developer.developer_id %}
                               <a rel="nofollow" onmouseover="$('.login_out').show()" class="login_out" href="/center/checklist"
                           style="width: 120px; cursor: pointer; display: none;">通知</a>
                       {% else %}
                            <a rel="nofollow" onmouseover="$('.login_out').show()" class="login_out" href="/center/checklist"
                           style="width: 120px; cursor: pointer; display: none;">通知</a>
                        {% endif %}
                    -->
                        <a rel="nofollow" href="/center?" class="login_out" onmouseover="$('.login_out').show()" style="width: 120px; cursor: pointer; display: none;">账户中心</a>

                        <a rel="nofollow" id="modify_pwd_id" href="/contact" onmouseover="$('.login_out').show()" class="login_out" style="width: 120px; cursor: pointer; display: none;">联系客服</a>
                        <a rel="nofollow" id="login_out_id" onclick="location.href='{% url 'logout' %}'" onmouseover="$('.login_out').show()" class="login_out" style="width: 120px; cursor: pointer; display: none;">退出</a>
                    </div>
            {% else %}
                  <a href="/center/login">
                            <span class="show-control;color: #ff0000 !import">登录</span>
                        </a>


            {% endif %}
    </div>
    </div>
</div>

{% if user.account_id %}
        {% if not user.developer.developer_id or user.developer.developer_check_status == 2 %}
            <!--
            <div class="wrapper">
                <div class="alert alert-danger">

                    <button type="button" class="close" data-dismiss="alert">×</button>


                    <i class="fa fa-bell-o"></i>&nbsp;&nbsp;帐号：[{{ user.account_id }}]&nbsp;&nbsp;<span>&nbsp;&nbsp;&nbsp;您还未申请成为开发者!<a href="/center" style="color: #ff6202;  margin-left: 20%;">加入开发者</a> </span>
                </div>
            </div>
            -->
        {% endif %}
    {% endif %}

{% block content %}
    <div class="wrapper mt20 fn-clear">
        <div class="leftSide">
            <div class="box1">
                <!-- 左侧菜单 begin -->

                <div class="menuBox">

                    <ul>
                        <li class="menu-li"><a href="/debug/debug_interface" target=""><i
                                class="icon-wrench"></i>调试接口</a></li>
                    </ul>
                </div>
                 <div class="menuBox">

                    <ul>
                        <li class="menu-li"><a href="/debug/debug_device" target=""><i
                                class="icon-compass"></i>调试设备</a></li>
                    </ul>
                </div>
                <div class="menuBox">
                    <ul>
                        <li class="menu-li" onclick="addHover('/sdk',this)"><a href="#"><i
                                class="icon-cloud-download"></i>下载中心</a></li>
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
        <a href="/contact">联系我们</a>
    </p>

    <p>Copyright©{% now 'Y' %} 53iq 版权所有</p>
</div>
<script src="{% static 'js/jquery-1.11.0.min.js' %}"></script>
<script src="{% static 'bootstrap/bootstrap.js' %}"></script>
<script>
    window.onload=function () {
            var height1 = document.body.scrollHeight;

            console.log(document.getElementsByClassName("footer")[0].style.marginTop)
            //document.getElementsByClassName("footer")[0].style.marginTop=(height1 / 2)-440+"px"
            console.log(document.body.scrollHeight)
        }
</script>
{% block script %}

{% endblock %}
</body>

</html>