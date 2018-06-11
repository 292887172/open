/** jsapi封装，用于跟android sdk进行通讯
 * Created by tsengdavid on 7/14/16.
 */

    /**
     *关闭微信登录网页
     *@return(String)
     */
    function WxLoginExit(status) {
            return window.jsapi.wxLoginExit(status);
    }

