import json
import sqlite3


class MyDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.init_relation_table()

    def init_relation_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS relations (
            tree_name TEXT NOT NULL,
            parent_id INTEGER NOT NULL,
            child_id INTEGER NOT NULL,
            relation_type TEXT,
            alias TEXT  
        )
        ''')
        self.conn.commit()

    def init_node_table(self, name):
        if not name.isidentifier():
            raise ValueError(f"非法的表名: {name}")

        sql = f'''
        CREATE TABLE IF NOT EXISTS {name} (
            id INTEGER PRIMARY KEY,
            node_name TEXT NOT NULL,
            node_type TEXT,
            node_value TEXT,
            node_exprn TEXT
        )
        '''
        self.cursor.execute(sql)
        self.conn.commit()

    def get_all_node_tables(self):
        query = '''
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT IN ('users', 'relations')
        '''
        self.cursor.execute(query)
        result = [row[0] for row in self.cursor.fetchall()]
        return result

    def get_node(self, table_name, node_id):
        if not table_name.isidentifier():
            raise ValueError(f"非法的表名: {table_name}")
        
        select_sql = f'''
        SELECT id, node_name, node_type, node_value, node_exprn FROM {table_name} WHERE id = ?
        '''
        self.cursor.execute(select_sql, (node_id,))
        result = self.cursor.fetchone()

        if result:
            id_, name, ty, value,node_exprn = result

            if ty == 'real list' and isinstance(value, str):
                value = json.loads(value)
            elif ty == 'int list' and isinstance(value, str):
                value = json.loads(value)
            return id_, name, ty, value, node_exprn
        return None
    
    def add_node(self, table_name, id, name, ty=None, value=None):
        if not table_name.isidentifier():
            raise ValueError(f"非法的表名: {table_name}")
        
        if isinstance(value, (list, dict)):
            value = json.dumps(value)

        insert_sql = f'''
        INSERT INTO {table_name} (id, node_name, node_type, node_value)
        VALUES (?, ?, ?, ?)
        '''
        self.cursor.execute(insert_sql, (id, name, ty, value))
        self.conn.commit()
    
    def add_exprn(self,table_name, id, exprn):
        if not table_name.isidentifier():
            raise ValueError(f"非法的表名: {table_name}")
        
        #exprn为字符串数组
        if isinstance(exprn, (list, dict)):
            exprn = json.dumps(exprn)

        #为已经存在的点添加exprn
        update_sql = f'''
        UPDATE {table_name}
        SET node_exprn = ?
        WHERE id = ?
        '''
        self.cursor.execute(update_sql, (id, exprn))
        self.conn.commit()
    


    def add_relation(self, tree_name, parent_id, child_id):
        insert_sql = '''
        INSERT INTO relations (tree_name, parent_id, child_id, relation_type, alias)
        VALUES (?, ?, ?, 'normal',?)
        '''
        self.cursor.execute(insert_sql, (tree_name, parent_id, child_id, None))
        self.conn.commit()
    
    def add_link(self, tree_name, parent_id, child_id, alias = None):
        if alias is None:
            select_name_sql = f'''
            SELECT node_name FROM {tree_name} WHERE id = ?
            '''
            self.cursor.execute(select_name_sql, (child_id,))
            row = self.cursor.fetchone()
            if row is None:
                raise ValueError(f"未找到 id={child_id} 的节点")
            alias = row[0]

        insert_sql = '''
        INSERT INTO relations (tree_name, parent_id, child_id, relation_type, alias)
        VALUES (?, ?, ?, 'link',?)
        '''
        self.cursor.execute(insert_sql, (tree_name, parent_id, child_id, alias))
        self.conn.commit()

    def find_child_by_name(self, tree_name, table_name, parent_id, target_name):
        if not table_name.isidentifier():
            raise ValueError(f"非法的表名: {table_name}")

        # 先查 relations 表，找到 parent_id 的所有子节点 id
        select_children_sql = '''
        SELECT child_id FROM relations WHERE tree_name = ? AND parent_id = ?
        '''
        self.cursor.execute(select_children_sql, (tree_name, parent_id))

        child_ids = [row[0] for row in self.cursor.fetchall()]

        if not child_ids:
            return None  # 没有子节点

        # 再查 node 表（原生节点） + link（通过别名匹配）
        placeholder = ','.join(['?'] * len(child_ids))
        select_nodes_sql = f'''
        SELECT id, node_name, node_type, node_value, node_exprn
        FROM {table_name}
        WHERE id IN ({placeholder}) AND node_name = ?
        UNION
        SELECT r.child_id AS id, n.node_name, n.node_type, n.node_value , n.node_exprn
        FROM relations r
        JOIN {table_name} n ON r.child_id = n.id
        WHERE r.parent_id = ? AND r.tree_name = ? AND r.alias = ?
        '''

        self.cursor.execute(
            select_nodes_sql,
            (*child_ids, target_name, parent_id, tree_name, target_name)
        )

        result = self.cursor.fetchone()

        return result  # 可能是 tuple 或 None
    
    def get_children(self, tree_name, table_name, parent_id):
        if not table_name.isidentifier():
            raise ValueError(f"非法的表名: {table_name}")

        select_children_sql = '''
        SELECT r.child_id, r.alias, n.node_name
        FROM relations r
        JOIN {table_name} n ON r.child_id = n.id
        WHERE r.tree_name = ? AND r.parent_id = ?
        '''.format(table_name=table_name)

        self.cursor.execute(select_children_sql, (tree_name, parent_id))
        rows = self.cursor.fetchall()

        if not rows:
            return None  # 没有子节点

        # 处理：如果 alias 存在就用 alias，否则用 node_name
        result = []
        for child_id, alias, node_name in rows:
            display_name = alias if alias else node_name
            result.append((child_id, display_name))

        return result


    def delete_node_and_children(self, table_name, node_id):
        if not table_name.isidentifier():
            raise ValueError(f"非法的表名: {table_name}")

        select_sql = '''
        SELECT child_id FROM relations WHERE tree_name = ? AND parent_id = ?
        '''
        self.cursor.execute(select_sql, (table_name, node_id))
        children = [row[0] for row in self.cursor.fetchall()]

        for child_id in children:
            self.delete_node_and_children(table_name, child_id)

        delete_relations_sql = '''
        DELETE FROM relations WHERE tree_name = ? AND (parent_id = ? OR child_id = ?)
        '''
        self.cursor.execute(delete_relations_sql, (table_name, node_id, node_id))

        delete_node_sql = f'''
        DELETE FROM {table_name} WHERE id = ?
        '''
        self.cursor.execute(delete_node_sql, (node_id,))

        self.conn.commit()

    def get_node_value(self, table_name, node_id):
        if not table_name.isidentifier():
            raise ValueError(f"非法的表名: {table_name}")

        select_sql = f'''
        SELECT node_value FROM {table_name} WHERE id = ?
        '''
        self.cursor.execute(select_sql, (node_id,))
        result = self.cursor.fetchone()

        if result:
            return result[0]
        return None
    
    def get_node_type(self, table_name, node_id):
        if not table_name.isidentifier():
            raise ValueError(f"非法的表名: {table_name}")

        select_sql = f'''
        SELECT node_type FROM {table_name} WHERE id = ?
        '''
        self.cursor.execute(select_sql, (node_id,))
        result = self.cursor.fetchone()

        if result:
            return result[0]
        return None

    def get_node_exprn(self, table_name, node_id):
        if not table_name.isidentifier():
            raise ValueError(f"非法的表名: {table_name}")

        select_sql = f'''
        SELECT node_exprn FROM {table_name} WHERE id = ?
        '''
        self.cursor.execute(select_sql, (node_id,))
        result = self.cursor.fetchone()

        if result:
            return result[0]
        return None

    def close(self):
        self.conn.close()
    
    def change_node(self, table_name, node_id, name=None, type=None, value=None):
        if not table_name.isidentifier():
            raise ValueError(f"非法的表名: {table_name}")

        fields = []
        values = []

        if name is not None:
            fields.append("node_name = ?")
            values.append(name)
        if type is not None:
            fields.append("node_type = ?")
            values.append(type)
        if value is not None:
            fields.append("node_value = ?")
            values.append(value)

        if not fields:
            # 没有字段要更新
            return True

        update_sql = f'''
        UPDATE {table_name}
        SET {', '.join(fields)}
        WHERE id = ?
        '''
        values.append(node_id)
        self.cursor.execute(update_sql, values)
        self.conn.commit()

        return True
