from py2neo import Graph, Subgraph, Node, Relationship, Path, NodeMatcher

graph = Graph('bolt://10.211.55.3:7474', auth=('neo4j', 'xiaoqian666'))  # neo4j数据库连接
matcher = NodeMatcher(graph)

''' 增 '''
# 创建节点
def create_node(label, name, category):
    n = Node(label, name=name, category=category)  # 分别指定节点的标签，name和 category属性
    graph.create(n)


# 创建指定节点间的关系
def create_relation(node1, node2, name):
    r = Relationship(node1, name, node2)  # 建立一条 node1 -> node2的边，边属性为 name
    graph.create(r)


# 创建指定名称的节点间的关系
def create_relation_by_name(label1, name1, label2, name2, name3):
    n1 = match_node(label1, name1)  # 指定名称的节点 1
    n2 = match_node(label2, name2)  # 指定名称的节点 2
    r = Relationship(n1, name3, n2)  # 建立一条 n1 -> n2的边，边属性为 name
    graph.create(r)


''' 删 '''
# 删除指定名称的节点间的关系
def delete_relation_by_name(label1, name1, label2, name2, name3):
    # 删除 name1和 name2间 name3的关系
    r = 'match (n:%s{name:"%s"})-[r:`%s`]->(m:%s{name:"%s"}) delete r' % (label1, name1, name3, label2, name2)
    graph.run(r)


# 清空数据库
def delete_all():
    graph.delete_all()


''' 查 '''
# 查询名称为 name的节点
def match_node(label, name):
    # 如果需要查询节点的信息，需要将查询到的数据封装为字典
    return matcher.match(label).where(name=name).first()


if __name__ == '__main__':
    # 1. 创建节点
    # create_node('medicine', '草药', 'medicine')
    # create_node('medicine', '防风草', 'medicine')
    # 2. 查询节点
    # node = matcher.match('medicine').where(name='草药').first()
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
    # r = 'match (n:medicine{name:"草药"})-[r:`%s`]->(m:medicine{name:"防风草"}) delete r' % name
    # graph.run(r)
    # delete_relation_by_name('medicine', '草药', 'medicine', '防风草', '好友')
    delete_all()
