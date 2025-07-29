from src.ccltt.ccl_manager import CclManager, build_tree_from_ccl, build_tree_from_json
from src.ccltt.ccl_tt_tree import CclTtTree
from src.ccltt.ccl_tt_node import merge,remove
# Removed redundant import as merge is already part of CclTtNodes

def test_initial_tree():
    print("")
    print("test_initial_tree")
    root = CclTtTree("source")
    assert root.num == 1
    assert root.root.index == 1 
    print("")

def test_initial_tree():
    print("")
    print("test_initial_tree")
    manager = CclManager()
    assert manager.trees["source"].name == "source"
    assert manager.db.get_all_node_tables()[0] == "source"
    print("")

def test_add_dir():
    manager = CclManager()
    tree = manager.trees["source"]
    root = tree.ROOT()
    assert root.name() == "root"
    print("")
    print("test_add_dir")
    assert root.add("a/w")
    assert root.add("a/d")
    assert root.add("a/df/ccc")
    assert root.add("a/ddg/ca")
    assert root.add("a/d/c")
    assert root.add("a/df/cb")
    a = merge(root.get("a/df/c*"),root.get("a/ddg/c*"))
    assert a.__str__() == "CclTtNodes (nodes: [CclTtNode (id=6 name=ccc), CclTtNode (id=10 name=cb), CclTtNode (id=8 name=ca)])"
    b = root.get("a/ddg/c*")
    c = remove(a,b)
    assert a.__str__() == "CclTtNodes (nodes: [CclTtNode (id=6 name=ccc), CclTtNode (id=10 name=cb), CclTtNode (id=8 name=ca)])"
    assert c.__str__() == "CclTtNodes (nodes: [CclTtNode (id=6 name=ccc), CclTtNode (id=10 name=cb)])"
    print("")

def test_add_tree():
    manager = CclManager()
    tree = manager.trees["source"]
    root = tree.ROOT()
    assert root.name() == "root"
    print("")
    print("test_add_tree")
    assert root.add("a/w")
    assert root.add("a/d")
    assert root.add("a/df/ccc")
    assert root.add("a/ddg/ca")
    assert root.add("a/d/c")
    assert root.add("a/df/cb")
    a = root.get("a/d")
    b = root.get("a/w") 
    b.add(a)
    assert b.get("*").__str__() == "CclTtNodes (nodes: [CclTtNode (id=11 name=d)])"
    assert b.get("*/*").__str__() == "CclTtNodes (nodes: [CclTtNode (id=12 name=c)])"
    assert a.get("*").__str__() == "CclTtNodes (nodes: [CclTtNode (id=9 name=c)])"
    assert root.get("a/*").__str__() == "CclTtNodes (nodes: [CclTtNode (id=3 name=w), CclTtNode (id=4 name=d), CclTtNode (id=5 name=df), CclTtNode (id=7 name=ddg)])"
    print("")

def test_delete_tree():
    manager = CclManager()
    tree = manager.trees["source"]
    root = tree.ROOT()
    assert root.name() == "root"
    print("")
    print("test_delete_tree")
    assert root.add("a/w")
    assert root.add("a/d")
    assert root.add("a/df/ccc")
    assert root.add("a/ddg/ca")
    assert root.add("a/d/c")
    assert root.add("a/df/cb")
    a = root.get("a/d")
    b = root.get("a/w") 
    c = merge(a,b)
    c.delete("c")
    assert root.get("a/*/*").__str__() == "CclTtNodes (nodes: [CclTtNode (id=6 name=ccc), CclTtNode (id=10 name=cb), CclTtNode (id=8 name=ca)])"
    print("")

def test_rename_node():
    manager = CclManager()
    tree = manager.trees["source"]
    root = tree.ROOT()
    assert root.name() == "root"
    print("")
    print("test_rename_node")
    assert root.add("a/w")
    assert root.add("a/d")
    assert root.add("a/df/ccc")
    assert root.add("a/ddg/ca")
    assert root.add("a/d/c")
    assert root.add("a/df/cb")
    a = root.get("a/d")
    b = root.get("a/w") 
    # a.rename("d1")
    c = merge(a,b)
    assert c.rename("d1") == False
    assert root.get("a/*").__str__() == "CclTtNodes (nodes: [CclTtNode (id=3 name=w), CclTtNode (id=4 name=d), CclTtNode (id=5 name=df), CclTtNode (id=7 name=ddg)])"
    # print(root.get("*/*"))
    assert a.get("*").__str__() == "CclTtNodes (nodes: [CclTtNode (id=9 name=c)])"
    print("")

def test_add_val():
    manager = CclManager()
    tree = manager.trees["source"]
    root = tree.ROOT()
    assert root.name() == "root"
    print("")
    print("test_add_val")
    assert root.add("a/w")
    assert root.add("a/d")
    assert root.add("a/df/ccc")
    assert root.add("a/ddg/ca")
    assert root.add("a/d/c")
    assert root.add("a/df/cb")
    a = root.get("a/d")
    b = root.get("a/w") 
    c = merge(a,b)
    assert c.__str__() == "CclTtNodes (nodes: [CclTtNode (id=4 name=d), CclTtNode (id=3 name=w)])"
    assert a.add_val("d1",True)
    assert a.add_val("d2","1")
    assert a.add_val("d3",0)
    assert a.add_val("d4",1.0)
    assert a.get("d1").value()
    assert a.get("d1").type() == "bool"
    assert a.get("d2").value() == "1"
    assert a.get("d2").type() == "str"
    assert a.get("d3").value() == "0"
    assert a.get("d3").type() == "int"
    assert a.get("d4").value() == "1.0"
    assert a.get("d4").type() == "real"
    assert a.get("d1").value() == "1"
    assert a.get("d1").add("x") == False
    e = a.get("c")
    e.add("wwww/eee/w",1)

    tree2 = manager.init_tree("target")
    root2 = tree2.ROOT()
    assert root2.name() == "root"
    assert root2.add(a)
    # print(root2.print())
    # assert root2.get("d").__str__() == "CclTtNodes (nodes: [CclTtNode (id=2 name=d)])"
    # assert root2.get("d").get("*").__str__() == "CclTtNodes (nodes: [CclTtNode (id=3 name=c), CclTtNode (id=4 name=d1), CclTtNode (id=5 name=d2), CclTtNode (id=6 name=d3), CclTtNode (id=7 name=d4)])"
    print("")

def test_add_link():
    manager = CclManager()
    tree = manager.trees["source"]
    root = tree.ROOT()
    assert root.name() == "root"
    print("")
    print("test_add_link")
    assert root.add("a/w")
    assert root.add("a/d")
    assert root.add("a/df/ccc")
    assert root.add("a/ddg/ca")
    assert root.add("a/d/c")
    assert root.add("a/df/cb")
    a = root.get("a/d")
    b = root.get("a/w") 
    # c = merge(a,b)
    assert b.add_link(a,"link") == True
    assert b.get("link").name() == "d"
    assert b.get("link").rename("link1")
    assert b.get("link").name() == "link1"

def test_build_from_json():
    print("")
    print("test_build_from_json")
    manager = build_tree_from_json("aesim_cb.input")
    tree = manager.trees["source"]
    root = tree.ROOT()
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(root.print())
    # print(root.print())
    print(root.get("*").transfrom())
    # print(root.get("periodicity_1/rotation_invariant_point").type())
    # print(root.get("*/*"))
    # print(root.get("*/*/*"))
    # print(root.get("*/*/*/*"))

def test_build_from_ccl():
    print("")
    print("test_build_from_json")
    manager = build_tree_from_ccl("ccl")
    # print(manager)
    tree = manager.trees["source"]
    root = tree.ROOT()
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(root.print())

def test_retype_node():
    manager = CclManager()
    tree = manager.trees["source"]
    root = tree.ROOT()
    assert root.name() == "root"
    print("")
    print("test_add_val")
    assert root.add("a/w")
    assert root.add("a/d")
    assert root.add("a/df/ccc")
    assert root.add("a/ddg/ca")
    assert root.add("a/d/c")
    assert root.add("a/df/cb")
    a = root.get("a/d")
    b = root.get("a/w") 
    
    c = merge(a,b)
    assert c.__str__() == "CclTtNodes (nodes: [CclTtNode (id=4 name=d), CclTtNode (id=3 name=w)])"
    assert a.add_val("d1",True)
    assert a.add_val("d2","1")
    assert a.add_val("d3",0)
    assert a.add_val("d4",1.0)
    assert a.get("d1").value()
    assert a.get("d1").type() == "bool"
    assert a.get("d2").value() == "1"
    assert a.get("d2").type() == "str"
    assert a.get("d3").value() == "0"
    assert a.get("d3").type() == "int"
    assert a.get("d4").value() == "1.0"
    assert a.get("d4").type() == "real"
    assert a.get("d1").value() == "1"
    assert a.get("d1").add("x") == False
    e = a.get("d3")
    assert e.type() == "int"
    assert e.value() == '0'
    e.retype("real")
    assert e.type() == "real"
    e.revalue(1)
    assert e.value() == '1'
    assert e.name() == "d3"
    w = a.get("*")
    # for i in w.cclnodes():
    #     print(i.name())
    # assert root2.get("d").__str__() == "CclTtNodes (nodes: [CclTtNode (id=2 name=d)])"
    # assert root2.get("d").get("*").__str__() == "CclTtNodes (nodes: [CclTtNode (id=3 name=c), CclTtNode (id=4 name=d1), CclTtNode (id=5 name=d2), CclTtNode (id=6 name=d3), CclTtNode (id=7 name=d4)])"
    print("")
