from manim import *
from manim_dsa import *
import random
import sys

def table_int_to_str(table: list[list[int]]):
    out = [[str(item) for item in row] for row in table]
    return out

class Hungarian(Scene):
    def construct(self):
        from hungarian import hungarian_step_generator
        def remove_edge(graph : MGraph, node1 : str, node2 : str):
            edge_name = (node1, node2)
            if edge_name in graph.edges:
                del graph.edges[edge_name]
                graph.remove(edge_name)
            edge_name2 = (node2, node1)
            if edge_name2 in graph.edges:
                del graph.edges[edge_name2]
                graph.remove(edge_name2)

        graph = {
            x: ['A'] for x in "1234ABCD"  # dummy to avoid issues
        }
        nodes_and_positions = {
            '1' : LEFT*2+UP*1.5,
            '2' : LEFT*2+UP*0.5,
            '3' : LEFT*2+DOWN*0.5,
            '4' : LEFT*2+DOWN*1.5,
            'A' : RIGHT*2+UP*1.5,
            'B' : RIGHT*2+UP*0.5,
            'C' : RIGHT*2+DOWN*0.5,
            'D' : RIGHT*2+DOWN*1.5,
        }
        preTable = [
            [18, 12, 9, 17],
            [12, 13, 10, 14],
            [15, 11, 14, 11],
            [16, 10, 12, 15]
        ]        
        table = Table(
            table_int_to_str(preTable),
            row_labels=[Text("1"), Text("2"), Text("3"), Text("4")],
            col_labels=[Text("A"), Text("B"), Text("C"), Text("D")],
            include_outer_lines=True,
            arrange_in_grid_config={"cell_alignment": RIGHT}
        )
        
        mGraph = MGraph(graph, nodes_position=nodes_and_positions, style=MGraphStyle.PURPLE)
        for x in "1234ABCD":
            remove_edge(mGraph, x, 'A')

        both = VGroup(table, mGraph)
        both.scale(0.8)
        both.arrange(buff=1)
        self.play(Create(both))
        self.play(Wait(1))

        generator = hungarian_step_generator(preTable)
        
        for state in generator:
            if state["done"]:
                break
                
            p = state["p"]
            size = len(preTable)
            assignment = [-1] * size
            for col in range(1, size + 1):
                assigned_row = p[col]
                if assigned_row > 0:
                    assignment[assigned_row - 1] = col - 1
            
            new_graph = {}
            row_labels = ["1", "2", "3", "4"]
            col_labels = ["A", "B", "C", "D"]
            for row_index, row_label in enumerate(row_labels):
                col_index = assignment[row_index]
                if 0 <= col_index < len(col_labels):
                    new_graph[row_label] = [col_labels[col_index]]
            if not new_graph:
                new_graph = {x: ['A'] for x in "1234ABCD"}
                
            new_mGraph = MGraph(new_graph, nodes_position=nodes_and_positions, style=MGraphStyle.PURPLE)
            if not assignment or all(x == -1 for x in assignment):
                for x in "1234ABCD":
                    remove_edge(new_mGraph, x, 'A')

            new_table = Table(
                table_int_to_str(preTable),
                row_labels=[Text("1"), Text("2"), Text("3"), Text("4")],
                col_labels=[Text("A"), Text("B"), Text("C"), Text("D")],
                include_outer_lines=True,
                arrange_in_grid_config={"cell_alignment": RIGHT}
            )
            
            new_both = VGroup(new_table, new_mGraph)
            new_both.scale(0.8)
            new_both.arrange(buff=1)
            
            self.play(Transform(both, new_both), run_time=1)
            self.play(Wait(1))

        self.play(Wait(3))



class GaleShapley(Scene):
    def construct(self):
        from GaleShapely import gale_shapley_generator
        def remove_edge(graph : MGraph, node1 : str, node2 : str):
            edge_name = (node1, node2)
            if edge_name in graph.edges:
                del graph.edges[edge_name]
                graph.remove(edge_name)
            edge_name2 = (node2, node1)
            if edge_name2 in graph.edges:
                del graph.edges[edge_name2]
                graph.remove(edge_name2)

        graph = {
            x: ['A'] for x in "ABCDEFGHIJ"  # dummy
        }
        nodes_and_positions = {
            'A' : LEFT*2+UP*2,
            'B' : LEFT*2+UP,
            'C' : LEFT*2,
            'D' : LEFT*2+DOWN,
            'E' : LEFT*2+DOWN*2,
            'F' : RIGHT*2+UP*2,
            'G' : RIGHT*2+UP,
            'H' : RIGHT*2,
            'I' : RIGHT*2+DOWN,
            'J' : RIGHT*2+DOWN*2,
        }
        men_pref = {
            'A': ['F', 'G', 'H', 'I', 'J'],
            'B': ['G', 'F', 'I', 'H', 'J'],
            'C': ['H', 'I', 'F', 'G', 'J'],
            'D': ['I', 'H', 'G', 'F', 'J'],
            'E': ['J', 'I', 'H', 'G', 'F']
        }
        women_pref = {
            'F': ['A', 'B', 'C', 'D', 'E'],
            'G': ['B', 'A', 'D', 'C', 'E'],
            'H': ['C', 'D', 'A', 'B', 'E'],
            'I': ['D', 'C', 'B', 'A', 'E'],
            'J': ['E', 'D', 'C', 'B', 'A']
        }

        mGraph = MGraph(graph, nodes_position=nodes_and_positions, style=MGraphStyle.PURPLE)
        for x in "ABCDEFGHIJ":  # remove dummy edges
            remove_edge(mGraph, x, 'A')
        self.play(Create(mGraph))    
        self.play(Wait(1))

        generator = gale_shapley_generator(men_pref, women_pref)

        for state in generator:
            if state["done"]:
                break
                
            engaged = state["engaged"]
            new_graph = {}
            for w, m in engaged.items():
                if m not in new_graph:
                    new_graph[m] = []
                new_graph[m].append(w)
            
            if not new_graph:
                new_graph = {x: ['A'] for x in "ABCDEFGHIJ"}
                
            new_mGraph = MGraph(new_graph, nodes_position=nodes_and_positions, style=MGraphStyle.PURPLE)
            if not engaged:
                for x in "ABCDEFGHIJ":
                    remove_edge(new_mGraph, x, 'A')
            
            self.play(Transform(mGraph, new_mGraph), run_time=1)
            self.play(Wait(0.5))

        self.play(Wait(3))

class Dinic(Scene):
    def construct(self):
        from dinic import dinic_generator
        graph = {
            'IN': [('A', 4), ('B', 3)],
            'A'     : [('C', 5)],
            'B'     : [('C', 7), ('D', 9)],
            'C'     : [('OUT', 8)],
            'D'     : [('E', 4)],
            'E'     : [('OUT', 6)],
            'OUT'   : []
        }
        nodes_and_positions = {
            'IN'    : LEFT*4,
            'A'     : LEFT*2 + UP,
            'B'     : LEFT*2 + DOWN,
            'C'     : UP,
            'D'     : DOWN,
            'E'     : RIGHT*2,
            'OUT'   : RIGHT*4
        }

        # Initial graph with 0 flow
        initial_graph = {}
        for u, edges in graph.items():
            initial_graph[u] = [(v, 0) for v, cap in edges]

        mGraph = MGraph(initial_graph, nodes_position=nodes_and_positions, style=MGraphStyle.PURPLE)
        self.play(Create(mGraph), run_time=0.5)
        self.play(Wait(2))

        generator = dinic_generator(graph, 'IN', 'OUT')
        
        for state in generator:
            if state["done"]:
                break
                
            state_graph = state["graph"]
            new_graph = {}
            for u, edges in state_graph.items():
                new_graph[u] = [(v, flow) for v, cap, flow in edges]
                
            new_mGraph = MGraph(new_graph, nodes_position=nodes_and_positions, style=MGraphStyle.PURPLE)
            
            self.play(Transform(mGraph, new_mGraph), run_time=0.5)
            self.play(Wait(1))

        self.play(Wait(3))