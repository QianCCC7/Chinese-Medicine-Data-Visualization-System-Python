from py2neo import Graph, Node, Relationship, NodeMatcher


# 获取图数据库对象
def get_graph():
    return Graph('http://10.211.55.3:7474', auth=('neo4j', 'xiaoqian666'))  # neo4j数据库连接


# 获取节点查询nodeMatcher对象
def get_matcher():
    return NodeMatcher(get_graph())


''' 增 '''
# 创建节点
def create_node(graph, label, name, category):
    n = Node(label, name=name, category=category)  # 分别指定节点的 label，name和 category属性
    graph.create(n)


# 创建指定名称的节点间的关系
def create_relation_by_name(graph, matcher, label1, name1, label2, name2, name3):
    n1 = get_node_by_name(matcher, label1, name1)  # 指定名称的节点 1
    n2 = get_node_by_name(matcher, label2, name2)  # 指定名称的节点 2
    r = Relationship(n1, name3, n2)  # 建立一条 n1 -> n2的边，边属性为 name
    graph.create(r)


''' 删 '''
# 删除指定名称的节点间的关系
def delete_relation_by_name(graph, label1, name1, label2, name2, name3):
    # 删除 name1和 name2间 name3的关系
    r = 'match (n:%s{name:"%s"})-[r:`%s`]->(m:%s{name:"%s"}) delete r' % (label1, name1, name3, label2, name2)
    graph.run(r)


# 删除指定 label的所有节点
def delete_nodes_by_label(graph, label):
    cql = 'match (n:%s) delete n' % label
    graph.run(cql)


# 删除所有的关系
def delete_all_relations(graph):
    cql = 'match (n)-[r]-(m) delete r'
    graph.run(cql)


''' 查 '''
# 查询名称为 name的节点
def get_node_by_name(matcher, label, name):
    # 如果需要查询节点的信息，需要将查询到的数据封装为字典
    return matcher.match(label).where(name=name).first()


if __name__ == '__main__':
    graph = get_graph()
    matcher = get_matcher()
    # 1. 创建节点
    # create_node(graph, 'medicine_herbs', '棕榈', 'a')
    # create_node(graph, 'medicine_herbs', '朱砂', 'b')
    # create_node(graph, 'prescription', '香丸', 'c')
    # create_node(graph, 'prescription', '竹林堂', 'd')
    # 2. 查询节点
    # node = matcher.match('medicine_herbs').where(name='棕榈').first()
    # print(node)
    # 2.1 封装节点为字典数据
    # l = dict(node)
    # for key in l.keys():
    #     print(key + '对应的值为：' + l.get(key))
    # print(l.get('name'))
    # 3. 建立关系
    # n1 = match_node('medicine', '草药')
    # n2 = match_node('medicine', '防风草')
    # create_relation(n1, n2, '好友')
    # 4. 删除关系
    # name = '好友'
    r = 'match (n:prescription{name:"济川煎"})-[r:`来源于`]->(m:medicine_herbs{name:"朱砂"}) delete r'
    graph.run(r)
    # delete_relation_by_name('medicine', '草药', 'medicine', '防风草', '好友')
    # create_relation_by_name(graph, matcher, 'prescription', '济川煎',
    #                         'medicine_herbs', '朱砂', '来源于')

