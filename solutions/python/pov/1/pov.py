from json import dumps

class Tree:
    def __dict__(self):
        return {self.label: [c.__dict__() for c in sorted(self.children)]}
    
    def __str__(self, indent=None):
        return dumps(self.__dict__(), indent=indent)

    def __repr__(self):
        return self.__str__()
    
    def __lt__(self, other):
        return self.label < other.label
    
    def __eq__(self, other):
        return self.__dict__() == other.__dict__()
    
    
    def __init__(self, label, children=None):
        self.label = label
        self.parent = None
        self.children = children if children is not None else []
        
        if self.children: 
            for child in self.children:
                child.parent = self

    def copy(self):
        return Tree(self.label, children=[child.copy() for child in self.children])

    def reparent(self, newparent):
        if self.parent is None or newparent != self.parent:
            # oldparent = self.parent
            # if self.parent is not None:
            #     # rotate existing parent into children    
            #     self.children.append(self.parent)
            # rotate new parent out of children into parent
            # self.parent = parent
            self.children.remove(newparent)
            # for child in self.children:
            #     child.reparent(self)
            if self.parent is not None:
                self.parent.reparent(self)
                self.children.append(self.parent)
                self.parent = newparent

    def get_node(self, label):
        if self.label == label:
            return self
            
        for child in self.children:
            candidate = child.get_node(label)
            if candidate is not None:
                return candidate

        return None

    def get_node_path(self, label):
        path = []
        return self._get_node_path(label, path)
        
    def _get_node_path(self, label, path):
        path.append(self.label)
        if self.label == label:
            return path
            
        for child in self.children:
            candidate = child._get_node_path(label, path.copy())
            if candidate is not None:
                return candidate

        return None
    
    def from_pov(self, from_label):
        node = self.copy().get_node(from_label)
        if node is None:
            raise ValueError("Tree could not be reoriented")
            
        if node.parent is not None:
            # if node is not root, change the current parent of node into a child of node
            node.parent.reparent(node)
            node.children.append(node.parent)
            # remove old parent/mark as root
            node.parent = None
        return node
        
    def path_to(self, from_label, to_label):
        povroot = self.from_pov(from_label)
        ret = povroot.get_node_path(to_label)
        
        if ret is None:
            raise ValueError("No path found")

        return ret