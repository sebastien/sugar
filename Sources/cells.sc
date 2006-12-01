
# TODO
# class Cell extends Object
class Cell:

	class attribute COUNT

	attribute Dict views
	attribute List facets
	attribute int  id

	constructor():
		views       = {}
		facets      = []
		id          = Cell.COUNT
		Cell.COUNT += 1
	end

	method bind( widget ):
		#@ensure(not widget._cell, "Widget already bound to a cell)
		widget._cell = self
		return widget
	end

	method merge( Dict members ):
		for member in members.keys():
			self.setSlot(member, members[member])
		end
	end

	method updater():
		if self.hasSlot("_updater"):
			return self._updater
		else:
			self._updater = ()->{self.updateState()}
			return self._updater
		end
	end

	method updateState():
	end

	method addFacet( facet ):
		self.facets[facet.name] = facet
	end

end
