import sys
import os
import toytree
import math
import toyplot
import toyplot.svg
from PyQt5.QtCore import QThread, pyqtSignal

class TreeVisualizerWorker(QThread):
    log_signal = pyqtSignal(str)
    done_signal = pyqtSignal(str)
    image_signal = pyqtSignal(str, object)

    def __init__(self, output_dir):
        super().__init__()
        self.output_dir = output_dir

    def run(self):
        def log(msg):
            self.log_signal.emit(msg)

        USE_OUTGROUP = True

        tree_dir = os.path.join(self.output_dir, "trees")
        support_files = [
            f for f in os.listdir(tree_dir)
            if f.endswith(".raxml.support") or f.endswith(".fasttree.support")
        ]
        group_labels = list(set(
            f.replace("_final.raxml.support", "").replace("_final.fasttree.support", "")
            for f in support_files
        ))

        log("\n🎨 Starting tree visualization...")

        for group_label in group_labels:
            raxml_path = os.path.join(tree_dir, f"{group_label}_final.raxml.support")
            fasttree_path = os.path.join(tree_dir, f"{group_label}_final.fasttree.support")

            if os.path.isfile(raxml_path):
                support_tree_path = raxml_path
                method = "RAxML"
            elif os.path.isfile(fasttree_path):
                support_tree_path = fasttree_path
                method = "FastTree"
            else:
                log(f"❌ Missing support tree for {group_label}")
                continue

            log(f"📁 Using {method} tree file: {support_tree_path}")

            try:
                unrooted_tree = toytree.tree(support_tree_path)
            except Exception as e:
                log(f"⚠ Could not parse tree for {group_label}: {e}")
                continue

            block_colors = {"B1": "red", "B2": "orange", "B3": "green", "B4": "lightgreen", "B5": "blue", "B6": "lightblue"}
            tip_colors = {
                tip: "black" if tip.split("-")[0] == "B0"
                else block_colors.get(tip.split("-")[0], "black")
                for tip in unrooted_tree.get_tip_labels()
            }
            ordered_colors = [tip_colors[tip] for tip in unrooted_tree.get_tip_labels()]

            # Unrooted version
            import toyplot.png
            log(f"🎨 Drawing UNROOTED tree for {group_label}...")
            canvas_unr, axes_unr, mark_unr = unrooted_tree.draw(
                width=800,
                height=800,
                layout="unr",
                edge_type="c", 
                node_labels=[
                    f"{(val * 100):.0f}" if "fasttree" in support_tree_path.lower() and isinstance(val, (int, float)) else
                    f"{val:.0f}" if isinstance(val, (int, float)) else ""
                    for val in unrooted_tree.get_node_data("support")
                ],
                node_labels_style={
                    "font-size": "12px",
                    "fill": "black",
                    "-toyplot-anchor-shift": "12px"
                },
                tip_labels_colors=ordered_colors,
                tip_labels_style={
                    "font-size": "14px",
                    "fill": "black",
                }
            )

            canvas_unr.style = {"background-color": "white"}
            mark_unr.style = {"background-color": "white"}

            unrooted_outpath = os.path.join(tree_dir, f"{group_label}_unrooted.png")
            canvas_unr.style = {"background-color": "white"}
            toyplot.png.render(canvas_unr, unrooted_outpath)
            log(f"🖼 Unrooted tree image saved: {unrooted_outpath}")


            # Rooted version
            if USE_OUTGROUP:
                outgroup = [tip for tip in unrooted_tree.treenode.get_leaf_names() if "B0" in tip]
                if outgroup:
                    rooted_tree = unrooted_tree.root(outgroup[0])
                    log(f"🔁 Rooted on {outgroup[0]}")
                else:
                    log("⚠ No outgroup found, skipping rooted tree")
                    continue
            else:
                rooted_tree = unrooted_tree

            # Recompute tip colors for rooted tree
            tip_colors_rooted = {
                tip: "black" if tip.split("-")[0] == "B0"
                else block_colors.get(tip.split("-")[0], "black")
                for tip in rooted_tree.get_tip_labels()
            }
            ordered_colors_rooted = [tip_colors_rooted[tip] for tip in rooted_tree.get_tip_labels()]

            log(f"🎨 Drawing ROOTED tree for {group_label}...")
            canvas_r, axes_r, mark_r = rooted_tree.draw(
                width=800,
                height=800,
                layout="r",
                node_labels=[
                    f"{(val * 100):.0f}" if "fasttree" in support_tree_path.lower() and isinstance(val, (int, float)) else
                    f"{val:.0f}" if isinstance(val, (int, float)) else ""
                    for val in rooted_tree.get_node_data("support")
                ],
                node_labels_style={
                    "font-size": "12px",
                    "fill": "black",
                    "-toyplot-anchor-shift": "12px"
                },
                tip_labels_colors=ordered_colors_rooted,
                tip_labels_style={
                    "font-size": "14px",
                    "fill": "black",
                }
            )
            canvas_r.style = {"background-color": "white"}
            mark_r.style = {"background-color": "white"}

            rooted_outpath = os.path.join(tree_dir, f"{group_label}_rooted.png")
            canvas_r.style = {"background-color": "white"}
            toyplot.png.render(canvas_r, rooted_outpath)
            log(f"🖼 Rooted tree image saved: {rooted_outpath}")


            self.image_signal.emit(group_label, None)

        self.done_signal.emit("All trees rendered.")
