'use strict';

angular.module('Product.portal', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/portal', {
            templateUrl: '/static/ng/product/portal/main.html',
            controller: 'PortalCtrl'
        });
    }])

    .controller('PortalCtrl', ['$scope', "$http", function ($scope, $http) {

        $scope.nav.selected("portalMenu");
        $scope.productImgSrc = "";
        $scope.teams_data = $scope.$parent.teams;
        $scope.addEmail = function () {
            var html = '<div class="col-xs-5"><input type="email" class="form-control ui-edit-email" placeholder="邮箱" ><button class="btn btn-primary" id="addTeamSubmit" onclick="submitEmail(this)" >确认</button></div>'
            $(".item-team-user").append(html)
        };

    }]);
function submitEmail(item) {

    var html = '<p style="margin-top: 10px;font-size: 14px" ng-repeat="t in teams_data"> - '+$(item).prev('input').val()+' <i onclick="delTeamEmail(this)" class="fa fa-minus-square-o del-team-user" aria-hidden="true"></i></p>'
    $("#team-email-info").append(html);
    $(item).parent('div').remove()
}
function delTeamEmail(item) {
    $(item).parent('p').remove();
    bootbox.alert('删除成功');
}