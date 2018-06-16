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
                method: "POST",
                url: location.href,
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
             var list_1 = [];
             $(".x1x input[value]").each(function () {
                 var v = $(this).val();
                 list_1.push(v);
             });
             $scope.response.frame_content =  list_1;
             $scope.response.start_check_number =  $("#input_04").val();
             $scope.response.end_check_number =  $("#input_05").val();
             $scope.response.checkout_algorithm = $("#select_option option:selected").val();
             console.log($scope.response);
             $http({
                    method: "POST",
                    url: location.href,
                    data: $scope.response,
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function (response) {$scope.response = response

             })
        }
    }]);