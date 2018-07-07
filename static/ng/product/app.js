'use strict';

// Declare product level module which depends on views, and components
angular.module('Product', [
    "ngRoute",
    "Product.base",
    "Product.main",
    // 产品信息
    "Product.info",
    // 产品服务
    // 生产测试
    // 开发者
    // 设备管理
    "Product.device",
    // "Product.dev",
    "Product.argue",
    "Product.edit",
    "Product.oven",
    "Product.content",
    "Product.app",
    //定义协议
    "Product.protocol",
    // 产品门户
    "Product.portal"

])
.config(['$routeProvider', "$interpolateProvider", function ($routeProvider, $interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
    $routeProvider.otherwise({redirectTo: '/content'});
}])
.filter('trustHtml', function ($sce) {
    return function (input) {
        return $sce.trustAsHtml(input);
    }
});