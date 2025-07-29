from functools import singledispatchmethod
from itertools import groupby
from typing import List, Union, Optional, Literal, Dict

import numpy as np

NodeT = Union[str, int]


class Edge:
    def __init__(self, node1: NodeT, node2: NodeT, score: float = 0):
        """
        构造图中的边
        :param node1: 节点1
        :param node2: 节点2
        :param score: 分数
        """
        self.node1 = node1 if isinstance(node1, str) else str(node1)
        self.node2 = node2 if isinstance(node2, str) else str(node2)
        self.score = score

    def __str__(self):
        return f'{self.node1} -> {self.node2}: {self.score}'

    def __len__(self):
        return 3

    def to_dict(self) -> dict[str, float]:
        return {'node1': self.node1, 'node2': self.node2, 'score': self.score}

    def same_node(self, edge: 'Edge') -> bool:
        """有方向判断节点相同"""
        return self.uuid() == edge.uuid()

    def same(self, edge: 'Edge') -> bool:
        """有方向判断所有相同"""
        return self.node1 == edge.node1 and self.node2 == edge.node2 and self.score == edge.score

    def __eq__(self, edge: 'Edge') -> bool:
        return self.same(edge)

    def uuid(self) -> str:
        return "{} -> {}".format(self.node1, self.node2)


class Edges:
    def __init__(self, edges=None):
        """输入的格式是切片类型，类型包括 Edge 数组 和 ndarray """
        self.__edges__: List[Edge] = []

        # 创建边索引 有方向
        self._edge_index_ = {}

        if edges is None:
            return

        for edge in edges:
            assert len(edge) == 3, Exception("格式不对")
            self.append(edge)

    @singledispatchmethod
    def append(self, item):
        """增加数据"""
        raise NotImplementedError()

    @append.register
    def _(self, edge: Edge):
        self._edge_index_[edge.uuid()] = edge
        self.__edges__.append(edge)

    @append.register
    def _(self, edge: list):
        assert len(edge) == 3, Exception("格式不对")
        edge = Edge(edge[0], edge[1], edge[2])
        self.append(edge)

    @append.register
    def _(self, edge: np.ndarray):
        edge = edge.tolist()
        self.append(edge)

    def extend(self, edges: List[Edge]):
        for edge in edges:
            self.append(edge)

    def __getitem__(self, idx) -> Union['Edges', Edge]:
        if isinstance(idx, int):
            return self.__edges__[idx]
        value = self.__edges__[idx]
        return Edges(value)

    def __len__(self) -> int:
        return len(self.__edges__)

    def to_dict(self) -> List[dict]:
        return [edge.to_dict() for edge in self]

    def find_left(self, node: NodeT) -> 'Edges':
        """输入节点的第一个名字来查询所有的数据"""
        value = [edge for edge in self if edge.node1 == node]
        return Edges(value)

    def find_right(self, node: NodeT) -> 'Edges':
        """输入节点的第二个名字来查询所有的数据"""
        value = [edge for edge in self if edge.node2 == node]
        return Edges(value)

    def search(self, node: NodeT) -> 'Optional[Edges]':
        """输入节点的名字来查询所有的数据：只需要判断其中一个节点即可"""
        value = [edge for edge in self if edge.node1 == node or edge.node2 == node]
        if value:
            return Edges(value)
        return None

    def index(self, edge: Edge) -> int:
        if edge in self.__edges__:
            return self.__edges__.index(edge)
        return -1

    @singledispatchmethod
    def match(self, data: Union[list, Edge]) -> Optional[Edge]:
        """
        匹配数据，只返回匹配成功的数据，没有返回 None
        输入可以是 Edge类型 和 [node_name,node_name]类型
        """
        raise NotImplementedError()

    @match.register
    def _(self, nodes: list) -> Optional[Edge]:
        return self.match(Edge(nodes[0], nodes[1]))

    @match.register
    def _(self, idx: int) -> Optional[Edge]:
        return self[idx]

    @match.register
    def _(self, node: str) -> Optional[Edge]:
        return self.search(node)

    @match.register
    def _(self, edge: Edge) -> Optional[Edge]:
        edge = self.has_edge(edge)
        return edge

    def sort(self, *, key, reverse=False) -> 'Edges':
        """排序"""
        value = sorted(self.__edges__, key=key, reverse=reverse)
        return Edges(value)

    def filter(self, *, key) -> Optional['Edges']:
        """过滤"""
        value = list(filter(key, self.__edges__))
        if len(value) == 0:
            return None
        return Edges(value)

    def __iter__(self):
        """迭代 支持 for 循环"""
        return self.__edges__.__iter__()

    def has_edge(self, edge: Edge) -> Optional[Edge]:
        """判断时候存在这样的边"""
        return self._edge_index_.get(edge.uuid())

    def group(self, column: Literal['node1', 'node2'] = 'node1') -> Dict[str, 'Edges']:
        value = sorted(self.__edges__, key=lambda x: x.node1 if column == 'node1' else x.node2)
        group = groupby(value, lambda x: x.node1 if column == 'node1' else x.node2)
        ds = {}
        for key, group in group:
            ds[key] = Edges(group)
        return ds

    def items(self) -> List[Edge]:
        return self.__edges__
