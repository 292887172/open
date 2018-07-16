 /** jsapi封装，用于跟android sdk进行通讯
 * Created by rdy on 8/14/17.
 */

    /**
     *发送控制指令
     *@return(String)
     */
    function sendCommand(commandList) {
         console.log(commandList);
         return window.jsapi.sendCommand(commandList);
    }

    /**
     *获取终端设备编号
     *@return(String)
     */
    function getDeviceId() {
        try{
            return window.jsapi.getDeviceId();
        }catch(e){
            console.log('在终端获取设备编号')
        }
    }
    /*
    *获取终端设备MacAddress
    */
    function getDeviceMacAddress() {
        try{
            return window.jsapi.getDeviceMacAddress();
        }
        catch(e){
            console.log('在终端获取设备mac地址')
        }
    }
    /*
    *获取终端设备产品秘钥key
    */
    function getDeviceKey() {
        try{
            return window.jsapi.getDeviceKey();
        }
        catch(e){
            console.log('在终端获取设备秘钥')
        }
    }
    /*
    *获取终端设备状态
    */
    function  askAllStatus(){
        try{
            return window.jsapi.askAllStatus();
        }catch(e){
            console.log('在终端获取设备当前状态')
        }
       
    }
    /*
     *调用终端消息提示
     type:0为Toast,1为Dialog
     */
    function  showMessage(type, title,content) {
        try{
            return window.jsapi.showMessage(type, title, content);
    
        }
        catch(e){
            console.log('在终端使用消息提示')
        }
       }
    /*
     *打开第三方App
     */
    function startOtherApp(packageName) {
        try{

          return window.jsapi.startOtherApp(packageName);
        }catch(e){
            console.log('在终端打开第三方应用')
        }
    }