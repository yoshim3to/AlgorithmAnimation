from manim import *
from manim_dsa import *
import random
import sys
import GaleShapley as gs
from hungarian import hungarian_visual_steps
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
        preTable = [
            [10, 19, 8, 15],
            [10, 18, 7, 17],
            [13, 16, 9, 14],
            [12, 19, 8, 18]
        ]
        
        row_labels = ["P1", "P2", "P3", "P4"]
        col_labels = ["T1", "T2", "T3", "T4"]
        
        table = Table(
            table_int_to_str(preTable),
            row_labels=[Text(label) for label in row_labels],
            col_labels=[Text(label) for label in col_labels],
            include_outer_lines=True,
            arrange_in_grid_config={"cell_alignment": RIGHT}
        ).scale(0.8)
        
        # Center the working matrix during the algorithm steps
        table.move_to(ORIGIN)

        # UI Elements
        info_text = Text("Hungarian Algorithm", font_size=32).to_edge(UP)
        
        # Only draw the table and the info text initially
        self.play(Create(table), Write(info_text))
        lines = VGroup()

        # Step through the yielded actions from hungarian.py
        for step_data in hungarian_visual_steps(preTable):
            step_type = step_data[0]
            matrix = step_data[1]

            # Generate the updated table
            new_table = Table(
                table_int_to_str(matrix),
                row_labels=[Text(label) for label in row_labels],
                col_labels=[Text(label) for label in col_labels],
                include_outer_lines=True,
                arrange_in_grid_config={"cell_alignment": RIGHT}
            ).scale(0.8).move_to(table.get_center())

            if step_type == "initial":
                continue

            elif step_type == "row_reduce":
                self.play(Transform(info_text, Text("Subtracting Row Minimums", font_size=32).to_edge(UP)))
                self.play(Transform(table, new_table), run_time=1.5)

            elif step_type == "col_reduce":
                self.play(Transform(info_text, Text("Subtracting Column Minimums", font_size=32).to_edge(UP)))
                self.play(Transform(table, new_table), run_time=1.5)

            elif step_type == "cover":
                covered_rows = step_data[2]
                covered_cols = step_data[3]

                self.play(Transform(info_text, Text(f"Drawing Minimum Lines: {len(covered_rows) + len(covered_cols)}", font_size=32).to_edge(UP)))
                self.play(FadeOut(lines))
                lines = VGroup()

                # Add horizontal lines for covered rows
                for r in covered_rows:
                    cell_left = table.get_cell((r+2, 2))
                    cell_right = table.get_cell((r+2, len(col_labels)+1))
                    line = Line(cell_left.get_left() + LEFT*0.2, cell_right.get_right() + RIGHT*0.2, color=BLUE, stroke_width=6)
                    lines.add(line)

                # Add vertical lines for covered columns
                for c in covered_cols:
                    cell_top = table.get_cell((2, c+2))
                    cell_bot = table.get_cell((len(row_labels)+1, c+2))
                    line = Line(cell_top.get_top() + UP*0.2, cell_bot.get_bottom() + DOWN*0.2, color=RED, stroke_width=6)
                    lines.add(line)

                self.play(Create(lines), run_time=1)
                self.play(Wait(1))

            elif step_type == "adjust":
                min_uncovered = step_data[4]
                self.play(Transform(info_text, Text(f"Lines < {len(matrix)}. Adjusting matrix by {min_uncovered}", font_size=32).to_edge(UP)))
                self.play(Transform(table, new_table), run_time=1.5)
                self.play(Wait(1))

            elif step_type == "done":
                assignment = step_data[4]
                total_cost = step_data[5]

                self.play(Transform(info_text, Text("Optimal Assignment Found!", font_size=32, color=GREEN).to_edge(UP)))
                self.play(FadeOut(lines))

                # Scale down to 0.45 to guarantee fit with the text block
                original_table = Table(
                    table_int_to_str(preTable),
                    row_labels=[Text(label) for label in row_labels],
                    col_labels=[Text(label) for label in col_labels],
                    include_outer_lines=True,
                    arrange_in_grid_config={"cell_alignment": RIGHT}
                ).scale(0.45) 
                
                reduced_table = Table(
                    table_int_to_str(matrix),
                    row_labels=[Text(label) for label in row_labels],
                    col_labels=[Text(label) for label in col_labels],
                    include_outer_lines=True,
                    arrange_in_grid_config={"cell_alignment": RIGHT}
                ).scale(0.45)

                # Add labels to the matrices, scaled down
                orig_label = Text("Original Costs", font_size=24).next_to(original_table, UP)
                red_label = Text("Reduced Matrix", font_size=24).next_to(reduced_table, UP)

                # Group tables with their labels
                orig_group = VGroup(orig_label, original_table)
                red_group = VGroup(red_label, reduced_table)

                # Arrange side-by-side with a smaller buffer, pin to left edge
                both_matrices = VGroup(orig_group, red_group).arrange(RIGHT, buff=0.4)
                both_matrices.to_edge(LEFT, buff=0.3)

                # Animate the transition
                self.play(
                    Transform(table, reduced_table),
                    FadeIn(original_table),
                    FadeIn(orig_label),
                    FadeIn(red_label),
                    run_time=1.5
                )

                # Setup highlights and the brand new final cost group
                highlights = VGroup()
                final_cost_group = VGroup()
                final_cost_group.add(Text("Assignments", font_size=28, color=BLUE))

                for r, c in enumerate(assignment):
                    # Grab the actual cell objects
                    cell_orig = original_table.get_cell((r+2, c+2))
                    cell_red = reduced_table.get_cell((r+2, c+2))
                    
                    # Create circles, match their size to the cell, scale to 80% to fit inside, and move to cell center
                    circle_orig = Circle(color=GREEN, stroke_width=4).match_height(cell_orig).scale(0.8).move_to(cell_orig)
                    circle_red = Circle(color=GREEN, stroke_width=4).match_height(cell_red).scale(0.8).move_to(cell_red)
                    
                    highlights.add(circle_orig, circle_red)
                    
                    worker = row_labels[r]
                    task = col_labels[c]
                    cost = preTable[r][c]
                    
                    final_cost_group.add(Text(f"{worker} -> {task}: {cost}", font_size=20))

                final_cost_group.add(Text(f"Total Cost: {total_cost}", font_size=28, color=GREEN))
                
                # Format the text list and pin it to the right edge
                final_cost_group.arrange(DOWN, aligned_edge=LEFT)
                final_cost_group.to_edge(RIGHT, buff=0.3) 

                # Reveal the highlights and the text at the same time
                self.play(Create(highlights), Write(final_cost_group))
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

        title = Text("Dinic's Algorithm", font_size=36, color=BLUE).to_edge(UP)
        flow_text = Text("Current Flow: 0", font_size=28, color=GREEN).to_corner(UL)
        
        self.play(Write(title), Write(flow_text))

        mGraph = MGraph(initial_graph, nodes_position=nodes_and_positions, style=MGraphStyle.PURPLE).scale(0.9).shift(DOWN * 0.5)
        self.play(Create(mGraph), run_time=1)
        self.play(Wait(1))
        
        generator = dinic_generator(graph, 'IN', 'OUT')
        current_flow = 0
        
        for state in generator:
            if state["done"]:
                if "max_flow" in state:
                    new_flow_text = Text(f"Max Flow: {state['max_flow']}", font_size=28, color=GREEN).to_corner(UL)
                    self.play(Transform(flow_text, new_flow_text))
                break
                
            aug_path = state.get("augmenting_path")
            if aug_path:
                animations = []
                for i in range(len(aug_path)-1):
                    u, v = aug_path[i], aug_path[i+1]
                    if (u, v) in mGraph.edges:
                        animations.append(Indicate(mGraph.edges[(u, v)], color=YELLOW, scale_factor=1.2))
                    elif (v, u) in mGraph.edges:
                        animations.append(Indicate(mGraph.edges[(v, u)], color=YELLOW, scale_factor=1.2))
                
                if animations:
                    path_text = Text(f"Augmenting Path: {' -> '.join(aug_path)}", font_size=24, color=YELLOW).to_edge(DOWN)
                    self.play(Write(path_text), run_time=0.5)
                    self.play(LaggedStart(*animations, lag_ratio=0.5), run_time=2)
                    self.play(Wait(0.5))
                    self.play(FadeOut(path_text), run_time=0.5)
                
            state_graph = state["graph"]
            new_graph = {}
            new_flow = 0
            for u, edges in state_graph.items():
                new_graph[u] = [(v, flow) for v, cap, flow in edges]
                if u == 'IN':
                    new_flow = sum(flow for v, cap, flow in edges)
            
            if new_flow > current_flow:
                current_flow = new_flow
                new_flow_text = Text(f"Current Flow: {current_flow}", font_size=28, color=GREEN).to_corner(UL)
                self.play(Transform(flow_text, new_flow_text), run_time=0.5)
                
            new_mGraph = MGraph(new_graph, nodes_position=nodes_and_positions, style=MGraphStyle.PURPLE).scale(0.9).shift(DOWN * 0.5)
            
            self.play(Transform(mGraph, new_mGraph), run_time=0.5)
            self.play(Wait(0.5))

        self.play(Wait(3))
