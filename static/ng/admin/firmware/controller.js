
'use strict';


angular.module('Admin.firmware', ['ngRoute', 'ngDialog'])


    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/firmware', {
            templateUrl: '/static/ng/admin/firmware/device.html',
            controller: 'firmwareAddCtrl'
         })
    }])


    .controller('firmwareAddCtrl', ['$scope', '$http', "ngDialog", function ($scope, $http, ngDialog) {
        // 对话框
        $scope.responses = 1;
        var xx=0;

        if (xx==0){
             $.ajax({
                 url: '/center/doc_firmware',
                 type: "GET",
                 success:function (response) {
                     response = JSON.parse(response)
                     $scope.responsess=response
                     $scope.$apply()
                     console.log('data',$scope.responsess)

                 }
            })
        }
        $scope.Del = function (that) {
            console.log(that)
            $.ajax({
                url: '/center/doc_firmware'+ '?' + "id=" + that,
                type: "POST",
                success:function (data) {
                    window.location.reload()
                }
            })
        }


    }]);




