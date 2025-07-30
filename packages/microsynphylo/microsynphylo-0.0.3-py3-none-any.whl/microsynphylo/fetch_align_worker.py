import os
import pandas as pd
import subprocess
from PyQt5.QtCore import QThread, pyqtSignal
from Bio import Entrez
from collections import defaultdict

Entrez.email = "your.email2@example.com"  # Replace with your actual email

class FetchAlignWorker(QThread):
    log_signal = pyqtSignal(str)
    done_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    enable_phylo_button = pyqtSignal()

    def __init__(self, csv_path, output_dir, grouped, save_fasta):
        super().__init__()
        self.csv_path = csv_path
        self.output_dir = output_dir
        self.grouped = grouped
        self.save_fasta = save_fasta

    def run(self):
        def log(msg):
            self.log_signal.emit(msg)

        df = pd.read_csv(self.csv_path)
        grouped_sequences = defaultdict(list)
        fetched = set()
        align_dir = os.path.join(self.output_dir, "alignments")
        os.makedirs(align_dir, exist_ok=True)

        log("📥 Fetching sequences from NCBI...")
        for group_name, gene_cols in self.grouped.items():
            aligned_path = os.path.join(align_dir, f"{group_name}_aligned.fasta")
            if os.path.exists(aligned_path):
                log(f"⏩ Skipping {group_name}: alignment already exists at {aligned_path}")
                continue

            fasta_path = os.path.join(self.output_dir, f"{group_name}.fasta")

            log(f"\n→ Processing group: {group_name}")
            for _, row in df.iterrows():
                species = row["Species"]
                for gene_col in gene_cols:
                    cell_value = row.get(gene_col, '')
                    if pd.isna(cell_value) or str(cell_value).strip() == "":
                        log(f"  • Skipping empty cell: {species} {gene_col}")
                        continue
                    gene_name = str(cell_value).strip().split()[0]
                    key = (species, gene_name)
                    if key in fetched:
                        continue
                    fetched.add(key)

                    try:
                        log(f"→ Searching NCBI for {gene_name} in {species}...")
                        search_term = f"{gene_name}[Gene Name] AND {species}[Organism]"
                        handle = Entrez.esearch(db="protein", term=search_term, retmode="xml", retmax=1)
                        record = Entrez.read(handle)
                        ids = record["IdList"]
                        if not ids:
                            log(f"✗ No hit found for {gene_name} in {species}")
                            continue
                        fetch = Entrez.efetch(db="protein", id=ids[0], rettype="fasta", retmode="text")
                        seq = fetch.read()
                        log(f"✓ Retrieved {gene_name} sequence for {species}")
                        header = f">{gene_col}_{species}_{gene_name.replace(' ', '_')}\n"
                        grouped_sequences[group_name].append(header + seq.partition('\n')[2])
                    except Exception as e:
                        log(f"⚠ Error retrieving {gene_name} from {species}: {e}")

            if self.save_fasta and grouped_sequences[group_name]:
                with open(fasta_path, "w") as f:
                    f.write("".join(grouped_sequences[group_name]))
                log(f"✓ Saved FASTA: {fasta_path}")

            if os.path.exists(fasta_path):
                log(f"  • Aligning {group_name}...")
                with open(aligned_path, "w") as aligned_file:
                    subprocess.run(["mafft", "--auto", fasta_path], stdout=aligned_file, stderr=subprocess.DEVNULL)
                log(f"✓ Alignment complete: {aligned_path}")
            else:
                log(f"⚠ Skipping alignment for {group_name}: no FASTA found.")

        self.progress_signal.emit(100)
        self.enable_phylo_button.emit()
        self.done_signal.emit("Sequences downloaded and aligned. Ready for phylogenetic analysis.")


