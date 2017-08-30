'use strict';

angular.module('Product.edit', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/edit', {
            templateUrl: '/static/ng/product/edit/edit.html',
            controller: 'argueCtrl'
        });
    }])
     .controller('argueCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.nav.selected("argueMenu");

        /**
         * 提交配置信息表单
         * @constructor
         */
        $scope.Save = function () {
            if($.trim($('#Stream_ID').val())==''){
					alert("请填写参数ID信息!!");
					return ;
				}
				if($.trim($('#name').val())==''){
					alert("请填写参数名称信息!!");
					return;
				}
				if($.trim($('#mxsLength').val())==''){
					alert("请填写参数长度!!");
					return;
				}
				var min=0;
				var max=0;
				var mxsNum=0;
				var types=document.getElementsByName("paramType");
				var paramDatas=document.getElementsByName("paramData");
				var paramDescs=document.getElementsByName("paramDesc");

				var errorType=-1;
				var mxs=[];
				if(types[0].checked){
					var msg=checkInt();
					if(msg.length>0){
						alert(msg);
						return;
					}
					min=parseInt($.trim($('#minInt').val()));
					max=parseInt($.trim($('#maxInt').val()));
					for(var i=0;i<paramDatas.length;i++){
						var data=$.trim(paramDatas[i].value);
						var desc=$.trim(paramDescs[i].value);
						if(desc=="" || data==""){
							errorType=1;
							break;
						}
						if(parseInt(data) < min || parseInt(data) > max){
							errorType=0;
							break;
						}
						mxs.push({data:data,desc:desc});
					}
					mxsNum=mxs.length+"";
				}
				if(errorType==1){
					alert("请填写数据说明和传送数据!!");
					return;
				}
				if(errorType==0){
					alert("传输数据必须位于最小值"+min+"和最大值"+max+"之间!!");
					return;
				}
				if(types[1].checked){
					var msg=checkFloat();
					if(msg.length>0){
						alert(msg);
						return;
					}
					min=parseFloat($.trim($('#minFloat').val()));
					max=parseFloat($.trim($('#maxFloat').val()));
					for(var i=0;i<paramDatas.length;i++){
						var data=$.trim(paramDatas[i].value);
						var desc=$.trim(paramDescs[i].value);
						if(desc=="" || data==""){
							errorType=1;
							break;
						}
						if(parseFloat(data) < min || parseFloat(data) > max){
							errorType=0;
							break;
						}
						mxs.push({data:data,desc:desc});
					}
				}
				if(errorType==1){
					alert("请填写数据说明和传送数据!!");
					return;
				}
				if(errorType==0){
					alert("传输数据必须位于最小值"+min+"和最大值"+max+"之间!!");
					return;
				}
				var indata={};
				indata.Stream_ID=$.trim($('#Stream_ID').val());
				indata.name=$.trim($('#name').val());
				if(types[0].checked){
					indata.paramType=1;//整数
				}else if(types[1].checked){
					indata.paramType=2;//浮点数
				}else{
					indata.paramType=3;//字符串
				}
				indata.mxs=mxs;
				indata.min=min;
				indata.max=max;
				indata.mxsNum=mxsNum;

				var url=location.href;
                var str=url.split("edit");
                var id;
                if  (str[1]){
                    id=str[1].split("=")[1];
                }
                else {
                    id="";
                }
                indata.id=id;
				if(document.getElementsByName("isControl")[0].checked){
					indata.isControl=1;//可控
				}else{
					indata.isControl=0;//不可控
				}
				if(document.getElementById("state").checked){
					indata.state=1;//启用
				}else{
					indata.state=0;//不启用
				}
				indata.corpName=$.trim($('#corpName').val());
				indata.corpMark=$.trim($('#corpMark').val());
				indata.mxsLength=$.trim($('#mxsLength').val());

				//保存操作
                $.ajax({
                    method: "POST",
                    url: location.href,
                    data: {"name": "save", "d": JSON.stringify(indata)},
                    success:(function (data) {
                    if (data=="modify_success") {
                    	alert("修改成功!");
                    }
                    else if(data=="add_success"){
                    	alert("添加成功!");
                    }
					location.href='#/argue';
                })

                })

        };

        /**
         * 提交重置AppSecret表单
         * @constructor
         */

       }]);
