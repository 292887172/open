var checkSubmitFlg = false;
var app_id="";
function create_product(type, type1) {
    try{
        // 重置面板
    resetItem();
    }catch (e){}

    $("#ScreenSize").text("(7寸)");
    if (type1 == "wifi1") {
        // $(".dtbox").hide();
        $(".technology").hide();
    }
    else {
        $(".dtbox").show();
        $(".technology").show();
    }
    $(".markLayout").show();

    if (type == '1') {
        $("#product_category_detail").val(1);
        $("#productType").html("油烟机");
        $("#productType1").html("油烟机");
        $("#product_name").val("油烟机");
        $("#show_logo").attr('src', "http://storage.56iq.net/group1/M00/1D/0C/CgoKQ1m3oSmAbhKvAAALicfeZeI743.png");
    }
    else if (type == '2') {
        $("#product_category_detail").val(2);
        $("#productType").html("集成灶");
        $("#productType1").html("集成灶");
        $("#product_name").val("集成灶");
        $("#show_logo").attr('src', "http://storage.56iq.net/group1/M00/1D/0C/CgoKQ1m3oYGANZPwAAAIvQGt7RM216.png");
    }
    else if (type == '11') {
        $("#ScreenSize").text("(5寸)");
        $("#product_category_detail").val(11);
        $("#productType").html("烤箱");
        $("#productType1").html("烤箱");
        $("#product_name").val("烤箱");
        $("#show_logo").attr('src', "http://storage.56iq.net/group1/M00/1D/0C/CgoKQ1m3oWqAbFICAAAKkW-6s_Q059.png");
    }
    else if (type == '31') {

        $("#product_category_detail").val(31);
        $("#productType").html("洗碗机");
        $("#productType1").html("洗碗机");
        $("#product_name").val("洗碗机");
        $("#show_logo").attr('src', "http://storage.56iq.net/group1/M00/44/79/CgoKQ1tEjDCAFxfRAAAHGI3eiDc451.png");
    }
    $("#newHtmlBox").css('display', 'block');
    $(document).ready(function () {
        $(".markLayout").click(function (event) {
            if (!$(this).hasClass("popBox") && !$(this).hasClass("tuya-btn tuya-btn-default mark-bottom-btn mark-children-bottom-btn")) {
                new_close();
            }
            event.stopPropagation(); //阻止事件冒泡
        });
    });
}
function show_detail() {
    if(app_id){
        console.log('xxx')
        window.location.href="/product/main/?ID="+app_id+"#/portal"
    }

}
function submit_product() {
    var form = $("form[name=formProduct]");
    var product_name = $("#product_name").val();

    try{
        // 更新标记，回调ifram获取返回值,部分页面有，目前只有快速创建模块有
        handlerFlag=1;
    }catch (e){}

    if (product_name == '') {
        check_name();
        return;
    }
    if (!checkSubmitFlg) {
        checkSubmitFlg = true;
        form.submit();
        try{
            showProcess('one');
        }catch (e){}


    }
    else {
        bootbox.alert("不能重复提交");
    }
}

function check_name() {
    if ($("#product_name").val() == '') {
        $('#productName').html("产品名称不能为空");
        $('#productName').css("display", "block");
        return '';
    }
    else {
        $('#productName').css("display", "none");
    }
}


function check_name() {
    if ($("#product_name").val() == '') {
        $('#productName').html("产品名称不能为空");
        $('#productName').css("display", "block");
        return '';
    }
    else {
        $('#productName').css("display", "none");
    }
}

function select_progm(val) {
    $(".product_group").val(val);
    if (document.getElementsByName('select_group')[0].checked) {

        $(".select-progm1").html("WiFi屏方案要求电控支持5V供电，一路串口，适用于烤箱，洗碗机");
    }
    else if (document.getElementsByName('select_group')[1].checked){
        $(".select-progm1").html("WiFi方案要求设备支持5V供电，两路串口")
    }
    else {
        $(".select-progm1").html("Android屏方案要求设备支持5V供电，一路串口");
    }
}

function new_close() {

    $(".markLayout").hide();
    $("#newHtmlBox").css('display', 'none');
    $("#product_name").val('');
    $("#show_logo").attr('src', "");
    $('#productName').css("display", "none");
    $(".m").hide();
    myPlayer.pause();
}

$("#dev-demo").click(function () {
    window.location.href = $(this).parent('div').data('url')
});
$("#WiFi-oven-demo").click(function () {
    $(".markLayout").show();
    $(".m").show();
    myPlayer.play();
});
$(".close-video").click(function () {
    new_close()
});

function dont_develop() {
    bootbox.confirm("您现在还不是开发者用户,请确定前往完善开发者信息", function (result) {
        if (result) {
            location.href = "/center";
        }

    })
}

function toggleTab(text) {
    var ps = document.querySelector("#template").querySelectorAll("p");
    console.log(ps)
    ps = Array.prototype.slice.call(ps);
    var lis = document.querySelector("#template").querySelectorAll("li");
    console.log(lis)
    ps.forEach(function (item, index) {
        if (item.id == text) {
            item.style.display = "block";
            lis[index].style.color = "#ff6202";
            lis[index].style.borderColor="#ff6202";
        } else {
            item.style.display = "none";
            lis[index].style.color = "#fff";
            lis[index].style.borderColor="#cdcdcd";
        }
    })
}

function getAccount() {
    var str = document.cookie;
    var obj = {};
    var arr = str.split("; ")
    arr.forEach(function (item) {
        var newArr = item.split("=");
        obj[newArr[0]] = newArr[1];
    })
    return obj;
}

function uploadInfo() {
    var user = document.querySelector("#user_address");
    var userInfo = {};
    userInfo.user_account = getAccount().COOKIE_USER_ACCOUNT;
    userInfo.contact_name = user.querySelector(".name").value;
    userInfo.contact_phone = user.querySelector(".phone").value;
    userInfo.contact_address = user.querySelector(".address").value;
    console.log(userInfo);
    if (nameBtn && phoneBtn && addressBtn) {
        $.ajax({
            type: "POST",
            url: "/api/save/user/address",
            data: userInfo,
            success: function (data) {
                $("#user_address").modal("hide");
                switch(data.code){
                    case 0:bootbox.alert("您的申请已受理，小助手尽快帮您安排邮寄");break;
                    case -1:bootbox.alert("请求方法错误");break;
                    case -2:bootbox.alert("保存失败，检查账号信息");break;
                    case -3:bootbox.alert("缺少参数");
                }
            }
        })
    }else{

        bootbox.alert("请输入正确的信息！");


    }
     document.getElementsByClassName("modal-content")[1].style.marginLeft="50px";
}

var nameBtn = false;
var phoneBtn = false;
var addressBtn = false;

function validateName(that) {
    var patt = /[\u4e00-\u9fa5]/;
    if (!patt.test(that.value)) {
        nameBtn = false;
        document.querySelector(".name_tooltip").textContent = " X";
        document.querySelector(".name_tooltip").style.color = "red";
    } else {
        nameBtn = true;
        document.querySelector(".name_tooltip").textContent = " √";
        document.querySelector(".name_tooltip").style.color = "#666";
    }
}

function validatePhone(that) {
    var patt = /^1[3|4|5|8][0-9]\d{8}$/;
    if (!patt.test(that.value)) {
        phoneBtn = false;
        document.querySelector(".phone_tooltip").textContent = " X";
        document.querySelector(".phone_tooltip").style.color = "red";
    } else {
        phoneBtn = true;
        document.querySelector(".phone_tooltip").textContent = " √";
        document.querySelector(".phone_tooltip").style.color = "#666";
    }
}

function validateAddress(that) {
    var patt = /([^\x00-\xff]|[A-Za-z0-9_])+/;
    if (!patt.test(that.value)) {
        addressBtn = false;
        document.querySelector(".address_tooltip").textContent = " X";
        document.querySelector(".address_tooltip").style.color = "red";
    } else {
        addressBtn = true;
        document.querySelector(".address_tooltip").textContent = " √";
        document.querySelector(".address_tooltip").style.color = "#666";
    }
}

        function RandomNum(Min, Max) {
            // 生成指定区间的随机数
          var Range = Max - Min;
          var Rand = Math.random();
          if(Math.round(Rand * Range)==0){
            return Min + 1;
          }else if(Math.round(Rand * Max)==Max)
          {
            index++;
            return Max - 1;
          }else{
            var num = Min + Math.round(Rand * Range) - 1;
            return num;
          }
     }

        function showProcess(step) {
            console.log(step);
            $(".popBox").css("height", '380px');
            $("#productSubmit").hide();
            setTimeout(function () {
                $("#ui-item-explain-"+step).removeClass('hide');
                $("#ui-item-explain-"+step).addClass('color-red');
                showSuccess(step);

            }, 500)
        }
        function showSuccess(step) {
            setTimeout(function () {
                $("#ui-item-explain-"+step+" i").removeClass('fa-spinner').removeClass("fa-spin").addClass("fa-check-circle-o");
                $("#ui-item-explain-"+step).removeClass('color-red');
                $("#ui-item-explain-"+step+" .tips").removeClass('hide');
                if(step=='one'){
                    showProcess('two')
                }
                else if(step=='two'){
                    showProcess('three')
                }
                else if(step=='three'){
                    console.log('ok');
                    $("#productShow").show();
                }
            }, RandomNum(1000, 2200))
        }
        function resetItem() {
            var item = ['one', 'two', 'three'];
            for(var i=0;i<3;i++){
                var s = item[i];
                $("#ui-item-explain-"+s).addClass('hide');
                $("#ui-item-explain-"+s+" i").removeClass("fa-check-circle-o").addClass('fa-spinner').addClass("fa-spin");
                $("#ui-item-explain-"+s+" .tips").addClass('hide');
            }
            $(".popBox").css("height", '340px');
            $("#productShow").hide();
            $("#productSubmit").show();

        }
                var handlerFlag = 0;
                function setOnloadCallBask(obj, event, handler) {
                    //for most explores
                    if (null != obj && null != obj.addEventListener) {
                        obj.addEventListener(event, handler, false);
                    }
                    //for IE
                    else if (null != obj && null != obj.attachEvent) {
                        obj.attachEvent('on'+event, handler);
                    }
                    //not support

                }
                /*
                *call back.
                */
                function ActionHandler()  {
                     //alert("call");
                     //文档加载或刷新时也会调用，因此需要通过标志位控制，提交时将标志位置为1，在这里处理之后修改标志位为0
                    if(0 != handlerFlag)  {
                        //do action
                        var value = document.getElementById("ifActionResult").contentWindow.document.body.innerHTML;
                        if(null!=value)  {
                             var obj = eval("("+value+")");
                             console.log(obj);

                             if(obj.code==0){
                                 app_id = obj.appid

                             }
                             console.log(app_id)

                        }
                        //update flag.
                        handlerFlag = 0;
                    }
                }
                $(document).ready(function()  {
                    //注意这里最好在文档加载完成的时候再获取元素，否则可能获取到的一直是null
                    setOnloadCallBask(document.getElementById("ifActionResult"),'load',ActionHandler);
                });


/**
 * Created by Administrator on 2018/2/2.
 */
