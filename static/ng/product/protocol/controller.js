'use strict';

angular.module('Product.protocol', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/protocol', {
            templateUrl: '/static/ng/product/protocol/protocol.html',

        })
    }])
    .controller('ProtocolCtrl', ['$scope', "$http", function ($scope, $http) {
        var xx = 0;
        if( xx == 0) {
         $http({
                method: "GET",
                url: "/product/protocol/" + '?' +"key=" + $scope.$parent.$parent.key,
                data: {'key': $scope.$parent.$parent.key},
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            })
                .success(function (response) {
                    $scope.response = response;
                })
        }

        $scope.SubmitProtocol = function (scope) {
             $scope.response.key = $scope.$parent.$parent.key;
             $scope.response.action = "update_protocol";
             $scope.response.heart_rate =  $("#input_01").val();
             $scope.response.repeat_rate =  $("#input_02").val();
             $scope.response.repeat_count =  $("#input_03").val();
             //input checked case
             var list_0 = [];
             var for1 = document.getElementsByClassName("bblchk");
             for (var u = 0, lll1 = for1.length; u < lll1; u++) {
                 var obj = for1[u].checked;
                 list_0.push(obj)
            }
             $scope.response.fivechoose = list_0;
             // 获取循环体的value
             var list_1 = [];
             $(".x1x input[value]").each(function () {
                 var v = $(this).val();
                 list_1.push(v);
             });
             $scope.response.frame_content =  list_1;
             $scope.response.start_check_number =  $("#input_04").val();
             $scope.response.end_check_number =  $("#input_05").val();
             $scope.response.checkout_algorithm = $("#select_option option:selected").val();
             console.log( $scope.response);
             $http({
                    method: "POST",
                    url: "/product/protocol/" + '?' +"key=" + $scope.$parent.$parent.key,
                    data: $scope.response,
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function (response) {$scope.response = response

             })
        }
    }]);