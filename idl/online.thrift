// 设备基础服务
service Device {
    oneway void ping(),
    // 获取服务统计信息（运维用）
    string stats(),
    // 查询设备在线状态
    // deviceId：设备编号
    // 返回消息示例：{'msg': '请求成功', 'data': 'online', 'code': '0'}
    map<string,string> get_status(1:string deviceId),
    // 提交心跳
    // deviceId：设备编号，interval：心跳间隔（单位秒）
    // 返回消息示例：{'msg': '请求成功', 'data': '', 'code': '0'}
    map<string,string> heartbeat(1:string deviceId,2:i32 interval),
    // 提交心跳（自定义状态）
    // deviceId：设备编号，status：在线状态（0=离线，1=在线），interval：心跳间隔（单位秒）
    // 返回消息示例：{'msg': '请求成功', 'data': '', 'code': '0'}
    map<string,string> heartbeat_diy(1:string deviceId,2:i32 status,3:i32 interval),
}