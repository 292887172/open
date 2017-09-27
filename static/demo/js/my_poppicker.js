/**
 * Created by rdy on 4/12/17.
 */
/**
 * 弹出选择列表插件
 * 此组件依赖 listpcker ，请在页面中先引入 mui.picker.css + mui.picker.js
 * varstion 1.0.1
 * by Houfeng
 * Houfeng@DCloud.io
 */

(function($, document) {

	//创建 DOM
	$.dom = function(str) {
		if (typeof(str) !== 'string') {
			if ((str instanceof Array) || (str[0] && str.length)) {
				return [].slice.call(str);
			} else {
				return [str];
			}
		}
		if (!$.__create_dom_div__) {
			$.__create_dom_div__ = document.createElement('div');
		}
		$.__create_dom_div__.innerHTML = str;
		return [].slice.call($.__create_dom_div__.childNodes);
	};

	var panelBuffer = '<div class="mui-poppicker" id="picture" style="width:82%;margin-left: 55px;border-radius: 25px;">\
		<h4 style="padding-left:15px;padding-top: 15px;font-size: 16px;">设置烘烤温度：<span id="block-range-tem" style="font-size: 17px;color:#f35019">200℃\
		</span></h4>\
		<div class="mui-input-row mui-input-range">\
		<div id="range-progressbar" class="mui-progressbar">\
                    <span style="translate3d(1%, 0px, 0px)"></span>\
                </div>\
	        <input type="range" value="200" min="30" max="220" id="block-range" style="background: rgba(0,0,0,0);z-index: 2;top:20px">\
        </div>\
		<div class="mui-poppicker-body" id="m-poppicker-body">\
		<h5 style="padding-left: 20px;padding-bottom: 5px; line-height: 30px;">设置烘烤时间：<span id="block-range-hour">1 </span>小时\
		<span id="block-range-min">0 </span>分钟</h5>\
		</div>\
		<div class="mui-poppicker-header">\
			<button class="mui-btn mui-btn-orange mui-poppicker-btn-ok" onclick="confirm()">确定</button>\
			<button class="mui-btn mui-poppicker-btn-cancel">取消</button>\
			<div class="mui-poppicker-clear"></div>\
		</div>\
	</div>';

	var pickerBuffer = '<div class="mui-picker">\
		<div class="mui-picker-inner">\
			<div class="mui-pciker-rule mui-pciker-rule-ft mui-picker-rule-left">小时</div>\
			<ul class="mui-pciker-list">\
			</ul>\
			<div class="mui-pciker-rule mui-pciker-rule-bg"></div>\
		</div>\
	</div>';

	//定义弹出选择器类
	var PopPicker = $.PopPicker = $.Class.extend({
		//构造函数
		init: function(options) {
			var self = this;
			self.options = options || {};
			self.options.buttons = self.options.buttons || ['取消', '确定'];
			self.panel = $.dom(panelBuffer)[0];
			document.body.appendChild(self.panel);
			self.ok = self.panel.querySelector('.mui-poppicker-btn-ok');
			self.cancel = self.panel.querySelector('.mui-poppicker-btn-cancel');
			self.body = self.panel.querySelector('.mui-poppicker-body');
			self.mask = $.createMask();
			self.cancel.innerText = self.options.buttons[0];
			self.ok.innerText = self.options.buttons[1];
			self.cancel.addEventListener('tap', function(event) {
				self.hide();
			}, false);

			self.mask[0].addEventListener('tap', function() {
				self.hide();
			}, false);
			self._createPicker();

		},
		_createPicker: function() {
			var self = this;
			var layer = self.options.layer || 1;
			var width = (100 / layer) + '%';
			self.pickers = [];
			for (var i = 1; i <= layer; i++) {
				var pickerElement = $.dom(pickerBuffer)[0];
				pickerElement.style.width = width;
				self.body.appendChild(pickerElement);
				var picker = $(pickerElement).picker();
				self.pickers.push(picker);
				pickerElement.addEventListener('change', function(event) {

					self.setchooseData(self.getSelectedItems());
					var nextPickerElement = this.nextSibling;
					if (nextPickerElement && nextPickerElement.picker) {
						var eventData = event.detail || {};
						var preItem = eventData.item || {};
						nextPickerElement.picker.setItems(preItem.children);
					}
					

				}, false);
			}
		},
		//填充数据
		setData: function(data) {
			var self = this;
			data = data || [];
			self.pickers[0].setItems(data);
		},
		//获取选中的项（数组）
		getSelectedItems: function() {
			var self = this;
			var items = [];
			for (var i in self.pickers) {
				var picker = self.pickers[i];
				items.push(picker.getSelectedItem() || {});
			}
			return items;
		},
		//显示
		show: function(callback) {
			var self = this;
			self.callback = callback;
			self.mask.show();
			document.body.classList.add($.className('poppicker-active-for-page'));
			self.panel.classList.add($.className('active'));
			//处理物理返回键
			self.__back = $.back;
			$.back = function() {
				self.hide();
			};
		},
		//隐藏
		hide: function() {
			var self = this;
			if (self.disposed) return;
			self.panel.classList.remove($.className('active'));
			self.mask.close();
			document.body.classList.remove($.className('poppicker-active-for-page'));
			//处理物理返回键
			$.back=self.__back;
			
		},
		dispose: function() {
			var self = this;
			self.hide();
			setTimeout(function() {
				self.panel.parentNode.removeChild(self.panel);
				for (var name in self) {
					self[name] = null;
					delete self[name];
				};
				self.disposed = true;
			}, 300);
		},
		// 自定义扩展方法,设置选中的值
		setchooseData:function (items) {
			var blockHour = document.getElementById('block-range-hour');
			var blockMin = document.getElementById('block-range-min');
			if (parseInt(items[0].text) < 10) {
				blockHour.innerText = items[0].text;
				blockMin.innerText = items[1].text;
			}
        }
	});

})(mui, document);