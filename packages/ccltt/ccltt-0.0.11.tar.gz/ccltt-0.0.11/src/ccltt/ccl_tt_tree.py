import fnmatch
from .ccl_tt_node import CclTtNode,CclTtNodes
from .data_base import MyDatabase

class CclTtTree:
    def __init__(self, name: str, db: MyDatabase):
        self.name = name
        self.db = db
        self.nodes = {}
        self.node_id_counter = 1

        # 创建表
        self.db.init_node_table(name)

        # 创建 root
        root = CclTtNode(self, node_id=self.node_id_counter, name = "root")
        self.nodes[self.node_id_counter] = root
        self.root = root

        self.db.add_node(self.name, root.node_id, root.name)

    def ROOT(self):
        return CclTtNodes([self.root])

    def build_tree(self, parent_id, name,ty = None, value = None):
        self.node_id_counter += 1
        node = CclTtNode(self, node_id=self.node_id_counter,name = name)
        self.nodes[self.node_id_counter] = node

        self.db.add_node(self.name, node.node_id, node.name, ty, value)
        self.db.add_relation(self.name, parent_id, node.node_id)

        return node.node_id

    def add_path(self, parent_id: int, path: str) -> 'CclTtNode':
        now =CclTtNode(self, node_id=parent_id)
        if now.type() is not None and now.value() is not None:
            return False
        # Split the path by '/' to get the directory names
        path_parts = path.split('/')
        
        current_parent_id = parent_id

        error = False
        # Iterate over each part of the path
        for part in path_parts:
            # Check if the node for this part already exists
            if error:
                return False
            node = self.db.find_child_by_name(self.name,self.name,current_parent_id, part)
            if node is None:  # If node does not exist, create it
                node = self.build_tree(current_parent_id, part)
                current_parent_id = node
            else:
                node_id, node_name, node_type, node_value, node_exprn = node
                if node_type is None and node_value is None:
                    current_parent_id = node_id
                else:
                    error = True
            # Set the parent to the newly created or found node
            
        if error:
            return False
        return True
    
    def add_val(self, parent_id: int, path: str, ty, val) -> 'CclTtNode':
        now =CclTtNode(self, node_id=parent_id)
        if now.type() is not None and now.value() is not None:
            return False
        # Split the path by '/' to get the directory names
        path_parts = path.split('/')
        
        current_parent_id = parent_id
        i = len(path_parts)
        error = False
        # Iterate over each part of the path
        for part in path_parts:
            i = i - 1
            # Check if the node for this part already exists
            if error:
                return False
            node = self.db.find_child_by_name(self.name,self.name,current_parent_id, part)
            if i == 0:
                if node is None:
                    node = self.build_tree(current_parent_id, part, ty, val)
                    return True
                else:
                    return False
            elif node is None:  # If node does not exist, create it
                node = self.build_tree(current_parent_id, part)
                current_parent_id = node
            else:
                node_id, node_name, node_type, node_value = node
                if node_type is None and node_value is None:
                    current_parent_id = node_id
                else:
                    error = True
            # Set the parent to the newly created or found node
            
        if error:
            return False
        return True
    
    def add_link(self, parent_id: int, child: int, alias: str | None) -> 'CclTtNode':
        now =CclTtNode(self, node_id=parent_id)
        if now.type() is not None and now.value() is not None:
            return False
        # Split the path by '/' to get the directory names
        node = self.db.find_child_by_name(self.name,self.name,parent_id, alias)
        if not node is None:
            return False
        self.db.add_link(self.name, parent_id, child, alias)
        return True

    def find_by_path_with_wildcard(self, start_node_id, path: str):
        path_parts = path.split('/')  # 例如 ["a*", "b"]
        current_nodes = [(start_node_id, "no")]  # 初始是根节点

        for part in path_parts:
            next_nodes = []
            for node in current_nodes:
                # 找到 node 的所有子节点
                node_id,node_name = node
                children = self.db.get_children(self.name,self.name,node_id)
                # 根据通配符匹配
                if not children is None:
                    matched = [child for child in children if fnmatch.fnmatch(child[1], part)]

                    next_nodes.extend(matched)

            current_nodes = next_nodes

            if not current_nodes:
                break  # 中途没找到，提前结束
        
        ans = [self.nodes[node[0]] for node in current_nodes]
        return ans

    def deep_copy(self, parent_id: int, node_id: int, source_tree = None):
        # 复制节点
        tree_name = self.name if source_tree is None else source_tree
        parent = self.db.get_node(self.name,parent_id)
        node = self.db.get_node(tree_name,node_id)
        if node is None:
            return False
        if parent[2] is not None and parent[3] is not None:
            return False
        if  self.find_by_path_with_wildcard(parent_id, node[1]):
            return False
        # print(node[1],node[2],node[3])
        new_node_id = self.build_tree(parent_id, node[1], node[2], node[3])
        # 复制子节点
        children = self.db.get_children(tree_name,tree_name,node_id)
        if not children is None:
            for child in children:
                if(not self.deep_copy(new_node_id, child[0],source_tree)):
                    return False
        return True
    
    def delete_node_and_children(self, node_id):
        self.db.delete_node_and_children(self.name, node_id)
        del self.nodes[node_id]

    def add_exprn(self,node_id,exprn):
        self.db.add_exprn(self.name, node_id, exprn)

    def rename(self,node_id,name):
        self.db.change_node(self.name,node_id=node_id,name=name,type=None,value=None)
    
    def retype(self,node_id,type):
        self.db.change_node(self.name,node_id=node_id,name=None,type=type,value=None)
    
    def revalue(self,node_id,value):
        self.db.change_node(self.name,node_id=node_id,name=None,type=None,value=value)
    