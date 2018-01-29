$(function(){
        // 渲染列表
        var renderList=[];
        var renderName=[];
        var logBtn=false;
        var configList=[];
        $.ajax({
            type: "GET",
            async:false,
            url: "/api/diy_ui_conf",
            data:{key:device_key},
            success: function(data){
                console.log(data);
                data.function.forEach(function(item){
                    renderList.push(item.title);
                    renderName.push(item.name);
                })
                logBtn=data.isLog;
                if(logBtn){
                    document.querySelector("#logTrue").checked=true;
                    document.querySelector("#logFalse").checked=false;
                }else{
                    document.querySelector("#logTrue").checked=false;
                    document.querySelector("#logFalse").checked=true;
                }

                configList=data.function;
            },
            error:function(){
                controlBtn=false;
              console.log("未保存过UI配置,使用初始化UI配置样式");

            }
         });
         var container=document.querySelector(".container");
         var sortable=document.createElement("ul");
         sortable.className="clearfix";
         sortable.id="sortable";
         if(configList[0]){
            configList.forEach(function(item,index){
                var display="block";
                var li=document.createElement("li");
                li.setAttribute("value",renderName[index]);
                li.className="clearfix ui-state-default";
                var str='<span class="title preApp pull-left"><i class="glyphicon glyphicon-align-justify"></i><span class="">'+renderList[index]+'</span></span><select name="" id="" class="moduleControl pull-left">';
                switch(item.model){
                    case "big":str+='<option value="medium">中模块</option><option value="big" selected>大模块</option><option value="small">小模块</option><option value="hidden">不显示</option>',display="block";break;
                    case "medium":str+='<option value="medium" selected>中模块</option><option value="big">大模块</option><option value="small">小模块</option><option value="hidden">不显示</option>',display="none";break;
                    case "small":str+='<option value="medium">中模块</option><option value="big">大模块</option><option value="small" selected>小模块</option><option value="hidden">不显示</option>',display="none";break;
                    case "hidden":str+='<option value="medium">中模块</option><option value="big">大模块</option><option value="small">小模块</option><option value="hidden" selected>不显示</option>',display="none";break;
                    default:str+='<option value="medium">中模块</option><option value="big">大模块</option><option value="small">小模块</option><option value="hidden">不显示</option>',display="none";
                }
                str+='</select><span class="col-md-2 switchIcon lis" data-toggle="modal" data-target="#iconList"><i class="glyphicon '+item.icon+' pull-right"></i><button class="btn pull-right margin iconBtn">选择图标</button></span><span style="display:'+display+'" class="col-md-2 switchBg lis" data-toggle="modal" data-target="#bgList"><img src="'+item.bg+'" class="squareBg pull-right"   /><button class="btn pull-right margin">选择背景</button></span>';
                li.innerHTML=str;
                sortable.appendChild(li);
                getConfig();
            })
         }else{
             $.ajax({
            type: "POST",
            async:false,
            url: "/api/pull_ui_conf",
            data:{key:device_key},
            success: function(data){
                console.log(data);
              var result=data.data.functions;
              result.forEach(function(item){
                renderList.push(item.title);
                renderName.push(item.name);
              })
            }
         });
            for(var i=0;i<renderList.length;i++){
            var li=document.createElement("li");
            li.setAttribute("value",renderName[i]);
            li.className="clearfix ui-state-default";
            var str='<span class="title preApp pull-left"><i class="glyphicon glyphicon-align-justify"></i><span class="">'+renderList[i]+'</span></span><select name="" id="" class="moduleControl pull-left"><option value="medium">中模块</option><option value="big">大模块</option><option value="small">小模块</option><option value="hidden">不显示</option></select><span class="col-md-2 switchIcon lis" data-toggle="modal" data-target="#iconList"><i class="glyphicon glyphicon-off pull-right"></i><button class="btn pull-right margin iconBtn">选择图标</button></span><span style="display:none;" class="col-md-2 switchBg lis" data-toggle="modal" data-target="#bgList"><img src="/static/image/bg/no.png" class="squareBg pull-right"/><button class="btn pull-right margin">选择背景</button></span>';
            li.innerHTML=str;
            sortable.appendChild(li);
         }
         }
        container.appendChild(sortable);
        // 初始预览手机端效果
        var fnList=document.querySelector(".fnList");
        function previewApp(){
            fnList.innerHTML="";
            for(var i=0;i<renderList.length;i++){
            var preLi=document.createElement("li");
            preLi.textContent=renderList[i];
            fnList.appendChild(preLi);
            }
        }
        previewApp();
        $( "#sortable" ).sortable({
            stop:function(event,ui){
                previewAppAgain();
                getConfig();
                var list=sortable.querySelectorAll("li");
                var logTrue=document.querySelector("#logTrue");
                    logTrue.checked==false?uiConfig.isLog=false:uiConfig.isLog=true;
                    uiConfig.currentTheme=currentTheme;
                var functions=[];
                list.forEach(function(item,index){
                    functions[index]=new Object();
                    functions[index].title=item.querySelector(".title").querySelector("span").textContent;
                    functions[index].order=index;
                    functions[index].name=item.getAttribute("value");
                    functions[index].model=item.querySelector(".moduleControl").value;
                    var str=item.querySelector(".switchIcon").querySelector("i").className;
                    var className=str.slice(10,str.length-11);
                    functions[index].icon=className;
                    var img=item.querySelector(".switchBg").querySelector("img")
                    var src=img.src;
                    if(src.slice(src.length-6)=="no.png"){
                        src="null";
                    }else if(src==""){ 
                        src="null";   
                    }
                    functions[index].bg=src;
                })
                uiConfig.function=functions;
                var moduleControl=document.querySelectorAll(".moduleControl");
                var changeModel=fnList.querySelectorAll("li");
                var switchBg=document.querySelectorAll(".switchBg");
                moduleControl.forEach(function(item,index){
                    item.addEventListener("change",function(){
                    if(this.value=="big"){
                        switchBg[index].setAttribute("style","display:block;")
                        changeModel[index].style.height="3em";
                        changeModel[index].style.width="calc(100% - 2px)";
                    }else{
                        switchBg[index].setAttribute("style","display:none;");
                        changeModel[index].style.height="1.3em";
                    }
                    if(this.value=="small"){
                        changeModel[index].style.width="calc(33% - 2px)";
                    }else if(this.value=="hidden"){
                        changeModel[index].style.display="none";
                    }else{
                        changeModel[index].style.display="block";
                    }
                })
    })
            }
        });
        var save=document.createElement("button");
        save.id="save";
        save.textContent="保存";
        container.appendChild(save);
        // RGB颜色转十六进制色
    function RGBToHex(rgb) { 
        var regexp = /^rgb\(([0-9]{0,3})\,\s*([0-9]{0,3})\,\s*([0-9]{0,3})\)/g; 
        var re = rgb.replace(regexp, "$1 $2 $3").split(" "); //利用正则表达式去掉多余的部分  
        var hexColor = "#"; var hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']; 
        for (var i = 0; i < 3; i++) { 
            var r = null; var c = re[i]; 
            var hexAr = []; 
            while (c > 16) { 
                r = c % 16; 
                c = (c / 16) >> 0; 
                hexAr.push(hex[r]); 
            } hexAr.push(hex[c]); 
            hexColor += hexAr.reverse().join(''); 
        } 
        return hexColor; 
    }
    //选择主题
    var bgs=document.querySelectorAll(".bgColor");
    bgs=Array.prototype.slice.call(bgs);
    var currentTheme="#ff8312";
    bgs.forEach(function(item){
        item.addEventListener("click",function(e){
            bgs.forEach(function(item){
                item.children[0].textContent=null;
            })
            e.target.textContent="√";
            currentTheme= RGBToHex(getComputedStyle(e.target.parentNode)["background"]);
        })
    })
    // 选择图标
    var icons=document.querySelector("#icons");
    var currentIcon="";
    icons.addEventListener("click",function(e){
        if(e.target.localName=="i"){
            currentIcon=e.target.className.slice(10);
            items=icons.querySelectorAll("i");
            items=Array.prototype.slice.call(items);
            items.forEach(function(item){
            item.style.color="#666";
            item.style.background="#fff";
        })
        e.target.style.color="#2222ff";
        e.target.style.background="#ccc";
        }
    })
    // 获取当前列表项
    var currentLi="";
    var iconBtns=document.querySelectorAll(".lis");
    iconBtns=Array.prototype.slice.call(iconBtns);
        iconBtns.forEach(function(item){
            item.addEventListener("click",function(e){
                currentLi=e.target.parentNode.parentNode;
            })
        })

    // 选择模块背景
    var changeBg=document.querySelector("#changeBg");
    var currentBg="";
    var imgs=changeBg.querySelectorAll("img");
    imgs=Array.prototype.slice.call(imgs);
    var bigImg=document.querySelector("#bigImg");
    changeBg.addEventListener("click",function(e){
        if(e.target.localName=="img"){
            currentBg=e.target.src;
            imgs.forEach(function(item){
                item.style.padding=0;
                item.style.border=0;
            })
            e.target.style.padding="2px";
            e.target.style.border="1px solid #333";
            bigImg.src=e.target.src;
        }
    })
    // 选择图标模态框
    var confirm=document.querySelector(".confirm");
    confirm.addEventListener("click",function(){
        currentLi.querySelector(".switchIcon").querySelector("i").className="glyphicon "+currentIcon+" pull-right";
    })
    //选择背景模态框
    var ensure=document.querySelector(".ensure");
    ensure.addEventListener("click",function(){
        currentLi.querySelector(".switchBg").querySelector("img").src=currentBg;
    })
    // 生成JSON格式配置文件
    var uiConfig={};
    function getConfig(){
        uiConfig={};
        var functions=[];
        var logTrue=document.querySelector("#logTrue");
        logTrue.checked==false?uiConfig.isLog=false:uiConfig.isLog=true;
        uiConfig.currentTheme=currentTheme;
        var lis=sortable.querySelectorAll("li");
        lis.forEach(function(item,index){
            functions[index]=new Object();
            functions[index].title=renderList[index];
            functions[index].order=index;
            functions[index].name=renderName[index];
            functions[index].model=item.querySelector(".moduleControl").value;
            var str=item.querySelector(".switchIcon").querySelector("i").className;
            var className=str.slice(10,str.length-11);
            functions[index].icon=className;
            var img=item.querySelector(".switchBg").querySelector("img");
            functions[index].bg=img.src;
        })
        uiConfig.function=functions;
    }
    save.addEventListener("click",function(){
        getConfig();
        console.log(uiConfig);
        $.ajax({
            type:"POST",
            url:"/api/upload_ui_conf",
            data:{ key:device_key,
                ui_conf:JSON.stringify(uiConfig)}

        })
    });
    // 预览手机端效果
    function previewAppAgain(){
        var changeModel=document.querySelectorAll(".preApp");
        fnList.innerHTML="";
        for(var i=0;i<changeModel.length;i++){
        var preLi=document.createElement("li");
        preLi.textContent=changeModel[i].querySelector("span").innerText;
        fnList.appendChild(preLi);
        }
    }
    //判断是否为大模块，是大模块加模块背景，其他模块取消背景
    var moduleControl=document.querySelectorAll(".moduleControl");
    moduleControl=Array.prototype.slice.call(moduleControl);
    var changeModel=fnList.querySelectorAll("li");
    var switchBg=document.querySelectorAll(".switchBg");
    moduleControl.forEach(function(item,index){
        item.addEventListener("change",function(){
            if(this.value=="big"){
                switchBg[index].setAttribute("style","display:block;")
                changeModel[index].style.height="3em";
                changeModel[index].style.width="calc(100% - 2px)";
            }else{
                switchBg[index].setAttribute("style","display:none;");
                changeModel[index].style.height="1.3em";
            }
            if(this.value=="small"){
                changeModel[index].style.display="block";
                changeModel[index].style.width="calc(33% - 2px)";
            }else if(this.value=="hidden"){
                changeModel[index].style.display="none";
            }else{
                changeModel[index].style.display="block";
            }
            if(this.value=="medium"){
                changeModel[index].style.height="1.3em";
                changeModel[index].style.width="calc(100% - 2px)";
            }
        })
    })
    //获取页面所有属性
    function getInfo(){
        var arr=[];
        var list=document.querySelector("#sortable").querySelectorAll("li");
        list.forEach(function(item,index){
            arr[index]=new Object();
            arr[index].tilte=item.querySelector(".title").textContent;
            arr[index].module=item.querySelector(".moduleControl").value;
            arr[index].icon=item.querySelector(".switchIcon").querySelector("i").className.slice(0,9);
            arr[index].bg=item.querySelector(".switchBg").querySelector("img").src;
        })
        return arr;
    }
})
