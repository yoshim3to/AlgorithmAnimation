# Novel Algorithm Analysis: Push-Relabel Algorithm for Max Flow

## Justification
For the assignment, we substituted Dinic's Algorithm (Option #3) with the **Push-Relabel algorithm**. Both algorithms solve the maximum flow problem, but Push-Relabel operates fundamentally differently. 

Instead of finding augmenting paths from the source to the sink across the entire residual network (like Edmonds-Karp or Dinic's), Push-Relabel works locally. It pushes "excess" flow between adjacent nodes and maintains a "height" function to ensure that flow always goes "downhill" toward the sink. We believed this localized approach would be better because:
1. **Asymptotic Complexity**: Push-Relabel with the FIFO selection rule achieves a time complexity of $O(V^3)$, and with the highest-label rule, it can achieve $O(V^2 \sqrt{E})$. This makes it highly efficient on dense graphs compared to Dinic's algorithm, which typically runs in $O(V^2 E)$.
2. **Local Adjustments vs. Global Searches**: Since it relies only on local node information (capacity and height of neighbors), it has an advantage in distributed network applications. We wanted to see how this local strategy compares in implementation simplicity to Dinic's global BFS + DFS structure.

## Final Analysis: Success or Failure?
**Success**.

### Implementation Experience
The implementation of the Push-Relabel algorithm was highly successful. The algorithm cleanly separates into intuitive `push()` and `relabel()` operations. We successfully computed the same maximum flow results as Dinic's algorithm on test networks.

### Animation Context
While the assignment notes that animating a novel algorithm is not required, analyzing its animation potential highlights why we chose not to animate it:
- **Dinic's algorithm** is visually intuitive. Finding a level graph (BFS) and pushing flow along an augmenting path (DFS) makes for a clean, global visual narrative that is easy for a human observer to follow.
- **Push-Relabel** is much harder to follow visually on a global scale. Because it operates on local nodes continuously pushing flow back and forth (often pushing flow back to the source), an animation would look chaotic and disjointed, lacking the clear "start-to-finish path" paradigm. 

### Conclusion
The Push-Relabel algorithm proved to be mathematically and programmatically superior (or at least highly competitive) for dense graphs due to its strict polynomial bounds. However, conceptually, its non-linear and localized progression makes Dinic's algorithm better suited for educational animations. Thus, implementing Push-Relabel served as an excellent computational novel alternative, while Dinic's was retained for the animation portion.