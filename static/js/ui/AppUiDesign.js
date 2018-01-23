$(function(){
        // 截取url参数
        var url="https://oven.53iq.com/static/html/controler.html?d=F0FE6B15E97B&t=1";
        //var url=window.location.href;
        function getUrlParam(url){
            var obj={};
            var str=url;
            var index=str.indexOf("?");
            var newStr=str.slice(index+1);
            var arr=newStr.split("&");
                arr.forEach(function(item){
                    var newArr=item.split("=");
                    obj[newArr[0]]=newArr[1];
                })
             return obj;
        }
        var params=getUrlParam(url);
        // 渲染列表
        var renderList=[];
        var renderName=[];
        $.ajax({
            type: "POST",
            async:false,
            url: "https://oven.53iq.com/api/device/config",
            data:{mac_addr:params.d,device_type: params.t},
            success: function(data){
              var result=data.data.functions;
              result.forEach(function(item){
                renderList.push(item.title);
                renderName.push(item.name);
              })
            }
         });
         var container=document.querySelector(".container");
         var sortable=document.createElement("ul");
         sortable.className="clearfix";
         sortable.id="sortable";
         for(var i=0;i<renderList.length;i++){
            var li=document.createElement("li");
            li.setAttribute("value",renderName[i]);
            li.className="clearfix ui-state-default";
            var str='<span class="title preApp pull-left"><i class="glyphicon glyphicon-align-justify"></i><span class="">'+renderList[i]+'</span></span><select name="" id="" class="moduleControl pull-left"><option value="medium">中模块</option><option value="big">大模块</option><option value="small">小模块</option><option value="hidden">不显示</option></select><span class="col-md-2 switchIcon lis" data-toggle="modal" data-target="#iconList"><i class="glyphicon glyphicon-off pull-right"></i><button class="btn pull-right margin iconBtn">选择图标</button></span><span class="col-md-2 switchBg lis" data-toggle="modal" data-target="#bgList"><img class="squareBg pull-right" /><button class="btn pull-right margin">选择背景</button></span>';
            li.innerHTML=str;
            sortable.appendChild(li);
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
                console.log(getInfo());
                var list=sortable.querySelectorAll("li");
                var logTrue=document.querySelector("#logTrue");
                    logTrue.checked==false?uiConfig.isLog=false:uiConfig.isLog=true;
                    uiConfig.currentTheme=currentTheme;
                var functions=[];
                console.log(list);
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
        return uiConfig;
    }
    save.addEventListener("click",function(){
        getConfig();
        console.log(JSON.stringify(uiConfig));
        $.ajax({
            type:"POST",
            url:"/api/get_ui_conf",
            data:{key:"F0FE6B15E97B",ui_conf:JSON.stringify(uiConfig)},
            dataType:'json',
            contentType: "application/json; charset=utf-8",
            success:function(data){
                console.log(data);
            }
        })
    })
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
