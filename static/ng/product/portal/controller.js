'use strict';

var portal = angular.module('Product.portal', ['ngRoute']);

    portal.config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/portal', {
            templateUrl: '/static/ng/product/portal/main.html',
            controller: 'PortalCtrl'
        });
    }]);

    portal.controller('PortalCtrl', ['$scope', "$http", function ($scope, $http) {

        $scope.nav.selected("portalMenu");
        $scope.productImgSrc = "";
        $scope.teams_data = $scope.$parent.teams;
        $scope.app_create_user = $scope.$parent.app_create_user;
        $scope.login_user = $scope.$parent.login_user;
        $scope.addEmail = function () {
            var html = '<div class="col-xs-5"><input type="email" class="form-control ui-edit-email" placeholder="邮箱" ><button class="btn btn-primary" id="addTeamSubmit" onclick="submitEmail(this)" >确认</button></div>'
            $(".item-team-user").append(html)
        };
        $scope.is_show_btn = function () {
            if($scope.app_create_user.indexOf($scope.login_user) > 0){
                return true
            }
            else{
                return false;
            }

        }

    }]);
function submitEmail(item) {
    var email = $(item).prev('input').val();
    if (email.indexOf("@")>1){
        var html = '<p style="margin-top: 10px;font-size: 14px" ng-repeat="t in teams_data"> - '+email+' <i onclick="delTeamEmail(this)" class="fa fa-minus-square-o del-team-user" aria-hidden="true"></i></p>'
        $("#team-email-info").append(html);
        $(item).parent('div').remove();
        $("#item-no-teams").hide();
        //通过controller来获取Angular应用
        var appElement = document.querySelector('[ng-controller=ProductBaseCtrl]');
          //获取$scope变量
        var $scope = angular.element(appElement).scope();
          //调用app_id变量
        var app_id = $scope.app_id;
          //上一行改变了msg的值，如果想同步到Angular控制器中，则需要调用$apply()方法即可
          // $scope.$apply();
        $.ajax({
             type: "POST",
             url: "/product/portal",
             data: {"app_id":app_id, "email": email,"action": "submitEmail"},
             dataType: "json",
             success: function(data){
                console.log(data)
              }
         });
    }else{
        bootbox.alert("请填写正确邮箱地址")
    }

}
function delTeamEmail(item) {

    var email = $(item).parent('p').text().split(" ")[2];
    //通过controller来获取Angular应用
    var appElement = document.querySelector('[ng-controller=ProductBaseCtrl]');
      //获取$scope变量
    var $scope = angular.element(appElement).scope();
      //调用app_id变量
    var app_id = $scope.app_id;
    bootbox.confirm("确定删除该项目成员?", function (result) {
      if(result){
          $.ajax({
         type: "POST",
         url: "/product/portal",
         data: {"app_id":app_id, "email": email,"action": "delEmail"},
         dataType: "json",
         success: function(data){
            console.log(data);
            $(item).parent('p').remove();
             layer.msg('删除成功', {icon: 1, time: 2000});
          }
     });
      }
    })


}