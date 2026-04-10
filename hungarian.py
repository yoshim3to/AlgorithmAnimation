def hungarian(cost_matrix: list[list[int]]) -> tuple[list[int], int]:
    """Solve a square assignment problem using the Hungarian algorithm."""
    size = len(cost_matrix)
    if size == 0:
        return [], 0

    if any(len(row) != size for row in cost_matrix):
        raise ValueError("hungarian: cost_matrix must be square")

    # Potential values for rows and columns.
    row_potentials = [0] * (size + 1)
    col_potentials = [0] * (size + 1)

    # p[j] is the row currently assigned to column j.
    # way[j] stores the previous column in the alternating path.
    p = [0] * (size + 1)
    way = [0] * (size + 1)

    for current_row in range(1, size + 1):
        p[0] = current_row
        column = 0
        min_cost = [float("inf")] * (size + 1)
        used = [False] * (size + 1)

        while True:
            used[column] = True
            row = p[column]
            best_delta = float("inf")
            next_column = 0

            for candidate in range(1, size + 1):
                if used[candidate]:
                    continue

                cost = cost_matrix[row - 1][candidate - 1]
                reduced_cost = cost - row_potentials[row] - col_potentials[candidate]

                if reduced_cost < min_cost[candidate]:
                    min_cost[candidate] = reduced_cost
                    way[candidate] = column

                if min_cost[candidate] < best_delta:
                    best_delta = min_cost[candidate]
                    next_column = candidate

            for j in range(size + 1):
                if used[j]:
                    row_potentials[p[j]] += best_delta
                    col_potentials[j] -= best_delta
                else:
                    min_cost[j] -= best_delta

            column = next_column
            if p[column] == 0:
                break

        while True:
            previous_column = way[column]
            p[column] = p[previous_column]
            column = previous_column
            if column == 0:
                break

    assignment = [-1] * size
    for col in range(1, size + 1):
        assigned_row = p[col]
        assignment[assigned_row - 1] = col - 1

    total_cost = sum(cost_matrix[row][assignment[row]] for row in range(size))
    return assignment, total_cost


def hungarian_step_generator(cost_matrix: list[list[int]]):
    """Solve a square assignment problem using the Hungarian algorithm, yielding intermediate states."""
    size = len(cost_matrix)
    if size == 0:
        yield {"assignment": [], "total_cost": 0, "row_potentials": [], "col_potentials": [], "done": True}
        return

    if any(len(row) != size for row in cost_matrix):
        raise ValueError("hungarian: cost_matrix must be square")

    row_potentials = [0] * (size + 1)
    col_potentials = [0] * (size + 1)

    p = [0] * (size + 1)
    way = [0] * (size + 1)

    for current_row in range(1, size + 1):
        p[0] = current_row
        column = 0
        min_cost = [float("inf")] * (size + 1)
        used = [False] * (size + 1)

        while True:
            used[column] = True
            row = p[column]
            best_delta = float("inf")
            next_column = 0

            for candidate in range(1, size + 1):
                if used[candidate]:
                    continue

                cost = cost_matrix[row - 1][candidate - 1]
                reduced_cost = cost - row_potentials[row] - col_potentials[candidate]

                if reduced_cost < min_cost[candidate]:
                    min_cost[candidate] = reduced_cost
                    way[candidate] = column

                if min_cost[candidate] < best_delta:
                    best_delta = min_cost[candidate]
                    next_column = candidate

            for j in range(size + 1):
                if used[j]:
                    row_potentials[p[j]] += best_delta
                    col_potentials[j] -= best_delta
                else:
                    min_cost[j] -= best_delta

            column = next_column
            
            # Yield after potential updates
            yield {
                "p": list(p),
                "row_potentials": list(row_potentials),
                "col_potentials": list(col_potentials),
                "current_row": current_row,
                "done": False,
            }

            if p[column] == 0:
                break

        while True:
            previous_column = way[column]
            p[column] = p[previous_column]
            column = previous_column
            if column == 0:
                break
        
        # Yield after augmenting path
        yield {
            "p": list(p),
            "row_potentials": list(row_potentials),
            "col_potentials": list(col_potentials),
            "current_row": current_row,
            "done": False,
        }

    assignment = [-1] * size
    for col in range(1, size + 1):
        assigned_row = p[col]
        assignment[assigned_row - 1] = col - 1

    total_cost = sum(cost_matrix[row][assignment[row]] for row in range(size))
    yield {
        "p": list(p),
        "assignment": assignment,
        "total_cost": total_cost,
        "row_potentials": list(row_potentials),
        "col_potentials": list(col_potentials),
        "done": True,
    }

# Honestly the square matrix above is all you really need.
# You can ignore everything below line 78, since that is graph based stuff.
def min_cost_matrix_assignment(cost_matrix: list[list[int]]) -> tuple[list[int], int]:
    """Compute the minimum-cost assignment for a square cost matrix."""
    return hungarian(cost_matrix)


def assignment_graph_from_matrix(
    row_labels: list[str],
    col_labels: list[str],
    cost_matrix: list[list[int]],
) -> tuple[dict[str, list[str]], int]:
    """Return an assigned bipartite graph from a square cost matrix.

    This helper is designed for use in an animation file like `animate.py`.
    The returned graph maps each row label to a list containing its assigned
    column label, which can be passed directly to `MGraph`.

    Example integration in `animate.py`:
        from hungarian import assignment_graph_from_matrix

        row_labels = ["1", "2", "3", "4"]
        col_labels = ["A", "B", "C", "D"]
        graph, total_cost = assignment_graph_from_matrix(row_labels, col_labels, cost_matrix)
        mgraph = MGraph(graph, nodes_position=nodes_and_positions, style=MGraphStyle.PURPLE)

    The `row_labels` and `col_labels` should match the node names used in
    `animate.py` so the graph can be rendered correctly.
    """
    assignment, total_cost = hungarian(cost_matrix)

    graph_assignment: dict[str, list[str]] = {}
    for row_index, row_label in enumerate(row_labels):
        col_index = assignment[row_index]
        if 0 <= col_index < len(col_labels):
            graph_assignment[row_label] = [col_labels[col_index]]

    return graph_assignment, total_cost


matrix_to_animate_graph = assignment_graph_from_matrix


def min_zero_cover(matrix: list[list[int]]) -> tuple[list[int], list[int], bool, list[int]]:
    """Helper to find the minimum number of lines to cover all zeros using bipartite matching."""
    size = len(matrix)
    match_row = [-1] * size
    match_col = [-1] * size

    # Find max matching
    def dfs(r, visited):
        for c in range(size):
            if matrix[r][c] == 0 and not visited[c]:
                visited[c] = True
                if match_col[c] == -1 or dfs(match_col[c], visited):
                    match_col[c] = r
                    match_row[r] = c
                    return True
        return False

    for i in range(size):
        visited = [False] * size
        dfs(i, visited)

    # Use König's theorem to find the minimum vertex cover
    Z_rows = set()
    Z_cols = set()

    unmatched_rows = [i for i in range(size) if match_row[i] == -1]
    queue = list(unmatched_rows)
    Z_rows.update(unmatched_rows)

    while queue:
        r = queue.pop(0)
        for c in range(size):
            if matrix[r][c] == 0 and c not in Z_cols:
                Z_cols.add(c)
                if match_col[c] != -1 and match_col[c] not in Z_rows:
                    Z_rows.add(match_col[c])
                    queue.append(match_col[c])

    covered_rows = [i for i in range(size) if i not in Z_rows]
    covered_cols = list(Z_cols)
    is_optimal = (len(covered_rows) + len(covered_cols)) == size

    return covered_rows, covered_cols, is_optimal, match_row

def hungarian_visual_steps(cost_matrix: list[list[int]]):
    """Yield steps for visualizing the true matrix-based Hungarian algorithm."""
    size = len(cost_matrix)
    matrix = [row[:] for row in cost_matrix]
    
    # Yield 1: Initial Matrix
    yield ("initial", [row[:] for row in matrix], [], [], 0, 0)

    # Yield 2: Row reduction
    for i in range(size):
        min_val = min(matrix[i])
        for j in range(size):
            matrix[i][j] -= min_val
    yield ("row_reduce", [row[:] for row in matrix], [], [], 0, 0)

    # Yield 3: Column reduction
    for j in range(size):
        min_val = min(matrix[i][j] for i in range(size))
        for i in range(size):
            matrix[i][j] -= min_val
    yield ("col_reduce", [row[:] for row in matrix], [], [], 0, 0)

    # Loop to draw lines and adjust matrix
    while True:
        covered_rows, covered_cols, is_optimal, match_row = min_zero_cover(matrix)
        
        # Yield 4: Draw covering lines
        yield ("cover", [row[:] for row in matrix], covered_rows, covered_cols, 0, 0)

        if is_optimal:
            # Optimal assignment found
            total_cost = sum(cost_matrix[i][match_row[i]] for i in range(size))
            yield ("done", [row[:] for row in matrix], covered_rows, covered_cols, match_row, total_cost)
            break

        # Find the smallest uncovered value
        min_uncovered = float('inf')
        for i in range(size):
            if i not in covered_rows:
                for j in range(size):
                    if j not in covered_cols:
                        if matrix[i][j] < min_uncovered:
                            min_uncovered = matrix[i][j]

        # Adjust the matrix: 
        # Add to double-crossed, subtract from uncovered. Single-covered stay the same.
        for i in range(size):
            for j in range(size):
                if i in covered_rows and j in covered_cols:
                    matrix[i][j] += min_uncovered
                elif i not in covered_rows and j not in covered_cols:
                    matrix[i][j] -= min_uncovered

        # Yield 5: Adjustment step
        yield ("adjust", [row[:] for row in matrix], covered_rows, covered_cols, min_uncovered, 0)

def hungarian_graph(rows: list[str], cols: list[str], edge_costs: dict[str, list[tuple[str, int]]]) -> tuple[dict[str, str], int]:
    """Solve a bipartite matching problem from a weighted graph."""
    if not rows or not cols:
        return {}, 0

    infinity = 10**9
    size = max(len(rows), len(cols))
    cost_matrix = [[infinity] * size for _ in range(size)]

    row_index = {row: index for index, row in enumerate(rows)}
    col_index = {col: index for index, col in enumerate(cols)}

    for row, edges in edge_costs.items():
        if row not in row_index:
            continue
        row_pos = row_index[row]
        for col, cost in edges:
            if col not in col_index:
                continue
            cost_matrix[row_pos][col_index[col]] = cost

    assignment, total_cost = hungarian(cost_matrix)
    matching: dict[str, str] = {}

    for row, row_pos in row_index.items():
        col_pos = assignment[row_pos]
        if col_pos < len(cols) and cost_matrix[row_pos][col_pos] < infinity:
            matching[row] = cols[col_pos]

    return matching, total_cost


def assignment_pairs(cost_matrix: list[list[int]], assignment: list[int]) -> list[tuple[int, int, int]]:
    """Convert a matrix assignment into index and cost triples."""
    return [
        (row, assignment[row], cost_matrix[row][assignment[row]])
        for row in range(len(assignment))
    ]


def _run_example() -> None:
    sample_matrix = [
        [18, 12, 9, 17],
        [12, 13, 10, 14],
        [15, 11, 14, 11],
        [16, 10, 12, 15],
    ]

    assignment, total_cost = hungarian(sample_matrix)
    print("Square matrix Hungarian assignment:")
    for row, col, cost in assignment_pairs(sample_matrix, assignment):
        print(f"  row {row} -> col {col} (cost={cost})")
    print(f"Total cost = {total_cost}\n")

    rows = ["A", "B", "C", "D"]
    cols = ["W", "X", "Y", "Z"]
    edge_costs = {
        "A": [("W", 5), ("X", 9)],
        "B": [("W", 6), ("Y", 7)],
        "C": [("X", 4), ("Z", 8)],
        "D": [("Y", 3), ("Z", 2)],
    }

    graph_assignment, graph_cost = hungarian_graph(rows, cols, edge_costs)
    print("Graph-based Hungarian assignment:")
    for row, col in graph_assignment.items():
        cost = next(cost for target, cost in edge_costs[row] if target == col)
        print(f"  {row} -> {col} (cost={cost})")
    print(f"Total cost = {graph_cost}")


if __name__ == "__main__":
    _run_example()
