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
        $scope.errorType = -1;
        $scope.errorData = null;
        $scope.flag = 'int';
        $scope.mxs = [];
        $scope.min=0;
        $scope.max=0;
        $scope.mxsNum=0;

        /**
         * 提交配置信息表单
         * @constructor
         */
		$scope.save_mxs = function (paramDatas,paramDescs,paramUI,isdefault) {
			for(var i=0;i<paramDatas.length;i++){
				var data=$.trim(paramDatas[i].value);
				var desc=$.trim(paramDescs[i].value);
				console.log('xx',data,desc)
				var control=$.trim(paramUI[i].value);
				var role=/^[0-9]*$/;
				if(desc=="" || data=="" ){
					$scope.errorType=1;
					break;
				}
				if(role.test(data)==false){
					$scope.errorType=-2;
					break;
				}
				if(!isdefault && edit_data["Stream_ID"]=="MODEL" && $("#device_type").val()==11 && parseInt(data)<=100){
					$scope.errorType=-3;
					break;
				}
				if($scope.flag == 'int'){
					if(parseInt(data) < $scope.min || parseInt(data) > $scope.max){
						$scope.errorType=0;
						break;
					}
				}
				else if ($scope.flag == 'error'){}
				var trig = getTrigger(data);
				$scope.mxs.push({data:data,desc:desc,trigger:trig,control:control});
			}
        };
        $scope.Save = function () {
        	var state = checkID();
			if (state !='correct' || !checkName()){
				return;
			}
			if($.trim($('#mxsLength').val())==''){
				$('#checkLength').html("长度不能为空!!");
				$('#checkLength').css("display","block");
				return ;
			}
			$scope.errorType = -1;
			$scope.mxs = [];
			$scope.min=0;
			$scope.max=0;
			$scope.mxsNum=0;
			$scope.flag = 'int';
			var types=document.getElementsByName("paramType");
			var paramDatas=document.getElementsByName("paramData");
			var paramDescs=document.getElementsByName("paramDesc");
			var paramUI=document.getElementsByName("paramUI");
			var paramDatas1=document.getElementsByName("paramData1");
			var paramDescs1=document.getElementsByName("paramDesc1");
			var paramUI1=document.getElementsByName("paramUI1");

			if(types[0].checked){
				var msg = checkBool();
				if (msg.length>0){
					return;
				}
				$scope.min=0;$scope.max=1;
			}
			else if(types[1].checked){
				var error_value = $.trim($('#errorValue').val());
				$scope.flag = "error";
				$scope.errorData = error_value;
				$scope.min=parseInt($.trim($('#minInt').val()));
				$scope.max=parseInt($.trim($('#maxInt').val()));
			}
			else if(types[2].checked){
				var msg=checkInt();
				if(msg.length>0){
					return;
				}
				$scope.min=parseInt($.trim($('#minInt').val()));
				$scope.max=parseInt($.trim($('#maxInt').val()));
				$scope.step=parseInt($.trim($('#amount').val()));
				//
			}
			else if (types[3].checked) {
				var msg=checkTimer();
				if(msg.length>0){
					return;
				}
				$scope.min=parseInt($.trim($('#minTimer').val()));
				$scope.max=parseInt($.trim($('#maxTimer').val()));
			}
			$scope.save_mxs(paramDatas,paramDescs,paramUI,true);
			$scope.save_mxs(paramDatas1,paramDescs1,paramUI1,false);
			$scope.mxsNum=$scope.mxs.length+"";
			if($scope.errorType==1){
				$('#checkArgue1').css("display","block");
				$('#checkArgue1').html("请填写数据说明和传送数据");
				return;
			}
			if($scope.errorType==0){
				$('#checkArgue1').css("display","block");
				$('#checkArgue1').html("传输数据必须位于最小值"+$scope.min+"和最大值"+$scope.max+"之间!!");
				return;
			}
			if($scope.errorType==-2){
				$('#checkArgue1').css("display","block");
				$('#checkArgue1').html("传输数据必须是数字！！");
				return;
			}
			if($scope.errorType==-3){
				$('#checkArgue1').css("display","block");
				$('#checkArgue1').html("请保持自定义参数值大于100！！");
				return;
			}
			var indata={};
			indata.Stream_ID=$.trim($('#Stream_ID').val());
			indata.name=$.trim($('#name').val());
			if(types[0].checked){
				indata.paramType=1;// 开关型
			}else if(types[1].checked){
				indata.paramType=3;//故障类型

			}else if(types[2].checked){
				indata.paramType=4;//整数
				indata.step = $scope.step
			}
			else if(types[3].checked){
				indata.paramType=5;//定时型
			}
			if($scope.errorData){
				indata.errorData = $scope.errorData;
			}
			indata.min=$scope.min;
			indata.max=$scope.max;
			indata.mxs=$scope.mxs;
			indata.mxsNum=$scope.mxsNum;
			if(!edit_data){
				indata.standa_or_define = 1;
			}
			var url=location.href;
			var str=url.split("edit");
			var id;
			if  (document.getElementById("vid")){
				id=document.getElementById("vid").value;
			}
			else {
				id='';
			}
			indata.id=id;
			if(document.getElementsByName("isControl")[0].checked){
				indata.isControl=1;//可控
			}else{
				indata.isControl=0;//不可控
			}
			if(document.getElementsByName("isFunction")[0].checked){
				indata.isFunction=1;//功能按钮
			}
			else{
				indata.isFunction=0;//属性按钮
			}
			indata.corpName=$.trim($('#corpName').val());
			indata.corpMark=$.trim($('#corpMark').val());
			indata.mxsLength=$.trim($('#mxsLength').val());

			//保存操作
			var msg_notice = '<div class="notification notification-success"><div class="notification-content" role="alert"><div class="notification-message">保存成功！</div><div class="notification-action"></div></div></div>';
			$.ajax({
				method: "POST",
				url: location.href,
				data: {"name": "save", "d": JSON.stringify(indata)},
				success:(function (data) {
				if (data=="modify_success") {
					console.log(location.href)
					var tt = location.href;
					var p = tt.split("#/")[1];
					console.log(p)
					if (p == "argue"){
						document.getElementsByClassName("main-container")[1].style.display='none'
            			document.getElementsByClassName("main-container")[0].style.display=''
						$("#grid-table").jqGrid({
                            postData:{"name": "list"},
                        }).trigger("reloadGrid")
					}else{
						location.replace("#/argue")
					}

					layer.msg('编辑成功', {icon: 6, time: 2000});

				}
				else if(data=="add_success"){

					console.log("申请审核该功能!");
				}

				setTimeout(function () {
					$(".notification-container").html('');
					location.href="#/argue"
				},2000);

			})

			})

        };

        /**
         * 提交重置AppSecret表单
         * @constructor
         */

       }]);
