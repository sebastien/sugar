// 8< ---[todo.js]---
function _meta_(v,m){var ms=v['__meta__']||{};for(var k in m){ms[k]=m[k]};v['__meta__']=ms;return v}
var todo={}
var __this__=todo
todo.TodoList=Extend.Class({
	// The todo list
	// The list's ui
	name:'todo.TodoList', parent:undefined,
	properties:{
		// The list name
		ui:undefined,
		name:undefined
	},
	initialize:_meta_(function(selector, name){
		var __this__=this
		__this__.ui = $(".TodoList", "#template").clone();
		$(selector).append(__this__.ui)
		__this__.name = name;
		__this__.makeUI()
		__this__.bindUI()
	},{arguments:[{'name': 'selector'}, {'name': 'name'}]}),
	methods:{
		makeUI:_meta_(function(){
			var __this__=this
			$(".name", __this__.ui).text(__this__.name)
		},{arguments:[]}),
		bindUI:_meta_(function(){
			var __this__=this
			$(".todoForm", __this__.ui).submit(_meta_(function(event){
				event.preventDefault()
				__this__.addTodo(new todo.Todo($(".in-todo", __this__.ui).val(), __this__))
			},{arguments:[{'name': 'event'}]}))
			$(".on-removeList", __this__.ui).click(_meta_(function(){
				if ( confirm((("Are you sure you want to remove the list : " + __this__.name) + " ?")) )
				{
					$(__this__.ui).remove()
				}
			},{arguments:[]}))
		},{arguments:[]}),
		// adds a todo to the list and binds the sortable stuff
		addTodo:_meta_(function(todo){
			var __this__=this
			$(".list", __this__.ui).append(todo.ui)
			$(".in-todo", __this__.ui).val("")
			__this__.resetSortable()
		},{arguments:[{'name': 'todo'}]}),
		// resets the sortable
		resetSortable:_meta_(function(){
			var __this__=this
			$("ul.list", __this__.ui).sortableDestroy()
			$("ul.list", __this__.ui).sortable()
		},{arguments:[]})
	}
})
todo.Todo=Extend.Class({
	// The todo it self
	// The todo's ui 
	name:'todo.Todo', parent:undefined,
	properties:{
		// The todo's label 
		ui:undefined,
		// true when the todo is done
		label:"",
		// the todo's parent list
		checked:false,
		list:undefined
	},
	initialize:_meta_(function(label, list){
		var __this__=this
		__this__.label = ""
		__this__.checked = false
		__this__.label = label;
		__this__.list = list;
		__this__.makeUI()
		__this__.bindUI()
	},{arguments:[{'name': 'label'}, {'name': 'list'}]}),
	methods:{
		makeUI:_meta_(function(){
			var __this__=this
			__this__.ui = html.li(html.input({"type":"checkbox"}), __this__.label, html.button("x"));
		},{arguments:[]}),
		bindUI:_meta_(function(){
			var __this__=this
			$("input", __this__.ui).click(_meta_(function(){
				$("ul.list", __this__.list.ui).sortableDestroy()
				if ( __this__.checked )
				{
					__this__.checked = false;
					$(".list", __this__.list.ui).append(__this__.ui)
				}
				else if ( true )
				{
					__this__.checked = true;
					$(".done-list", __this__.list.ui).append(__this__.ui)
				}
				$("ul.list", __this__.list.ui).sortable()
			},{arguments:[]}))
			$("button", __this__.ui).click(_meta_(function(){
				if ( confirm("Are you sure you want to remove this todo ?") )
				{
					$(__this__.ui).remove()
				}
			},{arguments:[]}))
		},{arguments:[]})
	}
})
todo.init=	_meta_(function(){
		var __this__=todo;
		$(document).ready(_meta_(function(){
			$("#NewTodoList").submit(_meta_(function(event){
				event.preventDefault()
				var name=$(".in-todoName", this).val();
				new todo.TodoList("#TodoLists", name)
				$(".in-todoName", this).val("")
			},{arguments:[{'name': 'event'}]}))
		},{arguments:[]}))
	},{arguments:[]})
todo.init()
