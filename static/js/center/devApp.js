var DevAppInfo = {
    isNomal: // 检查是否包含特殊字符
        function (value) {
            var pattern = new RegExp("[/\\\\:*?\"<>|;]");
            return !pattern.test(value);
            /**
             *
             * /^[^\|"'<>]*$/
             */
        },
    isNum:// 检查是否为数字
        function (value) {
            return (/^[0-9]*$/).test(value);
        },
    isNomalEmail:// 检查是否为邮件格式
        function (value) {
            return (/^[a-zA-Z0-9._\-]{1,}@[a-zA-Z0-9_\-]{1,}\.[a-zA-Z0-9_\-.]{1,}$/).test(value);
        },
    isPhone: function (value) {
        return (/^((0\d{2,3})-)(\d{7,8})(-(\d{3,}))?$/).test(value);
    },
    isMobile: /**
     手机号码有效性验证    */
        function (value) {
        return ( /^0?1[3|4|5|7|8][0-9]\d{8}$/).test(value);
    },
    doVerifyMobile: function (obj, flag, length) {
        var value = obj.value;
        var errorObj = $('#' + obj.name + 'ErrorId');
        if (flag) {
            if (value == null || value == '') {
                errorObj.html('请输入正确的手机号');
                return false;
            } else if (!this.isNum(value)) {
                errorObj.html('请输入正确的手机号');
                return false;
            } else {
                errorObj.html('');
                return true;
            }
        }
    },
    doVerifyEmail: function (obj, flag, length) {
        var value = obj.value;
        var errorObj = $('#' + obj.name + 'ErrorId');
        if (flag) {
            if (value == null || value == '' || !this.isNomalEmail(value) || $.trim(value).length > length) {
                errorObj.html('请输入正确的邮箱地址');
                return false;
            } else {
                errorObj.html('');
                return true;
            }
        }
    },
    doVerifyPhone: function (obj, flag, length) {
        var value = obj.value;
        var errorObj = $('#' + obj.name + 'ErrorId');
        if (value != null && value.length > 0 && (value.length > length || !this.isPhone(value))) {
            errorObj.html('请输入正确的电话信息');
            return false;
        } else {
            errorObj.html('');
            return true;
        }
    },
    // --end
    doVerifyNum: function (obj, flag, length) {
        var value = obj.value;
        var errorObj = $('#' + obj.name + 'ErrorId');
        if (flag) {
            if (value == null || value == '' || $.trim(value).length > length) {
                errorObj.html('请输入正确QQ号信息');
                return false;
            } else if (!this.isNomal(value)) {
                errorObj.html('输入信息中不能有特殊字符');
                return false;
            } else if (!this.isNum(value)) {
                errorObj.html('请输入正确QQ号信息');
                return false;
            } else {
                errorObj.html('');
                return true;
            }
        } else {
            if (!this.isNomal(value) || (value != null && value.length > length)) {
                errorObj.html('输入信息中不能有特殊字符');
                return false;
            } else if (!this.isNum(value)) {
                errorObj.html('请输入正确QQ号信息');
                return false;
            } else {
                errorObj.html('');
                return true;
            }
        }

    },
    doVerifyContent: // æ ¡éªŒç‰¹æ®Šå­—ç¬¦
        function (obj, flag, length) {
            var value = obj.value;
            var errorObj = $('#' + obj.name + 'ErrorId');
            if (flag) {
                if (value == null || value == '') {
                    errorObj.html('è¯·è¾“å…¥æ­£ç¡®çš„ä¿¡æ¯');
                    $(errorObj).css('visibility', 'visible');
                    this.changeProButtonCss(false);
                    return false;
                } else if ($.trim(value).length > length) {
                    errorObj.html('è¾“å…¥ä¿¡æ¯ä¸è¶…è¿‡' + length + 'å­—ç¬¦');
                    this.changeProButtonCss(false);
                    $(errorObj).css('visibility', 'visible');
                    return false;
                } else {
                    //errorObj.html('');
                    $(errorObj).css('visibility', 'hidden');
                }
            } else {
                if (value != null && value.length > length) {
                    errorObj.html('è¾“å…¥ä¿¡æ¯ä¸è¶…è¿‡' + length + 'å­—ç¬¦');
                    $(errorObj).css('visibility', 'visible');
                    this.changeProButtonCss(false);
                    return false;
                } else {
                    $(errorObj).css('visibility', 'hidden');
                    //errorObj.html('');
                }
            }
            this.changeProButtonCss(true);
            return true;
        },// --end
    doVerifyMsgName: function (obj, flag, length, errMsg) {
        var value = obj.value;
        var errorObj = $('#' + obj.name + 'ErrorId');
        if (flag) {
            if (value == null || value == '') {
                errorObj.html('请输入正确的' + errMsg);
                //  $(errorObj).css('visibility','visible');
                return false;
            } else if ($.trim(value).length > length) {
                errorObj.html('请输入正确的' + errMsg);
                //errorObj.html('è¾“å…¥ä¿¡æ¯ä¸è¶…è¿‡'+length+'å­—ç¬¦');
                // $(errorObj).css('visibility','visible');
                return false;
            } else if (!this.isNomal(value)) {
                errorObj.html('输入信息中不能有特殊字符');
                //$(errorObj).css('visibility','visible');
                return false;
            } else {
                errorObj.html('');
                //$(errorObj).css('visibility','hidden');
                return true;
            }
        } else {
            if (value != null && value.length > length) {
                errorObj.html('请输入正确的' + errMsg);
                //errorObj.html('è¾“å…¥ä¿¡æ¯ä¸è¶…è¿‡'+length+'å­—ç¬¦');
                //$(errorObj).css('visibility','visible');
                return false;
            } else if (!this.isNomal(value)) {
                errorObj.html('输入信息中不能有特殊字符');
                //$(errorObj).css('visibility','visible');
                return false;
            } else {
                errorObj.html('');
                //$(errorObj).css('visibility','hidden');
                return true;
            }
        }

    },
    doVerify: // 验证字符有效性¦
        function (obj, flag, length) {
            var value = obj.value;
            var errorObj = $('#' + obj.name + 'ErrorId');
            if (flag) {
                if (value == null || value == '') {
                    errorObj.html('è¯·è¾“å…¥æ­£ç¡®çš„ä¿¡æ¯');
                    return false;
                } else if ($.trim(value).length > length) {
                    errorObj.html('请输入小于' + length + '个字符');
                    return false;
                } else if (!this.isNomal(value)) {
                    errorObj.html('输入信息中不能有特殊字符');
                    return false;
                } else {
                    errorObj.html('');
                    return true;
                }
            } else {
                if (value != null && value.length > length) {
                    errorObj.html('请输入小于' + length + '个字符');
                    return false;
                } else if (!this.isNomal(value)) {
                    errorObj.html('输入信息中不能有特殊字符');
                    return false;
                } else {
                    errorObj.html('');
                    return true;
                }
            }

        },// --end
    isNetUrl: function (str_url) {
        var strRegex = "^((https|http|ftp|rtsp|mms)?://)"
            + "?(([0-9a-z_!~*'().&=+$%-]+: )?[0-9a-z_!~*'().&=+$%-]+@)?" // ftpçš„user@
            + "(([0-9]{1,3}\.){3}[0-9]{1,3}" // IPå½¢å¼çš„URL-
                // 199.194.52.184
            + "|" // å…è®¸IPå’ŒDOMAINï¼ˆåŸŸåï¼‰
            + "([0-9a-z_!~*'()-]+\.)*" // åŸŸå- www.
            + "([0-9a-z][0-9a-z-]{0,61})?[0-9a-z]\." // äºŒçº§åŸŸå
            + "[a-z]{2,6})" // first level domain- .com or .museum
            + "(:[0-9]{1,4})?" // ç«¯å£- :80
            + "((/?)|" // a slash isn't required if there is no file
                // name
            + "(/[0-9a-z_!~*'().;?:@&=+$,%#-]+)+/?)$";
        var re = new RegExp(strRegex);
        if (re.test(str_url)) {
            return (true);
        } else {
            return (false);
        }
    },
    doVerifyNetUrl: function (obj, flag, length) {
        var value = obj.value;
        if (value != null && value.length > 0 && value.length > length) {
            $('#coNetUrlErrorId').html('请输入正确的网址');

            return false;
        } else if (value != null && value.length > 0 && !this.isNetUrl(obj.value)) {
            $('#coNetUrlErrorId').html('请输入正确的网址');
            return false;
        } else {
            $('#coNetUrlErrorId').html('');
        }
        return true;
    },
    doVerifyDevCode: function (obj, length) {
        var value = obj.value;
        var errorObj = $('#' + obj.name + 'ErrorId');
        if (value == null || value == '') {
            errorObj.html('请输入正确的验证码');
            return false;
        } else if ($.trim(value).length != length) {
            errorObj.html('请输入正确的' + length + '位验证码');
            return false;
        } else if (!this.isNomal(value)) {
            errorObj.html('输入信息中不能有特殊字符');
            return false;
        } else {
            errorObj.html('');
            return true;
        }
    },
    doVerifyAgree: function (obj) {
        if (!obj.checked) {
            $('#agreeErrorId').css('visibility', 'visible');
            //$('#agreeErrorId').html('è¯·ç‚¹å‡»åŒæ„åè®®');
            //this.changeButtonCSS(false);
            $('#agreeErrorId').addClass('error');
            return false;
        }
//			  $('#agreeErrorId').html('');
        $('#agreeErrorId').css('visibility', 'hidden');
        $('#agreeErrorId').removeClass('error');
        this.changeButtonCSS(true);
        return true;
    },

    doVerifyValue: function (field, length, errMsg, show) {
        var value = jQuery('input[name=' + field + ']').val();
        var proObj = jQuery('#' + field + 'ErrorId');
        if (value == null || value == '') {
            if (show)proObj.html('请输入正确的' + errMsg);
            return false;
        } else if ($.trim(value).length > length) {
            if (show) proObj.html('请输入小于' + length + '字符');
            return false;
        } else if (!DevAppInfo.isNomal(value)) {
            if (show) proObj.html('输入信息中不能有特殊字符');
            return false;
        } else {
            proObj.html('');
            return true;
        }
    },
    /***
     * 改变按钮样式
     */
    changeButtonCSS: function (flag) {
        if (!flag) {
            this.changeCss(flag);
            return false;
        }

        console.log($("#coFacUidErrorId").attr('class'));
        if ($("#coFacUidErrorId").attr('class') == 'error') {
            this.changeCss(false);
            return false;
        }
        if (!DevAppInfo.doVerifyValue('coName', 64, '公司/团队名称123', true)) {

            this.changeCss(false);
            return false;
        }
        if (!DevAppInfo.doVerifyValue('coDevScale', 64, '开发团队人数', false)) {
            this.changeCss(false);
            return false;
        }
        if (!DevAppInfo.doVerifyValue('coContactName', 64, '联系人姓名', false)) {
            this.changeCss(false);
            return false;
        }
        if (!DevAppInfo.doVerifyValue('coContactRole', 64, '联系人职务', false)) {
            this.changeCss(false);
            return false;
        }

        var value = $('input[name=coContactMobile]').val();
        if (value == null || value == '') {
            this.changeCss(false);
            return false;
        } else if (!DevAppInfo.isNum(value)) {
            this.changeCss(false);
            return false;
        } else {
            $('#coContactMobileErrorId').html('');
        }
        var emailvalue = $('input[name=devEmail]').val();
        if (emailvalue == null || emailvalue == '') {
            //$('#devEmailErrorId').html('请输入正确的邮箱地址');
            this.changeCss(false);
            return false;
        } else if ($.trim(emailvalue).length > 64) {
            //$('#devEmailErrorId').html('邮箱地址小于64个字符串');
            this.changeCss(false);
            return false;
        } else if (!this.isNomalEmail(emailvalue)) {
            //$('#devEmailErrorId').html('输入信息中不能有特殊字符');
            this.changeCss(false);
            return false;
        } else {
            $('#devEmailErrorId').html('');
        }
        var devCodeValue = $('input[name=devCode]').val();
        if (devCodeValue == null || devCodeValue == '') {
            this.changeCss(false);
            return false;
        } else if ($.trim(devCodeValue).length != 6) {
            //$('#devCodeErrorId').html('请输入6位验证码');
            this.changeCss(false);
            return false;
        } else if (!DevAppInfo.isNomal(devCodeValue)) {
            //	$('#deCodeErrorId').html('输入信息中不能有特殊字符');
            this.changeCss(false);
            return false;
        } else {
            $('#devCodeErrorId').html('');
        }
        var checkeError = this.checkErro();
        if (!checkeError) {
            return checkeError;
        }
        this.changeCss(true);
        return true;
    },
    checkErro: function () {
        /****/
        var temp = $("#agreeErrorId").attr('class');
        if (temp.length > 0) {
            this.changeCss(false);
            return false;
        }
        return true;

    },
    changeCss: function (flag) {
        if (!flag) {
            jQuery("#submitBtn").addClass("disable");
            //jQuery("#submitBtn" ).disabled=true;
            jQuery("#submitBtn").attr('disabled', 'disabled');
        } else {
            jQuery("#submitBtn").removeClass("disable");
            //jQuery("#submitBtn" ).disabled=false;
            jQuery("#submitBtn").removeAttr('disabled');
        }

        $("span").each(
            function () {
                if ($.trim($(this).attr("id")) != '') {
                    if ($(this).attr("id").indexOf("ErrorId") > 0) {
                        if ($(this).css('visibility') == 'hidden') {
                            $(this).removeClass('error');
                        } else if ($(this).css('visibility') == 'visible') {
                            $(this).addClass('error');
                        }
                        else if ($.trim($(this).html()) == '') {
                            $(this).removeClass('error');
                        } else if ($.trim($(this).html()) != '') {
                            $(this).addClass('error');
                        }
                    }
                }
            }
        );
    },
    sAlert: function (txt) {
        var mask = document.getElementById("mask");
        var pop_win = document.getElementById("pop_win");
        mask.style.height = document.body.offsetHeight + "px";
        pop_win.getElementsByTagName("div")[0].innerHTML = txt;
        pop_win.style.display = "block";
        pop_win.style.marginTop = (0 - (pop_win.offsetHeight / 2)) + "px";
        mask.style.display = "block";
    },
    cAlert: function () {
        var mask = document.getElementById("mask");
        var pop_win = document.getElementById("pop_win");
        var urlId = $("#urlId").text();
        pop_win.style.display = "none";
        mask.style.display = "none";
        if (urlId != '') {
        //
            window.location.reload();
        }
    }

};
