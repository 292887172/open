$(function () {
    // 渲染列表
    var renderList = [];
    var renderName = [];
    var logBtn = false;
    var configList = [];
    var bgs = document.querySelectorAll(".bgColor");
    bgs = Array.prototype.slice.call(bgs);
    var initialList = [];
    var controlLoad = true;
    var theme = "#FF8312";
    var logTrue = document.querySelector("#logTrue");
    var logFalse = document.querySelector("#logFalse");
    var screen = document.querySelector(".screen");
    // 获取保存的自定义UI配置
    $.ajax({
        type: "GET",
        async: false,
        url: "/api/diy_ui_conf",
        data: {key: device_key},
        success: function (data) {
            console.log(data);
            data.function.forEach(function (item) {
                renderList.push(item.title);
                renderName.push(item.name);
            })
            logBtn = data.isLog;
            theme = data.currentTheme;
            configList = data.function;
            $.ajax({ //获取初始化UI配置功能列表
                type: "POST",
                async: false,
                url: "/api/pull_ui_conf",
                data: {key: device_key},
                success: function (data) {
                    initialList = data.data.functions;
                    if (configList.length == initialList.length) {
                        configList.forEach(function (item, index) {
                            var button = false;
                            initialList.forEach(function (value, order) {
                                if (item.title == value.title) {
                                    button = true;
                                }
                            })
                            if (controlLoad) {
                                if (!button) {
                                    controlLoad = false;
                                }
                            }
                        })
                    }
                    if (!controlLoad) {
                        renderList = [];
                        renderName = [];
                        initialList.forEach(function (item) {
                            renderList.push(item.title);
                            renderName.push(item.name);
                        })
                    }
                }
            });
        },
        error: function () {
            controlBtn = false;
            console.log("未保存过UI配置,使用初始化UI配置样式");

        }
    });
    var container = document.querySelector(".container");
    var sortable = document.createElement("ul");
    sortable.className = "clearfix";
    sortable.id = "sortable";
    if (controlLoad) {
        screen.style.backgroundColor = theme;
        bgs.forEach(function (item) {
            var value = item.getAttribute("value");
            item.querySelector("i").textContent = null;
            if (value == theme) {
                item.querySelector("i").textContent = "√";
            }
        })
        if (logBtn) {
            logTrue.checked = true;
            logFalse.checked = false;
        } else {
            logTrue.checked = false;
            logFalse.checked = true;
        }
        sortable.innerHTML = null;
        configList.forEach(function (item, index) {
            var display = "block";
            var li = document.createElement("li");
            li.setAttribute("value", renderName[index]);
            li.className = "clearfix ui-state-default";
            var str = '<span class="title preApp pull-left"><i class="iconfont icon-liebiao7"></i><span class="">' + renderList[index] + '</span></span><select name="" id="" class="moduleControl pull-left">';
            switch (item.model) {
                case "big":
                    str += '<option value="medium">中模块</option><option value="big" selected>大模块</option><option value="small">小模块</option><option value="hidden">不显示</option>', display = "block";
                    break;
                case "medium":
                    str += '<option value="medium" selected>中模块</option><option value="big">大模块</option><option value="small">小模块</option><option value="hidden">不显示</option>', display = "none";
                    break;
                case "small":
                    str += '<option value="medium">中模块</option><option value="big">大模块</option><option value="small" selected>小模块</option><option value="hidden">不显示</option>', display = "none";
                    break;
                case "hidden":
                    str += '<option value="medium">中模块</option><option value="big">大模块</option><option value="small">小模块</option><option value="hidden" selected>不显示</option>', display = "none";
                    break;
                default:
                    str += '<option value="medium">中模块</option><option value="big">大模块</option><option value="small">小模块</option><option value="hidden">不显示</option>', display = "none";
            }
            str += '</select><span class="col-md-2 switchIcon lis" data-toggle="modal" data-target="#iconList"><i class="iconfont ' + item.icon + ' pull-right"></i><button class="btn pull-right margin iconBtn">选择图标</button></span><span style="display:' + display + '" class="col-md-2 switchBg lis" data-toggle="modal" data-target="#bgList"><img src="' + item.bg + '" class="squareBg pull-right"   /><button class="btn pull-right margin">选择背景</button></span>';
            li.innerHTML = str;
            sortable.appendChild(li);
        })
    } else {
        sortable.innerHTML = null;
        for (var i = 0; i < renderList.length; i++) {
            var li = document.createElement("li");
            li.setAttribute("value", renderName[i]);
            li.className = "clearfix ui-state-default";
            var str = '<span class="title preApp pull-left"><i class="iconfont icon-liebiao7"></i><span class="">' + renderList[i] + '</span></span><select name="" id="" class="moduleControl pull-left"><option value="medium">中模块</option><option value="big">大模块</option><option value="small">小模块</option><option value="hidden">不显示</option></select><span class="col-md-2 switchIcon lis" data-toggle="modal" data-target="#iconList"><i class="iconfont icon-liebiao7 pull-right"></i><button class="btn pull-right margin iconBtn">选择图标</button></span><span style="display:none;" class="col-md-2 switchBg lis" data-toggle="modal" data-target="#bgList"><img src="/static/image/bg/no.png" class="squareBg pull-right"/><button class="btn pull-right margin">选择背景</button></span>';
            li.innerHTML = str;
            sortable.appendChild(li);
        }
    }
    container.appendChild(sortable);
    // 初始预览手机端效果
    var fnList = document.querySelector(".fnList");

    function previewApp() {
        fnList.innerHTML = "";
        for (var i = 0; i < renderList.length; i++) {
            var preLi = document.createElement("li");
            preLi.textContent = renderList[i];
            fnList.appendChild(preLi);
        }
    }

    previewApp();
    $("#sortable").sortable({
        stop: function (event, ui) {
            previewAppAgain();
        }
    });
    var backward = document.createElement("button");
    backward.id = "backward";
    backward.textContent = "返回";
    backward.addEventListener("click", function () {
        window.history.back();
    })
    container.appendChild(backward);
    var save = document.createElement("button");
    save.id = "save";
    save.textContent = "保存";
    container.appendChild(save);

    // RGB颜色转十六进制色
    function RGBToHex(rgb) {
        var regexp = /^rgb\(([0-9]{0,3})\,\s*([0-9]{0,3})\,\s*([0-9]{0,3})\)/g;
        var re = rgb.replace(regexp, "$1 $2 $3").split(" "); //利用正则表达式去掉多余的部分  
        var hexColor = "#";
        var hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'];
        for (var i = 0; i < 3; i++) {
            var r = null;
            var c = re[i];
            var hexAr = [];
            while (c > 16) {
                r = c % 16;
                c = (c / 16) >> 0;
                hexAr.push(hex[r]);
            }
            hexAr.push(hex[c]);
            hexColor += hexAr.reverse().join('');
        }
        return hexColor;
    }

    //选择主题
    var currentTheme = theme;
    bgs.forEach(function (item) {
        item.addEventListener("click", function (e) {
            bgs.forEach(function (item) {
                item.children[0].textContent = null;
            })
            e.target.textContent = "√";
            currentTheme = RGBToHex(getComputedStyle(e.target.parentNode)["background"]);
            screen.style.backgroundColor = currentTheme;
        })
    })
    // 选择图标
    var icons = document.querySelector("#icons");
    var currentIcon = "";
    icons.addEventListener("click", function (e) {
        if (e.target.localName == "i") {
            currentIcon = e.target.className.slice(9);
            items = icons.querySelectorAll("i");
            items = Array.prototype.slice.call(items);
            items.forEach(function (item) {
                item.style.color = "#666";
                item.style.background = "#fff";
            })
            e.target.style.color = "#2222ff";
            e.target.style.background = "#ccc";
        }
    })
    // 获取当前列表项
    var currentLi = "";
    var iconBtns = document.querySelectorAll(".lis");
    iconBtns = Array.prototype.slice.call(iconBtns);
    iconBtns.forEach(function (item, index) {
        item.addEventListener("click", function (e) {
            currentLi = e.target.parentNode.parentNode;
            console.log(currentLi.querySelector(".title").querySelector("span").textContent);
        })
    })
    // 选择模块背景
    var changeBg = document.querySelector("#changeBg");
    var currentBg = "";
    var imgs = changeBg.querySelectorAll("img");
    imgs = Array.prototype.slice.call(imgs);
    var bigImg = document.querySelector("#bigImg");
    changeBg.addEventListener("click", function (e) {
        if (e.target.localName == "img") {
            currentBg = e.target.src;
            imgs.forEach(function (item) {
                item.style.padding = 0;
                item.style.border = 0;
            })
            e.target.style.padding = "2px";
            e.target.style.border = "1px solid #333";
            bigImg.src = e.target.src;
        }
    })
    // 选择图标模态框
    var confirm = document.querySelector(".confirm");
    confirm.addEventListener("click", function () {
        currentLi.querySelector(".switchIcon").querySelector("i").className = "iconfont " + currentIcon + " pull-right";
    })
    //选择背景模态框
    var ensure = document.querySelector(".ensure");
    ensure.addEventListener("click", function () {
        currentLi.querySelector(".switchBg").querySelector("img").src = currentBg;
    })

    save.addEventListener("click", function () {
        console.log(getInfo());
        $.ajax({
            type: "POST",
            async: false,
            url: "/api/upload_ui_conf",
            data: {
                key: device_key,
                ui_conf: JSON.stringify(getInfo())
            }

        })
    });

    // 预览手机端效果
    function previewAppAgain() {
        var list=getInfo().function;
        console.log(list);
        fnList.innerHTML = "";
        list.forEach(function(item,index){
            var preLi = document.createElement("li");
            if(item.model=="big"&&item.bg.slice(-6)!="no.png"){
                console.log(1);
                preLi.style.backgroundImage="url("+item.bg+")";
            }
            preLi.textContent =item.title;
            fnList.appendChild(preLi);
        })
    }

    //判断是否为大模块，是大模块加模块背景，其他模块取消背景
    var moduleControl = document.querySelectorAll(".moduleControl");
    moduleControl = Array.prototype.slice.call(moduleControl);
    var changeModel = fnList.querySelectorAll("li");
    var switchBg = document.querySelectorAll(".switchBg");
    moduleControl.forEach(function (item, index) {
        item.addEventListener("change", function () {
            if (this.value == "big") {
                switchBg[index].setAttribute("style", "display:block;")
                changeModel[index].style.height = "3em";
                changeModel[index].style.width = "calc(100% - 2px)";
            } else {
                switchBg[index].setAttribute("style", "display:none;");
                changeModel[index].style.height = "1.3em";
            }
            if (this.value == "small") {
                changeModel[index].style.display = "block";
                changeModel[index].style.width = "calc(33% - 2px)";
            } else if (this.value == "hidden") {
                changeModel[index].style.display = "none";
            } else {
                changeModel[index].style.display = "block";
            }
            if (this.value == "medium") {
                changeModel[index].style.height = "1.3em";
                changeModel[index].style.width = "calc(100% - 2px)";
            }
        })
    })

    //获取页面所有属性
    function getInfo() {
        var uploadConfig = {};
        logTrue.checked == false ? uploadConfig.isLog = false : uploadConfig.isLog = true;
        uploadConfig.currentTheme = currentTheme;
        var arr = [];
        var list = document.querySelector("#sortable").querySelectorAll("li");
        list.forEach(function (item, index) {
            arr[index] = new Object();
            arr[index].name = item.getAttribute("value");
            arr[index].order = index;
            arr[index].title = item.querySelector(".title").textContent;
            arr[index].model = item.querySelector(".moduleControl").value;
            var className = item.querySelector(".switchIcon").querySelector("i").className;
            arr[index].icon = className.slice(9, className.length - 11);
            arr[index].bg = item.querySelector(".switchBg").querySelector("img").src;
        })
        uploadConfig.function = arr;
        return uploadConfig;
    }

})
//显示日志单选框添加事件，App日志预览
var preLog = document.querySelector("#preview").querySelector(".log");
var communicateLog = document.querySelector("#preview").querySelector(".communicateLog");

function previewLog(a) {
    a.value == "true" ? (preLog.style.display = "block", communicateLog.style.display = "block") : (preLog.style.display = "none", communicateLog.style.display = "none");
}