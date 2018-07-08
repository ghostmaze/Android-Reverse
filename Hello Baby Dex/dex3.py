# -*- coding: UTF-8 -*-
import frida,sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


js_code = '''
    Java.perform(function(){
		var hookClass = undefined;
		var ClassUse = Java.use("java.lang.Class");
		var objectclass= Java.use("java.lang.Object");
		var dexclassLoader = Java.use("dalvik.system.DexClassLoader");
		var orininclass = Java.use("cn.chaitin.geektan.crackme.MainActivity");
		var Integerclass = Java.use("java.lang.Integer");
		var mainAc = orininclass.$new();
		
		
		dexclassLoader.loadClass.overload('java.lang.String').implementation = function(name){
			var hookname = "cn.chaitin.geektan.crackme.MainActivityPatch";
			var result = this.loadClass(name,false);
			
			if(name == hookname){
				var hookClass = result;
				var hookClassCast = Java.cast(hookClass,ClassUse);
				console.log("-----------------------------GET Constructor-------------------------------------");
				var ConstructorParam =Java.array('Ljava.lang.Object;',[objectclass.class]);
				var Constructor = hookClassCast.getDeclaredConstructor(ConstructorParam);
				console.log("Constructor:"+Constructor);
				console.log("orinin:"+mainAc);
				var instance = Constructor.newInstance([mainAc]);
				console.log("patchAc:"+instance);
				send(instance);
				
				console.log("-----------------------------GET Methods----------------------------");
				var func = hookClassCast.getDeclaredMethods();
				console.log(func);
				console.log("--------------------------GET Joseph Function---------------------------");
				console.log(func[0]);
				var f = func[0];
				var num1 = Integerclass.$new(5);
				var num2 = Integerclass.$new(6);
				var numArr1 = Java.array('Ljava.lang.Object;',[num1,num2]);
				var num3 = Integerclass.$new(7);
				var num4 = Integerclass.$new(8);
				var numArr2 = Java.array('Ljava.lang.Object;',[num3,num4]);
				console.log("-----------------------------GET Array------------------------------");
				console.log(numArr1);
				console.log(numArr2);
				var rtn1 = f.invoke(instance,numArr1);
				var rtn2 = f.invoke(instance,numArr2);
				console.log("--------------------------------FLAG---------------------------------");
				console.log("DDCTF{"+rtn1+rtn2+"}");
				console.log("--------------------------------OVER--------------------------------");
				return result;

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