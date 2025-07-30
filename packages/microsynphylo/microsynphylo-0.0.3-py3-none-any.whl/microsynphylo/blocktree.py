import toytree
import toyplot
import toyplot.svg
from collections import defaultdict
from pathlib import Path
from itertools import combinations
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import linkage, to_tree


def infer_block_tree(gene_tree_files, output_path_base):
    block_pair_support = defaultdict(int)
    subtree_support = defaultdict(list)
    all_blocks = set()
    total_trees = 0

    print("🔍 Parsing gene tree files...")
    for treefile in gene_tree_files:
        print(f"📄 Reading: {treefile.name}")
        try:
            t = toytree.tree(treefile.read_text())
        except Exception as e:
            print(f"❌ Failed to parse tree {treefile.name}: {e}")
            continue

        leaf_blocks = {
            leaf: leaf.split("-")[0]
            for leaf in t.get_tip_labels()
            if "-" in leaf
        }

        block_to_leaves = defaultdict(list)
        for leaf, block in leaf_blocks.items():
            block_to_leaves[block].append(leaf)
        all_blocks.update(block_to_leaves.keys())

        for node in t.treenode.traverse("postorder"):
            if not node.is_leaf():
                leaves = [leaf.name for leaf in node.get_leaves() if leaf.name in leaf_blocks]
                blocks = set(leaf_blocks[leaf] for leaf in leaves)
                if len(blocks) >= 2:
                    key = tuple(sorted(blocks))
                    subtree_support[key].append(treefile.name)

        total_trees += 1

    print(f"🧮 Processed {total_trees} trees")
    if total_trees == 0 or not subtree_support:
        print("⚠ No valid gene trees processed. Skipping block tree generation.")
        return None

    all_blocks = sorted(all_blocks)
    print(f"🧩 Found blocks: {all_blocks}")
    mat = pd.DataFrame(1.0, index=all_blocks, columns=all_blocks)
    for key, val in subtree_support.items():
        if len(key) == 2:
            b1, b2 = key
            score = 1 - (len(val) / total_trees)
            mat.loc[b1, b2] = mat.loc[b2, b1] = score
    np.fill_diagonal(mat.values, 0)

    print("🔗 Performing hierarchical clustering...")
    from scipy.spatial.distance import squareform
    linked = linkage(squareform(mat.values), method="average")
    tree_root, _ = to_tree(linked, rd=True)

    def build_newick(node):
        if node.is_leaf():
            return f"{all_blocks[node.id]}"
        left = build_newick(node.left)
        right = build_newick(node.right)
        return f"({left},{right})"

    newick_str = build_newick(tree_root) + ";"
    print(f"🧾 Inferred Newick: {newick_str}")
    block_tree = toytree.tree(newick_str)

    block_colors = {"B1": "red", "B2": "orange", "B3": "green", "B4": "lightgreen", "B5": "blue", "B6": "lightblue"}

    tip_colors = {
        tip: block_colors.get(tip, "black") for tip in block_tree.get_tip_labels()
    }
    ordered_colors = [tip_colors[tip] for tip in block_tree.get_tip_labels()]

    for layout, suffix in [("r", "_rooted"), ("unr", "_unrooted")]:
        print(f"🎨 Rendering block tree ({suffix[1:]})...")
        canvas, axes, mark = block_tree.draw(
            width=800,
            height=800,
            layout=layout,
            tip_labels_style={"font-size": "14px", "fill": "black"},
            tip_labels_colors=ordered_colors,
            pad=500
        )
        canvas.style = {"background-color": "white"}
        mark.style = {"background-color": "white"}

        outpath = Path(str(output_path_base).replace(".png", f"{suffix}.png"))
        outpath.parent.mkdir(parents=True, exist_ok=True)
        toytree.save(canvas, outpath)
        print(f"✅ Block tree saved to: {outpath}")

    return Path(str(output_path_base).replace(".png", "_rooted.png"))
