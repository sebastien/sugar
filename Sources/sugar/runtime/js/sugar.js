var Sugar = {}
var S     = Sugar

//# TODO: Add extend-like class layer (but simplified)
//# TODO: Add getMethod(name) that  is directly callable

Sugar.VERSION = "0.0.7"
Sugar.Core = {

	superFor: function( currentClass, instance ) {
		var superClass = currentClass.parentClass
		var proxy   = {}
		var wrapper = function(f){
			return function(){
				f.apply(instance, arguments)
			}
		}
		for ( var key in superClass.prototype ) {
			proxy[key] = wrapper(superClass.prototype[key])
		}
		return proxy
	},
	
	// Creates a new function that will get the given method from the given instance, and invoke
	// it with the given context as first argument
	wrapMethod: function( instance, methodName ) {
		return function(){
			var args = []
			for ( var i=0 ; i<arguments.length ; i++ ) { args.push(arguments[i]) }
			args.push(this)
			return instance[methodName].apply(instance, args)
		}
	},
	
	// TODO: Add context
	iterate: function( value, callback, context ) {
		if ( value.length != undefined ) {
			for ( var i=0 ; i<value.length ; i++ ) {
				callback.call(context, value[i], i)
			}
		} else {
			for ( var k in value ) {
				callback.call(context, value[k], k)
			}
		}
		
	},

	// Returns an array that can be used as arguments. It is a merge of the args
	// array and the rest of the function arguments.
	makeArgs: function( args ) {
		var res = []
		for ( var i=0 ; i<args.length ; i++ ) { res.push(args[i]) }
		for ( var i=1 ; i<arguments.length ; i++ ) { res.push(arguments[i]) }
		return res
	},

	// This is a standard function for printing stuff out
	print: function() {
		if (console == undefined || console.log == undefined ) { return }
		var res = ""
		for ( var i=0 ; i<arguments.length ; i++ ) {
			var val = arguments[i]
			if ( typeof(val) == "object" && val.toSource != undefined) { val = val.toSource() }
			if ( i<arguments.length-1 ) { res += val + " " }
			else { res += val }
		}
		if ( typeof(console) != "undefined") { console.log(res) }
	}
	
}

// EOF
