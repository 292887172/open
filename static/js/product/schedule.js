var being = true;
$(".text-ellipsis .plan-namer").mouseover(function () {
    console.log("触摸啦")
    if(being){
        let w_span = $(this).width();
        if (w_span > 100){
            w_span = 100
        }
        $(this).parent(".text-ellipsis").siblings(".my-tooltip-box").css("left",-(100-w_span)/3 + "px");
        $(this).parent(".text-ellipsis").siblings(".my-tooltip-box").fadeIn();
    }
    being = false
}).mouseout(function () {
    being = true;
    $(this).parent(".text-ellipsis").siblings(".my-tooltip-box").fadeOut();
})

function Save_Party() {
    // 负责方添加
    //设置负责方
    // 负责人信息
    var aa =[]
    $("#ul_id_party input[type='text']").each(function(){

        aa.push({"title":$(this).val()})
      });
    console.log(app_id1)
    console.log(aa)

    var json_a = JSON.stringify(aa);

    $.ajax({
         url: '/product/party',
         type:"POST",
         data:{"key":keysss,"app_id":app_id1,"listed":json_a},
         success:function (data) {
             data = JSON.parse(data)
             console.log(data)
         }
    })
}

function open_plans(val) {
    var my_mask = $("<div></div>");
    my_mask.attr('id','mask-box');
    my_mask.appendTo("body");
    //新增计划
    if (val == 'new'){
        $("#newplans-window").fadeIn();
        var num = document.getElementById("ul_id").getElementsByTagName("li").length + 1 ;
        document.getElementById("hides").value = num
        ontimes()

    }
    //编辑计划
    if (val == 'edit'){
        $("#newplans-window").fadeIn();
        var ifnot = document.getElementsByClassName("task-ack-name")[0]
        console.log(ifnot)
        document.getElementById("news-plan-name").value= document.getElementsByClassName("task-plan-name")[0].innerHTML.replace(/[ /d]/g, '')
        document.getElementById("news-plan-remarks").value= document.getElementsByClassName("remarks")[0].innerHTML.split("：")[1]
        document.getElementById("hides").value = document.getElementsByClassName("task-id-name")[0].innerHTML
        $("#plans-users").val(document.getElementsByClassName("names")[0].innerHTML)
        ontimes(document.getElementsByClassName("times")[0].innerHTML)
    }
}

function add_user(){
    var my_mask = $("<div></div>");
    my_mask.attr('id','mask-box');
    my_mask.appendTo("body");
    $("#plans-user-list").fadeIn();
}
//关闭计划弹窗
$("#newplans-window i,.news-plan-btn .close-info").click(function () {
    $("#mask-box").remove();
    $("#newplans-window").fadeOut();
})

//点击计划弹窗确定
function upto_plans_info(){
    var plans_name = $("#news-plan-name").val();  //获取计划名称
    var plans_user = $("#plans-users").val();     //获取负责人名称
    var plans_time = $("#test15").val();          //获取计划时间
    var plans_remarks = $("#news-plan-remarks").val();  //获取备注

    console.log(plans_name,plans_user,plans_time,plans_remarks)
    if (plans_name == ""){
        layer.msg('请填写计划名称', {icon: 5,time:2000});
        return
    }
    if (plans_user == ""){
        layer.msg('请填写负责人名称', {icon: 5,time:2000});
        return
    }
    if (plans_time == ""){
        layer.msg('请填写计划时间', {icon: 5,time:2000});
        return
    }
    var idd = document.getElementById("hides").value
    console.log(idd,plans_user,plans_remarks,plans_time,plans_name)
    $.ajax({
         url: '/product/schedule',
         type:"POST",
         data:{"key":keysss,"action":"save","num":idd,"plans_name":plans_name,"plans_time":plans_time,"plans_user":plans_user,"plans_remarks":plans_remarks},
         success:function(data){
             console.log('xxxx')
             var ul_list = $("#ul_id")
             var addtr = $(
                      "<li class=\"div-flex ng-scope\">\n" +
                 "    <div class=\"plans-user-info div-flex\" data=\""+idd+"\" ng-click=\"Show_Detail_Plan(x."+ idd +")\">\n" +
                 "        <div style=\"font-size: 16px;\" class=\"ng-binding\">"+idd+"</div>\n" +
                 "        <div class=\"name\">\n" +
                 "            <p class=\"text-ellipsis\"><span class=\"plan-namer ng-binding\">"+plans_user+"</span></p>\n" +
                 "            <div class=\"my-tooltip-box show_div\">\n" +
                 "                <div class=\"my-ant-tooltip-inner ng-binding\">'负责人':\"+plans_user+\"</div>\n" +
                 "                <div class=\"my-ant-tooltip-arrow\"></div>\n" +
                 "            </div>\n" +
                 "        </div>\n" +
                 "        <div class=\"file-info\">\n" +
                 "            <span class=\"text-ellipsis ng-binding\">"+ plans_name +"</span>\n" +
                 "            <img src=\"http://storage.56iq.net/group1/M00/47/45/CgoKQ1thRrOAUQJIAAAET_wItzE030.png\">\n" +
                 "        </div>\n" +
                 "    </div>\n" +
                 "    <div class=\"confirm-info\">\n" +
                 "       \n" +
                 "       <p ng-if=\"x.ack==0\" data=\"0\" style=\"color: #2385ff;\" class=\"plans_comfirm ifnot ng-scope\" ng-click=\"Save_Plan(x.\"+ idd +\")\">确认</p>\n" +
                 "    </div>\n" +
                 "</li>"
                )
             addtr.appendTo(ul_list)
         }
    })
    layer.msg('新建成功', {icon: 1,time:2000});
    $("#mask-box").remove();
    $("#newplans-window").fadeOut();
}

// 上传一系列
function doUploadFile() {
    // 时间戳
    var idd = document.getElementsByClassName("task-id-name")[0].innerHTML
    var formData = new FormData();
    formData.append("file", document.getElementById("file").files[0]);
    formData.append("name", 'upload');
    formData.append("key", keysss);
    formData.append("id", idd);
    var thref = location.href
    formData.append("location", thref);

    if (document.getElementById("file").files[0]) {
        $.ajax({
            url: '/product/upload_file',
            type: "POST",
            data: formData,
            contentType: false,
            processData: false,
            xhr:function () {
                console.log("开始上传")
              var myXhr = $.ajaxSettings.xhr();
              if(myXhr.upload){
                myXhr.upload.addEventListener('progress',progressHandlingFunction, false)
              }
              return myXhr
            },
            success:function (data) {
            console.log("上传成功")
            data = JSON.parse(data)
            if (data['code'] == 0) {

                document.getElementsByClassName("close")[0].click();

                bootbox.alert('上传成功')
                 var file_list = $(".upfile")[0]
                 var addtr = $(
                        "<div class=\"file-list\">\n" +
                        "                    <div class=\"div-flex file-box\">\n" +
                        "                        <a class=\"file-name text-ellipsis\" href=\"/product/download?url="+ data['urll'] +"&name="+ data['filename'] +"\">"+ data['filename'] +"</a>\n" +
                        "                        <p class=\"file-user text-ellipsis\">"+ data['user'] +"</p>\n" +
                        "                        <p class=\"file-time\">"+ data['date'] +"</p>\n" +
                        "                        <p class=\"file-dell\" onclick='Deleted(this)'>删除</p>\n" +
                        "                    </div>\n" +
                        "                </div>"
                    )
                    addtr.appendTo(file_list)
            } else {
                document.getElementsByClassName("close")[0].click();
                bootbox.alert('上传失败，文件格式不支持')
            }
        }
        })
    } else {
        bootbox.alert('不能为空')
    }
}
function progressHandlingFunction(e){
    if(e.lengthComputable){
        var percent = e.loaded/e.total*100;
        let my_precent_data = percent.toFixed(2);
        if (my_precent_data >99){
            my_precent_data = 99;
        }
        $('#progress-text').html(my_precent_data + "%");
        $('#progress').css('width', my_precent_data + "%");
    }
}

var upto_file = $("#file");
var upto_text = $(".modal-name");
upto_file.on('change',function (e) {
    let upto_name = e.currentTarget.files[0].name;
    upto_text.text(upto_name);
    upto_text.attr('title',upto_name);
    $(".my_container").slideDown();
})

function Deleted(that) {
   var idd = document.getElementsByClassName("task-id-name")[0].innerHTML
   var filename =that.parentNode.firstElementChild.innerHTML
   $.ajax({
       url: '/product/schedule',
       type:"POST",
       data:{"key":keysss,"action":"del","del_id":idd,"del_filename":filename},
       success: function (data) {
       data = JSON.parse(data)
       if (data['code']===0){
           bootbox.alert("删除成功")
           window.location.reload()
       }else{
           bootbox.alert("删除失败")
       }

   }
   })
}
//关闭负责人弹窗
$("#plans-user-list i").click(function () {
    $("#mask-box").remove();
    $("#plans-user-list").fadeOut();
})

//时间范围实例
ontimes()
function ontimes(mytime){
    layui.use('laydate', function(){
        var laydate = layui.laydate;

        laydate.render({
        elem: '#test15'
        ,range: '到'
        ,value: mytime
        ,format: 'yyyy-MM-dd'
        ,done: function(value, date, endDate){
            console.log(value, date, endDate); //在控件上弹出value值
          }
        });
    });
}

//添加负责人
$(".plans-user-add").click(function () {
    let myuser_add = $("<li><input type='text' value=''><button class='my-user-del'>删除</button></li>");
    myuser_add.appendTo(".my-user-list ul")
})

    //点击负责方弹窗保存
    $(".user-btn-keep button").click(function () {
        $("#mask-box").remove();
        $("#plans-user-list").fadeOut();
    })

    //点击删除计划
    $("#dell_plan").click(function () {
        var idd = document.getElementsByClassName("task-id-name")[0].innerHTML
        layer.confirm('确定删除计划？', {
            btn: ['确定', '取消'] //按钮
        }, function () {
            console.log("确定",idd);
            $.ajax({
               url: '/product/schedule',
               type:"POST",
               data:{"key":keysss,"action":"delxu","del_id":idd},
               success:function (data) {
                   data = JSON.parse(data)
                   if (data['code']===0){
                       layer.msg('删除成功', {icon: 1,time:2000});
                       window.location.reload()
                   }else{
                       bootbox.alert("删除失败")
                   }
               }
           })

        }, function () {
            console.log("取消",idd);
        })
    })

    //点击确定计划
    $(".plans_comfirm").click(function () {
        var idd = document.getElementsByClassName("task-id-name")[0].innerHTML
        layer.confirm('确认提交计划？', {
            btn: ['确定', '取消'] //按钮

        }, function () {
            console.log("确定",idd);
            layer.msg('已确认', {icon: 1,time:2000});
        }, function () {
            console.log("取消",idd);
        })
    })

    //点击删除附件
    $(".file-list .file-dell").click(function () {
        layer.confirm('确认删除附件？', {
            btn: ['确定', '取消'] //按钮
        }, function () {
            console.log("确定");
            layer.msg('已删除', {icon: 1,time:2000});
        }, function () {
            console.log("取消");
        })
    })