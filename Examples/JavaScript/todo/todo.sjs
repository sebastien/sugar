@class TodoList
| The todo list
	
	@property ui
	| The list's ui
	
	@property name
	| The list name
	
	@constructor selector, name
		ui = $ (".TodoList", "#template") clone ()
		$ (selector) append (ui)
		
		self name = name
		makeUI ()
		bindUI ()
	@end
	
	@method makeUI
		$ (".name", ui) text (name)
	@end
	
	@method bindUI
		#binds the add new todo form submit
		$ (".todoForm", ui) submit { event |
			event preventDefault ()
			addTodo (new Todo ($ (".in-todo", ui) val (), self))
		} 
		
		# binds the list delete
		$ (".on-removeList", ui) click {
			if confirm ("Are you sure you want to remove the list : " + name + " ?")
				$ (ui) remove ()
			end
		}
	@end
	
	@method addTodo todo
	| adds a todo to the list and binds the sortable stuff
		
		$ (".list", ui) append (todo ui)
		$ (".in-todo", ui) val "" 
		
		# we need to reset the sortable because of the way sortable events are bound
		resetSortable ()
	@end
	
	@method resetSortable
	| resets the sortable
		$ ("ul.list", ui) sortableDestroy ()
		$ ("ul.list", ui) sortable ()
	@end

@end

@class Todo
| The todo it self
	
	@property ui
	| The todo's ui 
	
	@property label = ""
	| The todo's label 
	
	@property checked = False
	| true when the todo is done
	
	@property list
	| the todo's parent list
	
	@constructor label, list
		self label = label
		self list = list
		makeUI ()
		bindUI ()
	@end
	
	@method makeUI
		ui = html li (
			html input  {type:"checkbox"}
			label
			html button "x"
		)
	@end
	
	@method bindUI
		# when checking / unchecking a todo
		$ ("input", ui) click {
			# destroying the sortable before appending to another list 
			# makes it not sortable when it gets in the "done" list
			$ ("ul.list", list ui) sortableDestroy ()
			
			if checked 
				checked = False
				$ (".list", list ui) append (ui)
			else
				checked = True
				$ (".done-list", list ui) append (ui)
			end

			# re-making the todo list sortable
			$ ("ul.list", list ui) sortable ()
		}
		
		# when clicking on a remove todo button
		$ ("button", ui) click {
			if confirm "Are you sure you want to remove this todo ?"
				$ (ui) remove ()
			end
		}
	@end

@end

$ (document) ready {
	$ "#NewTodoList" submit {event|
		event preventDefault ()
		var name = $ (".in-todoName", target) val ()
		new TodoList ("#TodoLists", name)
		$ (".in-todoName", target) val ""
	}	
}
