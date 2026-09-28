"""无向图的全局最小割，只用标准库。

缺陷：平行边被覆盖成一条，而且只对「第一个顶点到最后一个顶点」做一次 s-t 最小割。
"""

from collections import deque


class CutError(ValueError):
    """输入不合法。缺陷：不带边下标。"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


def parse_edges(text):
    """解析 "a-b:1,a-b:2"。缺陷：权重不校验，报错不给下标。"""
    edges = []
    for item in text.split(","):
        item = item.strip()
        if not item:
            continue
        pair, sep, raw = item.partition(":")
        left, dash, right = pair.partition("-")
        if not dash or not sep:
            raise CutError("边格式不对：%s" % item)
        edges.append((left.strip(), right.strip(), int(raw)))
    return edges


def _min_cut_between(edges, nodes, source, sink):
    """固定源点的最小割（Edmonds-Karp）与源侧顶点。"""
    capacity = {}
    for left, right, value in edges:
        capacity[(left, right)] = capacity.get((left, right), 0) + value
        capacity[(right, left)] = capacity.get((right, left), 0) + value
    value = 0
    while True:
        parent = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            node = queue.popleft()
            for other in nodes:
                if other in parent:
                    continue
                if capacity.get((node, other), 0) > 0:
                    parent[other] = node
                    queue.append(other)
        if sink not in parent:
            break
        amount = None
        node = sink
        while parent[node] is not None:
            edge = (parent[node], node)
            amount = capacity[edge] if amount is None else min(amount, capacity[edge])
            node = parent[node]
        node = sink
        while parent[node] is not None:
            capacity[(parent[node], node)] -= amount
            capacity[(node, parent[node])] = capacity.get((node, parent[node]), 0) + amount
            node = parent[node]
        value += amount
    seen = {source}
    queue = deque([source])
    while queue:
        node = queue.popleft()
        for other in nodes:
            if other not in seen and capacity.get((node, other), 0) > 0:
                seen.add(other)
                queue.append(other)
    return value, sorted(seen)


def global_min_cut(edges):
    """缺陷：平行边覆盖成一条；只求第一个顶点到最后一个顶点的 s-t 割。"""
    weights = {}
    nodes = []
    for left, right, value in edges:
        if left == right:
            continue
        for node in (left, right):
            if node not in nodes:
                nodes.append(node)
        weights[(left, right)] = (left, right, value)  # 缺陷：覆盖而不是累加
    unique = list(weights.values())
    if len(nodes) < 2:
        return 0, []
    return _min_cut_between(unique, nodes, nodes[0], nodes[-1])
