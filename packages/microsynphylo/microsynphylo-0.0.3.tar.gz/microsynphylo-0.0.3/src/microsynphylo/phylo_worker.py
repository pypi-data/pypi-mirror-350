import os
import subprocess
from PyQt5.QtCore import QThread, pyqtSignal

class PhyloWorker(QThread):
    log_signal = pyqtSignal(str)
    done_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)

    def __init__(self, output_dir, grouped, model, bootstrap_count, thread_count, method="raxml"):
        super().__init__()
        self.output_dir = output_dir
        self.grouped = grouped
        self.model = model
        self.bootstrap_count = bootstrap_count
        self.thread_count = thread_count
        self.method = method

    def run(self):
        def log(msg):
            self.log_signal.emit(msg)

        align_dir = os.path.join(self.output_dir, "alignments")
        tree_dir = os.path.join(self.output_dir, "trees")
        os.makedirs(tree_dir, exist_ok=True)

        log("\n🔬 Starting phylogenetic analysis...")
        total = len(self.grouped)
        for i, group_label in enumerate(self.grouped):
            self.progress_signal.emit(int((i / total) * 100))
            aligned_path = os.path.join(align_dir, f"{group_label}_aligned.fasta")

            if not os.path.isfile(aligned_path):
                log(f"❌ Aligned file not found for {group_label}, skipping.")
                continue

            if self.method == "fasttree":
                tree_path = os.path.join(tree_dir, f"{group_label}_final.fasttree.support")
                log(f"🌳 Inference with FastTree for {group_label}...")
                result = subprocess.run(
                    ["fasttree", "-boot", str(self.bootstrap_count), aligned_path],
                    capture_output=True, text=True
                )
                tree_str = result.stdout.strip()
                if not tree_str.endswith(";"):
                    tree_str += ";"
                with open(tree_path, "w") as out_file:
                    out_file.write(tree_str)

                log(f"✓ Tree built with FastTree for {group_label} → {tree_path}")
            else:
                log(f"🌳 Inference (ML tree) with RAxML-NG for {group_label}...")
                ml_prefix = os.path.join(tree_dir, f"{group_label}_ml")
                subprocess.run([
                    "raxml-ng", "--msa", aligned_path, "--model", self.model,
                    "--prefix", ml_prefix, "--seed", "12345", "--threads", str(self.thread_count)
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                log(f"🔁 Bootstrapping for {group_label}...")
                bs_prefix = os.path.join(tree_dir, f"{group_label}_bs")
                subprocess.run([
                    "raxml-ng", "--bootstrap", "--msa", aligned_path, "--model", self.model,
                    "--prefix", bs_prefix, "--seed", "12345", "--bs-trees", str(self.bootstrap_count), "--threads", str(self.thread_count)
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                log(f"🔗 Computing support values for {group_label}...")
                final_prefix = os.path.join(tree_dir, f"{group_label}_final")
                subprocess.run([
                    "raxml-ng", "--support",
                    "--tree", f"{ml_prefix}.raxml.bestTree",
                    "--bs-trees", f"{bs_prefix}.raxml.bootstraps",
                    "--prefix", final_prefix
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                log(f"✓ Tree built and support values computed for {group_label}.")

        self.progress_signal.emit(100)
        self.done_signal.emit("All analyses completed successfully.")
