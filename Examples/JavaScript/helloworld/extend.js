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
function _meta_(v,m){var ms=v['__meta__']||{};for(var k in m){ms[k]=m[k]};v['__meta__']=ms;return v}
var Extend={}
var __this__=Extend
Extend._VERSION_='2.1.0f';
Extend.Registry={}
Extend.Counters={"Instances":0}
Extend.Class=	_meta_(function(declaration){
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
		var class_object=_meta_(function(){
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
		},{arguments:[]});
		class_object.isClass = _meta_(function(){
			return true
		},{arguments:[]});
		class_object._parent = declaration.parent;
		class_object._name = declaration.name;
		class_object._properties = {"all":{}, "inherited":{}, "own":{}};
		class_object._shared = {"all":{}, "inherited":{}, "own":{}};
		class_object._operations = {"all":{}, "inherited":{}, "own":{}, "fullname":{}};
		class_object._methods = {"all":{}, "inherited":{}, "own":{}, "fullname":{}};
		class_object.getName = _meta_(function(){
			return class_object._name
		},{arguments:[]});
		class_object.getParent = _meta_(function(){
			return class_object._parent
		},{arguments:[]});
		class_object.isSubclassOf = _meta_(function(c){
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
		},{arguments:[{'name': 'c'}]});
		class_object.hasInstance = _meta_(function(o){
			return o.getClass().isSubclassOf(class_object)
		},{arguments:[{'name': 'o'}]});
		class_object.bindMethod = _meta_(function(object, methodName){
			var this_method=object[methodName];
			return _meta_(function(){
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
					args.concat(arguments)
					return this_method.apply(object, args)
				}
			},{arguments:[]})
		},{arguments:[{'name': 'object'}, {'name': 'methodName'}]});
		class_object.bindCallback = _meta_(function(object, methodName){
			var this_method=object[methodName];
			return _meta_(function(){
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
					args.concat(arguments)
					args.push(this)
					return this_method.apply(object, args)
				}
			},{arguments:[]})
		},{arguments:[{'name': 'object'}, {'name': 'methodName'}]});
		class_object.getOperation = _meta_(function(name){
			var this_operation=class_object[name];
			return _meta_(function(){
				return this_operation.apply(class_object, arguments)
			},{arguments:[]})
		},{arguments:[{'name': 'name'}]});
		class_object.listMethods = _meta_(function(o, i){
			if ( (o === undefined) )
			{
				o = true;
			}
			if ( (i === undefined) )
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
		},{arguments:[{'name': 'o'}, {'name': 'i'}]});
		class_object.listOperations = _meta_(function(o, i){
			if ( (o === undefined) )
			{
				o = true;
			}
			if ( (i === undefined) )
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
		},{arguments:[{'name': 'o'}, {'name': 'i'}]});
		class_object.listShared = _meta_(function(o, i){
			if ( (o === undefined) )
			{
				o = true;
			}
			if ( (i === undefined) )
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
		},{arguments:[{'name': 'o'}, {'name': 'i'}]});
		class_object.listProperties = _meta_(function(o, i){
			if ( (o === undefined) )
			{
				o = true;
			}
			if ( (i === undefined) )
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
		},{arguments:[{'name': 'o'}, {'name': 'i'}]});
		class_object.proxyWithState = _meta_(function(o){
			var proxy={};
			var constr=undefined;
			var wrapper=_meta_(function(f){
				return _meta_(function(){
					return f.apply(o, arguments)
				},{arguments:[]})
			},{arguments:[{'name': 'f'}]});
			var proxy_object=_meta_(function(){
				return class_object.prototype.initialize.apply(o, arguments)
			},{arguments:[]});
			proxy_object.prototype = proxy;
			 for (var key in class_object.prototype) {
			  var w = wrapper(class_object.prototype[key])
			  if (key == "initialize") { constr=w }
			  proxy[key] = w
			  // This should not be necessary
			  proxy_object[key] = w
			 }
			
			proxy_object.getSuper = _meta_(function(){
				return class_object.getParent().proxyWithState(o)
			},{arguments:[]});
			return proxy_object
		},{arguments:[{'name': 'o'}]});
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
		instance_proto.getClass = _meta_(function(){
			return class_object
		},{arguments:[]});
		instance_proto.isClass = _meta_(function(){
			return false
		},{arguments:[]});
		instance_proto.getMethod = _meta_(function(methodName){
			var this_object=this;
			return class_object.bindMethod(this_object, methodName)
		},{arguments:[{'name': 'methodName'}]});
		instance_proto.getCallback = _meta_(function(methodName){
			var this_object=this;
			return class_object.bindCallback(this_object, methodName)
		},{arguments:[{'name': 'methodName'}]});
		instance_proto.isInstance = _meta_(function(c){
			return c.hasInstance(this)
		},{arguments:[{'name': 'c'}]});
		if ( declaration.initialize )
		{
			instance_proto.initialize = declaration.initialize;
		}
		else if ( true )
		{
			instance_proto.instance_proto = {};
		}
		instance_proto.getSuper = _meta_(function(c){
			return c.proxyWithState(this)
		},{arguments:[{'name': 'c'}]});
		if ( declaration.operations != undefined ) {
			for ( var name in declaration.operations ) {
				instance_proto[name] = instance_proto[full_name + "_" + name] = class_object.getOperation(name)
		}}
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
	},{arguments:[{'name': 'declaration'}]})
Extend.Protocol=	_meta_(function(pdata){
		var __this__=Extend;
	},{arguments:[{'name': 'pdata'}]})
Extend.Singleton=	_meta_(function(sdata){
		var __this__=Extend;
	},{arguments:[{'name': 'sdata'}]})
Extend.getClass=	_meta_(function(name){
		var __this__=Extend;
		return Extend.Registry[name]
	},{arguments:[{'name': 'name'}]})
Extend.getClasses=	_meta_(function(){
		var __this__=Extend;
		return Extend.Registry
	},{arguments:[]})
Extend.invoke=	_meta_(function(t, f, args, extra){
		// The 'invoke' method allows advanced invocation (supporting by name, as list
		// and as map invocation schemes) provided the given function 'f' has proper
		// '__meta__' annotation.
		// 
		// These annotations are expected to be like:
		// 
		// >    f __meta__ = {
		// >        arity:2
		// >        arguments:{
		// >           b:2,
		// >           "*":[1]
		// >           "**":{c:3,d:4}
		// >        }
		// >    }
		// 
		var __this__=Extend;
		var meta=f["__meta__"];
		var actual_args=[];
		Extend.iterate(extra["*"], _meta_(function(v){
			args.push(v)
		},{arguments:[{'name': 'v'}]}), __this__)
		Extend.iterate(extra["**"], _meta_(function(v, k){
			extra[k] = v;
		},{arguments:[{'name': 'v'}, {'name': 'k'}]}), __this__)
		Extend.iterate(args, _meta_(function(v){
			actual_args.push(args)
		},{arguments:[{'name': 'v'}]}), __this__)
		var start=args.length;
		while ((start < meta.arity))
		{
			var arg=meta.arguments[start];
			actual_args.push(extra[arg.name])
			start = (start + 1);
		}
		Extend.print("CALLING ", f.toSource())
		Extend.print(" with", actual_args.toSource())
		return f.apply(t, actual_args)
	},{arguments:[{'name': 't'}, {'name': 'f'}, {'name': 'args'}, {'name': 'extra'}]})
Extend.getChildrenOf=	_meta_(function(aClass){
		var __this__=Extend;
		var res={};
		var values = Extend.getClasses()
		for ( key in values ) {
			if ( values[key] != aClass && values[key].isSubclassOf(aClass) )
			{ res[key] = values[key] }
		}
		
		return res
	},{arguments:[{'name': 'aClass'}]})
Extend.range=	_meta_(function(start, end, step){
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
	},{arguments:[{'name': 'start'}, {'name': 'end'}, {'flags': '?', 'name': 'step'}]})
Extend.iterate=	_meta_(function(value, callback, context){
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
		
	},{arguments:[{'name': 'value'}, {'name': 'callback'}, {'name': 'context'}]})
Extend.sliceArguments=	_meta_(function(args, index){
		// This is a utility function that will return the rest of the given
		// arguments list, without using the 'slice' operation which is only
		// available to arrays.
		var __this__=Extend;
		var res=[];
		 while (index<args.length) { res.push(args[index++]) }
		
		return res
	},{arguments:[{'name': 'args'}, {'name': 'index'}]})
Extend.slice=	_meta_(function(value, start, end){
		var __this__=Extend;
		start = start === undefined ? 0 : start
		end = end === undefined ? undefined : end
		if ( Extend.isString(value) )
		{
			if ( (end === undefined) )
			{
				end = value.length;
			}
			if ( (start < 0) )
			{start = (value.length + start);}
			if ( (end < 0) )
			{end = (value.length + end);}
			return value.substring(start, end)
		}
		else if ( Extend.isList(value) )
		{
			if ( (end === undefined) )
			{
				end = value.length;
			}
			if ( (start < 0) )
			{start = (value.length + start);}
			if ( (end < 0) )
			{end = (value.length + end);}
			return value.slice(start, end)
		}
		else if ( true )
		{
			throw ("Unsupported type for slice:" + value)
		}
	},{arguments:[{'name': 'value'}, {'flags': '=', 'name': 'start'}, {'flags': '=', 'name': 'end'}]})
Extend.isIn=	_meta_(function(value, list){
		// Returns true if the given value is in the given list
		var __this__=Extend;
		if ( Extend.isList(list) )
		{
			 for ( var i=0 ; i<list.length ; i++) {
			   if (list[i]==value) { return true }
			 }
			 return false
			
		}
		else if ( Extend.isMap(list) )
		{
			 for ( var i in list ) {
			   if (list[i]==value) { return true }
			 }
			 return false
			
		}
		else if ( true )
		{
			return false
		}
	},{arguments:[{'name': 'value'}, {'name': 'list'}]})
Extend.createMapFromItems=	_meta_(function(items){
		var __this__=Extend;
		items = Extend.sliceArguments(arguments,0)
		 var result = {}
		 for ( var i=0 ; i<items.length ; i++ ) {
		   result[items[i][0]] = items[i][1]
		 }
		 return result
		
	},{arguments:[{'flags': '*', 'name': 'items'}]})
Extend.isDefined=	_meta_(function(value){
		var __this__=Extend;
		return (! (value === undefined))
	},{arguments:[{'name': 'value'}]})
Extend.isList=	_meta_(function(value){
		var __this__=Extend;
		 return !!( !(value===null) && typeof value == "object" && value.join && value.splice);
		
	},{arguments:[{'name': 'value'}]})
Extend.isString=	_meta_(function(value){
		var __this__=Extend;
		return (typeof(value) == "string")
	},{arguments:[{'name': 'value'}]})
Extend.isMap=	_meta_(function(value){
		var __this__=Extend;
		 return !!(!(value===null) && typeof value == "object" && !Extend.isList(value))
		
	},{arguments:[{'name': 'value'}]})
Extend.isFunction=	_meta_(function(value){
		var __this__=Extend;
		 return !!(typeof value == "function")
		
	},{arguments:[{'name': 'value'}]})
Extend.isInstance=	_meta_(function(value, ofClass){
		// Tells if the given value is an instance (in the sense of Extend) of the
		// given 'ofClass'. If there is no given class, then it will just return
		// true if the value is an instance of any class.
		var __this__=Extend;
		ofClass = ofClass === undefined ? undefined : ofClass
		if ( ofClass )
		{
			return (Extend.isDefined(value.getClass) && value.isInstance(ofClass))
		}
		else if ( true )
		{
			return Extend.isDefined(value.getClass)
		}
	},{arguments:[{'name': 'value'}, {'flags': '=', 'name': 'ofClass'}]})
Extend.print=	_meta_(function(args){
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
		
	},{arguments:[{'flags': '*', 'name': 'args'}]})
Extend.init=	_meta_(function(){
		var __this__=Extend;
	},{arguments:[]})
Extend.init()
