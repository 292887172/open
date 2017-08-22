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

        /**
         * 提交基本信息表单
         * @constructor
         */
        $scope.showHide=function () {
            var a=$("#selectCommand").val();
            if (a=='是'){
                $("#mylabel1").hide();
                $("#mylabel2").show();
            }
            else {
                $("#mylabel2").hide();
                $("#mylabel1").show();
            }
        };
        $scope.SubmitInfoForm = function () {
            var productImg = $("#productImg");
            $scope.infoFormData.app_device_value=$("#secondDevType option:selected").val();
            if (!startWith(productImg.attr("src"), "http://dldir.56iq.net")){
                $.ajaxFileUpload({
                    url: "http://dldir.56iq.net/api/upload/?type=callback&t="+new Date().getTime(),
                    fileElementId: "productImgFile",
                    dataType: 'json',
                    success: function (data) {
                        $scope.infoFormData.app_logo = data;
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
