common._dialog = function () {
	var o,
	tpl = '<div class="modulebox">\
						<iframe width="100%" height="100%" frameborder="0" class="modulebox_iframe"></iframe>\
						<div class="modulebox_mask"></div>\
						<div class="modulebox_win">\
							<a href="javascript:;" class="modulebox_close" title="关闭"></a>\
							<h2 class="modulebox_title">提示</h2>\
							<div class="modulebox_content"></div>\
						</div>\
					</div>';
	var m = $(tpl).appendTo($('body')),
	w = m.find('.modulebox_win'),
	b = m.find('.modulebox_close'),
	t = m.find(".modulebox_title"),
	c = m.find(".modulebox_content")
		o = {
		"dom" : {
			"box" : m,
			"win" : w,
			"close_btn" : b,
			"title" : t,
			"content" : c
		},
		"close" : function (op) {
			op && op.beforeClose && op.beforeClose();
			m.hide();
			op && op.afterClose && op.afterClose();
			$("body").removeAttr("scroll").removeClass("noscroll");
		},
		"show" : function (op) {
			typeof(op.title) != "undefined" && t.html(op.title);
			typeof(op.text) != "undefined" && c.html(op.text);

			if (op.width) {
				if (/^\d+%$/.test(op.width)) {
					op.width = (document.documentElement.clientWidth || document.body.clientWidth) * parseInt(op.width) * 0.01;
				}
				w.css({
					'width' : op.width,
					'margin-left' : -parseInt(op.width, 10) / 2
				});
			}

			if (op.height) {
				if (/^\d+%$/.test(op.height)) {
					op.height = (document.documentElement.clientHeight || document.body.clientHeight) * parseInt(op.height) * 0.01;
					op.height = op.height | 0;
				}
				w.css({
					'height' : op.height,
					'margin-top' : -parseInt(op.height, 10) / 2
				});
				c.css({
					'height' : op.height - 41
				});
			}

			if (!m.is(":visible")) {
				m.show();
				op.callback && op.callback();
				if (op.hideScroller) {
					$("body").attr("scroll", "no").addClass("noscroll");
				}
			}
		},
		"alert" : function (op, callback) {
			var settings = {
				"width" : 420,
				"height" : 150,
				"text" : "",
				"title" : "提示"
			},
			tpl = '<form style="text-align:center;margin:0 20px;">\
						 		  <div style="text-align:left;display:inline-block;* display:inline;zoom:1;margin:22px auto 14px;word-wrap:break-word;word-break:break-all;">\
						 			##\
						 		  </div>\
					 		</form>\
					 		<div align="center">\
					 		  	<input type="button" class="btn2 close_btn" value="确定"/>\
					 		</div>';
			if (typeof(op) === "string") {
				op = tpl.replace('##', op);
				settings = $.extend(settings, {
						"text" : op
					}); //
			} else if (typeof(op) === "object") {
				op.text = tpl.replace('##', op.text);
				$.extend(settings, op);
			}
			this.show(settings);
			c.find(".close_btn").bind("click", function (event) {
				var isClose = callback && callback(event);
				if (isClose !== false) {
					o.close();
				}
			});
		},
		"confirm" : function (op, okFn, cancelFn) {
			var settings = {
				"width" : 420,
				"height" : 150,
				"text" : "",
				"title" : "提示"
			},
			tpl = '<div style="text-align:center;margin:0 20px;">\
						 		  <div style="text-align:left;display:inline-block;* display:inline;zoom:1;margin:22px auto 14px;word-wrap:break-word;word-break:break-all;">\
						 			##\
						 		  </div>\
					 		</div>\
					 		<div align="center">\
					 		  	<a href="javascript:;" class="btn2 sure_btn">确定</a>\
					 		  	<a href="javascript:;" class="btn3 close_btn">取消</a>\
					 		</div>';
			if (typeof(op) === "string") {
				op = tpl.replace('##', op);
				settings = $.extend(settings, {
						"text" : op
					}); //
			} else if (typeof(op) === "object") {
				op.text = tpl.replace('##', op.text);
				$.extend(settings, op);
			}
			this.show(settings);
			c.find(".sure_btn").bind("click", function () {
				o.close();
				okFn && okFn();
			});
			c.find(".close_btn").bind("click", function () {
				o.close();
				cancelFn && cancelFn();
			});
		},
		"showFrame" : function (op) {
			var settings = {
				"width" : "420",
				"height" : "150",
				"text" : "about:blank",
				"title" : "提示"
			},
			tpl = '<iframe src="{text}" frameborder="0" width="100%" height="100%" marginwidth="0" marginheight="0"></iframe>';

			if (typeof(op) === "string") {
				settings = $.extend(settings, {
						"text" : op
					});
			} else if (typeof(op) === "object") {
				settings = $.extend(settings, op);
			}

			settings.text = tpl.replace(/\{(\w+)\}/g, function () {
					var i = arguments[1] || "";
					if (settings[i]) {
						return settings[i];
					} else {
						return "{" + i + "}";
					}
				});
			this.show(settings);
		}
	};
	b.bind("click", function () {
		o.close();
	});
	return o;
};
