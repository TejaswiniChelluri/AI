from itertools import combinations

class BridgeState:
    def __init__(self, left, right, side, time):
        self.left = frozenset(left)
        self.right = frozenset(right)
        self.side = side  # 'left' or 'right'
        self.time = time
        self.goal_time = 60

    def goalTest(self):
        return len(self.left) == 0 and self.time <= self.goal_time

    def moveGen(self):
        times = {
            'Amogh': 5,
            'Ameya': 10,
            'Grandmother': 20,
            'Grandfather': 25
        }
        children = []

        if self.side == 'left':
            # Two people cross from left to right
            for p1, p2 in combinations(self.left, 2):
                new_left = self.left - {p1, p2}
                new_right = self.right | {p1, p2}
                t = max(times[p1], times[p2])
                new_time = self.time + t
                if new_time <= self.goal_time:
                    children.append(BridgeState(new_left, new_right, 'right', new_time))
        else:
            # One person returns from right to left with the torch
            for p in self.right:
                new_left = self.left | {p}
                new_right = self.right - {p}
                t = times[p]
                new_time = self.time + t
                if new_time <= self.goal_time:
                    children.append(BridgeState(new_left, new_right, 'left', new_time))

        return children

    def __eq__(self, other):
        return (self.left == other.left and
                self.right == other.right and
                self.side == other.side and
                self.time == other.time)

    def __hash__(self):
        return hash((self.left, self.right, self.side, self.time))

    def __str__(self):
        return (f"Left: {sorted(self.left)}, Right: {sorted(self.right)}, "
                f"Side: {self.side}, Time: {self.time}")


def removeSeen(children, OPEN, CLOSED):
    open_nodes = [node for node, parent in OPEN]
    closed_nodes = [node for node, parent in CLOSED]
    return [node for node in children if node not in open_nodes and node not in closed_nodes]


def reconstructPath(node_pair, CLOSED):
    parent_map = {node: parent for node, parent in CLOSED}
    node, parent = node_pair
    path = [node]
    while parent is not None:
        path.append(parent)
        parent = parent_map.get(parent)
    path.reverse()
    print("\n Solution Path:")
    for step in path:
        print(step)
    print(f"\n Total Time: {path[-1].time} minutes")
    return path


def bfs(start):
    print(" Running BFS...")
    OPEN = [(start, None)]
    CLOSED = []
    while OPEN:
        node_pair = OPEN.pop(0)
        node, parent = node_pair
        if node.goalTest():
            print("\n Goal found with BFS!")
            return reconstructPath(node_pair, CLOSED)
        CLOSED.append(node_pair)
        new_nodes = removeSeen(node.moveGen(), OPEN, CLOSED)
        OPEN += [(child, node) for child in new_nodes]
    print("\n No solution found with BFS.")
    return []


def dfs(start):
    print(" Running DFS...")
    OPEN = [(start, None)]
    CLOSED = []
    while OPEN:
        node_pair = OPEN.pop(0)
        node, parent = node_pair
        if node.goalTest():
            print("\n Goal found with DFS!")
            return reconstructPath(node_pair, CLOSED)
        CLOSED.append(node_pair)
        new_nodes = removeSeen(node.moveGen(), OPEN, CLOSED)
        OPEN = [(child, node) for child in new_nodes] + OPEN
    print("\n No solution found with DFS.")
    return []


# 🚦 Start State
start_state = BridgeState(
    left={'Ameya', 'Amogh', 'Grandfather', 'Grandmother'},
    right=set(),
    side='left',
    time=0
)

print(f"Start state: {start_state}")
bfs(start_state)
print("\n" + "="*40 + "\n")
dfs(start_state)
