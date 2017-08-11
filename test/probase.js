/**
 * Created by rdy on 8/9/17.
 */
/**
 * 产品基本信息修改页面js对象;
 * @type {{}}
 * @author cdluojs
 * @since 2015-1-16
 */
var productBaseInfoJS = {};
/**
 * 为保存产品检查输入项;
 * @param url
 *
 */
productBaseInfoJS.checkForSave = function(actionType)
{
    // 组装产品参数;
    var jsonData = {};
    // 产品名称;
    var productName = $("#productNameText").val();
    productName = $.trim(productName);
    if(!productName)
    {
        $("#productNameTips").html("产品名称不能为空");
        $("#productNameTips").show();
        return false;
    }
    if(!iJS.checkStr(productName, "inVal"))
    {
        $("#productNameTips").html("产品名称格式不正确，不能包含特殊字符");
        $("#productNameTips").show();
        return false;
    }
    if(productName.length > 18)
    {
        $("#productNameTips").html("产品名称超长");
        $("#productNameTips").show();
        return false;
    }
    // 产品品牌;
    var brandId = $("#brandAddText").attr("name");
    // 产品型号;
    var productModel = productBaseInfoJS.getModels();
    if(!productModel)
    {
        $("#productModelTips").html("型号不能为空");
        $("#productModelTips").show();
        return false;
    }
    // 产品描述;
    var productDescription = $("#productDescriptionlText").val();
    productDescription = $.trim(productDescription);
    if(!productDescription)
    {
        $("#productDescriptionlTips").html("产品描述不能为空");
        $("#productDescriptionlTips").show();
        return false;
    }
    var productDescriptionUrl = $("#productDescriptionlUrl").val();
    productDescriptionUrl = $.trim(productDescriptionUrl);
    if(productDescriptionUrl && productDescriptionUrl.length > 512)
    {
        $("#productDescriptionlUrlTips").html("产品描述url超长，字符长度不能超过512");
        $("#productDescriptionlUrlTips").show();
        return false;
    }
    if(productDescriptionUrl && (productDescriptionUrl.indexOf("http://") !=0 && productDescriptionUrl.indexOf("https://") !=0))
    {
        $("#productDescriptionlUrlTips").html('产品描述url,请以"http://"或者"https://"开头');
        $("#productDescriptionlUrlTips").show();
        return false;
    }

    if(!iJS.checkStr(productDescription, "inVal"))
    {
        $("#productDescriptionlTips").html("产品描述格式不正确，不能包含特殊字符");
        $("#productDescriptionlTips").show();
        return false;
    }
    // 产品图片;
    var productImg = $("#upload-input-id").val();
    if(!productImg)
    {
        $("#productImgTips").html("产品图标不能为空");
        $("#productImgTips").show();
        return false;
    }
    // 网关配件添加方式;
    if($("#gwSubAddTypeSel").length > 0)
    {
        var gwSubAddType = $("#gwSubAddTypeSel").val();
        if(!gwSubAddType || isNaN(gwSubAddType))
        {
            $("#gwSubAddTypeSelTips").html("设备添加方式不能为空");
            $("#gwSubAddTypeSelTips").show();
            return false;
        }
        jsonData.gwSubAddType = gwSubAddType;
    }
    // 产品WIFI code;
    if($("#productConfigTypeCodeText").length > 0)
    {
        var productConfigTypeCode = $("#productConfigTypeCodeText").val();
        productConfigTypeCode = $.trim(productConfigTypeCode);
        if(!productConfigTypeCode)
        {
            $("#productConfigTypeCodeTips").html("产品联网方式编码不能为空");
            $("#productConfigTypeCodeTips").show();
            return false;
        }
        // 判断是否为正确的类型;
        if($("#productConfigTypeCodeDesc").html() == "")
        {
            $("#productConfigTypeCodeTips").html("产品联网方式编码不正确");
            $("#productConfigTypeCodeTips").show();
            return false;
        }
        jsonData.productConfigTypeCode = productConfigTypeCode;
    }
    // 产品WIFI模块产品device id;
    var moduleDeviceId = $("#moduleDeviceIdText").val();
    moduleDeviceId = $.trim(moduleDeviceId);
    jsonData.moduleDeviceId = moduleDeviceId;
    // 产品配置说明;

    if($(".onekey_tab").is(":visible") ){
        if( productBaseInfoJS.buildManualStep("onekey",jsonData) != 0){
            if( productBaseInfoJS.buildManualStep("onekey",jsonData) == -1){
                $("#productManualTips").html("一键配置步骤操作不能为空");
                $("#productManualTips").show();
                return false;
            }else{
                $("#productManualTips").html("一键配置图片不能为空");
                $("#productManualTips").show();
                return false;
            }
        }
    }
    if($(".softap_tab").is(":visible")){
        if( productBaseInfoJS.buildManualStep("softap",jsonData) != 0){
            if( productBaseInfoJS.buildManualStep("softap",jsonData) == -1){
                $("#productManualTips").html("softap步骤操作不能为空");
                $("#productManualTips").show();
                return false;
            }else{
                $("#productManualTips").html("softap图片不能为空");
                $("#productManualTips").show();
                return false;
            }
        }
    }
    if($(".thunder_tab").is(":visible")){
        if( productBaseInfoJS.buildManualStep("thunder",jsonData) != 0){
            if( productBaseInfoJS.buildManualStep("thunder",jsonData) == -1){
                $("#productManualTips").html("thunder步骤操作不能为空");
                $("#productManualTips").show();
                return false;
            }else{
                $("#productManualTips").html("thunder图片不能为空");
                $("#productManualTips").show();
                return false;
            }
        }
    }

    $("#productManualTips").hide();
    // 组装局域网配置;
    productBaseInfoJS.checkLanConfigForJson(jsonData);
    // 如果是发布时的检查，则直接返回结果;
    if(actionType == "releaseCheck")
    {
        return true;
    }
    jsonData.productId = $("#productId").val();
    jsonData.productSecret = $("#productSecret").val();
    jsonData.productName = productName;
    jsonData.brandId = brandId;
    jsonData.productModel = productModel;
    jsonData.productDescription = productDescription;
    jsonData.productImg = productImg;
    jsonData.productDescriptionUrl = productDescriptionUrl;
    jsonData.productUuid = $("#productUuid").val();
    jsonData.secretKey = $("#secretKey").val();
    jsonData.firewareCode = $("#firewareCode").val();
    productBaseInfoJS.saveBaseInfo(jsonData);
};
productBaseInfoJS.buildManualStep = function(type ,data){
    var size;
    if(type == "onekey"){
        size = oneKeyCnt;
    }else if(type == "softap"){
        size = softApCnt;
    }else if(type == "thunder"){
        size = thunderCnt;
    }
   // var size = $("." + type + "Step").size();

    var cnt = 0;
    for(var i = 0; i < size ;i ++){
        if($("#"+type+"Detail" + (i + 1)).length > 0){
            var detail = $("#"+type+"Detail" + (i + 1)).val().replace(/\n|\r\n/g,"<br>");
            var url = $("#"+type+"Img" + (i + 1) ).attr('src');
            if(!detail){
                return -1;
            }
            if(!url){
                return -2;
            }
            eval("data."+type +"Detail" + (cnt + 1) + " = detail");
            eval("data."+ type + "Url" + (cnt + 1) +" = $('#"+type+"Img" + (i + 1) + "').attr('src');");
            cnt++;
        }
    }

    eval("data."+type+"count = cnt;");
    return 0;
}
/**
 * 查询局域网配置，并存入JSON;
 * @param jsonData
 */
productBaseInfoJS.checkLanConfigForJson = function(jsonData)
{
    var productLanVersion = $("#productLanVersionSelect").val();
    if(productLanVersion && productLanVersion!="null")
    {
        jsonData.productLanVersion = productLanVersion;
    }
};

/**
 * 保存产品;
 * @param url
 */
var isSave = false;
productBaseInfoJS.saveBaseInfo = function(jsonData)
{
    if(isSave){
        return;
    }
    isSave = true;
    $.ajax({
        url: "/product/update",
        type: "POST",
        dataType: "json",
        data: jsonData,
        success: function (data)
        {
            isSave = false;
            if(data.code == "200")
            {

                alert("产品基本信息保存成功");
                // 跳至下一页面;
                if($("#callBackMenu").length > 0)
                {
                    $("#callBackMenu").children("a").click();
                }
                else
                {
                    $("#paramInfoMenu").children("a").click();
                }
                // 将基本信息标志置为1表示信息完整;
                $("#baseProductFlag").val("1");
            }
            else
            {
                alert(data.errorMsg);
            }
        }
    });
};
/**
 * 查询WIFI联网识别码;
 */
productBaseInfoJS.checkConfigTypeCode = function ()
{
    var code = $("#productConfigTypeCodeText").val();
    code = $.trim(code);
    if(!code)
    {
        // 当没有识别码时，清空类型名称;
        $("#productConfigTypeCodeDesc").html("");
        $("#moduleDeviceIdText").val("");
        $("#moduleDeviceIdText").css("display", "none");
        $("#wifiSecQ").css("display", "none");
        return;
    }
    // 清空原来的识别码类型;
    $("#productConfigTypeCodeDesc").html("");
    $.ajax({
        //url: "/dev/home/viewConfigType",
        url: "/product/viewConfigType",
        data: "product.configTypeCode=" + code,
        success: function(msg)
        {

            $("#productConfigTypeCodeDesc").html(msg.data.chip_name);
            // 古北需要添加模块deviceid;
            if($("#productConfigTypeCodeText").val() == "D7KHCFQHRFYTMCVQ")
            {
                // 古北处理;
                $("#moduleDeviceIdText").css("display", "");
                $("#moduleDeviceIdText").attr("placeholder", "请输入该模块产品的device id");
                $("#moduleDeviceIdText").attr("title", "请输入该模块产品的device id");
                $("#wifiSecQ").css("display", "");
                $("#wifiSecQ_p").html("此处为古北为您的产品分配的编号，请从模块厂商处获得；");
            }
            else if($("#productConfigTypeCodeText").val() == "U65NUZ3BUYC4SFG9")
            {
                // 海尔处理;
                $("#moduleDeviceIdText").css("display", "");
                $("#moduleDeviceIdText").attr("placeholder", "请输入SDKDeviceType");
                $("#moduleDeviceIdText").attr("title", "请输入SDKDeviceType");
                $("#wifiSecQ").css("display", "");
                $("#wifiSecQ_p").html("此处为海尔为您的产品类别分配的编号；");
            }
            else
            {
                $("#moduleDeviceIdText").val("");
                $("#moduleDeviceIdText").css("display", "none");
                $("#wifiSecQ").css("display", "none");
            }
            // 根据设备的联网类型，查看是否需要保存
            productBaseInfoJS.updateConfigEdit(msg.data.config_type) ;
        }
    });
};
/**
 * 根据联网类型更新配置编辑框
 * @returns
 */
productBaseInfoJS.updateConfigEdit = function(configType){
    if(configType.is_oneconfig_on == 1
        && configType.is_softap_on == 0
        && configType.is_thunder_on == 0 ){
        // 一键
        $(".onekey_tab").show();
        $(".softap_tab").hide();
        $(".thunder_tab").hide();

        $(".onekey_warpper").show();
        $(".softap_warpper").hide();
        $(".thunderConfig_warpper").hide();
        $(".cpinfo ul li").removeClass("cur");
        $(".onekey_tab").addClass("cur");
    }else if(configType.is_oneconfig_on == 0
        && configType.is_softap_on == 1
        && configType.is_thunder_on == 0 ){
        // softAp
        $(".onekey_tab").hide();
        $(".softap_tab").show();
        $(".thunder_tab").hide();

        $(".onekey_warpper").hide();
        $(".softap_warpper").show();
        $(".thunderConfig_warpper").hide();
        $(".cpinfo ul li").removeClass("cur");
        $(".softap_tab").addClass("cur");
    }else if(configType.is_oneconfig_on == 1
        && configType.is_softap_on == 1
        && configType.is_thunder_on == 0){
        // softAp + 一键
        $(".onekey_tab").show();
        $(".softap_tab").show();
        $(".thunder_tab").hide();
        $(".onekey_warpper").show();
        $(".softap_warpper").hide();
        $(".thunderConfig_warpper").hide();

        $(".cpinfo ul li").removeClass("cur");
        $(".onekey_tab").addClass("cur");
    } else{
        $(".onekey_tab").show();
        $(".softap_tab").hide();
        $(".thunder_tab").hide();

        $(".onekey_warpper").show();
        $(".softap_warpper").hide();
        $(".thunderConfig_warpper").hide();

        $(".cpinfo ul li").removeClass("cur");
        $(".onekey_tab").addClass("cur");
    }
};

// 品牌列表数据缓存;
productBaseInfoJS.brandListData = null;
/**
 * 获取品牌列表;
 * @returns {boolean}
 */
productBaseInfoJS.getBrandList = function()
{
    if(productBaseInfoJS.brandListData)
    {
        return;
    }
    $.ajax({
        url: "/brandInfo/getList",
        type: "post",
        dataType: "json",
        data: null,
        success: function (data) {
            if(data.code == "200")
            {
                productBaseInfoJS.brandListData = data.data;
            }
            else
            {
                alert("获取品牌列表失败，请稍后重试！" );
            }
        }
    });
};
// 显示品牌选择层;
productBaseInfoJS.showBrandList = function(ulID, qVal)
{
    $("#" + ulID).show();
    $("#" + ulID).html("");
    if(qVal)
    {
        for(var i=0; i<productBaseInfoJS.brandListData.length; i++)
        {
            var brandName = productBaseInfoJS.brandListData[i].brandName;
            if(brandName.indexOf(qVal) == -1)
            {
                continue;
            }
            $("#" + ulID).append($("<li onclick='productBaseInfoJS.clickQueryDiv(this)' id='"+productBaseInfoJS.brandListData[i].id+"'>"+productBaseInfoJS.brandListData[i].brandName+"</li>"));
        }
    }
    else
    {
        for(var i=0; i<productBaseInfoJS.brandListData.length; i++)
        {
            $("#" + ulID).append($("<li onclick='productBaseInfoJS.clickQueryDiv(this)' id='" + productBaseInfoJS.brandListData[i].id+"'>"+productBaseInfoJS.brandListData[i].brandName+"</li>"));
        }
    }

};
// 点周某个品牌项后操作;
productBaseInfoJS.clickQueryDiv = function(liObj)
{
    var $liObj = $(liObj);
    var $textObj = $liObj.parent().parent().children(":first");
    $textObj.val($liObj.html());
    $textObj.attr("title", $liObj.html());
    $textObj.attr("name", $liObj.attr("id"));
    $liObj.parent().hide();
};
/**
 * 收缩显示产品型号;
 * @type {boolean}
 */
productBaseInfoJS.modelsFlag = true;
productBaseInfoJS.flexModels = function(){
    if(productBaseInfoJS.modelsFlag){
        $(".shoubox").slideToggle();
        $(".shoubox .del").slideToggle();
        $(".shou").animate().toggleClass(".shou sq");
        productBaseInfoJS.modelsFlag = false;
        setTimeout(function(){productBaseInfoJS.modelsFlag = true;
        }, 500);
    }
};
/**
 * 添加型号输入框;
 */
productBaseInfoJS.addModelInputText = function()
{
    // 先展示型号输入框;
    if($(".shoubox").is(":hidden"))
    {
        productBaseInfoJS.flexModels();
    }
    $(".shoubox").append("<p><input type='text' name='productModel' class='ipt2 w280' maxlength='50' placeholder='请输入产品型号' /><input type='button' class='del' onclick='productBaseInfoJS.delModelInputText(this);'></p>");
};
/**
 * 删除型号输入框;
 * @param tO
 */
productBaseInfoJS.delModelInputText = function(tO)
{
    $(tO).parent().remove();
};
/**
 * 获取型号
 */
productBaseInfoJS.getModels = function()
{
    var models = $.trim($("#productModelText").val());
    if(!models)
    {
        return models;
    }
    var modelInputTexts = document.getElementsByName("productModel");
    for(var i=0; i<modelInputTexts.length; i++)
    {
        var modelStr = modelInputTexts[i].value;
        modelStr = $.trim(modelStr);
        if(modelStr)
        {
            models  = models + "#####" + modelStr;
        }
    }
    return models;
};
/**
 * 在发布状态下保存产品型号;
 */
productBaseInfoJS.checkForModelSave = function() {
    $("#tipsWinBox_model").show();
    $(".markLayout").show();
};

/**
 * 删除动态操作步骤
* */
productBaseInfoJS.delItemsButton = function(e){
    $(e).parent().parent().remove();
}
/**
 *用户点击添加操作步骤按钮
 * */
productBaseInfoJS.addManualStep = function(e) {
    var stepWrapper = "." + e + "Step";
    var stepSize = Number( $(stepWrapper).size());

    if(stepSize >= 10){
        return;
    }
    var cnt = 0;
    if(e == "onekey"){
        cnt = oneKeyCnt;
    }else if(e == "softap"){
        cnt = softApCnt;
    }else if(e == "thunder"){
        cnt = thunderCnt;
    }

    var type = e;
    var _step_model=$(".step_model").clone(true);
    _step_model.removeClass("step_model").addClass(type + "Step");
    _step_model.find("textarea").attr("id",type + "Detail" + (cnt + 1)).attr("placeholder","步骤描述" );
    _step_model.find("img").attr("id",type + "Img" + (cnt + 1));
    _step_model.find("a").attr("id",type + "Upload" + (cnt + 1));
    _step_model.find("input").attr("id",type + "uploadInput" + (cnt + 1));
    if(stepSize < 1){
        _step_model.find("button").remove();
    }
    _step_model.show();
    _step_model.insertBefore($("#"+ type+"Add").parent());

    productBaseInfoJS.bindPlupload(type,cnt);
    if(e == "onekey"){
        oneKeyCnt++;
    }else if(e == "softap"){
        softApCnt++;
    }else if(e == "thunder"){
        thunderCnt++;
    }
}
var oneKeyCnt = 1;
var softApCnt = 1;
var thunderCnt = 1;
/**
 * 动态绑定plupload组件
 */
productBaseInfoJS.bindPlupload = function(type,size){
    var runtimesStr = window.attachEvent ? "silverlight,html4" : "html5,flash";
    var manualImgPickerId = type + "Upload" + (size + 1);
    var img = "#" + type + "Img" + (size + 1);
    //实例化一个plupload上传对象
    var manualUploader = new plupload.Uploader({
        runtimes : runtimesStr,
        filters: {
            mime_types : [ //只允许上传图片;
                { title : "Image files", extensions : "jpg,gif,png" }
            ],
            max_file_size : '1024kb', //最大只能上传2M的文件
            prevent_duplicates : false //不允许选取重复文件
        },
        browse_button : manualImgPickerId, //触发文件选择对话框的按钮，为那个元素id
        url : '/dev/mydev/imageUpload', //服务器端的上传页面地址
    });

    //在实例对象上调用init()方法进行初始化
    manualUploader.init();
    //绑定各种事件，并在事件监听函数中做你想做的事
    manualUploader.bind('FilesAdded',function(uploader,files){
        manualUploader.start(); //调用实例对象的start()方法开始上传文件，当然你也可以在其他地方调用该方法
        $(img).css("display", "");
        $(img).attr("src","/images/loading.gif");
        //每个事件监听函数都会传入一些很有用的参数，
        //我们可以利用这些参数提供的信息来做比如更新UI，提示上传进度等操作
    });
    manualUploader.bind('UploadProgress',function(uploader,file){
        //每个事件监听函数都会传入一些很有用的参数，
        //我们可以利用这些参数提供的信息来做比如更新UI，提示上传进度等操作
    });
    manualUploader.bind('Error',function(uploader,errObject){
        alert(errObject.message);
    });
    manualUploader.bind('FileUploaded',function(a1, a2, rsp){
        if(rsp.status != 200)
        {
            alert("图片上传失败:" + rsp.status + "，请重试")
            return false;
        }
        var jssImgUrl = rsp.response;
        $(img).css("display", "");
        if(jssImgUrl.indexOf("<pre>") != -1)   // 判断有无其他字符，有则清理;
        {
            jssImgUrl = jssImgUrl.replace("<pre>", "");
            jssImgUrl = jssImgUrl.replace("</pre>", "");
        }
        jssImgUrl = jssImgUrl.replace("s200x200_", "");
        $(img).attr("src",jssImgUrl);
    });
}

productBaseInfoJS.modelSave = function() {
    // 先关闭确认提示框;
    $('.popBox a.close').click();
    var brandId = $("#brandAddText").attr("name");
    // 组装产品参数;
    var jsonData = {};
    // 品牌组装;
    if(brandId)
    {
        jsonData.brandId = brandId;
    }
    jsonData.id = $("#productId").val();
    jsonData.productModel = productBaseInfoJS.getModels();
    $.ajax({
        url: "/product/updateModel",
        type: "POST",
        dataType: "json",
        data: jsonData,
        success: function (data)
        {
            if(data.code == "200")
            {
                alert("产品更新成功！");
                $("#baseInfoMenu").children("a").click();
            }
            else
            {
                alert("产品更新失败，请稍候再试！");
            }
        }
    });
};
/**
 * 提示已发布产品进行品牌维护;
 */
productBaseInfoJS.showFillBrandTips = function()
{
    var box = new PromptBox({
        title: "完善品牌",
        content: "此产品还没有[品牌]，请在当前页面选择[品牌]后，点击页面下方的[保存]。",
        select: "确定",
        height: "200px;"
    });
    // 绑定关闭事件;
    $(".popBoxNew a.closeNew").click(function () {
        box.hide();
    });
    // 确定按钮回调事件;
    box.select(function () {
        box.hide();
        // 聚焦品牌选择框;
        $("#brandAddText").click();
        $("#brandAddText").focus();
    });
    // 弹出显示窗口;
    box.show();
};

/**
 *  处理切换配置
 */
productBaseInfoJS.checkTab = function(e){
    $(".manualWrapper").hide();

    if("一键配置" == $(e).text()){
        $(".onekey_warpper").show();
    }else if("SoftAp" == $(e).text()){
        $(".softap_warpper").show();
    }else if("ThunderConfig" == $(e).text()){
        $(".thunderConfig_warpper").show();
    }
    $(".cpinfo ul li").removeClass("cur");
    $(e).addClass("cur");

};
// 初始化项;
$(function()
{
    // 绑定各输入框聚集时，隐藏
    $("#productNameText").bind("focus", function()
    {
        $("#productNameTips").hide();
    });
    $("#productModelText").bind("focus", function()
    {
        $("#productModelTips").hide();
    });
    $("#productDescriptionlText").bind("focus", function()
    {
        $("#productDescriptionlTips").hide();
    });
    $("#productConfigTypeCodeText").bind("focus", function()
    {
        $("#productConfigTypeCodeTips").hide();
    });

    $("textarea").each(function(){
        var reg = new RegExp("<br>","g"); //创建正则RegExp对象
        var newstr = $(this).val().replace(reg,"\n");
        $(this).val(newstr);
    });

    if(Number($("#productReleaseState").val()) <= 0){
        // 初始化操作步骤上传图片组件
        var stepSize = Number( $(".onekeyStep").size());
        oneKeyCnt = stepSize + 1;
        for(var i = 0; i < stepSize; i++ ){
            productBaseInfoJS.bindPlupload("onekey",i);
        }

        stepSize = Number( $(".softapStep").size());
        softApCnt = stepSize + 1;
        for(var i = 0; i < stepSize; i++ ){
            productBaseInfoJS.bindPlupload("softap",i);
        }

        stepSize = Number( $(".thunderStep").size());
        thunderCnt  = stepSize + 1;
        for(var i = 0; i < stepSize; i++ ){
            productBaseInfoJS.bindPlupload("thunder",i);
        }
    }
    Number($("#productReleaseState").val()) <= 0
});