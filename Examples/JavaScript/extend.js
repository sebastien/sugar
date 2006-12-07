// vim: tw=80 ts=4 sw=4 noet
// ----------------------------------------------------------------------------
// Project   : Extend - Prototype OOP extension
// URL       : <http://www.ivy.fr/js/extend>
// ----------------------------------------------------------------------------
// Author    : Sebastien Pierre                              <sebastien@ivy.fr>
// License   : Revised BSD License
// ----------------------------------------------------------------------------
// Creation  : 08-Sep-2006
// Last mod  : 17-Nov-2006
// ----------------------------------------------------------------------------

// The Extend object holds all the information required to implement the
// inheritance and other OO-goodness.
Extend = {
	VERSION:           1.1,
	CLASSDEF:          "CLASSDEF",
	DELETE:            "DELETE",
	// These are a list of methods of class instances that are reserved by the
	// OO layer (see the reparent method for more info)
	INSTANCE_RESERVED: {
		CLASSDEF:    true,
		getClass:    true,
		parentClass: true
	},

	// Sets up a class
	setupClass: function( _class, declaration )
	{
		// We create an empty prototype if the user did not provide one
		declaration        = declaration || {}
		_class.prototype   = declaration
		// We clone the given method definition, because they will be augmented
		// with the ones defined in the parent class
		_class.methods     = {} 
		for ( var key in declaration ) { _class.methods[key] = declaration[key] }
		_class.inherited   = {}
		_class.parentClass = undefined
		if ( declaration[Extend.CLASSDEF] )
		{ _class.className = declaration[Extend.CLASSDEF].name }
		else
		{ _class.className = undefined }
		_class.subclasses  = _class.subclasses || []
		_class.constructor = Extend.Operations.constructor
		_class.reparent    = Extend.Operations.reparent
		_class.method      = Extend.Operations.method
		_class.update      = Extend.Operations.update
		if ( declaration[Extend.CLASSDEF] )
		{ _class.reparent(declaration[Extend.CLASSDEF].parent) }
		// We update the class methods with an `ofClass` method that returns the
		// class, so that instances will have a proper
		declaration.getClass    = function() {return _class}
		declaration.parentClass = function() {return this.getClass().parentClass}
		declaration.parentCall  = function() {
			var new_args = []
			for ( var i=1;i<arguments.length;i++ ) {new_args.push(arguments[i])}
			return this.parentClass().method(arguments[0]).apply(this, new_args)
		}
		declaration.setClass    = function(newClass) {
			return this.getClass().parentClass
		}
		// We reparent the subclasses if any
		for ( var i=0 ; i<_class.subclasses ; i++ ) {
			_class.subclasses[i].reparent(_class)
		}
		return _class
	},
	// These are operations that will be "mixed-in" with the new classes
	Operations: {
		constructor: function() {
			return this.prototype.initialize || function() {}
		},
		// Reparents this class
		reparent: function( newParentClass )
		{
			if ( this.parentClass )
			{
				var this_index = this.subclasses.indexOf(this)
				this.parentClass.subclasses.splice(this_index, 1)
				for ( var method_name in this.inherited ) {
					this.method(method_name, null, this.parentClass)
				}
			}
			this.parentClass   = newParentClass
			if ( !newParentClass ) return
			var parent_methods = newParentClass.prototype
			// We iterate on all the parent methods
			for ( parent_method_name in parent_methods ) {
				// If the method is a reserved one, we skip it
				if ( Extend.INSTANCE_RESERVED[parent_method_name] == true ) { continue }
				// If the method is not directly defined in the current class, we add it
				if ( this.methods[parent_method_name] == undefined )
				{
					this.method( parent_method_name,
						parent_methods[parent_method_name],
						newParentClass.inherited[parent_method_name] || newParentClass
					)
				}
			}
			newParentClass.subclasses.push(this)
		},
		update: function(newPrototype) {
			Extend.setupClass(this, newPrototype||this.prototype)
		},
		// Returns, sets or deletes a method in this class
		method: function( name, body, declaredIn ) {
			if ( body == undefined )
			{
				var method = this.prototype[name]
				if ( name == undefined ) throw new Error("Method not found: "+name)
				return method
			}
			else
			{
				declaredIn = declaredIn || this
				// If the method is declared in this class
				if ( declaredIn == this )
				{
					if ( body == Extend.DELETE ) {
						delete this.methods[name]
						delete this.inherited[name]
						delete this.prototype[name]
						// If the method is defined in the parent we set it
						if ( this.parentClass ) {
							var parent_method = this.parentClass.method(name)
							if ( parent_method ) {
								this.method(name, parent_method, this.parentClass.inherited[name] || this.parentClass)
							}
						}
					} else {
						this.methods[name]   = body
						this.prototype[name] = body
						delete this.inherited[name]
					}
				}
				// Or if its declared in another class
				else
				{
					if ( body == Extend.DELETE ) {
						delete this.inherited[name]
						delete this.methods[name]
						delete this.prototype[name]
						// If the method is defined in the parent we set it
						if ( this.parentClass ) {
							var parent_method = this.parentClass.method(name)
							if ( parent_method ) {
								this.method(name, parent_method, this.parentClass.inherited[name] || this.parentClass)
							}
						}
					}
					else {
						if ( this.methods[name] == undefined ) {
							this.inherited[name] = declaredIn
							this.prototype[name] = body
						}
					}
				}
				for ( var i=0 ; i<this.subclasses.length ; i++ )
				{
					this.subclasses[i].method(name,body,declaredIn)
				}
			}
		}
	}
}

// In case prototype is not available, we use this instead
try {
	Class = Class
} catch ( Error ) {
	Class = {create:function() {return function() {this.initialize.apply(this, arguments)}}}
}
Class._create = Class.create
Class.create  = function( declaration ) {
	var new_class = Extend.setupClass(Class._create(declaration), declaration)
	 // The following only works on FireFox
	/*
	new_class.watch("prototype", function(id,oldval,newval) {
		new_class.prototype = newval
		Extend.setupClass(new_class, newval)
		return newval
	})*/
	return new_class
}

// EOF
