'use strict';

angular.module('Product.content', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/content', {
            templateUrl: '/static/ng/product/content/main.html',
            controller: 'ContentCtrl'
        });
    }])
    .controller('ContentCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.nav.selected("contentMenu");
        $("#loadingDiv").hide();
        $scope.click = function(ele){
          if (ele == 0 || ele ==-1){
              bootbox.confirm("申请发布后产品信息不可更改，确定申请？", function (result) {
                  if(result){
                      $scope.ReleaseProduct();
                  }
              })
          }
          else if(ele == 1){
              bootbox.confirm("确定取消发布？", function (result) {
                  if(result){
                      $scope.CancelReleaseProduct();
                  }
              })
          }
          else if(ele == 2){
              bootbox.confirm("是否下架产品？", function (result) {
                  if(result){
                       $scope.OffProduct();
                  }
              })
          }
        };
        $scope.ReleaseProduct = function () {
            $scope.releaseFormData["action"] = "release_product";
            if(!$scope.band_name)
            {
                bootbox.alert("该产品没有选择品牌暂不能发布，请为产品添加品牌!");
                return;
            }
            $http({
                method: "POST",
                url: location.href,
                data: $.param($scope.releaseFormData),
                headers: {'Content-Type': 'application/x-www-form-urlencoded' }
            }).success(function (data) {
                if(data.code == 10000) {
                    window.location.href="/product/list";
                }
            }).error(function (error) {
                alert(error);
            })
        };
        /**
         *
         * @constructor
         */
        $scope.CancelReleaseProduct = function () {
            $scope.cancelReleaseFormData["action"] = "cancel_release_product";
            $http({
                method: "POST",
                url: location.href,
                data: $.param($scope.cancelReleaseFormData),
                headers: {'Content-Type': 'application/x-www-form-urlencoded' }
            }).success(function (data) {
                if(data.code == 10000) {
                    window.location.href="/product/list";
                }
            }).error(function (error) {
                alert(error);
            })
        };

        /**
         *
         * @constructor
         */
        $scope.OffProduct = function () {
            $scope.offFormData["action"] = "off_product";
            $http({
                method: "POST",
                url: location.href,
                data: $.param($scope.offFormData),
                headers: {'Content-Type': 'application/x-www-form-urlencoded' }
            }).success(function (data) {
                if(data.code == 10000) {
                    window.location.href="/product/list";
                }
            }).error(function (error) {
                alert(error);
            })
        };
    }]);
