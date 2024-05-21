# Requirements

You need to have the following software installed:

- Aria2c
- GNU parallel
- Python 3
- AWK
- Infernal

In addition, the following Python packages are required:

- tqdm
- orjson
- RNApolis

# Running

1. Prepare the raw data (Rfam 14.10 FASTA files and 2D structures from RNAsolo 3.326 annotated via RNApolis Annotator):

   ```
   ./00-prepare-raw-data.sh
   ```

2. Run the main Rfam analysis.

   This script will analyze all sequences in all FASTA files:

   ```
   ./01-run.sh
   ```

   Once it finishes or the computations were interrupted, check if there are any errors and continue. Repeat these three scripts as long as there are some unprocessed sequences:

   ```
   ./02-find-nonfull-matches.py
   ./03-generate-stats.sh
   ./04-run-for-missing.sh
   ```

3. Divide secondary structures into motifs.

   ```
   ./05-generate-stats.sh
   ./06-prepare-dbn.py
   ./07-run-motif-extractor.py
   ```

4. Generate CSV with loops from Rfam:

   ```
   ./08-rfam.py
   ```

5. Generate CSV with loops from RNAsolo:

   ```
   ./09-rnasolo.py
   ```
