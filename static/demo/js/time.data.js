/**
 * Created by rdy on 4/11/17.
 */
c1 = [];
c2 = [];

for(var i=1; i< 60; i++){
    t1 = {
        value: "110101",
        text: String(i)
    };
    c1.push(t1)
}
for(var i=0; i< 60; i++){
    t1 = {
        value: "110102",
        text: String(i)
    };
    c2.push(t1)
}
var timeData =[{
            value: '110000',
            text: '0',
            children: c1
},{
            value: '120000',
            text: '1',
            children: c2
}];