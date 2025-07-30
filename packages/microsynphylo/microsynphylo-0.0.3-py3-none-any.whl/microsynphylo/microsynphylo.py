import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QSpinBox, QLineEdit, QTextEdit, QMessageBox, QCheckBox,
    QProgressBar, QScrollArea, QFrame,  QButtonGroup
)
from PyQt5.QtCore import QThread, pyqtSignal
from .fetch_align_worker import FetchAlignWorker
from .phylo_worker import PhyloWorker
from .tree_visualizer import TreeVisualizerWorker
from .blocktree import infer_block_tree
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class PhyloApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Microsynteny Phylogenetic Analysis")
        self.resize(1100, 1000)

        main_layout = QHBoxLayout(self)

        # Left panel: Controls
        control_layout = QVBoxLayout()
        control_container = QWidget()
        control_container.setLayout(control_layout)
        control_container.setMaximumWidth(400)
        main_layout.addWidget(control_container, stretch=1)

        self.label = QLabel("Step 1: Upload CSV")
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        control_layout.addWidget(self.label)

        self.upload_button = QPushButton("Upload Gene CSV")
        self.upload_button.clicked.connect(self.upload_csv)
        control_layout.addWidget(self.upload_button)

        self.block_spin = QSpinBox()
        self.block_spin.setMinimum(1)
        self.block_spin.setMaximum(10)
        self.block_spin.setValue(4)
        control_layout.addWidget(QLabel("Step 2: Number of Gene Blocks"))
        control_layout.addWidget(self.block_spin)

        self.genes_input = QTextEdit()
        self.genes_input.setPlaceholderText("Enter homology groups, one per line\nFormat: GroupName: B1-Gene1, B2-Gene4")
        control_layout.addWidget(QLabel("Step 3: Define Homology Groups"))
        control_layout.addWidget(self.genes_input)

        self.output_button = QPushButton("Select Output Folder")
        self.output_button.clicked.connect(self.select_output_folder)
        control_layout.addWidget(self.output_button)

        self.output_label = QLabel("No output folder selected")
        control_layout.addWidget(self.output_label)

        self.align_button = QPushButton("Download and Align Sequences")
        self.align_button.clicked.connect(self.download_and_align)
        control_layout.addWidget(self.align_button)

        self.fasttree_checkbox = QCheckBox("FastTree")
        self.fasttree_checkbox.setChecked(True)
        self.raxml_checkbox = QCheckBox("RAxML")

        self.tree_method_group = QButtonGroup()
        self.tree_method_group.setExclusive(True)
        self.tree_method_group.addButton(self.fasttree_checkbox)
        self.tree_method_group.addButton(self.raxml_checkbox)

        tree_method_layout = QHBoxLayout()
        tree_method_layout.addWidget(self.fasttree_checkbox)
        tree_method_layout.addWidget(self.raxml_checkbox)
        control_layout.addWidget(QLabel("Tree Inference Method:"))
        control_layout.addLayout(tree_method_layout)

        self.raxml_params_container = QVBoxLayout()

        self.model_input = QLineEdit("LG+G")
        self.raxml_params_container.addWidget(QLabel("RAxML Model (e.g., LG+G):"))
        self.raxml_params_container.addWidget(self.model_input)

        self.thread_spin = QSpinBox()
        self.thread_spin.setMinimum(1)
        self.thread_spin.setMaximum(16)
        self.thread_spin.setValue(4)
        self.raxml_params_container.addWidget(QLabel("Threads:"))
        self.raxml_params_container.addWidget(self.thread_spin)

        control_layout.addLayout(self.raxml_params_container)

        self.bootstrap_spin = QSpinBox()
        self.bootstrap_spin.setMinimum(10)
        self.bootstrap_spin.setMaximum(1000)
        self.bootstrap_spin.setValue(100)
        control_layout.addWidget(QLabel("Bootstrap Trees:"))
        control_layout.addWidget(self.bootstrap_spin)

        self.run_button = QPushButton("Run Phylogenetic Analysis")
        self.run_button.setEnabled(False)
        self.run_button.clicked.connect(self.run_analysis)
        control_layout.addWidget(self.run_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        control_layout.addWidget(self.progress_bar)

        self.view_rooted_checkbox = QCheckBox("Show rooted trees")
        self.view_rooted_checkbox.setChecked(True)
        control_layout.addWidget(self.view_rooted_checkbox)


        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        control_layout.addWidget(QLabel("Log Output"))
        control_layout.addWidget(self.log_output)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.tree_canvas_layout = QVBoxLayout(scroll_content)
        scroll_content.setLayout(self.tree_canvas_layout)
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area, stretch=2)

        self.fasttree_checkbox.stateChanged.connect(self.update_parameter_visibility)
        self.raxml_checkbox.stateChanged.connect(self.update_parameter_visibility)
        self.update_parameter_visibility()

    def update_parameter_visibility(self):
        show_raxml = self.raxml_checkbox.isChecked()
        for i in range(self.raxml_params_container.count()):
            widget = self.raxml_params_container.itemAt(i).widget()
            if widget:
                widget.setVisible(show_raxml)

    def log(self, message):
        self.log_output.append(message)
        self.log_output.ensureCursorVisible()
        print(message)

    def upload_csv(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if filepath:
            self.label.setText(f"📂 Selected: {filepath}")
            self.csv_path = filepath

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_dir = folder
            self.output_label.setText(f"📁 Output: {folder}")

    def parse_gene_groups(self):
        lines = self.genes_input.toPlainText().splitlines()
        grouped = {}
        for line in lines:
            if ":" in line:
                group_name, genes_str = line.strip().split(":")
                gene_list = [g.strip() for g in genes_str.split(",") if g.strip()]
                grouped[group_name.strip()] = gene_list
        return grouped

    def download_and_align(self):
        if not hasattr(self, 'csv_path') or not hasattr(self, 'output_dir'):
            QMessageBox.warning(self, "Missing Input", "Upload CSV and select output folder.")
            return

        grouped = self.parse_gene_groups()
        save_fasta = True

        self.thread = FetchAlignWorker(
            csv_path=self.csv_path,
            output_dir=self.output_dir,
            grouped=grouped,
            save_fasta=save_fasta
        )
        self.thread.log_signal.connect(self.log)
        self.thread.progress_signal.connect(self.progress_bar.setValue)
        self.thread.done_signal.connect(lambda msg: QMessageBox.information(self, "Done", msg))
        self.thread.enable_phylo_button.connect(lambda: self.run_button.setEnabled(True))
        self.thread.start()

    def run_analysis(self):
        if not hasattr(self, 'output_dir'):
            QMessageBox.warning(self, "Missing Input", "Select output folder.")
            return
        
        # Clear existing tree visualizations from canvas
        while self.tree_canvas_layout.count():
            child = self.tree_canvas_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        grouped = {}
        align_dir = os.path.join(self.output_dir, "alignments")
        if not os.path.isdir(align_dir):
            QMessageBox.warning(self, "Missing Alignments", "Alignment folder not found.")
            return

        for fname in os.listdir(align_dir):
            if fname.endswith("_aligned.fasta"):
                group_name = fname.replace("_aligned.fasta", "")
                grouped[group_name] = []

        method = "raxml" if self.raxml_checkbox.isChecked() else "fasttree"
        self.thread = PhyloWorker(
            output_dir=self.output_dir,
            grouped=grouped,
            model=self.model_input.text().strip(),
            bootstrap_count=self.bootstrap_spin.value(),
            thread_count=self.thread_spin.value(),
            method=method
        )
        self.thread.log_signal.connect(self.log)
        self.thread.progress_signal.connect(self.progress_bar.setValue)
        self.thread.done_signal.connect(self.visualize_trees)
        self.thread.start()

    def visualize_trees(self):
        self.view_rooted_checkbox.stateChanged.connect(self.refresh_displayed_trees)

        if not hasattr(self, 'output_dir'):
            QMessageBox.warning(self, "Missing Output", "Select output folder.")
            return

        self.tree_thread = TreeVisualizerWorker(output_dir=self.output_dir)
        self.tree_thread.log_signal.connect(self.log)
        self.tree_thread.image_signal.connect(self.display_tree_canvas)
        self.tree_thread.done_signal.connect(self.render_block_tree)
        self.tree_thread.start()

    def render_block_tree(self):
        trees_dir = os.path.join(self.output_dir, "trees")
        if not os.path.exists(trees_dir):
            return

        from pathlib import Path
        tree_files = list(Path(trees_dir).glob("*_final.*.support"))
        print(f"🧪 Found {len(tree_files)} support trees for block inference")
        if not tree_files:
            print("⚠ No support tree files found for block tree inference.")
            return

        output_path = os.path.join(self.output_dir, "trees/block_tree_rooted.png")
        result = infer_block_tree(tree_files, output_path)
        if result and os.path.exists(output_path):
            self.display_block_tree(output_path)

    def display_tree_canvas(self, group_label, _):
        from PyQt5.QtWidgets import QLabel
        from PyQt5.QtGui import QPixmap

        # Decide which tree image to show based on checkbox
        suffix = "rooted" if self.view_rooted_checkbox.isChecked() else "unrooted"
        tree_image_path = os.path.join(self.output_dir, "trees", f"{group_label}_{suffix}.png")

        if os.path.exists(tree_image_path):
            label = QLabel(f"<b>{group_label} ({suffix})</b>")
            image_label = QLabel()
            pixmap = QPixmap(tree_image_path)
            image_label.setPixmap(pixmap)
            image_label.setScaledContents(True)
            image_label.setMinimumSize(600, 500)

            self.tree_canvas_layout.addWidget(label)
            self.tree_canvas_layout.addWidget(image_label)


    def display_block_tree(self, tree_path):
        label = QLabel("<b>Consensus Block Tree</b>")
        image_label = QLabel()
        pixmap = QPixmap(tree_path)
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        image_label.setMinimumSize(600, 500)

        self.tree_canvas_layout.addWidget(label)
        self.tree_canvas_layout.addWidget(image_label)


    def refresh_displayed_trees(self):
        # Clear and re-display based on checkbox toggle
        while self.tree_canvas_layout.count():
            child = self.tree_canvas_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Re-display previously rendered images
        tree_dir = os.path.join(self.output_dir, "trees")
        if not os.path.exists(tree_dir):
            return

        group_labels = []
        for fname in os.listdir(tree_dir):
            if fname.endswith("_final.raxml.support") or fname.endswith("_final.fasttree.support"):
                group = fname.split("_final")[0]
                if group not in group_labels:
                    group_labels.append(group)

        for group in group_labels:
            self.display_tree_canvas(group, None)


        suffix = "_rooted.png" if self.view_rooted_checkbox.isChecked() else "_unrooted.png"
        block_tree_path = os.path.join(self.output_dir, "trees", f"block_tree{suffix}")
        if os.path.exists(block_tree_path):
            self.display_block_tree(block_tree_path)



def main():
    app = QApplication(sys.argv)
    window = PhyloApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()