service Device {
    oneway void ping(),
    string stats(),
    map<string,string> get_status(1:string deviceId),
    map<string,string> heartbeat(1:string deviceId,2:i32 interval),
    map<string,string> heartbeat_diy(1:string deviceId,2:i32 status,3:i32 interval),
}