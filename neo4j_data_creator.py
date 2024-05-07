# 分别引入药名节点，药性节点，药味节点，归经节点，省份节点
from getPageInfo import medicine_name, attribution, flavor, target, provinces

from neo4j_connect import delete_all


# 1. 清空所有数据
# delete_all()

# 2. 创建节点
def create_nodes():
    print(medicine_name)
