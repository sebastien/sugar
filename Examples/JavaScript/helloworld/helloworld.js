// 8< ---[helloworld.js]---
function _meta_(v,m){var ms=v['__meta__']||{};for(var k in m){ms[k]=m[k]};v['__meta__']=ms;return v}
var helloworld={}
var __this__=helloworld
helloworld.HelloWorld=Extend.Class({
	name:'helloworld.HelloWorld', parent:undefined,
	properties:{
		message:undefined
	},
	initialize:_meta_(function(){
		var __this__=this
		__this__.message = "Hello, World !";
	},{arguments:[]}),
	methods:{
		say:_meta_(function(){
			var __this__=this
			alert(__this__.message)
		},{arguments:[]})
	}
})
helloworld.init=	_meta_(function(){
		var __this__=helloworld;
	},{arguments:[]})
helloworld.init()
