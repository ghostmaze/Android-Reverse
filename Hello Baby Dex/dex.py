# -*- coding: UTF-8 -*-
import frida,sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


js_code = '''
    Java.perform(function(){
		var robust = Java.use("com.meituan.robust.utils.EnhancedRobustUtils");
		robust.invokeReflectMethod.implementation = function(v1,v2,v3,v4,v5){
			var result = this.invokeReflectMethod(v1,v2,v3,v4,v5);
			if(v1=="Joseph"){
				console.log("functionName:"+v1);
				console.log("functionArg3:"+v3);
				console.log("functionArg4:"+v4);
				send(v4);
				console.log("return:"+result);
				console.log("-----------------------------------------------------")
			}
			
			else if(v1=="equals"){
				console.log("functionName:"+v1);
				console.log("functionArg3:"+v3);
				console.log("functionArg4:"+v4);
				send(v4);
				console.log("return:"+result);
			}
			return result;
		}
});
'''
session = frida.get_usb_device().attach("cn.chaitin.geektan.crackme")
script = session.create_script(js_code)
script.on('message',on_message)
script.load()
sys.stdin.read()