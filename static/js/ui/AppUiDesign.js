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
    var fnList = document.querySelector(".fnList");
    // 获取保存的自定义UI配置
    $.ajax({
        type: "GET",
        async: false,
        url: "/api/diy_ui_conf",
        data: {key: device_key},
        success: function (data) {
            if (JSON.stringify(data) != "{}") {
                data.function.forEach(function (item) {
                    renderList.push(item.title);
                    renderName.push(item.name);
                })
                logBtn = data.isLog;
                theme = data.currentTheme;
                configList = data.function;
            } else {
                controlLoad = false;
            }
            $.ajax({ //获取初始化UI配置功能列表
                type: "POST",
                async: false,
                url: "/api/pull_ui_conf",
                data: {key: device_key},
                success: function (data) {
                    initialList = data.data.functions;
                    if (!controlLoad) {
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
            preLog.style.display = "block";
            communicateLog.style.display = "block";
            logTrue.checked = true;
            logFalse.checked = false;
        } else {
            preLog.style.display = "none";
            communicateLog.style.display = "none";
            logTrue.checked = false;
            logFalse.checked = true;
        }
        sortable.innerHTML = "";
        configList.forEach(function (item, index) {
            var display = "block";
            var li = document.createElement("li");
            li.setAttribute("value", renderName[index]);
            li.className = "clearfix ui-state-default";
            var str = '<span class="title preApp pull-left"><i class="iconfont icon-dp_list"></i><span class="">' + renderList[index] + '</span></span><select name="" id="" class="moduleControl pull-left">';
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
        screen.style.backgroundColor = "#FF8312";
        sortable.innerHTML = null;
        for (var i = 0; i < renderList.length; i++) {
            var li = document.createElement("li");
            li.setAttribute("value", renderName[i]);
            li.className = "clearfix ui-state-default";
            var str = '<span class="title preApp pull-left"><i class="iconfont icon-dp_list"></i><span class="">' + renderList[i] + '</span></span><select name="" id="" class="moduleControl pull-left"><option value="medium">中模块</option><option value="big">大模块</option><option value="small">小模块</option><option value="hidden">不显示</option></select><span class="col-md-2 switchIcon lis" data-toggle="modal" data-target="#iconList"><i class="iconfont icon-dp_power2 pull-right"></i><button class="btn pull-right margin iconBtn">选择图标</button></span><span style="display:none;" class="col-md-2 switchBg lis" data-toggle="modal" data-target="#bgList"><img src="/static/image/bg/01.jpg" class="squareBg pull-right"/><button class="btn pull-right margin">选择背景</button></span>';
            li.innerHTML = str;
            sortable.appendChild(li);
        }
    }
    container.appendChild(sortable);
    previewApp();
    toggleBg();
    $("#sortable").sortable({
        stop: function (event, ui) {
            previewApp();
            toggleBg();
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

    //选择主题
    var currentTheme = theme;
    bgs.forEach(function (item) {
        item.addEventListener("click", function (e) {
            bgs.forEach(function (item) {
                item.children[0].textContent = null;
            })
            e.target.textContent = "√"
            currentTheme = e.target.parentNode.getAttribute("value");
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
        previewApp();
    })
    //选择背景模态框
    var ensure = document.querySelector(".ensure");
    ensure.addEventListener("click", function () {
        currentLi.querySelector(".switchBg").querySelector("img").src = currentBg;
        previewApp();
    })

    save.addEventListener("click", function () {
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
    function previewApp() {
        var list = getInfo().function;
        fnList.innerHTML = "";
        list.forEach(function (item, index) {
            var preLi = document.createElement("li");
            var url = "url(" + item.bg + ")";
            if (item.model == "big") {
                var i = document.createElement("i");
                i.style = "color:#fff;margin-top:1px;";
                i.className = "iconfont " + item.icon;
                preLi.appendChild(i);
                preLi.style.paddingTop = "2px";
                preLi.style.backgroundImage = url;
                preLi.style.backgroundSize = "cover";
                preLi.style.height = "4em";
                preLi.style.color = "#000";
                var p = document.createElement("p");
                p.textContent = item.title;
                p.style.marginTop = "6px";
                preLi.appendChild(p);
            }
            if (item.model == "small") {
                var i = document.createElement("i");
                i.style = "color:#fff;margin-top:1px;";
                i.className = "iconfont " + item.icon;
                preLi.appendChild(i);
                preLi.style.paddingTop = "2px";
                preLi.style.backgroundSize = "cover";
                preLi.style.height = "3em";
                preLi.style.color = "#000";
                preLi.style.width = "25%";
                preLi.style.margin = "0 4%";
                preLi.style.backgroundColor = "inherit";
                preLi.style.border = "0";
                var p = document.createElement("p");
                p.textContent = item.title;
                preLi.appendChild(p);
            }
            if (item.model == "medium") {
                var i = document.createElement("i");
                i.style = "color:#fff;margin-top:1px;position:absolute;left:20px;";
                i.className = "iconfont " + item.icon;
                preLi.appendChild(i);
                preLi.style.paddingTop = "2px";
                preLi.style.backgroundSize = "cover";
                preLi.style.height = "1.7em";
                preLi.style.color = "#000";
                var span = document.createElement("span");
                span.textContent = item.title;
                span.style = "margin-left:56%;";
                preLi.appendChild(span);
            }
            if (item.model == "hidden") {
                preLi.style.display = "none";
            } else {
                preLi.style.display = "block";
            }
            fnList.appendChild(preLi);
        })
    }

    //判断是否为大模块，是大模块加模块背景，其他模块取消背景
    function toggleBg() {
        var selectModule = document.querySelectorAll(".moduleControl");
        selectModule = Array.prototype.slice.call(selectModule);
        var switchBg = document.querySelectorAll(".switchBg");
        selectModule.forEach(function (item, index) {
            item.addEventListener("change", function () {
                if (this.value == "big") {
                    switchBg[index].setAttribute("style", "display:block;")
                } else {
                    switchBg[index].setAttribute("style", "display:none;");
                }
                previewApp();
            })
        })
    }


    //获取页面所有属性
    function getInfo() {
        var uploadConfig = {};
        logTrue.checked == false ? uploadConfig.isLog = false : uploadConfig.isLog = true;
        uploadConfig.currentTheme = currentTheme;
        var arr = [];
        var list = document.querySelector("#sortable").querySelectorAll("li");
        list = Array.prototype.slice.call(list);
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