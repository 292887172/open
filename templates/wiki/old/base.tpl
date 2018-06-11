{%load staticfiles%}
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>开发文档</title>
<link rel="stylesheet" href="{%static 'css/base.min.css' %}" />
<link rel="stylesheet" href="{%static 'css/wiki/site.css' %}"
	type="text/css" />
{%block styles%}{%endblock%}
</head>
<body>
	<!--头部-->
	<div class="nav">
		<h1>
			<a href="#"></a>
		</h1>
		<ul>
			<li><a href="/wiki/new_wiki">首页</a></li>
			<li><a href="/wiki/webtools">调试工具</a></li>
			<li><a href="/wiki/doc">开发文档</a></li>
			<li><a href="/wiki/download">资源下载</a></li>			
		</ul>
	</div>
	<div class="nav_sjoe"></div>
	<!--中间-->
	<div class="zibng">{%block content%}{%endblock%}</div>
	<!--底部-->

	<div class="foot">
		Copyright © 2000-{% now "Y"%} 56iq All Rights Reserved<a name="chaper"
			href="javascript:scroll(0,0);" style="cursor: pointer; float: right;"><img
			src="{%static 'image/wiki/zhid2.png'%}" alt="回到顶部" /></a>
	</div>
	<script src="{%static 'js/jquery-1.11.0.min.js' %}"></script>
	{%block scripts%}
	{%endblock%}
</body>
</html>