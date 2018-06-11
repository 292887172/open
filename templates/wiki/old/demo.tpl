{% extends "wiki/old/base.tpl" %}
<!-- 样式 -->
{%block styles%} {%endblock%} 
<!--内容 -->
{%block content%}
<div class="zibng_left">
	<div style="height: 1000px; float: left;"></div>
<div class="erjnav">
      <ul>
        <li><a href="#" class="dianq">应用如何接入</a></li>
        <li><a href="#" >平台政策</a></li>
        <li><a href="#" >API签名算法</a></li>
        <li><a href="#" >API测试</a></li>
      </ul>
    </div>
	<div class="jiszhic">
		<div class="jiszhic_a">相关资料</div>
		<div class="jiszhic_b">
			<ul>
				<li><a href="https://readthedocs.org/">read the docs</a></li>
				<li><a href="https://www.python.org/">python.org</a></li>
			</ul>
		</div>
	</div>
</div>
<div class="zibng_left_s"></div>
<div class="zibng_right">
	<div class="zbshyw">
		<h2>应用接入</h2>
		<div class="zbshyw_a">
			<a href="#">如何接入</a> <a href="#">平台政策</a> <a href="#">签名算法</a>
		</div>
	</div>
	<div class="zbshyw">
		<h2>API文档</h2>
		<div class="kfwnd">
			<ul>
				<li>
					<h3>商家类API</h3> <span style="color: #1a5c7e;"><a href="#">.get
							(获取商家所属分类API)</a></span> <span><a href="#">.list.get (获取商家列表API)</a></span>
					<span><a href="#">.get (获取商家详细信息API)</a></span> <span><a
						href="#">ads.get (获取商家广告信息API)</a></span>
				</li>
				<li>
					<h3>商品类API</h3> <span><a href="#">itemcats.get
							(获取商品分类API)</a></span> <span><a href="#">items.search (商品搜索API)</a></span> <span><a
						href="#">items.get (获取商品详情API)</a></span> <span> &nbsp;</span>
				</li>
				<li>
					<h3>画报类API</h3> <span><a href="#">pictorials.list.get
							(获取画报列表)</a></span> <span><a href="#">pictorials.get (获取画报详细)</a></span> <span>&nbsp;</span>
				</li>
				<li>
					<h3>促销类API</h3> <span><a href="#">promocats.get
							(获取促销信息分类API)</a></span> <span><a href="#">promos.list.get
							(获取促销列表API)</a></span> <span><a href="#">promos.get (获取促销详细信息API)</a></span>
				</li>
				<li>
					<h3>优惠券API</h3> <span><a href="#">coupon.list.get
							(获取优惠券列表)</a></span> <span><a href="#">coupon.get (获取优惠券详细介绍)</a></span><span><a
						href="#">coupon.item.get (获取优惠券码)</a></span>
				</li>
				<li>
					<h3>功能类API</h3> <span><a href="#">orders.report.get
							(获取收入报表)</a></span>
				</li>
			</ul>
		</div>
	</div>
	<div class="zbshyw">
		<h2>资源下载</h2>
		<div class="ziyxz">
			<ul>
				<li><a href="#">php sdk</a></li>
				<li><a href="#">.net sdk</a></li>
				<li><a href="#">java sdk</a></li>
				<li><a href="#">python sdk</a></li>
			</ul>
		</div>
	</div>
	<div class="zbshyw">
		<h2>常见问题</h2>
		<div class="zbshyw_a">
			<ul>
				<li><a href="#">请问App key的有效期是多长时间？</a></li>
				<li><a href="#">你好, 想请问要怎样才能再次查看我应用的 App_key 和 App_secret？</a></li>
				<li><a href="#">Api获取到的数据与页面显示不一致怎么办？</a></li>
				<li><a href="#">一个网站可不可以使用多个appkey？</a></li>
				<li><a href="#">调用API为什么总是出错？</a></li>
				<li><a href="#">开放平台如何创建应用？</a></li>
			</ul>
		</div>
	</div>
</div>
{%endblock%}
{%block scripts%}
<script>
$(function(){
	//选中的选项
	var index=3;
	$(".nav ul li a:eq("+index+")").addClass("hover");
})
</script>
	{%endblock%}