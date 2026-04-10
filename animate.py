from manim import *
from manim_dsa import *
import random
import sys
import GaleShapley as gs
import hungarian
from collections import defaultdict

def table_int_to_str(table: list[list[int]]):
    out = [[str(item) for item in row] for row in table]
    return out

def int_to_ordinal(num):
    ordinal_dict = defaultdict(lambda: "th")
    ordinal_dict.update({1: "st", 2: "nd", 3: "rd"})
    mod = num % 10
    suffix = ordinal_dict[mod]
    return f"{num}{suffix}"

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
        mGraph = MGraph(graph, nodes_position=nodes_and_positions, style=MGraphStyle.PURPLE).scale(0.8)
        for x in "ABCDEFGHIJ":  # remove dummy edges
            remove_edge(mGraph, x, 'A')
        self.play(Create(mGraph))    
        self.play(Wait(0.5))


        half = len(graph) // 2
        men = list(graph.keys())[:half]
        women = list(graph.keys())[half:]
        men_pref = { man : random.sample(women, len(women)) for man in men }   # assign random preferences to everyone
        women_pref = { woman : random.sample(men, len(men)) for woman in women }
        print(men_pref.values())
        men_pref_table = Table(
            list(men_pref.values()),
            row_labels=[Text(man, stroke_width=2) for man in men],
            col_labels=[Text(int_to_ordinal(rank+1), stroke_width=2) for rank in range(half)],
            include_outer_lines=False,
            arrange_in_grid_config={"cell_alignment": [0,0,0]},
            h_buff=0.5,
            v_buff=0.8
        ).move_to([-4.1,0.2,0]).scale(0.5)
        
        men_pref_table.remove(*men_pref_table.get_vertical_lines()[1:])
        women_pref_table = Table(
            list(women_pref.values()),
            row_labels=[Text(woman, stroke_width=2) for woman in women],
            col_labels=[Text(int_to_ordinal(rank+1), stroke_width=2) for rank in range(half)],
            include_outer_lines=False,
            arrange_in_grid_config={"cell_alignment": [0,0,0]},
            h_buff=0.5,
            v_buff=0.8
        ).move_to([4.1,0.2,0]).scale(0.5)
        women_pref_table.remove(*women_pref_table.get_vertical_lines()[1:])

        self.play(AnimationGroup(
            Write(Text("Group A preferences").scale(0.6).shift([-4, 2.5, 0])),
            Write(Text("Group B preferences").scale(0.6).shift([4, 2.5, 0])),
            Create(men_pref_table), Create(women_pref_table),
            ))
        free_men = list(graph.keys())[:half]
        engaged = {} ##this will be woman -> man
        proposals = {man: 0 for man in men_pref} ##this will track which woman each man will propose to next

        big_steppa = gs.GaleShapley(women_pref, men_pref, free_men, engaged, proposals)

        steps = 0
        old_man = men[0]
        highlighted_men = []
        bordered_women = []
        yellow_rectangle = Rectangle(YELLOW, men_pref_table.get_cell((1,1)).height, men_pref_table.get_cell((1,1)).width*7.5, fill_color=YELLOW, fill_opacity=0.2)
        green_box = Rectangle(GREEN, yellow_rectangle.height-0.1, yellow_rectangle.height-0.1, fill_color=GREEN, fill_opacity=0.2)
        more_box = green_box.copy()
        less_box = green_box.copy().set_color(RED)
        row_coords = { man : men_pref_table.get_cell((int(men.index(man))+2, 4)).get_center() for man in men }
        # men_rectangles = { man : yellow_rectangle.copy().move_to(row_coords[man]) for man in men}
        women_boxes = { man : green_box.copy() for man in men }
        yellow_rectangle.move_to(row_coords['A'])
        self.play(Create(yellow_rectangle))
        while big_steppa.free_men and steps < 20:
            tried_man = big_steppa.free_men[0]
            yellow_rectangle.generate_target()
            yellow_rectangle.target.move_to(row_coords[tried_man])
            self.play(MoveToTarget(yellow_rectangle))
            print(f"free_men: {free_men}")
            _, removed_edge, new_edge = big_steppa.step(graph)
            if new_edge is None:    # means there was a rejection, show it
                tried_woman = big_steppa.men_pref[tried_man][big_steppa.proposals[tried_man]-1]
                tried_man_row = int(men.index(tried_man))+2
                tried_woman_row = int(women.index(tried_woman))+2
                if(tried_man != big_steppa.free_men[0]):
                    yellow_rectangle.generate_target()
                    yellow_rectangle.target.move_to(row_coords[tried_man])
                    self.play(MoveToTarget(yellow_rectangle))
                red_cell = men_pref_table.get_cell((tried_man_row, big_steppa.proposals[tried_man]+1), color=RED)
                men_pref_table.add(red_cell)
                self.play(Wait(0.2))
                men_pref_table.remove(red_cell)
                self.play(Wait(0.2))
                men_pref_table.add(red_cell)
                self.play(Wait(0.2))
                men_pref_table.remove(red_cell)
                less_box.move_to(women_pref_table.get_cell((tried_woman_row, int(women_pref[tried_woman].index(tried_man))+2)))
                more_box.move_to(women_pref_table.get_cell((tried_woman_row, int(women_pref[tried_woman].index(big_steppa.engaged[tried_woman]))+2)))
                self.play(Create(VGroup(less_box, more_box)))
                self.play(FadeOut(VGroup(less_box, more_box)))
                self.remove(less_box)
                self.remove(more_box)
                
                print(f"steps: {steps} new_edge: {new_edge}")
                continue
            steps += 1
            man_str = new_edge[0]
            man_row = int(men.index(man_str))+2
            end_cell = men_pref_table.get_cell((man_row, 6))
            highlighted_men.append(man_str)
            women_boxes[man_str].move_to(men_pref_table.get_cell((man_row, int(men_pref[man_str].index(new_edge[1]))+2)))
            
            green_box.move_to(men_pref_table.get_cell((2, 2)).get_center())

            if removed_edge is not None:
                removed_man_str = removed_edge[0]
                removed_woman_str = removed_edge[1]
                removed_man_row = int(men.index(removed_man_str))+2
                removed_woman_col = int(men_pref[man_str].index(new_edge[1]))+2
                more_cell = women_pref_table.get_cell((int(women.index(removed_woman_str))+2, int(women_pref[removed_woman_str].index(man_str))+2))
                more_box.move_to(more_cell.get_center())
                less_cell = women_pref_table.get_cell((int(women.index(removed_woman_str))+2, int(women_pref[removed_woman_str].index(removed_man_str))+2))
                less_box.move_to(less_cell.get_center())
                self.play(Create(VGroup(less_box, more_box)))
                self.play(FadeOut(VGroup(less_box, more_box)))
                    
                old_man = man_str
                self.play(Indicate(mGraph.edges[(removed_edge[0], removed_edge[1])], color=RED), run_time=0.5)
                remove_edge(mGraph, removed_edge[0], removed_edge[1])
                remove_edge(mGraph, removed_edge[1], removed_edge[0])
                self.play(Indicate(women_boxes[removed_man_str], color=RED))
                self.remove(women_boxes[removed_man_str])
                self.remove(more_box)
                self.remove(less_box)                
            
            mGraph.add_edge(man_str, new_edge[1])
            mGraph.edges[(man_str, new_edge[1])].highlight(GREEN)
            self.play(AnimationGroup(
                mGraph.animate.add_edge(new_edge[1], man_str),
                Create(women_boxes[man_str])
            ), run_time=0.5)
            old_man = man_str
        self.play(Wait(2))

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
