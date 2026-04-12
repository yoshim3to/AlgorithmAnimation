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
    
    # Initial Matrix
    yield ("initial", [row[:] for row in matrix], [], [], 0, 0)

    # Row reduction step-by-step
    for i in range(size):
        min_val = min(matrix[i])
        min_j = matrix[i].index(min_val)
        
        # Highlight minimum in the current row
        yield ("row_min", [row[:] for row in matrix], i, min_j, min_val, 0)
        
        for j in range(size):
            matrix[i][j] -= min_val
            
        # Show the matrix after the row is reduced
        yield ("row_reduce", [row[:] for row in matrix], i, -1, min_val, 0)

    # Column reduction step-by-step
    for j in range(size):
        min_val = min(matrix[i][j] for i in range(size))
        min_i = 0
        for i in range(size):
            if matrix[i][j] == min_val:
                min_i = i
                break
                
        # Highlight minimum in the current column
        yield ("col_min", [row[:] for row in matrix], min_i, j, min_val, 0)
        
        for i in range(size):
            matrix[i][j] -= min_val
            
        # Show the matrix after the column is reduced
        yield ("col_reduce", [row[:] for row in matrix], -1, j, min_val, 0)

    # Loop to draw lines and adjust matrix
    while True:
        covered_rows, covered_cols, is_optimal, match_row = min_zero_cover(matrix)
        
        # Draw covering lines
        yield ("cover", [row[:] for row in matrix], covered_rows, covered_cols, 0, 0)

        # Optimal assignment found
        if is_optimal:
            total_cost = sum(cost_matrix[i][match_row[i]] for i in range(size))
            yield ("done", [row[:] for row in matrix], covered_rows, covered_cols, match_row, total_cost)
            break

        # Find the smallest uncovered value and track its coordinates
        min_uncovered = float('inf')
        min_i, min_j = -1, -1
        for i in range(size):
            if i not in covered_rows:
                for j in range(size):
                    if j not in covered_cols:
                        if matrix[i][j] < min_uncovered:
                            min_uncovered = matrix[i][j]
                            min_i = i
                            min_j = j

        # Highlight the minimum uncovered value
        yield ("adjust_min", [row[:] for row in matrix], covered_rows, covered_cols, min_uncovered, (min_i, min_j))

        # Adjust the matrix: 
        # Add to double-crossed, subtract from uncovered. Single-covered stay the same.
        for i in range(size):
            for j in range(size):
                if i in covered_rows and j in covered_cols:
                    matrix[i][j] += min_uncovered
                elif i not in covered_rows and j not in covered_cols:
                    matrix[i][j] -= min_uncovered

        # Highlight adjustment step math
        yield ("adjust_math", [row[:] for row in matrix], covered_rows, covered_cols, min_uncovered, 0)

if __name__ == "__main__":
    # Example usage
    cost_matrix = [
        [1, 2, 3, 4],
        [2, 4, 8, 7],
        [3, 6, 6, 5],
        [4, 8, 9, 10]
    ]
    assignment, total_cost = hungarian(cost_matrix)
    print("Assignment:", assignment)
    print("Total Cost:", total_cost)
