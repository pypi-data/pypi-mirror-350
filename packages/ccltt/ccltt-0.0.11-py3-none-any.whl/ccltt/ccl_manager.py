import json
import re
from .ccl_tt_tree import CclTtTree
from .data_base import MyDatabase
from .ccl_tt_node import CclTtNode, CclTtNodes
from collections import OrderedDict


class CclManager:
    def __init__(self):
        self.db = MyDatabase()
        self.trees = {}
        self.init_tree("source")
    
    def init_tree(self, name: str):
        if name in self.trees:
            return False
        tree = CclTtTree(name, self.db)
        self.trees[name] = tree
        return tree

def build_tree(father:CclTtNodes,data):
    name = data["name"]
    ty = data.get("type", None)
    value = data.get("value", None)
    if ty is not None or value is not None:
        if ty == "int":
            father.add(name, int(value))
        elif ty == "bool":
            father.add(name, bool(value))
        elif ty == "str":
            father.add(name, str(value))
        elif ty == "real":
            father.add(name, float(value))
        elif ty == "int list":
            father.add(name, [int(val) for val in value])
        elif ty == "real list":
            father.add(name, [float(val) for val in value])
    else:
        father.add(name)
    exprn = data.get("exprn", None)
    if exprn is not None:
        child = father.get(name)
        child.add_exprn(exprn)
    node = father.get(name)
    for child_data in data.get('children', []):
        build_tree(node,child_data)


def parse_config_to_dict(config_text):
    #先创建一个根节点
    root = {
        "name": "root",
        "children": []
    }
    current_node = root
    stack = [current_node]
    lines = config_text.splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("//"):
            continue
        #如果这一行是一个名字，并且接下来一行是一个{
        if re.match(r'^[a-zA-Z0-9_][a-zA-Z0-9_ :]*$', line):
            new_node = {
                "name": line,
                "children": []
            }
            current_node["children"].append(new_node)
            stack.append(current_node)
        elif line == "{":
            current_node = new_node
        elif line == "}":
            if stack:
                current_node = stack[-1]
                stack.pop()
            else:
                current_node = root
        elif re.match(r'^[a-zA-Z0-9_][a-zA-Z0-9_ :]*\s*=\s*.*$', line):
            #如果这一行是一个名字=值
            name, value = line.split("=", 1)
            name = name.strip()
            value = value.strip()
            name = name.strip('"')
            value = value.strip('"')
            type = "str"
            if value.lower() == "true":
                value = True
                type = "bool"
            elif value.lower() == "false":
                value = False
                type = "bool"
            elif re.match(r'^\d+$', value):
                value = int(value)
                type = "int"
            elif re.match(r'^\d+\.\d+$', value):
                value = float(value)
                type = "real"
            #1.0e-5
            elif re.match(r'^\d+\.?\d*[eE][+-]?\d+$', value):
                value = float(value)
                type = "real"
            #0.0,0.0,1.0
            elif re.match(r'^\d+(,\d+)*$', value):
                value = [int(val) for val in value.split(",")]
                type = "int list"
            elif re.match(r'^[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?(?:\s*,\s*[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)*$', value):
                value = [float(v) for v in value.split(",")]
                type = "real list"
            #velocity[0]=0.0;velocity[1]=0.0;velocity[2]=0.0;
            elif re.match(r'(\w+\[?\d*\]?)=("[^"]*"|[^;]+)', value):
                pattern = r'(\w+\[?\d*\]?)=("[^"]*"|[^;]+)'
                value_node = {
                    "name": name,
                    "children": []
                }
                for key, v in re.findall(pattern, value):
                    key = key.strip()
                    v = v.strip()
                    type = "str"
                    if v.startswith('"') and v.endswith('"'):
                        v = v[1:-1]
                        type = "str"
                    if re.match(r'^\d+$', v):
                        v = int(v)
                        type = "int"
                    elif re.match(r'^\d+\.\d+$', v):
                        v = float(v)
                        type = "real"
                    elif re.match(r'^\d+\.?\d*[eE][+-]?\d+$', v):
                        v = float(v)
                        type = "real"
                    elif re.match(r'^\d+(,\d+)*$', v):
                        v = [int(val) for val in v.split(",")]
                        type = "int list"
                    elif re.match(r'^\d+(\.\d+)?(,\d+(\.\d+)?)*$', v):
                        v = [float(val) for val in v.split(",")]
                        type = "real list"
                    value_node["children"].append({"name": key, "value": v, "type": type})
                current_node["children"].append(value_node)
                continue

            value_node = {
                "name": name,
                "value": value,
                "type": type,
            }
            current_node["children"].append(value_node)
        else:
            print(f"无法解析的行: {line}")
            return None
    return root
        


def build_tree_from_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        config_text = f.read()
    root = parse_config_to_dict(config_text)
    if root is None:
        raise ValueError("配置文件解析失败，请检查配置文件格式")
    json_str = json.dumps(root, indent=4, ensure_ascii=False)
    # print(json_str)
    data = json.loads(json_str, object_pairs_hook=OrderedDict)
    manager = CclManager()
    tree = manager.trees["source"]
    root = tree.ROOT()
    for child_data in data.get('children', []):
        build_tree(root,child_data)
    return manager

def merge_lines_with_slash(lines):
    result = []
    buffer = ''
    skip = False

    for i, line in enumerate(lines):
        if skip:
            skip = False
            continue

        line = line.rstrip('\n')

        if line.endswith('\\'):
            if i + 1 < len(lines):
                merged = line[:-1].rstrip() + ' ' + lines[i + 1].lstrip()
                result.append(merged)
                skip = True
            else:
                result.append(line[:-1])  # 如果最后一行以 / 结尾
        else:
            result.append(line)

    return result

def parse_ccl_to_dict(ccl_text):
    lines = merge_lines_with_slash(ccl_text.splitlines())
    root = {
        "name": "root",
        "children": []
    }
    current_node = root
    stack = []
    
    for line in lines:
        # line = line.split()
        line = line.strip()
        if not line:
            continue
        #以一个关键字开头，最后是一个冒号，可以有空格
        if re.match(r'^[a-zA-Z0-9 _]+\s*:', line):
            stack.append(current_node)
            new_node = {
                "name": line.strip(':'),
                "children": []
            }
            current_node["children"].append(new_node)
            current_node = new_node
        #以一个关键字开头，最后是一个冒号，可以有空格 ,冒号后面也是带数字的关键字
        elif re.match(r'^[a-zA-Z0-9_][a-zA-Z0-9_]*\s*:\s*[a-zA-Z0-9_][a-zA-Z0-9_]*\s*$', line):
            stack.append(current_node)
            ty = line.split(":")[0].strip()
            name = line.split(":")[1].strip()
            new_node = {
                "name": name,
                "type": ty,
                "children": []
            }
            current_node["children"].append(new_node)
            current_node = new_node
        #END
        elif re.match(r'^END$', line):
            if stack:
                current_node = stack[-1]
                stack.pop()
            else :
                current_node = root
        # 匹配任何"前面内容=后面内容"形式的赋值语句
        elif '=' in line:
            parts = line.split('=', 1)
            name = parts[0].strip()
            value = parts[1].strip()
            
            # 判断是否为数组带单位格式
            # array_with_unit_match = re.match(r'^(\[.*\])\s*(\[.*\])$', value)
            if re.match(r'^([a-zA-Z0-9+\-*. ]*)\[([^\[\]]+)\]$', value):
                # match = re.match(r'^[a-zA-Z0-9+\-*]*\[[a-zA-Z0-9+\-*]+\]$', value)
                # print("1",value)
                match = re.match(r'^([a-zA-Z0-9+\-*. ]*)\[([^\[\]]+)\]$', value)
                if match:
                    value_ = match.group(1) if match.group(1) else "1"
                
                unit = match.group(2)
                value_ = value_.strip()
                if len(value_) == 0:
                    value_ = "1"
                type = "str"
                if value_.lower() == "true":
                    value_ = True
                    type = "bool"
                elif value_.lower() == "false":
                    value_ = False
                    type = "bool"
                elif re.match(r'^\d+$', value_):
                    value_ = int(value_)
                    type = "int"
                elif re.match(r'^\d+\.\d*$', value_):
                    value_ = float(value_)
                    type = "real"
                #1.0e-5
                elif re.match(r'^\d+\.?\d*[eE][+-]?\d+$', value_):
                    value_ = float(value_)
                    type = "real"
                value_node = {
                    "name": name,
                    "value": value_,
                    "exprn": unit,
                    "type": type
                }
            elif re.match(r'^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$', value):
                value_ = value.strip()
                type = "str"
                if value_.lower() == "true":
                    value_ = True
                    type = "bool"
                elif value_.lower() == "false":
                    value_ = False
                    type = "bool"
                elif re.match(r'^\d+$', value_):
                    value_ = int(value_)
                    type = "int"
                elif re.match(r'^\d+\.\d+$', value_):
                    value_ = float(value_)
                    type = "real"
                #1.0e-5
                elif re.match(r'^\d+\.?\d*[eE][+-]?\d+$', value_):
                    value_ = float(value_)
                    type = "real"
                value_node = {
                    "name": name,
                    "value": value_,
                    "type": type
                }
            elif re.match(r'^[^,\[\]]+(?:\s*,\s*[^,\[\]]+)+$', value):
                type = "str list"
                if re.match(r'^\d+(,\d+)*$', value):
                    value = [int(val) for val in value.split(",")]
                    type = "int list"
                elif re.match(r'^[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?(?:\s*,\s*[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)*$', value):
                    value = [float(v) for v in value.split(",")]
                    type = "real list"
                else:
                    value = [v for v in value.split(",")]
                value_node = {
                    "name": name,
                    "value": value,
                    "type": type
                }
            elif re.match(r'(?:[^,\[\]]*?\[[^\[\]]*?\])(?:,(?:[^,\[\]]*?\[[^\[\]]*?\]))*', value):
                value_list = value.split(",")
                value_after_tt = []
                unit_list = []
                type = 0
                # print(value_list)
                for value in value_list:
                    # print(value)
                    match = re.match(r'^([^\[\]]+)\[([^\[\]]+)\]$', value)
                    value_ = match.group(1).strip()
                    unit = match.group(2).strip()
                    # print(value_)
                    if re.match(r'^\d+$', value_):
                        value_after_tt.append (int(value_))
                        type = max(type,1)
                    elif re.match(r'^\d+\.\d*$', value_):
                        value_after_tt.append (float(value_))
                        type = max(type,2)
                    #1.0e-5
                    elif re.match(r'^\d+\.?\d*[eE][+-]?\d+$', value_):
                        value_after_tt.append (float(value_))
                        type = max(type,2)
                    elif len(value_.strip()) == 0:
                        value_after_tt.append (1)
                        type = max(type,1)
                    unit_list.append(unit)
                if type > 1:
                    type = "real list"
                elif type >0 :
                    type = "int list"
                else :
                    type = "str list"
                value_node = {
                    "name": name,
                    "value": value_after_tt,
                    "exprn": unit_list,
                    "type": type
                }
                # print(value_node)
            else:
                value_node = {
                    "name": name,
                    "value": value,
                    "type": "str"
                }
            current_node["children"].append(value_node)
        else:
            print(f"无法解析的行: ss{line}ss")
            return None
    
    return root

def build_tree_from_ccl(path: str):
    with open(path, "r", encoding="utf-8") as f:
        config_text = f.read()
    root =  parse_ccl_to_dict(config_text)
    json_str = json.dumps(root, indent=4, ensure_ascii=False)
    # print(json_str)
    data = json.loads(json_str, object_pairs_hook=OrderedDict)
    with open("output2.txt", "w", encoding="utf-8") as f:
        f.write(json_str)
    manager = CclManager()
    tree = manager.trees["source"]
    root = tree.ROOT()
    for child_data in data.get('children', []):
        build_tree(root,child_data)
    return manager         
            