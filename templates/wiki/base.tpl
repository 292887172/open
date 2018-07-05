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
    <title>{% block title %}{% endblock %} 智能厨房电器方案提供商</title>
    <link rel="shortcut icon" href="{% static 'image/53iq.ico' %}"/>
    <link rel="stylesheet" href="{% static 'bootstrap/bootstrap.css' %}"/>
    <link rel="stylesheet" href="{% static 'css/wiki/global.css' %}" type="text/css"/>
    <link rel="stylesheet" href="{% static 'css/center/dev.css' %}"/>
    <link rel="stylesheet" href="{% static 'css/base/main.css' %}"/>
    <link rel="stylesheet" href="/static/common/css/font-awesome.min.css">
    <link rel="stylesheet" href="/static/css/product/bootbox.css">
    <link rel="stylesheet" href="/static/css/product/list.css"/>

    <style>
        .nav{
        margin-top: 30px;
    }
        #header{
            position: fixed;
            width: 100%;
            top:0;
        }
        .leftSide {
            float: left;
            width: 204px;
            border: 1px solid #dddddd;
            margin-bottom: 0px;
            padding-bottom: 0px;
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
      li a:hover{
        color: #ff6202;
        text-decoration: underline;
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
<h1 class="logo"><a href="{% if user.account_id %}/product/list{% else %}/{% endif %}"><img src="{% static 'image/home/logo-dev1.png' %}" height="40"/></a>
        </h1>
        {% block menu %}

        {% endblock %}
<div class="sign_out">
        {% if user.account_id %}
                <!-- 登录 -->
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
                <!-- 登录 -->

                    <a style="min-width: 75px;" class="user-login" href="{% url 'login' %}">登录</a>

            {% endif %}
    </div>
</div>
</div>
{% block content %}
    <div class="title">
            <div class="wrapper">
            {% for default_app in default_apps %}
                <input type="hidden" class="default-app" data-appid={{ default_app.app_id }}>
            {% endfor %}
            {% for a in all_app %}
                {% if a.check_status != 3%}
                    <input type="hidden" class="owner-app" data-appid={{ a.app_id }}>
                {% endif %}
            {% endfor %}
            <ol class="breadcrumb" style="width: 36%;float: left">
                <li><a href="/product/list">产品管理</a></li>
                <li style="color: #ff6202;">开发指南</li>
            </ol>
            <ol style="width: 50%;float: left;margin: 6px 0 1px;line-height: 0;" class="new-app">
                <li style="color: #c6c6c6;">模板创建：</li>
                {% for app in default_apps %}
                    <li>
                        {% if user.developer.developer_id%}
                            <a href="javascript:void(create_procuct('{{ app.app_device_type }}'))" >{{ app.app_name }}</a>
                        {% else %}
                            <a href="javascript:void(dont_develop())">{{ app.app_name }}</a>
                        {% endif %}
                    </li>
                    {% if forloop.counter == 3 %}
                        <li><a style="color: #ff6202" href="javascript:{% if user.developer.developer_id %}void(create_procuct(11,'wifi')){% else %}void(dont_develop()){% endif %}" >WiFi烤箱</a></li>
                        <li style="padding-left: 84px"> <a href="{% url 'product/main' %}?ID={{ app.app_id }}#/demo/{{ app.app_name }}">开发示例</a></li>
                    {% endif %}
                {% endfor %}
            </ol>
            </div>

        </div>
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

        <li><a href="/contact" target="" rel="nofollow">联系我们</a></li>

    </ul>
    <p>Copyright©{% now 'Y' %} 53iq 版权所有</p><a name="chaper" class="ui-scroll-top"
                                      href="javascript:scroll(0,0);"><img src="{% static 'image/wiki/zhid2.png' %}"
                                                                          title="回到顶部"/></a>
</div>
<div class="popBox" id="newHtmlBox" style="display: none;">
        <a href="javascript:" onclick="new_close()" class="close">关闭</a>
        <h3 style="text-align: center;height: auto;">创建<span id="productType"></span>类产品</h3>
        <div class="cont mt20" style="margin-top: -15px;">
            <div style="float:left;">
                <img id="show_logo" style="width: 110px;height: 120px;margin:0 0 0 -3%;"
                     src="http://storage.56iq.net/group1/M00/1D/0C/CgoKQ1m3oSmAbhKvAAALicfeZeI743.png">
            </div>
            <div class="warnCont" style="width: 76%">
                <form name="formProduct" method="post" class="fd7_create_product-form" action="/product/add/">
                    <div class="ant-row ant-form-item">
                        <label for="product_name" class="">产品名称:</label>
                        <span class="ant-input-wrapper">
                            <input type="text" value="" id="product_name" onblur="check_name()" name="product_name"
                                   class="ant-input ant-input-lg">
                        </span>
                        <div id="productName" style="color: #f50;font-size: 12px;padding-left: 76px"></div>
                    </div>
                    <div class="ant-row ant-form-item" id="com_type">
                        <label class="dtbox">技术方案:</label>

                        <p class="technology" style="float: right;width: 75%"><input class="magic-radio" type="radio" onclick="select_progm(2)" name="select_group" id="c1" checked>
                            <label for="c1">WiFi</label>
                            <input class="magic-radio" type="radio" name="select_group" onclick="select_progm(1)" id="c2" >
                            <label for="c2">Android屏<span id="ScreenSize"></span></label>
                        </p>

                        <div  class="select-progm1" style="font-size: 12px;color: #2980b9;">WiFi方案要求设备支持5V供电，两路串口</div>
                    </div>

                    <div class="ant-row ant-form-item">
                        <label for="product_name" class="">产品类型:</label>
                        <span class="ant-input-wrapper">厨房类
                            <input type="hidden" value="厨房类" readonly="readonly" name="product_category"
                                   class="ant-input ant-input-lg">
                        </span>
                    </div>
                    <input type="hidden" value="" id="product_category_detail" name="product_category_detail" class="">
                    <input type="hidden" value="{{ user.developer.developer_id }}" name="developer_id">
                    <input type="hidden" value="2" name="product_group" class="product_group">
                    <input type="hidden" value="是" name="product_command">

                </form>
            </div>
        </div>
        <div class="btnBar" style="background: none;height: 57px;">
              <span>
                <a href="javascript:" onclick="submit_product()" id="productSubmit" class="btn-blue"
                   style="background: #ff6202;">提交</a>
              </span>
        </div>
    </div>
<div class="markLayout"></div>
<script src="{% static 'js/jquery-1.11.0.min.js' %}"></script>
<script src="{% static 'bootstrap/bootstrap.js' %}"></script>
<script src="{% static 'js/center/bootbox.js' %}"></script>
<script src="{% static 'js/check-ie.js' %}"></script>
<script src="/static/js/product/fast_create.js"> </script>
<script>
    //判断ie浏览器版本是否低于9
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
    if (menus!=="" && menus!==undefined) {
        menus = JSON.parse(menus);
    }
    else{
        menus={}
    }
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