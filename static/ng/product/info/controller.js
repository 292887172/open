'use strict';

angular.module('Product.info', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/info', {
            templateUrl: '/static/ng/product/info/main.html',
            controller: 'InfoCtrl'
        });
    }])
    .directive("fileread", [function () {
        return {
            scope: {
                fileread: "="
            },
            link: function (scope, element, attributes) {
                element.bind("change", function (changeEvent) {
                    var reader = new FileReader();
                    reader.onload = function (loadEvent) {
                        scope.$apply(function () {
                            scope.fileread = loadEvent.target.result;
                        });
                    };
                    reader.readAsDataURL(changeEvent.target.files[0]);
                });
            }
        }
    }])
    .controller('InfoCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.nav.selected("infoMenu");
        $scope.productImgSrc = "";

        var startWith = function (s, srceen) {
            if (s == null || srceen == "" || s.length == 0 || srceen.length > s.length) return false;
            if (s.substr(0, srceen.length) == srceen) return true;
            else return false;
        };

        // 一开始获取产品的设备类型，如果是普通app就不显示出指令类型选择
        if ($scope.infoFormData.app_group=='1'){
            $('#command-type').css("display","none");
        }
        else {
            $('#command-type').css("display","block");
        }

        // 类似的将根据指令类型显示出提示
        if ($("#selectCommand").val()=='是'){
            $("#my-label-2").show();
        }
        else {
            $("#my-label-1").show();
        }

        //指令提示功能根据选择不同，将不同提示显示
        $scope.showHide=function () {
            var a=$("#selectCommand").val();
            if (a=='是'){
                $("#my-label-1").hide();
                $("#my-label-2").show();
            }
            else {
                $("#my-label-2").hide();
                $("#my-label-1").show();
            }
        };
        $scope.HideCommand=function () {
            var a=$("#product_type option:selected").val();
             a= a.split('string:')[1];
            if (a=='1'){
                $('#command-type').css("display","none");
            }
            else {
                $('#command-type').css("display","block");
            }
        };
        $scope.change=function () {
            var value = $("#secondProType option:selected").val();
            var type_name = value.split('string:')[1];
            var html = '';
            if(type_name =='厨房类'){
                html = '<option value="1">油烟机</option><option value="2">集成灶</option><option value="6">冰箱</option>' +
                    '<option value="11">烤箱</option><option value="20">蒸箱</option><option value="22">电磁灶</option>'
            }
            else if(type_name =='卫浴类'){
                html = '<option value="12">马桶</option><option value="19">饮水机</option>'
            }
            $("#secondDevType").html(html);
        };
        /**
         * 提交基本信息表单
         * @constructor
         */
        $scope.SubmitInfoForm = function () {
            var productImg = $("#productImg");
            $scope.infoFormData.app_device_value = $("#secondDevType option:selected").val();
            if (!startWith(productImg.attr("src"), "http://dldir.56iq.net")){
                $.ajaxFileUpload({
                    url: "http://dldir.56iq.net/api/upload/?type=callback&t="+new Date().getTime(),
                    fileElementId: "productImgFile",
                    dataType: 'json',
                    success: function (data) {
                        if (data!='undefined'){
                            $scope.infoFormData.app_logo = data;
                        }
                    },
                    error: function (data, status, e) {
                        console.log(status);
                    },
                    complete: function (res) {
                        $scope.infoFormData.action = "update_info";
                        $http({
                            method: "POST",
                            url: location.href,
                            data: $.param($scope.infoFormData),
                            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
                        }).success(function (data) {
                            if(data.code == 10000) {
                                window.location.reload();
                            }
                        }).error(function (error) {
                            alert(error);
                        })
                    }
                });
            }else{
                $scope.infoFormData.action = "update_info";
                $scope.infoFormData.app_logo = "";
                $http({
                    method: "POST",
                    url: location.href,
                    data: $.param($scope.infoFormData),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
                }).success(function (data) {
                    if(data.code == 10000) {
                        window.location.reload();
                    }
                }).error(function (error) {
                    alert(error);
                })
            }

        };
    }]);
