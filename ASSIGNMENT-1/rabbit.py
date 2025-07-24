class RabbitState:
    def __init__(self, config, goal):
        self.config = config
        self.goal = goal

    def goalTest(self):
        return self.config == self.goal

    def moveGen(self):
        children = []
        idx = self.config.index('_')

        # E rabbit moves right (walk)
        if idx > 0 and self.config[idx - 1] == 'E':
            new_config = self.config[:]
            new_config[idx], new_config[idx - 1] = new_config[idx - 1], new_config[idx]
            children.append(RabbitState(new_config, self.goal))

        # E rabbit jumps right (jump over 1)
        if idx > 1 and self.config[idx - 2] == 'E':
            new_config = self.config[:]
            new_config[idx], new_config[idx - 2] = new_config[idx - 2], new_config[idx]
            children.append(RabbitState(new_config, self.goal))

        # W rabbit moves left (walk)
        if idx < len(self.config) - 1 and self.config[idx + 1] == 'W':
            new_config = self.config[:]
            new_config[idx], new_config[idx + 1] = new_config[idx + 1], new_config[idx]
            children.append(RabbitState(new_config, self.goal))

        # W rabbit jumps left (jump over 1)
        if idx < len(self.config) - 2 and self.config[idx + 2] == 'W':
            new_config = self.config[:]
            new_config[idx], new_config[idx + 2] = new_config[idx + 2], new_config[idx]
            children.append(RabbitState(new_config, self.goal))

        return children

    def __eq__(self, other):
        return self.config == other.config

    def __hash__(self):
        return hash(tuple(self.config))

    def __str__(self):
        return ''.join(self.config)


def removeSeen(children, OPEN, CLOSED):
    open_nodes = [node for node, _ in OPEN]
    closed_nodes = [node for node, _ in CLOSED]
    return [node for node in children if node not in open_nodes and node not in closed_nodes]


def reconstructPath(node_pair, CLOSED):
    parent_map = {node: parent for node, parent in CLOSED}
    N, parent = node_pair
    path = [N]
    while parent is not None:
        path.append(parent)
        parent = parent_map[parent]
    path.reverse()
    return path


def bfs(start):
    print(" Running BFS...")
    OPEN = [(start, None)]
    CLOSED = []
    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair
        if N.goalTest():
            print(" Goal found with BFS!")
            return reconstructPath(node_pair, CLOSED)
        CLOSED.append(node_pair)
        children = N.moveGen()
        new_nodes = removeSeen(children, OPEN, CLOSED)
        OPEN.extend([(child, N) for child in new_nodes])
    print(" No solution found with BFS.")
    return None


def dfs(start):
    print(" Running DFS...")
    OPEN = [(start, None)]
    CLOSED = []
    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair
        if N.goalTest():
            print(" Goal found with DFS!")
            return reconstructPath(node_pair, CLOSED)
        CLOSED.append(node_pair)
        children = N.moveGen()
        new_nodes = removeSeen(children, OPEN, CLOSED)
        OPEN = [(child, N) for child in new_nodes] + OPEN
    print(" No solution found with DFS.")
    return None


# Initial and goal configurations
start_config = ['E', 'E', 'E', '_', 'W', 'W', 'W']
goal_config = ['W', 'W', 'W', '_', 'E', 'E', 'E']
start_state = RabbitState(start_config, goal_config)

print("\n=== Rabbit BFS ===")
bfs_path = bfs(start_state)
if bfs_path:
    for step in bfs_path:
        print(step)

print("\n=== Rabbit DFS ===")
dfs_path = dfs(start_state)
if dfs_path:
    for step in dfs_path:
        print(step)
