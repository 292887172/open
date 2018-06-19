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

                    console.log($scope.response)
                    $scope.list_mode = []
                    for(var i=0;i<$scope.response.frame_content.length;i++){
                     if($scope.response.frame_content[i]['code']){
                         var tmp = {"title": $scope.response.frame_content[i]['title'], "val": $scope.response.frame_content[i]['code'][0]['value'], 'number': $scope.response.frame_content[i]['number']}
                     }else{
                         if(parseInt($scope.response.frame_content[i]['length'])/8>1){
                             var t_val = "00*"+parseInt($scope.response.frame_content[i]['length'])/8
                         }
                         else{
                             t_val = "00"
                         }
                         tmp = {"title": $scope.response.frame_content[i]['title'], "val": t_val, 'number': $scope.response.frame_content[i]['number']}
                     }
                     console.log(tmp)
                    $scope.list_mode.push(tmp)

                    }
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
             // 根据是否启用获取响应的value 启用则获取value 不启用这

             var list_1 = [];
             $(".x1x input[value]").each(function () {
                 var v = $(this).val();
                 list_1.push(v);
             });

             var list_2 =[];
             var for2 = document.getElementsByClassName("taf");
             for (var g = 0, lll2 = for2.length; g < lll2; g++) {
                 var obj1 = for2[g].checked;
                 list_2.push(obj1)
            }
            // 终极循环
             var li = [];
             var z1 = document.getElementsByClassName("x1x");
             for (var z=0, list_z1 = z1.length; z < list_z1; z++ ){
                var list_code = [];
                var dict_1={"code":list_code};
                var z2 = z1[z].getElementsByTagName("input");
                console.log(z2)
                dict_1["title"] = z2[0].value;
                dict_1["is_enabled"] = z2[1].checked;
                dict_1["number"] = z2[2].value;
                dict_1["length"] = z2[3].value;
                for (var zz=4,list_z2 = z2.length; zz<list_z2;zz=zz+2 ){
                list_code.push({"value":z2[zz].value,"desc":z2[zz+1].value});
                }
                li.push(dict_1)
            }
            console.log(li);


             $scope.response.frame_taf =  list_2;
             $scope.response.frame_content =  li;
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