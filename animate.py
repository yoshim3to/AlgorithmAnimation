from manim import *
from manim_dsa import *
import random
import sys
sys.path.append('..')
from GaleShapelyAlgorithm import GaleShapley

def table_int_to_str(table: list[list[int]]):
    out = [[str(item) for item in row] for row in table]
    return out

class Hungarian(Scene):
    def construct(self):
        graph = {
            x: ['A'] for x in "ABCDEFGHIJ"  # a vertex wont be displayed unless it has an edge
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
        both = VGroup(table, MGraph(graph, nodes_and_positions, style=MGraphStyle.PURPLE))
        both.scale(0.8)
        both.arrange(buff=1)
        self.play(Create(both))
        # while(not done):
        #     new_table = Hungarian(table)
        #     new_graph = Hungarian(graph)
        #     new_both = VGroup(new_table, MGraph(new_graph, nodes_and_positions, style=MGraphStyle.PURPLE))
        #     self.play(Transform(group, new_group), runtime=1)
        #     self.play(Wait(1))
        self.play(Wait(3))



class GaleShapley(Scene):
        def construct(self):
            graph = {x: [] for x in "ABCDEFGHIJ"}
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
            mGraph = MGraph(graph, nodes_and_positions, style=MGraphStyle.PURPLE)
            self.play(Create(mGraph))
            men = "ABCDE"
            while any(not graph[node] for node in men):
                graph, new_edge = GaleShapley(graph)
                if new_edge:
                    new_mGraph = MGraph(graph, nodes_and_positions, style=MGraphStyle.PURPLE)
                    self.play(Transform(mGraph, new_mGraph), run_time=1)
                    self.play(Indicate(new_mGraph.edges[new_edge]), run_time=1)
                self.wait(1)
            self.play(Wait(3))

class Dinic(Scene):
    def construct(self):
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

        mGraph = MGraph(graph, nodes_and_positions, style=MGraphStyle.PURPLE)
        self.play(Create(mGraph), run_time=0.5)
        self.play(Wait(2))
        # while(not done):
        #     graph = Dinic(graph)
        #     mGraph = MGraph(graph, nodes_and_positions, style=MGraphStyle.PURPLE)
        #     self.play(Create(mGraph), runtime=0.5)
        #     and maybe highlight the chosen augmenting path too
        #     self.play(Indicate(augmenting path), runtime=1)
        #     self.play(Wait(2))
        # self.play(Wait(3))

        