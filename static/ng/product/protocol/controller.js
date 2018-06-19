'use strict';

angular.module('Product.protocol', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/protocol', {
            templateUrl: '/static/ng/product/protocol/protocol.html',

        })
    }])
    .controller('ProtocolCtrl', ['$scope', "$http", function ($scope, $http) {
        var xx = 0;
        $scope.list_mode = [{"val":"A55A", "title": "帧头", "number": 1}, {"val":"00", "title": "流水号", "number": 2},{"val":"00", "title": "协议版本","number": 3},
          {"val":"00", "title": "数据类型", "number": 4},{"val":"00", "title": "帧长", "number": 5}, {"val":"00x15", "title": "帧数据","number": 6},
          {"val":"00", "title": "校验", "number": 7}];
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
                 console.log(obj);
                 list_0.push(obj)
            }
             $scope.response.fivechoose = list_0;
             // 获取循环体的value
             // 根据是否启用获取响应的value 启用则获取value 不启用这

             var list_1 = [];
             $(".x1x input[value]").each(function () {

                 var v = $(this).val();

                 console.log(v);
                 list_1.push(v);
             });

             var list_2 =[];
             var for2 = document.getElementsByClassName("taf");
             for (var g = 0, lll2 = for2.length; g < lll2; g++) {
                 var obj1 = for2[g].checked;
                 console.log(obj1);
                 list_2.push(obj1)
            }
             console.log(list_2);
             $scope.response.frame_taf =  list_2;
             $scope.response.frame_content =  list_1;
             $scope.response.start_check_number =  $("#input_04").val();
             $scope.response.end_check_number =  $("#input_05").val();
             $scope.response.checkout_algorithm = $("#select_option option:selected").val();

             $http({
                    method: "POST",
                    url: "/product/protocol/" + '?' +"key=" + $scope.$parent.$parent.key,
                    data: $scope.response,
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function (response) {$scope.response = response

             })
        }
    }]);