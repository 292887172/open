/**
 * Created by achais on 15/9/8.
 */
'use strict';

angular.module('Product.main', ['ngRoute'])

    .controller('MainCtrl', ['$scope', "$http", function ($scope, $http) {

        /**
         *
         * @constructor
         */
        $scope.ReleaseProduct = function () {
            $scope.releaseFormData["action"] = "release_product";
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