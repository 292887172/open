var common = {
	"store" : (function() {
		var api = {}, win = window, doc = win.document, localStorageName = 'localStorage', globalStorageName = 'globalStorage', storage;

		api.set = function(key, value) {
		};
		api.get = function(key) {
		};
		api.remove = function(key) {
		};
		api.clear = function() {
		};
		api.getItems = function() {
		};

		if (localStorageName in win && win[localStorageName]) {
			storage = win[localStorageName];
			api.set = function(key, val) {
				storage.setItem(key, val)
			};
			api.get = function(key) {
				return storage.getItem(key)
			};
			api.remove = function(key) {
				storage.removeItem(key)
			};
			api.clear = function() {
				storage.clear()
			};
			api.getItems = function() {
				var o = {};
				for ( var i in storage) {
					o[i] = storage[i];
				}
				return o;
			}
		} else if (globalStorageName in win && win[globalStorageName]) {
			storage = win[globalStorageName][win.location.hostname];
			api.set = function(key, val) {
				storage[key] = val
			};
			api.get = function(key) {
				return storage[key] && storage[key].value
			};
			api.remove = function(key) {
				delete storage[key]
			};
			api.clear = function() {
				for ( var key in storage) {
					delete storage[key]
				}
			};
			api.getItems = function() {
				var o = {};
				for ( var i in storage) {
					o[i] = storage[i];
				}
				return o;
			}
		} else if (doc.documentElement.addBehavior) {
			function getStorage() {
				if (storage) {
					return storage
				}
				storage = doc.body.appendChild(doc.createElement('div'));
				storage.style.display = 'none';
				storage.addBehavior('#default#userData');
				storage.load(localStorageName);
				return storage;
			}
			api.set = function(key, val) {
				var storage = getStorage(), items = storage
						.getAttribute("sessionKey")
						|| "";
				storage.setAttribute(key, val);
				if (items.search(new RegExp("\\b" + key + "\\b")) === -1) {
					storage.setAttribute("sessionKey", items.split("|").concat(
							key).join("|"));
				}
				storage.save(localStorageName);
			};
			api.get = function(key) {
				var storage = getStorage();
				return storage.getAttribute(key);
			};
			api.remove = function(key) {
				var storage = getStorage();
				storage.removeAttribute(key);
				storage.save(localStorageName);
			}
			api.clear = function() {
				var storage = getStorage();
				var attributes = storage.XMLDocument.documentElement.attributes;
				;
				storage.load(localStorageName);
				for (var i = 0, attr; attr = attributes[i]; i++) {
					storage.removeAttribute(attr.name);
				}
				storage.save(localStorageName);
			}
		}
		return api;
	})(),
	"_oauth" : function() {
		var o = {};
		if (window.localStorage) {
			for (var i = 0, k = localStorage.length, key; i < k; i++) {
				var key = localStorage.key(i);
				var value = localStorage.getItem(key);
				o[key] = value;
			}
		} else {
			var keys = (common.store.get("sessionKey") || "").split("|");
			for (var i = 0, l = keys.length, key; i < l; i++) {
				key = keys[i];
				if (key) {
					var value = common.store.get(key);
					o[key] = value;
				}
			}
		}
		return o;
	},
	"defaultConfig" : {
		"appkey" : "801058005",
		"appsecret" : "31cc09205420a004f3575467387145a7"
	},
	"containsElements" : function(elems, o) {
		for (var i = 0, k = elems.length; i < k; i++) {
			if (elems[i].contains(o)) {
				return elems[i];
			}
		}
		return false;
	},
	"initUserInfo" : function(o) {
		var params = {
			"opent" : {
				"qq" : {
					"p_uin" : common.oauth.p_uin || "",
					"p_skey" : common.oauth.p_skey || "",
					"p_luin" : common.oauth.p_luin || "",
					"p_lskey" : common.oauth.p_lskey || ""
				},
				"tx" : {
					"_uin" : common.oauth._uin,
					"_oskey" : common.oauth._oskey
				},
				"py" : {
					"uin" : common.oauth.puin,
					"skey" : common.oauth.pskey
				},
				"1.0a" : {},
				"2.0" : {},
				"2.1" : {}
			},
			"openqq" : {
				"openqq" : {}
			}
		}[common.api_type];

		if (!(params && params[o.oauth_version])) {
			return false;
		}
		var str = '<table class="accout_table" border="1" cellpadding="6" width="100%" borderColor="#ccc">'
				+ '<tr><th width="120">授权方式：</th>'
				+ '<td>'
				+ {
					"1.0a" : "oAuth1.0a授权",
					"2.0" : "oAuth2.0授权",
					"2.1" : "openid&openkey授权",
					"qq" : "QQ帐号登录",
					"tx" : "腾讯互联",
					"py" : "朋友社区登录",
					"openqq" : "腾讯互联"
				}[o.oauth_version]
				+ ' <a href="javascript:;" onclick="$(\'.getToken\').trigger(\'click\');return false;" style="margin-left:20px;" hidefocus>'
				+ (common.api_type === "openqq" && '切换帐号' || '选择其它授权方式')
				+ '</a>'
				+ (common.api_type === "openqq"
						&& ' <a href="javascript:;" onclick="common.showOpenQQLoginForm()">系统指定帐号登录</a>' || '')
				+ '</td>' + '</tr>';
		for ( var i in o) {
			if (i === "oauth_version") {
				continue;
			}
			str += '<tr><th>' + i + '：</th><td><div class="breakword">' + o[i]
					+ '</div></td></tr>';
		}
		str += "</table>";
		if (common.oauth.oauth_version) {
			$("#login_info").html(str);
		}

		if (params[o.oauth_version]) {
			var str = "", p = params[o.oauth_version];
			for ( var i in p) {
				str += '<li>'
						+ '<input type="text" class="input_text para_name" placeholder="参数名" value="'
						+ i
						+ '" pretag="cookie_">'
						+ ' = '
						+ '<input type="text" class="input_text para_value" placeholder="参数值" value="'
						+ p[i]
						+ '">'
						+ '<a href="javascript:;" class="para_del icon_del" title="删除">×</a>'
						+ '</li>';
			}
			$("#cookies_panel").show();
			$("#cookies_list").html(str);
			$("#cookies_panel")
					.find("h3.t1")
					.append(
							$('<span class="t1_right"><a href="javascript:;" class="para_add btn2" id="add_cookie" type="text">添加cookie</a></span>'));
			$("#add_cookie")
					.click(
							function() {
								$("#cookies_list")
										.append(
												$('<li><input type="text" class="input_text para_name" placeholder="参数名" pretag="cookie_"/> = <input type="text" class="input_text para_value" placeholder="参数值"/><a href="javascript:;" class="para_del icon_del" title="删除">×</a></li>'));
							});
			$("#cookies_list").click(function(event) {
				if ($(event.target).hasClass('icon_del')) {
					$(event.target).parent().remove();
					return false;
				}
			});
		} else {
			$("#cookies_list").html("");
			$("#cookies_panel").hide();
		}

	},
	"init" : function(api_type) {

		common.api_type = api_type || "opent";
		common.oauth = common._oauth();
		common.initUserInfo(common.oauth);
		common.loadAPI();
		// window.onscroll = common.onscroll;
		var dialog = common.dialog = common._dialog && common._dialog();

		if (!!window.find) {
			HTMLElement.prototype.contains = function(B) {
				return this.compareDocumentPosition(B) - 19 > 0
			}
		}
		;

		$("#add_para,#add_para_pic")
				.click(
						function() {
							var type = $(this).attr("type") || "text", input = {
								"text" : '<input type="text" class="input_text para_value" placeholder="参数值"/>',
								"file" : '<input type="file" class="para_value" placeholder="参数值"/>'
							}[type];

							if ($("#para_list li").size() < 20) {
								$("#para_list")
										.append(
												$('<li>\
																<input type="text" class="input_text para_name" placeholder="参数名"/> = '
														+ input
														+ '\
																<a href="javascript:;" class="para_del icon_del" title="删除">&times;</a>\
															</li>'));
							} else {
								dialog.alert("参数过多");
							}
						});

		$("#para_list").delegate(".icon_del", "click", function() {
			// alert("删除内容")
			var t = $(this).parent(), p = t.parent();
			if (p.find("li").size() > 0) {
				p[0].removeChild(t[0]);
			} else {
				dialog.alert("参数过少，不能再删除");
			}
		});

		$(".getToken")
				.click(
						function() {
							var l = 1;
							if (typeof (common.innerComp) === "undefined") {
								l = 0;
							}
							if (common.api_type === "opent") {
								dialog
										.show({
											"width" : 465,
											"height" : [ 150, 190 ][l],
											"title" : '选择登录方式',
											"text" : [
													'<ul class="loginbtns">',
													'<li style="width:auto;float:none;padding:5px 10px;">授权流程调试请使用 <a href="http://dev.t.qq.com/auth_tool/index.html" target="_blank" style="color:blue;">腾讯微博授权及接口调试工具</a></li>',
													'<li><a href="javascript:;" onclick="common.setConfigForm(\'1.0a\',\'opent\');return false;" class="btn2" title="适用于站外应用、客户端应用，除非用户取消授权否则token永久有效">oauth1.0授权</a></li>',
													'<li><a href="javascript:;" onclick="common.setConfigForm(\'2.0\',\'opent\');return false;" class="btn2" title="适用于站外应用、客户端应用，token有效期有时间限制">oauth2.0授权</a></li>',
													'<li><a href="javascript:;" onclick="common.setConfigForm(\'2.1\',\'opent\');return false;" class="btn2" title="适用于上架到应用频道的站内应用，可共享腾讯其它开放平台的登录态">openid+openkey</a></li>',
													l
															&& '<li><a href="javascript:;" onclick="common.setConfigForm(\'qq\',\'opent\');return false;" class="btn3">QQ帐号登录</a></li>'
															|| '',
													l
															&& '<li><a href="javascript:;" onclick="common.setConfigForm(\'tx\',\'opent\');return false;" class="btn3">腾讯互联</a></li>'
															|| '',
													l
															&& '<li><a href="javascript:;" onclick="common.setConfigForm(\'py\',\'opent\');return false;" class="btn3">朋友登录</a></li>'
															|| '', '</ul>' ]
													.join("")
										});
							} else {
								common.setConfigForm("openqq", "openqq");
							}
						});

		$("#save_api").click(function() {
			common.saveAPI(this.form);
		});

		$("body")
				.bind(
						"click",
						function(event) {
							var o = (window.event && window.event.srcElement)
									|| (event && event.target), elems = $(".cgi_url_span"), host_list = $(
									"#host_list").parent();
							if (/^qq|tx|py$/.test(common.oauth.oauth_version)) {
								if (common.containsElements(elems, o)) {
									host_list.removeClass("none");
								} else {
									host_list.addClass("none");
								}
							}
						});

		$("#iframe_tab")
				.find(".tab")
				.click(
						function(event) {
							alert("点击了");
							var that = $(this), dfor = that.attr("data-for"), apipath = $(
									"#api_list").find("li.active").attr(
									"data-name");
							if (typeof (event.keyCode) != "undefined"
									&& that.hasClass("active")) {
								return;
							}
							that.parent().find(".tab").removeClass("active");
							that.addClass("active");

							if (dfor === "result") {
								$("#oauth_form_result").attr("src",
										"about:blank").attr("height", 0);
								$(".form_debuger").removeClass("none");
							} else if (dfor === "wiki") {
								// $("#oauth_form_result").attr("src",
								// "apilist.js?action=get_xml_for_wiki&domain="
								// + location.hostname + "&path=" + apipath +
								// "&type=" + common.api_type);
								$(".form_debuger").addClass("none");
							} else if (dfor === "wiki_code") {
								$("#oauth_form_result").attr(
										"src",
										"controller.php?action=get_xml_for_wiki&domain="
												+ location.hostname + "&path="
												+ apipath + "&type="
												+ common.api_type + "&code=1");
								$(".form_debuger").addClass("none");
							}

							return false;
						});

		setTimeout(function() {
			var callee = arguments.callee;
			if (common.api) {
				common.initSearchForm();
				common.rederAppList();
			} else {
				setTimeout(callee, 100);
			}
		}, 1);
	},
	"getLoginUrl" : function(surl) {
		return "http://ui.ptlogin2.qq.com/cgi-bin/login?appid=46000101&daid=6&pt_no_auth=1&s_url="
				+ encodeURIComponent(location.href.replace(/(\w+.html|#|\?).*/,
						"")
						+ surl)
				+ "&style=11&low_login=1&hide_title_bar=1&hide_close_icon=1&target=self&link_target=self&hln_logo=http://mat1.gtimg.com/app/opent/images/websites/space.gif";
	},
	"showOpenQQLoginForm" : function(form) {
		var url = "oauth_openqq/login.php?appid="
				+ (form && form.appid && form.appid.value || "") + "&appkey="
				+ (form && form.appkey && form.appkey.value || "");
		if (form) {
			url = common.getLoginUrl(url);
		}
		common.dialog.showFrame({
			"width" : 485,
			"height" : 380,
			"title" : "登录",
			"text" : url
		});
	},
	"setConfigForm" : function(v) {
		var dialog = common.dialog;
		if (/^1\.0a|2\.0|2\.1|py|openqq$/.test(v)) {
			var form = {
				"opent" : {
					"action" : {
						"1.0a" : "oauth_v1/demo/index.php",
						"2.0" : "oauth_v2/demo.php",
						"2.1" : "oauth_v2/demo.php",
						"py" : "oauth_v2/demo.php"
					}[v],
					"params" : {
						"appkey" : common.oauth.appkey
								|| common.defaultConfig.appkey,
						"appsecret" : common.oauth.appsecret
								|| common.defaultConfig.appsecret
					}
				},
				"openqq" : {
					"action" : {
						"openqq" : ""
					}[v],
					"params" : {
						"appid" : common.defaultConfig.appkey,
						"appkey" : common.defaultConfig.appsecret
					}
				}
			}[common.api_type], h = 200, str = '<form method="get" action="'
					+ form.action
					+ '" style="margin:15px 0 0 50px;" target="_blank">';
			if (v === "py") {
				form.params["appid"] = common.oauth.appid
						|| common.defaultConfig.appkey;
				h = 240;
			}
			str += '<table>';
			str += '<input type="hidden" value="' + v + '" name="go_oauth">';
			for ( var para in form.params) {
				str += '<tr><td align="right">'
						+ para
						+ '：</td><td><input type="text" value="'
						+ form.params[para]
						+ '" name="'
						+ para
						+ '" class="input_text" style="width:210px;"/></td></tr>';
			}
			str += '<tr><td></td><td>';
			if (common.api_type === "opent") {
				str += '<input type="submit" value="点击授权" class="btn2"/>';
			} else if (common.api_type === "openqq") {
				str += '<input type="button" value="点此登录" class="btn2" onclick="common.showOpenQQLoginForm(this.form);"/>';
			}
			str += '</td></tr>';
			str += "</table>";
			dialog.show({
				"width" : 450,
				"height" : h,
				"title" : '配置应用信息',
				"text" : str
			});
		} else if (/^qq$/.test(v)) {
			var url = common.getLoginUrl("oauth_qq/"
					+ encodeURIComponent("?type=" + v));
			;
			dialog.showFrame({
				"width" : 485,
				"height" : 380,
				"title" : "登录",
				"text" : "oauth_qq/index.php?callback="
						+ encodeURIComponent(url)
			});
		} else if (/^tx$/.test(v)) {
			var form = {
				"params" : {
					"oauth_consumer_key" : common.oauth.oauth_consumer_key
							|| common.defaultConfig.appkey
				}
			}
			str = '';
			for ( var para in form.params) {
				str += '<div style="margin:0 0 5px;padding:0;">' + para
						+ '：</div><input type="text" value="'
						+ form.params[para] + '" name="' + para
						+ '" class="input_text" style="width:210px;"/>';
			}
			str += "";
			dialog.alert({
				"height" : 200,
				"title" : '配置应用信息',
				"text" : str
			}, function() {
				var appkey = dialog.dom.content.find(
						"input[name='" + para + "']").val();
				var url = "http://ui.ptlogin2.qq.com/cgi-bin/login?"
						+ $.param({
							"appid" : 46000101,
							"daid" : 6,
							"pt_no_auth" : 1,
							"s_url" : location.href.replace(
									/(index.html|#|\?).*/, "")
									+ "oauth_qq/"
									+ encodeURIComponent("?oauth_consumer_key="
											+ appkey + "&type=" + v),
							"f_url" : "loginerroralert",
							"style" : 1,
							"low_login" : 1,
							"link_target" : "blank",
							"target" : "self",
							"hide_title_bar" : 1,
							"dummy" : 1,
							"lang" : 2052,
							"bgcolor" : "ffffff"
						});
				dialog.showFrame({
					"width" : 485,
					"height" : 380,
					"title" : "登录",
					"text" : "oauth_qq/index.php?callback="
							+ encodeURIComponent(url)
				});
				return false;
			});
		}
		return false;
	},
	"goLogin" : function() {
		var f = $("#oauth_form"), app = {
			"appkey" : f.find("input[name='appkey']").val(),
			"appsecret" : f.find("input[name='appsecret']").val()
		}, v = $(this).attr("data-default"), url, uin = /\buin\b=(\bo?\d+\b)/
				.exec(document.cookie), skey = /\bskey\b=(@\b\w+\b)/
				.exec(document.cookie);

		uin = uin && uin[1] || "";
		skey = skey && skey[1] || "";

		if (typeof (v) != "undefined") {
			var v = $(this).attr("data-default"), needAppkey = true;
			if (v === "1.0a") {
				url = "oauth_v1/demo/index.php?appkey=" + app["appkey"]
						+ "&appsecret=" + app["appsecret"] + "&go_oauth";
			} else if (v === "2.0" || v === "2.1") {
				url = "oauth_v2/demo.php?appkey=" + app["appkey"]
						+ "&appsecret=" + app["appsecret"] + "&go_oauth=" + v;
			} else if (/^(qq|tx|py)$/.test(v)) {
				url = "oauth_qq/index.php?callback="
						+ encodeURIComponent("http://ui.ptlogin2.qq.com/cgi-bin/login?appid=46000101&daid=6&pt_no_auth=1&s_url="
								+ encodeURIComponent(location.href.replace(
										/(index.html|#|\?).*/, "")
										+ "oauth_qq%3ftype%3d" + v)
								+ "&f_url=loginerroralert&style=1&low_login=1&link_target=blank&target=parent&hide_title_bar=1&dummy=1&lang=2052&bgcolor=ffffff");
				needAppkey = false;
			}
		}

		if (needAppkey === true && !app["appkey"] && !app["appsecret"]) {
			dialog.alert("请先填写appKey和appSecret");
			return false;
		}
		window
				.open(
						url,
						"loginWin",
						"width=700,height=540,top=0,left=0,toolbar=no,menubar=no,scrollbars=no,location=yes,resizable=no,status=no");
	},
	"loadAPI" : function() {
		/*
		 * var url = "js/apilist.js?action=get_api_list&type=" + common.api_type + ({
		 * "py" : 1, "tx" : 1, "qq" : 1 } [common.oauth.oauth_version] &&
		 * "&host_list=true" || ""); $.getScript(url, function () { var image =
		 * new Image(), src = "http://dayu.oa.com/avatars/avatar.gif"; if
		 * (common.innerComp === undefined) { image.onload = function () { if
		 * (image.src === src) { common.innerComp = true; } } image.src = src;
		 * setTimeout(function () { image.src = "about:blank"; }, 3000); } });
		 */
		// common.loadJS(url, "utf-8");
		// common.loadJS("js/relogininfo.js?action=req_login_info&callback=wiki.login",
		// "utf-8");
	},
	"loadJS" : function(v, c) {
		var element = document.createElement("script");
		element.src = v;
		element.type = "text/javascript";
		if (c)
			element.charset = c;
		document.body.appendChild(element);
	},
	"rederAppList" : function() {
		var api = common.api.sort(function(v1, v2) {
			return v2.list.length - v1.list.length
		}), list, hashParam = location.hash.slice(1).split(':'), hash = hashParam
				.pop(), tabname = hashParam[0], dialog = common.dialog, api_list = $("#api_list");
		for (var i = 0, k = api.length; i < k; i++) {
			api_list.append($('<h3 class="api_category_name" data-index=' + i
					+ '><span class="api_category_name_icon"></span>'
					+ api[i].name + ' <span class="s1 c2 normal">('
					+ api[i].list.length + ')</span></h3>'))
			if (api[i].list && api[i].list.length) {
				var str = '';
				list = api[i].list;
				for (var j = 0, kk = list.length; j < kk; j++) {
					var path = api[i].baseURI + '/' + list[j].api_url;
					str += '<li data-name="' + path + '" title="'
							+ list[j].api_name + '&#10;' + path
							+ '" class="api_list_li';
					str += '" filepath="' + list[j].filepath + '">'
							+ '<div class="api_list_li_div">'
							+ '<label class="name_ch">' + list[j].api_name
							+ '</label><cite class="name_en">' + path
							+ '</cite>' + '</div><a href="#' + path
							+ '"></a></li>';
				}
				api_list.append($([ '<ul class="none api_list_ul">', str,
						'</ul>' ].join('')));
			}
		}

		if (!hash) {
			hash = api_list.find("li").first().attr("data-name");
		} else if (api_list.find("li[data-name='" + hash + "']").size() === 0) {
			dialog.alert("尚未配置您指定的API信息");
		}

		api_list.find("h3").bind("click", function() {
			if ($(this).next("ul").is(":visible")) {
				$(this).removeClass("active");
				$(this).next("ul").slideUp("fast");
				return;
			}
			api_list.find("ul").slideUp("fast");
			api_list.find("h3").removeClass("active");
			$(this).addClass("active").next("ul").slideDown("fast");
		});
		api_list.find("li[data-name='" + hash + "']").parent().prev("h3")
				.trigger("click");

		api_list
				.find("li")
				.bind(
						"click",
						function(event) {
							var t = $(this), p, api_category, api_info, oauth_para = {}, appinfo = common.oauth.oauth_version === "qq"
									&& "?appid=800100334&app_password=hFhqFZT5iX"
									|| "", api_url_obj = {
								"opent" : {
									"1.0a" : "http://open.t.qq.com/api/",
									"2.0" : "https://open.t.qq.com/api/",
									"2.1" : "http://open.t.qq.com/api/",
									"qq" : "http://#ip#:8080/innerapi/",
									"tx" : "http://#ip#:8080/innerapi/",
									"py" : "http://#ip#:8080/innerapi/"
								},
								"openqq" : {
									"openqq" : "http://openapi.tencentyun.com/v3/"
								}
							}[common.api_type], api_url = api_url_obj[common.oauth.oauth_version]
									|| api_url_obj[{
										"opent" : "1.0a",
										"openqq" : "openqq"
									}[common.api_type]], appinfo = {
								"1.0a" : "",
								"2.0" : "",
								"2.1" : "",
								"qq" : "?appid=800100334&app_password=hFhqFZT5iX",
								"tx" : "?oauth_consumer_key="
										+ common.oauth.oauth_consumer_key,
								"py" : "?appid=" + common.oauth.appid
										+ "&openid=" + common.oauth.openid
										+ "&openkey=" + common.oauth.openkey
							}[common.oauth.oauth_version || "1.0a"];

							api_url = api_url.replace(/#ip#/, common.host_list
									&& common.host_list[0] || "");

							api_list.find("ul").addClass("none").end().find(
									"li").removeClass("active");
							t.addClass("active").parent().removeClass("none");

							var p = (t.attr("data-name") || "").split("/");

							for ( var i in common.api) {
								if (common.api[i].baseURI === p[0]) {
									for ( var j in common.api[i].list) {
										if (common.api[i].list[j].api_url === p[1]) {
											api_category = common.api[i];
											api_info = common.api[i].list[j];
											break;
										}
									}
									;
								}
							}
							while ($('#para_list').find("li").size() > 0) {
								$('#para_list').find("li").last().remove();
							}

							if (api_info) {
								$("input[name='cgi_url']").val(
										[ api_url, api_category.baseURI, '/',
												api_info.api_url, appinfo ]
												.join(""));
								var geo = {};
								for ( var i in api_info.paras) {
									$('#add_para').trigger("click");
									var li = $('#para_list').find("li").last();
									li.find("input.para_name").val(i);
									li.find("input.para_value").val(
											api_info.paras[i]);
									if (/\bpic\b/.test(i)) {
										li
												.find("input.para_value")
												.after(
														$('<input type="file" value="" class="para_value" name="pic" />'))
												.remove();
									}
									if (i === "jing" || i === "wei") {
										if (common.geolocation) {
											li.find("input.para_value").val(
													common.geolocation.coords[{
														"jing" : "latitude",
														"wei" : "longitude"
													}[i]]);
										} else if (navigator.geolocation) {
											geo[i] = li;
											navigator.geolocation
													.getCurrentPosition(
															function(pos) {
																common.geolocation = pos;
																var p = {
																	"jing" : pos.coords.latitude,
																	"wei" : pos.coords.longitude
																};
																geo["jing"]
																		.find(
																				"input.para_value")
																		.val(
																				p["jing"]);
																geo["wei"]
																		.find(
																				"input.para_value")
																		.val(
																				p["wei"]);
															}, function() {
															});
										}
									}
								}
								$("select[name='cgi_method']").val(
										api_info["method"]);
							}

							if ($("#iframe_tab").find(".tab.active").attr(
									"data-for") != "result") {
								$("#iframe_tab").find(".tab.active").trigger(
										"click");
							} else if (tabname) {
								$("#iframe_tab").find(".tab").filter(
										"[data-for='" + tabname + "']")
										.trigger("click");
							}
						}).filter("[data-name='" + hash + "']")
				.trigger("click");

		common.host_list && common.renderHostList(common.host_list);

		$("#host_list").find("dd").find("input").bind("click", function() {
			var ip = $(this).val(), input = $("input[name='cgi_url']");
			common.changeCgiHost(input, ip);
		}).end().end().find("dd:eq(0)").find("input")
				.attr("checked", "checked");

		if (typeof (common.uPower) === "undefined") {
			$("#save_api").remove();
		} else if (common.uPower === 1) {
			$("#apides")
					.append(
							'<a href="javascript:;" class="c2" style="margin-left:10px;" onclick="common.editMapTable()">编辑映射表</a>');
		}
	},
	"editMapTable" : function() {
		var dialog = common.dialog, reqinfo = {
			"action" : "get_map_content",
			"type" : common.api_type
		};

		$
				.ajax({
					url : "controller.php?" + $.param(reqinfo),
					dataType : "text",
					type : "get",
					success : function(responseText) {
						dialog
								.show({
									"text" : '<form style="text-align:center;height:100%;">'
											+ '<textarea name="apixml">'
											+ responseText
											+ '</textarea>'
											+ '<br/>'
											+ '<input type="button" class="btn2 saveapi" value="保存" onclick="common.saveMapTable(this)"/>'
											+ '</form>',
									"width" : "90%",
									"height" : "90%",
									"title" : "编辑" + reqinfo["type"] + "映射表",
									"callback" : function() {
										var c = dialog.dom.content;
										c.find("textarea").css({
											"width" : c.width() - 20,
											"height" : c.height() - 60,
											"margin" : "5px"
										});
									},
									"hideScroller" : true
								});
					}
				});
	},
	"saveMapTable" : function(o) {
		var form = o.form, dialog = common.dialog, apixml = form.apixml.value, querystr = $
				.param({
					"action" : "save_map_content",
					"type" : common.api_type
				});
		$.ajax({
			url : "controller.php?" + querystr,
			dataType : "json",
			type : "post",
			data : {
				"apixml" : apixml
			},
			success : function(d) {
				if (d.ret == 0) {
					dialog.alert("保存成功!", function() {
						location.reload();
					});
				} else {
					dialog.alert(d.msg);
				}
			},
			error : function() {
				dialog.alert("网络连接失败");
			}
		});
	},
	/*------------------------------------------------------------------------------------------------------提交内容  Begin------------------------------------------------------------------------------------------------------------*/
	"submit" : function(form) {
		// 验证部分
		var apiUrl = $("input[name='api_url']").val();
		if (/^\s*$/gi.test(apiUrl)) {
			common.dialog.alert("请求地址不能为空！");
			return false;
		}
		var f = $("#oauth_form"), t = common.api_type;
		/*
		 * if (!common.oauth.oauth_version) { //alert("提交中……");
		 * common.dialog.alert("你还未对程序进行授权，不能进行此操作！"); return false; }
		 */
		if (t === "opent") {
			if (common.oauth.oauth_version === "1.0a") {
				form.action = "request.php?"
						+ [
								"appkey=" + common.oauth.appkey,
								"appsecret=" + common.oauth.appsecret,
								"name=" + common.oauth.name,
								"version=" + common.oauth.oauth_version,
								"oauth_token=" + common.oauth.access_token,
								'oauth_token_secret='
										+ common.oauth.access_token_secret,
								"cgi_url="
										+ encodeURIComponent(f.find(
												"input[name='cgi_url']").val()),
								"cgi_method="
										+ f.find("select[name='cgi_method']")
												.val() ].join("&");
			} else if ((common.oauth.oauth_version | 0) === 2) {
				form.action = "request.php?"
						+ [
								"appkey=" + common.oauth.appkey,
								"appsecret=" + common.oauth.appsecret,
								"version=" + common.oauth.oauth_version,
								"oauth_token=" + common.oauth.access_token,
								"openid=" + common.oauth.openid,
								"openkey=" + common.oauth.openkey,
								"cgi_url="
										+ encodeURIComponent(f.find(
												"input[name='cgi_url']").val()),
								"cgi_method="
										+ f.find("select[name='cgi_method']")
												.val() ].join("&");
			} else if (/^qq|tx|py$/.test(common.oauth.oauth_version)) {
				if (typeof (common.hostQueue) === "undefined") {
					common.hostQueue = [];
					common.hostQueue = $("#host_list").find(
							"input[name='host_name']:checked").val();
				}
				if ($("#host_list").find("dd").find(":checked").size() > 1) {
					$("#add_para").trigger("click");
					var lastpara = $("#para_list").find("li").last(), ipArr = [];
					$("#host_list").find("dd").find(":checked").each(
							function() {
								ipArr.push($(this).val());
							});
					lastpara.hide();
					lastpara.find("input.para_name").val(
							"host_list_for_request").addClass(
							"host_list_for_request");
					lastpara.find("input.para_value").val(ipArr.join(","));
				} else {
					$("#para_list").find("input.host_list_for_request")
							.parent().remove();
				}

				form.action = "request.php?"
						+ [
								"version=" + common.oauth.oauth_version,
								"cgi_url="
										+ encodeURIComponent(f.find(
												"input[name='cgi_url']").val()),
								"cgi_method="
										+ f.find("select[name='cgi_method']")
												.val() ].join("&");
			}
		} else if (t === "openqq") {
			if (/^openqq$/.test(common.oauth.oauth_version)) {
				form.action = "request.php?"
						+ [
								"version=" + common.oauth.oauth_version,
								"cgi_url="
										+ encodeURIComponent(f.find(
												"input[name='cgi_url']").val()),
								"cgi_method="
										+ f.find("select[name='cgi_method']")
												.val(),
								"appid=" + common.oauth.appid,
								"appkey=" + common.oauth.appkey,
								"openid=" + common.oauth.openid,
								"openkey=" + common.oauth.openkey ].join("&");
			}
		}
		if ($(form).find("input[type='file']").size() > 0) {
			$(form).attr("enctype", "multipart/form-data");
		} else {
			$(form).attr("enctype", "application/x-www-form-urlencoded");
		}

		$(form).find(".para_list").find("li").find("input.para_value").each(
				function() {
					var p = $(this).parent().find(".para_name"), pretag = p
							.attr("pretag")
							|| "";
					var name = pretag + p.val();
					$(this).attr("name", name);
				});
		// alert("请求了");
	},
	/*------------------------------------------------------------------------------------------------------提交内容 End------------------------------------------------------------------------------------------------------------*/
	"oauthReturn" : function(data) {
		common.oauth = data;
		common.store.clear();
		for ( var i in data) {
			common.store.set(i, data[i]);
		}
		common.initUserInfo(data, common.api_type || "opent");
		location.reload();
	},
	"saveAPI" : function(form) {
		var url = $("input[name='cgi_url']").val().replace(/\s/g, ""), dialog = common.dialog, para = {}, reqinfo = {}, curapi = $(
				"#api_list").find("li.active"), filepath = curapi
				.attr("filepath")
				|| "";
		reqinfo["action"] = "get_api_content";
		reqinfo["path"] = url.replace(
				/(^https?:\/\/[^\/]+\/[^\/]+\/)|(\?.*$)/g, "");
		reqinfo["type"] = common.api_type;
		reqinfo["cover"] = !!form;
		reqinfo["method"] = $("select[name='cgi_method']").val();
		if (curapi.attr("data-name") !== reqinfo["path"]) {
			filepath = reqinfo["path"];
		}
		$(form).find("#para_list").find("li").find("input.para_value").each(
				function() {
					var name = $(this).parent().find(".para_name").val();
					var value = $(this).val();
					para[name] = value;
				});

		$
				.ajax({
					url : "controller.php?" + $.param(reqinfo),
					data : para,
					dataType : "text",
					type : "post",
					success : function(responseText) {
						dialog
								.show({
									"text" : '<form style="text-align:center;height:100%;">'
											+ '<div style="text-align:left;margin:10px 0 0 10px;">'
											+ 'API路径：<input type="text" value="'
											+ reqinfo["path"]
											+ '" class="input_text" size="30" name="path"/> '
											+ '映射保存到：'
											+ '<input type="text" value="'
											+ filepath
											+ '" class="input_text" size="30" name="savepath"/>'
											+ '</div>'
											+ '<textarea name="apixml">'
											+ responseText
											+ '</textarea>'
											+ '<br/>'
											+ '<input type="button" class="btn2 saveapi" value="保存" onclick="common.postAPIInfo(this)"/>'
											+ '</form>',
									"width" : "90%",
									"height" : "90%",
									"title" : "编辑api(" + reqinfo["path"]
											+ ")内容",
									"callback" : function() {
										var c = dialog.dom.content;
										c.find("textarea").css({
											"width" : c.width() - 20,
											"height" : c.height() - 110,
											"margin" : "5px"
										});
									},
									"hideScroller" : true
								});
					}
				});
	},
	"postAPIInfo" : function(o) {
		var form = o.form, dialog = common.dialog, apipath = form.path.value, savepath = form.savepath.value, apixml = form.apixml.value, querystr = $
				.param({
					"action" : "save_api",
					"type" : common.api_type
				});
		$.ajax({
			url : "controller.php?" + querystr,
			dataType : "json",
			type : "post",
			data : {
				"apipath" : apipath,
				"apixml" : apixml,
				"savepath" : savepath
			},
			success : function(d) {
				if (d.ret == 0) {
					dialog.alert("保存成功!", function() {
						location.href = {
							"openqq" : "openqq.html",
							"opent" : "index.html"
						}[common.api_type] + "#" + apipath;
					});
				} else {
					dialog.alert(d.msg);
				}
			},
			error : function() {
				dialog.alert("网络连接失败");
			}
		});

	},
	"invertSelection" : function(o, elems) {
		if ($(o).is(":checked")) {
			elems.attr("checked", "checked");
		} else {
			elems.removeAttr("checked");
		}
	},
	"changeCgiHost" : function(input, host) {
		var url = input.val();
		input.val(url.replace(/^(https?:\/\/)([0-9a-zA-Z\-\.]+)(:\d+)/, "$1"
				+ host + "$3"));
	},
	"renderHostList" : function(list) {
		$("#host_list")
				.html(
						function(list) {
							var arr = [];
							arr
									.push('<dt>共有<span class="f1 c1">'
											+ list.length
											+ '</span>台主机 <span class="selection">'
											+ '<input type="checkbox" name="selectAll" id="select_all_host" onclick="common.invertSelection(this,$(\'#host_list\').find(\'input:checkbox\'))"/>'
											+ '<label for="select_all_host">全选</label></span></dt>')
							for (var i = 0, k = list.length; i < k; i++) {
								arr
										.push('<dd><input type="checkbox" name="host_name" value="'
												+ list[i]
												+ '" id="host_name_'
												+ i
												+ '"> <label for="host_name_'
												+ i
												+ '">'
												+ list[i]
												+ '</label></dd>');
							}
							if (common.uPower) {
								arr
										.push('<dd><a href="javascript:;" onclick="common.modifyHostList();">编辑主机配置信息</a></dd>');
							}
							return arr.join("");
						}(list));
	},
	"modifyHostList" : function() {
		var dialog = common.dialog;
		dialog
				.alert(
						{
							"width" : 540,
							"height" : 380,
							"title" : "正在编辑",
							"text" : '<textarea style="width:494px;height:250px;border:1px solid #ccc;">'
									+ (common.host_list.join("\n"))
									+ '</textarea>'
						},
						function() {
							var str = dialog.dom.content.find("textarea").val()
									.replace(/[\n\t\s]+/g, ",");
							$
									.ajax({
										"url" : "controller.php?action=save_host&type=opent",
										"data" : {
											"host_list" : str
										},
										"type" : "post",
										"dataType" : "json",
										"success" : function(d) {
											if (d.ret === 0) {
												dialog
														.alert(
																"保存成功！",
																function() {
																	common.host_list = str
																			.split(",");
																	common
																			.renderHostList(str
																					.split(","));
																});
											} else {
												dialog.alert(d.msg);
											}
										},
										"error" : function() {
											dialog.alert("网络连接失败");
										}
									});
						});
	},
	"editApiInfo" : function(path, action) {
		var dialog = common.dialog, dom = dialog.dom.content;
		dialog
				.alert(
						{
							"title" : "添加" + path + "的"
									+ [ "接口说明", "使用场景" ][action],
							"text" : '<form style="margin:0;">'
									+ '<textarea name="" style="width:376px;height:180px;overflow:auto;"></textarea>'
									+ '</form>',
							"height" : 310
						},
						function() {
							var str = dom.find("form").find("textarea").val();
							$
									.ajax({
										"url" : "controller.php?action=edit_api_node&type="
												+ common.api_type,
										"type" : "post",
										"dataType" : "json",
										"data" : {
											"path" : path,
											"nodeName" : [ "apides",
													"apistatus" ][action],
											"nodeValue" : str
										},
										"success" : function(d) {
											var ret = +d.ret, msg = d.msg;
											if (ret === 0) {
												dialog
														.alert(
																"保存成功",
																function() {
																	$("#oauth_form_result")[0].contentWindow.location
																			.reload();
																});
											} else {
												dialog.alert("保存失败," + msg);
											}
										},
										"error" : function() {
											dialog.alert("网络连接失败");
										}
									});
						});
	},
	"onscroll" : function() {
		var d = document.documentElement || document.body, y = $("#footer")
				.offset().top, dch = d.clientHeight, dsh = d.scrollHeight, dst = document.documentElement.scrollTop
				|| document.body.scrollTop;
		if (dst < 100) {
			$(".bottomnav").fadeOut("slow");
		} else {
			$(".bottomnav").fadeIn("slow");
		}
		if (y < dch + dst) {
			$(".bottomnav").css({
				"position" : "absolute",
				"bottom" : "auto",
				"top" : y - 30
			});
		} else {
			if (!-[ 1, ] && !window.XMLHttpRequest) {
				document.title = [ y, dch + dst, dch, dst ].toString();
				// ie6
				$(".bottomnav").css({
					"bottom" : "auto",
					"top" : dch + dst - 30
				});
			} else {
				// 非ie6
				$(".bottomnav").css({
					"position" : "fixed",
					"bottom" : "0",
					"top" : "auto"
				})
			}
		}
	},
	"scrollWin" : function() {
		var t = document.documentElement.scrollTop || document.body.scrollTop, i = 0, times = 20, callback = function(
				i, k) {
			if (i < times) {
				window.scrollBy(0, -k);
				setTimeout(function() {
					callback(++i, k);
				}, 10);
			}
		};
		window.scrollBy(0, 0 - t % times);
		callback(0, (t - t % times) / times);
	},
	"initSearchForm" : function() {
		var tpl = [
				'<form class="searchform">',
				'<input type="text" name="search" placeholder="搜索关键字" accesskey="s" class="searchform_text" autocomplete="off">',
				'<input type="button" name="fulltext" value="搜索" title="搜索该文字的页面" class="searchform_btn">',
				'<ul class="search_list none"></ul>', '</form>' ].join("\n"),

		initSearch = function() {
			var t = $(".searchform_text"), searchlist = $(".search_list"), initSearchListEvent = function(
					list) {
				list.bind("click", function(event) {
					if (event.target.tagName === "LI") {
						onSearch($(event.target));
						list.hide();
					}
				}).bind("mouseover", function(event) {
					if (event.target.tagName === "LI") {
						list.find("li").removeClass("active");
						$(event.target).addClass("active");
					}
				});
			}, hideOnBlur = function(e) {
				if ($.contains(searchlist.parent()[0], e.target)) {
					return;
				} else {
					searchlist.hide();
				}
			}, search = function() {
				var text = t.val(), arr = [], arr2 = [];
				for (var i = 0, k = common.api.length; i < k; i++) {
					var basename = common.api[i].baseURI, list = common.api[i].list;
					for (var ii = 0, kk = list.length; ii < kk; ii++) {
						var p = basename + "/" + list[ii].api_url;
						if (p.indexOf(text) > -1) {
							arr.push([ list[ii].api_name, p ]);
						}
					}
				}
				if (arr.length) {
					searchlist.show();
					for (var i = 0, k = arr.length; i < k; i++) {
						arr2.push('<li><label class="search_list_ch">'
								+ arr[i][0]
								+ '</label><label class="search_list_en">'
								+ arr[i][1] + '</label></li>');
					}
					searchlist.html(arr2.join("\n")).find("li:eq(0)").addClass(
							"active");
				} else {
					searchlist.html('<li class="null">没有找到相关联的API接口</li>');
				}
			}, onscroll = function(i) {
				var o = searchlist.find(".active"), n = (i > 0 ? o.next() : o
						.prev());
				if (searchlist && searchlist.is(":visible")) {
					if (n.size()) {
						searchlist.find("li").removeClass("active");
						n.addClass("active");
						if (n[0].offsetTop + n.height() > searchlist[0].scrollTop
								+ searchlist[0].clientHeight) {
							searchlist[0].scrollTop += 50;
						} else if (n[0].offsetTop < searchlist[0].scrollTop) {
							searchlist[0].scrollTop -= 50;
						}
					}
				}
			}, onSearch = function(o) {
				var url = o.find(".search_list_en").html(), li = $("#api_list")
						.find("li[data-name='" + url + "']");
				t.val(url);
				if (!li.parent().is(":visible")) {
					li.parent().prev(".api_category_name").trigger("click");
				}
				li.trigger("click");
				location.hash = li.find("a").attr("href").replace(/^.*#/, "");
				;
			};

			t.bind("keyup", function(event) {
				if (event.keyCode === 38 || event.keyCode === 40) {
					onscroll(event.keyCode === 38 ? -1 : 1);
				} else if (event.keyCode === 13) {
					return false;
				} else {
					search();
				}
				;
			}).bind("keydown", function(event) {
				if (event.keyCode === 13) {
					searchlist.find("li.active").trigger("click");
					return false;
				}
			}).bind("focus", function() {
				if (/\S+/.test(t.val())) {
					t.trigger("keyup");
				}
			});
			;

			$("body").bind("click", hideOnBlur);

			initSearchListEvent(searchlist);
		};
		$(".wrapper_left").prepend(tpl);
		initSearch();
	}
};

var wiki = {
	"setLoginInfo" : function(u) {
		var r = {
			'html' : '',
			'class' : ''
		};
		if (u && u.name) {
			r["html"] = [
					'<span title="' + u.nick + '(' + u.name
							+ ')" class="login_name">' + u.nick + '</span>',
					'<span class="nav_arrow"></span>',
					'<a href="http://dev.t.qq.com/development/developer/" class="f12">编辑开发者信息</a>',
					'<a href="javascript:;" id="logoutBtn" class="f12" onclick="wiki.loginOut();">退出</a>' ]
					.join("\n");
			r["class"] = 'subnav subnav_login';
		} else if (u && !u.name && !u.nick) {
			r["html"] = [
					'<span title="还未开通微博" class="login_name">还未开通微博</span>',
					'<span class="nav_arrow"></span>',
					'<a class="f12" href="http://reg.t.qq.com/index.php?pref=test.open.t.qq.com" target="_blank">开通微博</a>',
					'<a class="f12" href="javascript:;" id="logoutBtn" onclick="wiki.loginOut();">退出</a>' ]
					.join("\n");
			r["class"] = 'subnav subnav_login';
		} else {
			r["html"] = '<a title="点击此处登录" class="login_btn" href="javascript:void(0);" id="loginBtn" hidefocus onclick="$(\'.getToken\').trigger(\'click\');" style="float:right;">登录</a>';
			r["class"] = '';
		}
		return r;
	},
	"setCookie" : function(name, value, options) {
		if (typeof value != 'undefined') {
			options = options || {};
			if (value === null) {
				value = '';
				options.expires = -1;
			}
			var expires = '';
			if (options.expires
					&& (typeof options.expires == 'number' || options.expires.toUTCString)) {
				var date;
				if (typeof options.expires == 'number') {
					date = new Date();
					date.setTime(date.getTime()
							+ (options.expires * 24 * 60 * 60 * 1000));
				} else {
					date = options.expires;
				}
				expires = '; expires=' + date.toUTCString();
			}
			var path = options.path ? '; path=' + (options.path) : '';
			var domain = options.domain ? '; domain=' + (options.domain) : '';
			var secure = options.secure ? '; secure' : '';
			document.cookie = [ name, '=', encodeURIComponent(value), expires,
					path, domain, secure ].join('');
		} else {
			var cookieValue = null;
			if (document.cookie && document.cookie != '') {
				var cookies = document.cookie.split(';');
				for (var i = 0; i < cookies.length; i++) {
					var cookie = jQuery.trim(cookies[i]);
					if (cookie.substring(0, name.length + 1) == (name + '=')) {
						cookieValue = decodeURIComponent(cookie
								.substring(name.length + 1));
						break;
					}
				}
			}
			return cookieValue;
		}
	},
	"login" : function(d) {
		var o = document.getElementById("login_status"), ret = d && d.ret, data = d
				&& d.data, errCode = d && d.errCode, info = wiki
				.setLoginInfo(data);
		wiki.u = data;
		o.innerHTML = info.html;
		o.className = info["class"];
		$("body").bind("mouseover", function(event) {
			if ($(o).find(".menu").size() === 0) {
				return false;
			}
			if ($.contains(o, event.target) || o === event.target) {
				$(o).addClass("menuContainer");
			} else {
				$(o).removeClass("menuContainer");
			}
		});
	},
	"loginOut" : function() {
		var clearLoginInfo = function() {
			if (window.pt_logout) {
				pt_logout.logout(function(n) {
					wiki.setLoginInfo({});
					wiki.setCookie('uin', null, {
						domain : 'qq.com',
						path : '/'
					});
					wiki.setCookie('skey', null, {
						domain : 'qq.com',
						path : '/'
					});
					wiki.setCookie('luin', null, {
						domain : 'qq.com',
						path : '/'
					});
					wiki.setCookie('lskey', null, {
						domain : 'qq.com',
						path : '/'
					});
					wiki.setCookie('p_uin', null, {
						domain : 't.qq.com',
						path : '/'
					});
					wiki.setCookie('p_skey', null, {
						domain : 't.qq.com',
						path : '/'
					});
					wiki.setCookie('p_luin', null, {
						domain : 't.qq.com',
						path : '/'
					});
					wiki.setCookie('p_lskey', null, {
						domain : 't.qq.com',
						path : '/'
					});
					location.reload();
				});
			}
		};
		if (window.pt_logout) {
			clearLoginInfo();
		} else {
			$.getScript(
					"http://imgcache.qq.com/ptlogin/ac/v9/js/ptloginout.js",
					clearLoginInfo);
		}
		return false;
	}
};

$(function() {
	$("body")
			.mouseover(
					function(event) {
						var target = event.target, subnavlist = $(".subnav"), currentSubNav = (function() {
							for (var i = 0, k = subnavlist.length; i < k; i++) {
								if ($.contains(subnavlist[i], target)
										|| target === subnavlist[i]) {
									return subnavlist[i];
								}
							}
							return false;
						})();
						if (currentSubNav) {
							$(currentSubNav).addClass("subnav_hover");
						} else {
							subnavlist.removeClass("subnav_hover");
						}
					});
	// 添加文本参数
	function addParamAndValue(key, value) {
		var type = "text", input = {
			"text" : '<input type="text" class="input_text para_value" placeholder="参数值" value="'
					+ value + '"/>',
			"file" : '<input type="file" class="para_value" placeholder="参数值" />'
		}[type];

		if ($("#para_list li").size() < 20) {
			$("#para_list")
					.append(
							$('<li>\
															<input type="text" class="input_text para_name" value="'
									+ key
									+ '" placeholder="参数名"/> = '
									+ input
									+ '\
															<a href="javascript:;" class="para_del icon_del" title="删除">&times;</a>\
														</li>'));
		} else {
			dialog.alert("参数过多");
		}
	}
	// 绑定api接口方法
	$("#ulApiList li").delegate(
			"a",
			"click",
			function() {
				var url = $(this).attr("data-url");
				var params = $(this).attr("data-param");
				var id = $(this).attr("data-id");
				var host = "smart.56iq.net";//location.host;
				$("input[name='api_url']").val("http://" + host + url);
				$(this).addClass("dianq").parent("li").siblings("li").children(
						"a").removeClass("dianq");
				$("#viewDoc").attr("href", "doc?id=" + id);
				// 点击后自动加载默认参数和默认值
				if (!/^\s*$/gi.test(params)) {
					var paramsArr = params.split("&");
					$("#para_list").html("");
					$.each(paramsArr, function(index, item) {
						var paramsArrKeyValue = item.split("=");
						addParamAndValue(paramsArrKeyValue[0],
								paramsArrKeyValue[1]);
					});
				}
				// $(this).addClass("dianq");
			})
	// 根据参数自动加载接口信息
	function initApi() {

		var links = $("#ulApiList li a");
		var id = GetUrlValueByParas(location.href, "id");
		if (!/^\s*$/gi.test(id)) {
			$.each(links, function(index, item) {
				var aid = $(item).attr("data-id");
				if (id == aid) {
					$(item).click();
				}
			});
		} else {
			$("#ulApiList li a:first").trigger("click");
		}
	}
	initApi();
});
