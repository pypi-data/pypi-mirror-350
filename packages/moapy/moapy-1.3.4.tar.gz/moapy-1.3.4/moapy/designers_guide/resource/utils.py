from collections import defaultdict


class Node:
    def __init__(self):
        self.id = None
        self.upstream = []
        self.downstream = []

    def set_id(self, id: str):
        self.id = id

    def add_upstream(self, node: "Node"):
        self.upstream.append(node)
        node.downstream.append(self)

    # def add_downstream(self, node: "Node"):
    #     self.downstream.append(node)
    #     node.upstream.append(self)

    def __hash__(self):
        if self.id is None:
            raise ValueError("Node id is not set")
        return hash(self.id)

    def __repr__(self):
        # return f"Node(id={self.id}, upstream={self.upstream}, downstream={self.downstream})"
        return f"Node<id={self.id}>"


def create_node(component: dict):
    node = Node()
    node.set_id(component["id"])
    return node


class G:  # graph
    def __init__(self):
        self.nodes: list[Node] = []

    def find_node(self, id: str) -> Node:
        for node in self.nodes:
            if node.id == id:
                return node
        raise ValueError(f"Node with id {id} not found")

    def add_node(self, node_or_nodelist: Node | list[Node]):
        if isinstance(node_or_nodelist, Node):
            node_or_nodelist = [node_or_nodelist]

        for node in node_or_nodelist:
            self.nodes.append(node)

    @property
    def root_nodes(self) -> list[Node]:
        root_nodes = []
        for node in self.nodes:
            if not node.upstream:
                root_nodes.append(node)
        return root_nodes

    @property
    def leaf_nodes(self) -> list[Node]:
        leaf_nodes = []
        for node in self.nodes:
            if not node.downstream:
                leaf_nodes.append(node)
        return leaf_nodes

    # def union_find(self) -> dict[str, list[str]]:
    #     """연결되어 있는 노드들의 리스트의 딕셔너리를 반환"""
    #     class Group(G):
    #         def __init__(self, id: str):
    #             super().__init__()
    #             self.id = id

    #     class UnionFind:
    #         def __init__(self, nodes: list[Node]):
    #             self.groups = {node: Group(node.id) for node in nodes}

    #         def find(self, node: Node) -> G:
    #             if self.groups[node].id != node.id:
    #                 self.groups[node] = self.find(self.groups[node])
    #             return self.groups[node]

    #         def union(self, node1: Node, node2: Node):
    #             group1 = self.find(node1)
    #             group2 = self.find(node2)
    #             group1.update(group2)
    #             self.groups[node2] = group1

    #     uf = UnionFind(self.nodes)
    #     for node in self.nodes:
    #         for upstream in node.upstream:
    #             uf.union(node, upstream)
    #     return {node: uf.find(node) for node, group in uf.groups.items()}
    #     # return uf.groups
    #     # return {node: group.nodes for node, group in uf.groups.items()}

    def groups(self) -> list["G"]:
        """연결된 노드들로 구성된 그래프 리스트를 반환"""
        visited = set()
        groups = []

        def collect_connected_nodes(node: Node) -> set[Node]:
            if node in visited:
                return set()

            connected = {node}
            visited.add(node)

            # 상류와 하류 노드들을 재귀적으로 탐색
            for upstream in node.upstream:
                connected.update(collect_connected_nodes(upstream))
            for downstream in node.downstream:
                connected.update(collect_connected_nodes(downstream))

            return connected

        # 모든 노드에 대해 연결된 노드들을 찾아 그룹화
        for node in self.nodes:
            if node not in visited:
                connected_nodes = collect_connected_nodes(node)
                if connected_nodes:
                    new_group = G()
                    new_group.add_node(list(connected_nodes))
                    groups.append(new_group)

        return groups

    def is_single_component(self) -> bool:
        return len(self.groups()) == 1


def create_graph():
    g = G()
    return g


def create_graph_from_component_list(component_list: list[dict], skip_notfound_required: bool = False) -> G:
    g = create_graph()
    node_list = [create_node(comp) for comp in component_list]
    g.add_node(node_list)

    for id, required in (
        (comp["id"], comp["required"])
        for comp in component_list
        if comp.get("required")
    ):
        downstream_node = g.find_node(id)
        for req_id in required:
            try:
                upstream_node = g.find_node(req_id)
            except ValueError:
                msg = f"Node with id {req_id} not found"
                if skip_notfound_required:
                    print(msg)
                    continue
                raise ValueError(msg)
            downstream_node.add_upstream(upstream_node)

    return g


def find_root_component(component_list: list[dict]):
    g = create_graph_from_component_list(component_list)
    return g.root_nodes


def create_content_report(component_list: dict, skip_notfound_required: bool = False):
    g = create_graph_from_component_list(component_list, skip_notfound_required=skip_notfound_required)

    res = {}

    res["nodes"] = [node.id for node in g.nodes]
    res["root"] = g.root_nodes
    res["leaf"] = g.leaf_nodes
    
    res["groups"] = [sorted(group.nodes, key=lambda x: x.id) for group in g.groups()]
    res["is_single_component"] = g.is_single_component()
    return res


if __name__ == "__main__":
    from moapy.designers_guide.resource.component37 import component_list

    print(create_content_report(component_list))
