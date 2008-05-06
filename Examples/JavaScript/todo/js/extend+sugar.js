// 8< ---[Extend.js]---
// This module implements a complete OOP layer for JavaScript that makes it
// easy to develop highly structured JavaScript applications.
// 
// Classes are created using extend by giving a dictionary that contains the
// following keys:
// 
// - 'name', an optional name for this class
// - 'parent', with a reference to a parent class (created with Extend)
// - 'initialize', with a function to be used as a constructor
// - 'properties', with a dictionary of instance attributes
// - 'methods', with a dictionary of instance methods
// - 'shared', with a dictionary of class attributes
// - 'operations', with a dictionary of class operations
// 
// Extend 2.0 is a rewritten, simplified version of the Extend 1 library. It is
// not compatible with the previous versions, but the API will be stable from
// this release.
// 
// You can get more information at the Extend [project
// page](http://www.ivy.fr/js/extend).
var Extend={}
Extend._VERSION_='2.0.0';
Extend.Registry={}
Extend.Class=	function(declaration){
		// Classes are created using extend by giving a dictionary that contains the
		// following keys:
		// 
		// - 'name', an optional name for this class
		// - 'parent', with a reference to a parent class (created with Extend)
		// - 'initialize', with a function to be used as a constructor
		// - 'properties', with a dictionary of instance attributes
		// - 'methods', with a dictionary of instance methods
		// - 'shared', with a dictionary of class attributes
		// - 'operations', with a dictionary of class operations
		// 
		// Invoking the 'Class' function will return you a _Class Object_ that
		// implements the following API:
		// 
		// - 'isClass()' returns *true*( (because this is an object, not a class)
		// - 'getName()' returns the class name, as a string
		// - 'getParent()' returns a reference to the parent class
		// - 'getOperation(n)' returns the operation with the given name
		// - 'hasInstance(o)' tells if the given object is an instance of this class
		// - 'isSubclassOf(c)' tells if the given class is a subclass of this class
		// - 'listMethods()' returns a dictionary of *methods* available for this class
		// - 'listOperations()' returns a dictionary of *operations* (class methods)
		// - 'listShared()' returns a dictionary of *class attributes*
		// - 'listProperties()' returns a dictionary of *instance attributes*
		// - 'bindMethod(o,n)' binds the method with the given name to the given object
		// - 'proxyWithState(o)' returns a *proxy* that will use the given object as if
		// it was an instance of this class (useful for implementing 'super')
		// 
		// When you instanciate your class, objects will have the following methods
		// available:
		// 
		// - 'isClass()' returns *true*( (because this is an object, not a class)
		// - 'getClass()' returns the class of this instance
		// - 'getMethod(n)' returns the bound method which name is 'n'
		// - 'getCallback(n)' the equivalent of 'getMethod', but will give the 'this' as
		// additional last arguments (useful when you the invoker changes the 'this',
		// which happens in event handlers)
		// - 'isInstance(c)' tells if this object is an instance of the given class
		// 
		// Using the 'Class' function is very easy (in *Sugar*):
		// 
		// >   var MyClass = Extend Class {
		// >      name:"MyClass"
		// >      initialize:{
		// >         self message = "Hello, world !"
		// >      }
		// >      methods:{
		// >        helloWorld:{print (message)}
		// >      }
		// >   }
		// 
		// instanciating the class is very easy too
		// 
		// >   var my_instance = new MyClass()
		var __this__=Extend;
		var full_name=declaration.name;
		var class_object=function(){
			if ( (! ((arguments.length == 1) && (arguments[0] == "__Extend_SubClass__"))) )
			{
				 var properties = class_object.listProperties()
				 for ( var prop in properties ) {
				   this[prop] = properties[prop];
				 }
				
				if ( this.initialize )
				{
					return this.initialize.apply(this, arguments)
				}
			}
		};
		class_object.isClass = function(){
			return true
		};
		class_object._parent = declaration.parent;
		class_object._name = declaration.name;
		class_object._properties = {"all":{}, "inherited":{}, "own":{}};
		class_object._shared = {"all":{}, "inherited":{}, "own":{}};
		class_object._operations = {"all":{}, "inherited":{}, "own":{}, "fullname":{}};
		class_object._methods = {"all":{}, "inherited":{}, "own":{}, "fullname":{}};
		class_object.getName = function(){
			return class_object._name
		};
		class_object.getParent = function(){
			return class_object._parent
		};
		class_object.isSubclassOf = function(c){
			var parent=this;
			while (parent)
			{
				if ( (parent == c) )
				{
					return true
				}
				parent = parent.getParent();
			}
			return false
		};
		class_object.hasInstance = function(o){
			return o.getClass().isSubclassOf(class_object)
		};
		class_object.bindMethod = function(object, methodName){
			var this_method=object[methodName];
			return function(){
				var a=arguments;
				if ( (a.length == 0) )
				{
					return this_method.call(object)
				}
				else if ( (a.length == 1) )
				{
					return this_method.call(object, a[0])
				}
				else if ( (a.length == 2) )
				{
					return this_method.call(object, a[0], a[1])
				}
				else if ( (a.length == 3) )
				{
					return this_method.call(object, a[0], a[1], a[2])
				}
				else if ( (a.length == 4) )
				{
					return this_method.call(object, a[0], a[1], a[2], a[3])
				}
				else if ( (a.length == 5) )
				{
					return this_method.call(object, a[0], a[1], a[2], a[3], a[4])
				}
				else if ( true )
				{
					var args=[];
					return this_method.apply(object, args)
				}
			}
		};
		class_object.bindCallback = function(object, methodName){
			var this_method=object[methodName];
			return function(){
				var a=arguments;
				if ( (a.length == 0) )
				{
					return this_method.call(object, this)
				}
				else if ( (a.length == 1) )
				{
					return this_method.call(object, a[0], this)
				}
				else if ( (a.length == 2) )
				{
					return this_method.call(object, a[0], a[1], this)
				}
				else if ( (a.length == 3) )
				{
					return this_method.call(object, a[0], a[1], a[2], this)
				}
				else if ( (a.length == 4) )
				{
					return this_method.call(object, a[0], a[1], a[2], a[3], this)
				}
				else if ( (a.length == 5) )
				{
					return this_method.call(object, a[0], a[1], a[2], a[3], a[4], this)
				}
				else if ( true )
				{
					var args=[];
					return this_method.apply(object, args)
				}
			}
		};
		class_object.getOperation = function(name){
			var this_operation=class_object[name];
			return function(){
				return this_operation.apply(class_object, arguments)
			}
		};
		class_object.listMethods = function(o, i){
			if ( (o == undefined) )
			{
				o = true;
			}
			if ( (i == undefined) )
			{
				i = true;
			}
			if ( (o && i) )
			{
				return class_object._methods.all
			}
			else if ( ((! o) && i) )
			{
				return class_object._methods.inherited
			}
			else if ( (o && (! i)) )
			{
				return class_object._methods.own
			}
			else if ( true )
			{
				return {}
			}
		};
		class_object.listOperations = function(o, i){
			if ( (o == undefined) )
			{
				o = true;
			}
			if ( (i == undefined) )
			{
				i = true;
			}
			if ( (o && i) )
			{
				return class_object._operations.all
			}
			else if ( ((! o) && i) )
			{
				return class_object._operations.inherited
			}
			else if ( (o && (! i)) )
			{
				return class_object._operations.own
			}
			else if ( true )
			{
				return {}
			}
		};
		class_object.listShared = function(o, i){
			if ( (o == undefined) )
			{
				o = true;
			}
			if ( (i == undefined) )
			{
				i = true;
			}
			if ( (o && i) )
			{
				return class_object._shared.all
			}
			else if ( ((! o) && i) )
			{
				return class_object._shared.inherited
			}
			else if ( (o && (! i)) )
			{
				return class_object._shared.own
			}
			else if ( true )
			{
				return {}
			}
		};
		class_object.listProperties = function(o, i){
			if ( (o == undefined) )
			{
				o = true;
			}
			if ( (i == undefined) )
			{
				i = true;
			}
			if ( (o && i) )
			{
				return class_object._properties.all
			}
			else if ( ((! o) && i) )
			{
				return class_object._properties.inherited
			}
			else if ( (o && (! i)) )
			{
				return class_object._properties.own
			}
			else if ( true )
			{
				return {}
			}
		};
		class_object.proxyWithState = function(o){
			var proxy={};
			var constr=undefined;
			var wrapper=function(f){
				return function(){
					return f.apply(o, arguments)
				}
			};
			var proxy_object=function(){
				return class_object.prototype.initialize.apply(o, arguments)
			};
			proxy_object.prototype = proxy;
			 for (var key in class_object.prototype) {
			  var w = wrapper(class_object.prototype[key])
			  if (key == "initialize") { constr=w }
			  proxy[key] = w
			  // This should not be necessary
			  proxy_object[key] = w
			 }
			
			proxy_object.getSuper = function(){
				return class_object.getParent().proxyWithState(o)
			};
			return proxy_object
		};
		if ( declaration.parent != undefined ) {
			// We proxy parent operations
			for ( var name in declaration.parent._operations.fullname ) {
				var operation = declaration.parent._operations.fullname[name]
				class_object._operations.fullname[name] = operation
				class_object[name] = operation
			}
			for ( var name in declaration.parent._operations.all ) {
				var operation = declaration.parent[name]
				class_object[name] = operation
				class_object._operations.all[name] = operation
				class_object._operations.inherited[name] = operation
			}
			for ( var name in declaration.parent._methods.all ) {
				var method = declaration.parent._methods.all[name]
				class_object._methods.all[name] = method
				class_object._methods.inherited[name] = method
			}
			// We copy parent class attributes default values
			for ( var name in declaration.parent._shared.all ) {
				var attribute = declaration.parent._shared.all[name]
				class_object[name] = attribute
				class_object._shared.all[name] = attribute
				class_object._shared.inherited[name] = attribute
			}
			// We copy parent instance attributes default values
			for ( var name in declaration.parent._properties.all ) {
				var prop = declaration.parent._properties.all[name]
				class_object._properties.all[name] = prop
				class_object._properties.inherited[name] = prop
			}
		}
		if ( declaration.operations != undefined ) {
			for ( var name in declaration.operations ) {
				var operation = declaration.operations[name]
				class_object[name] = operation
				class_object[full_name + "_" + name] = operation
				class_object._operations.all[name] = operation
				class_object._operations.all[name] = operation
				class_object._operations.own[name] = operation
				class_object._operations.fullname[full_name + "_" + name] = operation
			}
		}
		if ( declaration.methods != undefined ) {
			for ( var name in declaration.methods ) {
				var method = declaration.methods[name]
				class_object._methods.all[name] = method
				class_object._methods.own[name] = method
			}
		}
		if ( declaration.shared != undefined ) {
			for ( var name in declaration.shared ) {
				var attribute = declaration.shared[name]
				class_object[name] = attribute
				class_object._shared.all[name] = attribute
				class_object._shared.own[name] = attribute
			}
		}
		if ( declaration.properties != undefined ) {
			for ( var name in declaration.properties ) {
				var attribute = declaration.properties[name]
				class_object._properties.all[name] = attribute
				class_object._properties.own[name] = attribute
			}
		}
		
		var instance_proto={};
		if ( declaration.parent )
		{
			instance_proto = new declaration.parent("__Extend_SubClass__");
			instance_proto.constructor = class_object;
		}
		instance_proto.isInstance = undefined;
		instance_proto.getClass = function(){
			return class_object
		};
		instance_proto.isClass = function(){
			return false
		};
		instance_proto.getMethod = function(methodName){
			var this_object=this;
			return class_object.bindMethod(this_object, methodName)
		};
		instance_proto.getCallback = function(methodName){
			var this_object=this;
			return class_object.bindCallback(this_object, methodName)
		};
		instance_proto.isInstance = function(c){
			return c.hasInstance(this)
		};
		if ( declaration.initialize )
		{
			instance_proto.initialize = declaration.initialize;
		}
		else if ( true )
		{
			instance_proto.instance_proto = {};
		}
		instance_proto.getSuper = function(c){
			return c.proxyWithState(this)
		};
		if ( declaration.methods != undefined ) {
			for ( var name in declaration.methods ) {
				instance_proto[name] = instance_proto[full_name + "_" + name] = declaration.methods[name]
		}}
		if ( declaration.initialize != undefined ) {
			instance_proto.initialize = instance_proto[full_name + "_initialize"] = declaration.initialize
		}
		
		class_object.prototype = instance_proto;
		if ( declaration.name )
		{
			Extend.Registry[declaration.name] = class_object;
		}
		return class_object
	}
Extend.Protocol=	function(pdata){
		var __this__=Extend;
	}
Extend.Singleton=	function(sdata){
		var __this__=Extend;
	}
Extend.getClass=	function(name){
		var __this__=Extend;
		return Extend.Registry[name]
	}
Extend.getClasses=	function(){
		var __this__=Extend;
		return Extend.Registry
	}
Extend.getChildrenOf=	function(aClass){
		var __this__=Extend;
		var res={};
		var values = Extend.getClasses()
		for ( key in values ) {
			if ( values[key] != aClass && values[key].isSubclassOf(aClass) )
			{ res[key] = values[key] }
		}
		
		return res
	}
Extend.range=	function(start, end, step){
		// Creates a new list composed of elements in the given range, determined by
		// the 'start' index and the 'end' index. This function will automatically
		// find the proper step (wether '+1' or '-1') depending on the bounds you
		// specify.
		var __this__=Extend;
		var result=[];
		 if (start < end ) {
		   for ( var i=start ; i<end ; i++ ) {
		     result.push(i);
		   }
		 }
		 else if (start > end ) {
		   for ( var i=start ; i>end ; i-- ) {
		     result.push(i);
		   }
		 }
		
		return result
	}
Extend.iterate=	function(value, callback, context){
		// Iterates on the given values. If 'value' is an array, the _callback_ will be
		// invoked on each item (giving the 'value[i], i' as argument) until the callback
		// returns 'false'. If 'value' is a dictionary, the callback will be applied
		// on the values (giving 'value[k], k' as argument). Otherwise the object is
		// expected to define both 'length' or 'getLength' and 'get' or 'getItem' to
		// enable the iteration.
		var __this__=Extend;
		  if ( !value ) { return }
		  if ( value.length != undefined ) {
		    var length = undefined
		    // Is it an object with the length() and get() protocol ?
		    if ( typeof(value.length) == "function" ) {
		      length = value.length()
		      for ( var i=0 ; i<length ; i++ ) {
		        var cont = callback.call(context, value.get(i), i)
		        if ( cont == false ) { i = length + 1 };
		      }
		    // Or a plain array ?
		    } else {
		      length = value.length
		      for ( var i=0 ; i<length ; i++ ) {
		       var cont = callback.call(context, value[i], i);
		       if ( cont == false ) { i = length + 1 };
		      }
		    }
		  } else {
		    for ( var k in value ) {
		      var cont = callback.call(context, value[k], k);
		      if ( cont == false ) { i = length + 1 };
		    }
		  }
		
	}
Extend.sliceArguments=	function(args, index){
		// This is a utility function that will return the rest of the given
		// arguments list, without using the 'slice' operation which is only
		// available to arrays.
		var __this__=Extend;
		var res=[];
		 while (index<args.length) { res.push(args[index++]) }
		
		return res
	}
Extend.print=	function(args){
		// Prints the given arguments to the JavaScript console (available in Safari
		// and in Mozilla if you've installed FireBug), or using the 'print' command
		// in SpiderMonkey. If neither 'console' or 'print' is defined,
		// this won't do anything.
		// 
		// When objects are given as arguments, they will be printed using the
		// 'toSource' method they offer.
		// 
		// Example:
		// 
		// >    Extend print ("Here is a dict:", {a:1,b:2,c:3})
		// 
		// will output
		// 
		// >    "Here is a dict: {a:1,b:2,c:3}"
		var __this__=Extend;
		args = Extend.sliceArguments(arguments,0)
		 if (typeof(console)=="undefined"&&typeof(print)=="undefined"){return;}
		 var res = ""
		 for ( var i=0 ; i<args.length ; i++ ) {
		   var val = args[i]
		   if ( val!=undefined && typeof(val) == "object" && val.toSource != undefined) { val = val.toSource() }
		   if ( i<args.length-1 ) { res += val + " " }
		   else { res += val }
		 }
		 if(typeof(console)!="undefined"){console.log(res);}
		 else if(typeof(document)=="undefined"&&typeof(print)!="undefined"){print(res);}
		
	}
Extend.init=	function(){
		var __this__=Extend;
	}
Extend.init()
