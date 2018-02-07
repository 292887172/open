var checkSubmitFlg = false;
        function create_procuct(type,type1) {
            if(type1=="wifi"){
                $(".dtbox").hide();
                $(".technology").hide();
            }
            else{
                $(".dtbox").show();
                $(".technology").show();
            }
            $(".markLayout").show();
            if (type == '1') {
                $("#product_category_detail").val('1');
                $("#productType").html("油烟机");
                $("#show_logo").attr('src', "http://storage.56iq.net/group1/M00/1D/0C/CgoKQ1m3oSmAbhKvAAALicfeZeI743.png");
            }
            else if (type == '2') {
                $("#product_category_detail").val('2');
                $("#productType").html("集成灶");
                $("#show_logo").attr('src', "http://storage.56iq.net/group1/M00/1D/0C/CgoKQ1m3oYGANZPwAAAIvQGt7RM216.png");
            }
            else if (type == '11') {
                $("#product_category_detail").val('11');
                $("#productType").html("烤箱");
                $("#show_logo").attr('src', "http://storage.56iq.net/group1/M00/1D/0C/CgoKQ1m3oWqAbFICAAAKkW-6s_Q059.png");
            }
                $("#newHtmlBox").css('display', 'block');
            $(document).ready(function () {
                $(".markLayout").click(function (event) {
                    if (!$(this).hasClass("popBox") && !$(this).hasClass("tuya-btn tuya-btn-default mark-bottom-btn mark-children-bottom-btn")) {
                        new_close();
                    }
                    event.stopPropagation(); //阻止事件冒泡
                });
            });
        }
        function submit_product() {
                var form = $("form[name=formProduct]");

                var product_name = $("#product_name").val();
                if (product_name == '') {
                    check_name();
                    return;
                }
                if (!checkSubmitFlg) {
                    checkSubmitFlg = true;
                    form.submit();

                    // $(".markLayout").hide();
                    // new_close();
                    //$("#loadingDiv").show();
                }
                else {
                    bootbox.alert("不能重复提交");
                }
            }
        function check_name() {
            if ($("#product_name").val() == '') {
                $('#productName').html("产品名称不能为空");
                $('#productName').css("display", "block");
                return '';
            }
            else {
                $('#productName').css("display", "none");
            }
        }
        function select_progm(val) {
            $(".product_group").val(val);
            if(document.getElementsByName('select_group')[0].checked){
            $(".select-progm1").html("WiFi方案要求设备支持5V供电，两路串口，适用于集成灶，油烟机");
            }
            else{
                $(".select-progm1").html("Android屏方案要求设备支持5V供电，一路串口，适用于烤箱，冰箱");
            }
        }
        function new_close() {

                $(".markLayout").hide();
                $("#newHtmlBox").css('display', 'none');
                $("#product_name").val('');
                $("#show_logo").attr('src', "");
                $('#productName').css("display", "none");
                $(".m").hide();
                myPlayer.pause();
            }
        $("#dev-demo").click(function () {
                window.location.href = $(this).parent('div').data('url')
            });
        $("#WiFi-oven-demo").click(function () {
            $(".markLayout").show();
            $(".m").show();
            myPlayer.play();
        });
        $(".close-video").click(function () {
            new_close()
        });
        function dont_develop() {
                bootbox.confirm("您现在还不是开发者用户,请确定前往完善开发者信息",function(result){
                    if(result){
                        location.href="/center";
                    }

            })
        }
        /**
 * Created by Administrator on 2018/2/2.
 */
