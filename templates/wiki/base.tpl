{% load staticfiles %}
<!DOCTYPE html>
<html ng-app>

<head lang="en">
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no"/>
    <meta name="Keywords" content="53iq智能，开放平台,超级APP,互联互通,硬件开发，物联开发，物联网，智能硬件开发，智能家居开发，健康设备开发，开发者中心"/>
    <meta name="Description" content="中国物联网与智能硬件行业领先的技术平台，为硬件厂商和开发者提供智能产品接入和推广的快捷通道，智能开发从53iq开始。"/>
    <title>{% block title %}{% endblock %} 智能厨房电器方案提供商</title>
    <link rel="shortcut icon" href="{% static 'image/53iq.ico' %}"/>
    <link rel="stylesheet" href="{% static 'bootstrap/bootstrap.css' %}"/>
    <link rel="stylesheet" href="{% static 'css/wiki/global.css' %}" type="text/css"/>
    <link rel="stylesheet" href="{% static 'css/center/dev.css' %}"/>
    <link rel="stylesheet" href="{% static 'css/base/main.css' %}"/>
    <style>
        .leftSide {
            float: left;
            width: 204px;
            border: 1px solid #dddddd;
            margin-bottom: -9999px;
            padding-bottom: 9999px;
            background-color: #fff;
        }


        .rightMain {
            float: right;
            width: 894px;
            height: 100%;
            min-height: 750px;
            background-color: #fff;
            border: 1px solid #ddd;

        }

        .menuBox {
            padding: 20px 0px 0 0px;

        }

        .menuBox ul {
            padding-left: 0px;
            border-top: 1px solid #f5f5f5;
            padding-top: 7px;
        }

        .menuBox ul li{
            padding-bottom: 5px;
            padding-left: 23px;
        }

        .icon-caret-right {
            background: url("{% static 'image/wiki/arrow_down.png' %}") no-repeat center;
            background-size: 80%;
            width: 15px;
            height: 15px;
            position: absolute;
            margin-left: 82%;
        }

        .icon-caret-down {
            background: url("{% static 'image/wiki/arrow_up.png' %}") no-repeat center;
            background-size: 80%;
            width: 15px;
            height: 15px;
            position: absolute;
            margin-left: 82%;
        }

        h5 {
            padding-left: 15px;
            padding-bottom: 20px;
            cursor: pointer;
            position: relative;
        }

        h5 p {
            padding-left: 17px;
        }

        a {
            color: #333;
        }

        a:hover {
            text-decoration: none;
        }
        .footer{
            background-color: #F1F4F9;
            border-top:1px solid #ddd
        }
        .footer ul {
            width: 100%;
        }

        .ui-scroll-top {
            position: fixed;
            bottom: 10px;
            right: 3%;
            z-index: 99;
            display: none;
            width: 40px;
            height: auto;
            text-align: center;
            cursor: pointer;
        }
        .nav-current{
            text-decoration:none; border-bottom: 3px solid #ff6202;height: 35px;
        }
    </style>
    {% block style %}


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
<div id="header">
<div class="wrapper">
    <h1 class="logo">
            <a href="{% url 'home' %}">
                {% if user.developer.developer_id %}
                    <img src="{% static 'image/home/logo-dev1.png' %}" height="40"
                                            title="53iq云智能云">
                {% else %}
                    <img src="{% static 'image/home/logo-dev.png' %}" height="40"
                                            title="53iq云智能云">
                {% endif %}
            </a>
    </h1>
    <ul class="nav">
        {% block menu %}
            {% if user.developer.developer_id and user.developer.developer_check_status == 1%}
                <li><a href="{% url 'product/list' %}">产品管理</a></li>
            {% endif %}
                <li><a href="{% url 'home/guide' %}">开发指南</a></li>
                <li><a href="/wiki/" class="nav-current" >开发文档</a></li>
        {% endblock %}
    </ul>
<div class="sign_out">
        {% if user.account_id %}
                <!-- 登录 -->
                <a href="#" onclick="$('.login_out').width($(this).width()+46);$('.login_out').toggle();"
                       style="text-decoration: none;">{{ user.account_id }}<span class="corner"></span></a>
                    <div onmouseout="$('.login_out').hide()" style="position: absolute;background: #F1F4F9; box-shadow: 0 1px 6px rgba(0,0,0,.2);">
                       {% if user.developer.developer_id %}
                               <a rel="nofollow" onmouseover="$('.login_out').show()" class="login_out" href="/center/checklist"
                           style="width: 120px; cursor: pointer; display: none;">通知</a>
                       {% else %}
                            <a rel="nofollow" onmouseover="$('.login_out').show()" class="login_out" href="/center/checklist"
                           style="width: 120px; cursor: pointer; display: none;">通知</a>
                        {% endif %}

                        <a rel="nofollow" href="/center?" class="login_out" onmouseover="$('.login_out').show()" style="width: 120px; cursor: pointer; display: none;">帐号管理</a>
                        <a rel="nofollow" id="modify_pwd_id" onclick="location.href='{% url 'modify_pwd' %}'" onmouseover="$('.login_out').show()" class="login_out" style="width: 120px; cursor: pointer; display: none;">修改密码</a>
                        <a rel="nofollow" id="modify_pwd_id" href="/guide#" onclick="addHover('/contact',this)" onmouseover="$('.login_out').show()" class="login_out" style="width: 120px; cursor: pointer; display: none;">联系客服</a>
                        <a rel="nofollow" id="login_out_id" onclick="location.href='{% url 'logout' %}'" onmouseover="$('.login_out').show()" class="login_out" style="width: 120px; cursor: pointer; display: none;">退出</a>
                    </div>
            {% else %}
                <!-- 登录 -->

                    <a style="min-width: 75px;" class="user-login" href="{% url 'login' %}">登录</a>

            {% endif %}
    </div>
</div>
</div>
{% block content %}
    <div class="wrapper mt20 fn-clear">
        <div class="leftSide">
            <div class="box1">

            </div>
        </div>
        {% block right %}
        {% endblock %}
    </div>
{% endblock %}
<div class="footer">
    <ul>
        <li><a href="http://www.53iq.com/about" target="_blank" rel="nofollow">关于53iq</a></li>
        <li>|</li>
        <li><a href="/guide">53iq云</a></li>
        <li>|</li>

        <li><a href="/guide#contact" target="_blank" rel="nofollow">联系我们</a></li>

    </ul>
    <p>Copyright©2015 53iq 版权所有</p><a name="chaper" class="ui-scroll-top"
                                      href="javascript:scroll(0,0);"><img src="{% static 'image/wiki/zhid2.png' %}"
                                                                          title="回到顶部"/></a>
</div>
<script src="{% static 'js/jquery-1.11.0.min.js' %}"></script>
<script src="{% static 'bootstrap/bootstrap.js' %}"></script>
<script src="{% static 'js/center/bootbox.js' %}"></script>
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
    var menus = '{{ request.session.menus|safe }}';
    menus = JSON.parse(menus);
    function my_menu(menus) {
        var total_menu = [];
        var temp_menu = [];

        var len = menus.length;
        for (var i = 0; i < len; i++) {
            var menu = menus[i];
            // 根节点
            if (menu.menu_parent_id == 0) {
                var first_menu = new Object();
                first_menu.id = menu.menu_id;
                first_menu.url = menu.menu_url;
                first_menu.name = menu.menu_name;
                first_menu.ordernum = menu.menu_ordernum;
                first_menu.nodes = [];
                total_menu.push(first_menu)
            }
            else {
                var second_menu = new Object();
                second_menu.parent_id = menu.menu_parent_id;
                second_menu.id = menu.menu_id;
                second_menu.url = menu.menu_url;
                second_menu.name = menu.menu_name;
                second_menu.ordernum = menu.menu_ordernum;
                temp_menu.push(second_menu)
            }
        }
        // 对一级和二级菜单整合
        for (var l = 0; l < total_menu.length; l++) {
            for (var k = 0; k < temp_menu.length; k++) {
                if (temp_menu[k].parent_id == total_menu[l].id) {
                    total_menu[l].nodes.push(temp_menu[k])
                }
            }
        }
        // 对一级菜单排序
        total_menu.sort(function (a, b) {
            return a.ordernum > b.ordernum ? 1 : -1;
        });
        // 对二级菜单排序
        for (var z = 0; z < total_menu.length; z++) {
            total_menu[z].nodes.sort(function (a, b) {
                return a.ordernum > b.ordernum ? 1 : -1;
            })
        }

        return make_menu(total_menu)

    }
    function make_menu(menus) {
        var len = menus.length;
        var html = '';
        if (len == 0) {
            return html;
        }

        for (var i = 0; i < len; i++) {
            var menu = menus[i];
            // 根节点+无子菜单
            if (menu.nodes.length == 0) {
                html += '<div class="menuBox"><h5 class="h5pro" onclick="load_url2(this)"><a  class="' + menu.id + '" name="' + menu.url + '" href="#' + menu.id + '" >' + menu.name + '</a></h5></div>';
            }
            // 根节点+带有子菜单
            else {
                html += '<div class="menuBox"><h5 class="h5pro" onclick="ul_toggle(this)"><i class="icon-caret-right"></i><p>' + menu.name + '</p></h5><ul hidden="hidden" class="menuUl">';
                for (var j = 0; j < menu.nodes.length; j++) {
                    html += '<li class="menu-li"><a onclick="load_url(this)" class="' + menu.nodes[j].id + '" name="' + menu.nodes[j].url + '" href="#' + menu.nodes[j].id + '" >'
                    + menu.nodes[j].name + '</a></li>';
                }

                html += '</ul></div>';
            }
            {#                        // 根节点+带有子菜单#}
            {#                        if (menu.menu_parent_id == parent_id && menu.menu_is_parent == 1) {#}
            {##}
            {##}
            {#                            html += '<div class="menuBox"><h5 class="h5pro" onclick="ul_toggle(this)"><i class="icon-caret-right"></i><p>'+menu.menu_name+'</p></h5><ul hidden="hidden" class="menuUl">';#}
            {#                            html += make_menu(menu.menu_id, menus);#}
            {#                            html += '</ul></div>';#}
            {#                        }#}
            {#                        // 根节点+无子菜单#}
            {#                        else if (menu.menu_parent_id == parent_id && menu.menu_is_parent == 0 && parent_id == 0) {#}
            {#                            html += '<div class="menuBox"><h5 class="h5pro"><p><a onclick="load_url2(this)" class="'+menu.menu_id+'" name="'+menu.menu_url+'" href="#' + menu.menu_id+ '" >'+menu.menu_name+'</a></p></h5></div>';#}
            {#                        // 子菜单#}
            {#                        } else if (menu.menu_parent_id == parent_id && parent_id != 0) {#}
            {#                            html += '<li class="menu-li"><a onclick="load_url(this)" class="'+menu.menu_id+'" name="'+menu.menu_url+'" href="#' + menu.menu_id + '" >'#}
            {#                            + menu.menu_name + '</a></li>';#}
            {#                        }#}
        }
        return html;
    }
    $(function () {

        var html = my_menu(menus);
        $('.box1').html(html);
        //获取滚动条高度
        function getScrollTop() {
            var scrollTop = 0;
            if (document.documentElement && document.documentElement.scrollTop) {
                scrollTop = document.documentElement.scrollTop;
            }
            else if (document.body) {
                scrollTop = document.body.scrollTop;
            }
            return scrollTop;
        }

        //绑定页面滚动函数
        $(document).scroll(function () {
            var top = getScrollTop();
            var doc = $(document).height();
            var win = $(window).height();
            if (top > win / 2) {
                $('.ui-scroll-top').show();
            } else {
                $('.ui-scroll-top').css('display', 'none');
            }

        });
    })
</script>
{% block script %}

{% endblock %}
</body>

</html>