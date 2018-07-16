/**
 * Created by Administrator on 2017/11/29.
 */

function lessIE9() {
    if(navigator.appName == "Microsoft Internet Explorer"&&parseInt(navigator.appVersion.split(";")[1].replace(/[ ]/g, "").replace("MSIE",""))<9){
        return true;
    }
}
function isIE() {
         if(!!window.ActiveXObject || "ActiveXObject" in window){
                return true;
            }
         else {
             return false;
         }
    }