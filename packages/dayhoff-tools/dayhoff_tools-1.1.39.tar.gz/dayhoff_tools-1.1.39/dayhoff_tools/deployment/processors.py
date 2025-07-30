import csv
import json
import logging
import os
import shlex
import shutil
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

logger = logging.getLogger(__name__)


class Processor(ABC):
    """Processes data locally.  Abstract class for specific calculations.
    Takes in a single file and produces a single file or folder of outputs."""

    @abstractmethod
    def run(self, input_file: str) -> str:
        """Do the calculation, including reading from input_file
        and writing to output_file"""
        output_path = "output_file"

        return output_path


class InterProScanProcessor(Processor):
    """Processes a single FASTA file using InterProScan and extracts target domains.

    This processor handles the analysis of protein sequences using InterProScan,
    and extracts specific domains based on their InterPro accession IDs.
    It maps sequence identifiers correctly using MD5 hashes from the TSV output
    to handle differences in sequence ID representation between input FASTA and
    InterProScan JSON output.
    """

    def __init__(
        self,
        interproscan_install_dir: str,  # Path to the InterProScan installation
        interproscan_temp_dir_mount: str,  # Path to temporary directory for InterProScan
        num_threads: int,  # Number of CPU threads for InterProScan to use
        output_formats: list[
            str
        ],  # List of desired output formats (e.g., ["JSON", "TSV"])
        target_iprs: set[str],  # Set of InterPro IDs to extract domains for
        other_interproscan_options: (
            str | None
        ) = None,  # Additional command-line options
    ):
        """Initialize the InterProScanProcessor.

        Args:
            interproscan_install_dir: Path to the InterProScan installation directory.
            interproscan_temp_dir_mount: Path to the temporary directory for InterProScan.
            num_threads: Number of CPU threads for InterProScan to use.
            output_formats: List of desired output formats (e.g., ["JSON", "TSV"]).
            target_iprs: A set of InterPro accession IDs to extract domain sequences for.
            other_interproscan_options: Additional command-line options for interproscan.sh.
        """
        self.interproscan_sh_path = Path(interproscan_install_dir) / "interproscan.sh"
        if not self.interproscan_sh_path.is_file():
            raise FileNotFoundError(
                f"interproscan.sh not found at {self.interproscan_sh_path}"
            )

        self.interproscan_temp_dir_mount = Path(interproscan_temp_dir_mount)
        # Ensure the temp directory exists
        self.interproscan_temp_dir_mount.mkdir(parents=True, exist_ok=True)

        self.num_threads = num_threads
        self.output_formats = output_formats

        # Ensure both JSON and TSV formats are included for domain extraction
        if "JSON" not in self.output_formats:
            self.output_formats.append("JSON")
        if "TSV" not in self.output_formats:
            self.output_formats.append("TSV")

        self.target_iprs = target_iprs
        self.other_options = (
            other_interproscan_options if other_interproscan_options else ""
        )

        logger.info(
            f"InterProScanProcessor initialized with script: {self.interproscan_sh_path}"
        )
        logger.info(
            f"Temp dir mount for InterProScan: {self.interproscan_temp_dir_mount}"
        )
        logger.info(f"Target IPRs: {self.target_iprs}")

    def run(self, input_file: str) -> str:
        """Run InterProScan on the input FASTA file and extract domain sequences.

        This method processes a FASTA file through InterProScan, extracts domains
        of interest based on the target_iprs list, and writes the extracted domains
        to a separate FASTA file. Domain sequences are correctly mapped using MD5 hashes
        from the TSV output to handle differences in sequence ID representation.

        Args:
            input_file: Path to the input FASTA file.

        Returns:
            Path to the output directory containing extracted domain sequences and raw results.
        """
        from Bio import SeqIO
        from Bio.Seq import Seq

        input_file_path = Path(input_file).resolve()
        input_file_stem = input_file_path.stem

        # Create output directory structure
        chunk_output_dir = Path(f"results_{input_file_stem}").resolve()
        chunk_output_dir.mkdir(parents=True, exist_ok=True)

        raw_ipr_output_dir = chunk_output_dir / "raw_ipr_output"
        raw_ipr_output_dir.mkdir(parents=True, exist_ok=True)

        # --- Clean input FASTA file to remove stop codons ---
        cleaned_input_file_path = (
            raw_ipr_output_dir / f"{input_file_stem}_cleaned.fasta"
        )
        logger.info(
            f"Cleaning input FASTA file: {input_file_path} to remove '*' characters."
        )
        cleaned_records = []
        has_asterisks = False

        for record in SeqIO.parse(input_file_path, "fasta"):
            original_seq_str = str(record.seq)
            if "*" in original_seq_str:
                has_asterisks = True
                cleaned_seq_str = original_seq_str.replace("*", "")
                record.seq = Seq(cleaned_seq_str)
                logger.debug(f"Removed '*' from sequence {record.id}")
            cleaned_records.append(record)

        if has_asterisks:
            SeqIO.write(cleaned_records, cleaned_input_file_path, "fasta")
            logger.info(f"Cleaned FASTA written to {cleaned_input_file_path}")
            ipr_input_file_to_use = cleaned_input_file_path
        else:
            logger.info(
                f"No '*' characters found in {input_file_path}. Using original."
            )
            ipr_input_file_to_use = input_file_path
        # --- End of cleaning ---

        # Set up InterProScan output base path
        ipr_output_base = raw_ipr_output_dir / input_file_stem

        # Build the InterProScan command
        cmd = [
            str(self.interproscan_sh_path),
            "-i",
            str(ipr_input_file_to_use),
            "-b",
            str(ipr_output_base),
            "-f",
            ",".join(self.output_formats),
            "--cpu",
            str(self.num_threads),
            "--tempdir",
            str(self.interproscan_temp_dir_mount),
            "--disable-precalc",
        ]

        # Add additional options if provided
        if self.other_options:
            cmd.extend(self.other_options.split())

        # Run InterProScan
        logger.info(f"Running InterProScan command: {' '.join(cmd)}")
        try:
            process = subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info(f"InterProScan STDOUT: {process.stdout}")
            if process.stderr:
                logger.info(f"InterProScan STDERR: {process.stderr}")
        except subprocess.CalledProcessError as e:
            logger.error(f"InterProScan failed for {input_file_path}")
            logger.error(f"Return code: {e.returncode}")
            logger.error(f"STDOUT: {e.stdout}")
            logger.error(f"STDERR: {e.stderr}")
            # Create a failure marker file
            Path(chunk_output_dir / "INTERPROSCAN_FAILED.txt").touch()
            return str(chunk_output_dir)

        # Define paths for output files
        extracted_domains_fasta_path = (
            chunk_output_dir / f"{input_file_stem}_extracted_domains.fasta"
        )
        json_output_path = ipr_output_base.with_suffix(".json")
        tsv_output_path = ipr_output_base.with_suffix(".tsv")

        # Check for required output formats
        if "JSON" not in self.output_formats or not json_output_path.is_file():
            logger.warning(
                f"JSON output format not requested or file not found: {json_output_path}. Cannot extract domains."
            )
            return str(chunk_output_dir)

        if "TSV" not in self.output_formats or not tsv_output_path.is_file():
            logger.warning(
                f"TSV output format not found: {tsv_output_path}. This is needed to map sequence IDs."
            )
            return str(chunk_output_dir)

        # Extract domains using the JSON and TSV outputs
        try:
            # Create MD5 to sequence ID mapping from TSV
            md5_to_id = {}
            with open(tsv_output_path, "r") as f:
                for line in f:
                    parts = line.strip().split("\t")
                    if len(parts) >= 3:  # Ensure there are enough columns
                        seq_id = parts[0]
                        md5 = parts[1]
                        md5_to_id[md5] = seq_id

            logger.debug(f"Created MD5 to ID mapping with {len(md5_to_id)} entries")

            # Load protein sequences for coordinate mapping
            protein_sequences = SeqIO.to_dict(
                SeqIO.parse(ipr_input_file_to_use, "fasta")
            )

            # Process JSON for domain extraction
            extracted_count = 0
            with (
                open(extracted_domains_fasta_path, "w") as f_out,
                open(json_output_path, "r") as f_json,
            ):
                data = json.load(f_json)
                if "results" not in data:
                    logger.info(f"No 'results' key in JSON output {json_output_path}")
                    return str(chunk_output_dir)

                for result in data.get("results", []):
                    # Map sequence via MD5 hash
                    md5 = result.get("md5")
                    if not md5 or md5 not in md5_to_id:
                        logger.debug(f"MD5 hash not found in mapping: {md5}")
                        continue

                    protein_acc = md5_to_id[md5]
                    if protein_acc not in protein_sequences:
                        logger.debug(f"Sequence ID not found in FASTA: {protein_acc}")
                        continue

                    original_seq_record = protein_sequences[protein_acc]
                    for match in result.get("matches", []):
                        # Extract the InterPro domain entry
                        signature = match.get("signature", {})
                        entry = signature.get("entry")
                        if not entry or entry.get("accession") not in self.target_iprs:
                            continue

                        ipr_id = entry.get("accession")
                        ipr_desc = entry.get("description", "N/A").replace(" ", "_")
                        logger.info(
                            f"Found target domain {ipr_id} ({ipr_desc}) in sequence {protein_acc}"
                        )

                        for location in match.get("locations", []):
                            start = location.get("start")
                            end = location.get("end")
                            if start is not None and end is not None:
                                domain_seq_str = str(
                                    original_seq_record.seq[start - 1 : end]
                                )
                                domain_fasta_header = f">{original_seq_record.id}|{ipr_id}|{start}-{end}|{ipr_desc}"
                                f_out.write(f"{domain_fasta_header}\n")
                                f_out.write(f"{domain_seq_str}\n")
                                extracted_count += 1
                                logger.debug(
                                    f"Extracted domain {ipr_id} ({start}-{end}) from {protein_acc}"
                                )

            logger.info(
                f"Extracted {extracted_count} domain sequences to {extracted_domains_fasta_path}"
            )

        except FileNotFoundError:
            logger.error(
                f"Input FASTA file {ipr_input_file_to_use} not found during domain extraction."
            )
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from {json_output_path}.")
        except Exception as e:
            logger.error(f"Error during domain extraction: {e}", exc_info=True)

        # Clean up if the input file was a temporary one
        if has_asterisks and cleaned_input_file_path != input_file_path:
            if cleaned_input_file_path.exists():
                cleaned_input_file_path.unlink()

        return str(chunk_output_dir)


class BoltzPredictor(Processor):
    """Processor for running Boltz docking predictions.

    This class wraps the Boltz docking tool to predict protein structures
    from sequence data.
    """

    def __init__(self, num_workers: int, boltz_options: str | None = None):
        """Initialize the BoltzPredictor.

        Args:
            num_workers: Number of worker threads to use as a default.
                         This can be overridden if --num_workers is present
                         in boltz_options.
            boltz_options: A string containing additional command-line options
                           to pass to the Boltz predictor. Options should be
                           space-separated (e.g., "--option1 value1 --option2").
        """
        self.num_workers = num_workers
        self.boltz_options = boltz_options

    def run(self, input_file: str) -> str:
        """Run Boltz prediction on the input file.

        Constructs the command using the input file, default number of workers,
        and any additional options provided via `boltz_options`. If `--num_workers`
        is specified in `boltz_options`, it overrides the default `num_workers`.

        Args:
            input_file: Path to the input file containing sequences

        Returns:
            Path to the output directory created by Boltz

        Raises:
            subprocess.CalledProcessError: If Boltz prediction fails
        """
        # Determine expected output directory name
        input_base = os.path.splitext(os.path.basename(input_file))[0]
        expected_output_dir = f"boltz_results_{input_base}"
        logger.info(f"Expected output directory: {expected_output_dir}")

        # Start building the command
        cmd = ["boltz", "predict", input_file]

        # Parse additional options if provided
        additional_args = []
        num_workers_in_opts = False
        if self.boltz_options:
            try:
                parsed_opts = shlex.split(self.boltz_options)
                additional_args.extend(parsed_opts)
                if "--num_workers" in parsed_opts:
                    num_workers_in_opts = True
                    logger.info(
                        f"Using --num_workers from BOLTZ_OPTIONS: {self.boltz_options}"
                    )
            except ValueError as e:
                logger.error(f"Error parsing BOLTZ_OPTIONS '{self.boltz_options}': {e}")
                # Decide if we should raise an error or proceed without options
                # For now, proceed without the additional options
                additional_args = []  # Clear potentially partially parsed args

        # Add num_workers if not specified in options
        if not num_workers_in_opts:
            logger.info(f"Using default num_workers: {self.num_workers}")
            cmd.extend(["--num_workers", str(self.num_workers)])

        # Add the parsed additional arguments
        cmd.extend(additional_args)

        # Log the final command
        # Use shlex.join for safer command logging, especially if paths/args have spaces
        try:
            safe_cmd_str = shlex.join(cmd)
            logger.info(f"Running command: {safe_cmd_str}")
        except AttributeError:  # shlex.join is Python 3.8+
            logger.info(f"Running command: {' '.join(cmd)}")

        # Stream output in real-time
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        stdout = process.stdout
        if stdout:
            for line in iter(stdout.readline, ""):
                logger.info(f"BOLTZ: {line.rstrip()}")

        # Wait for process to complete
        return_code = process.wait()
        if return_code != 0:
            logger.error(f"Boltz prediction failed with exit code {return_code}")
            raise subprocess.CalledProcessError(return_code, cmd)

        logger.info(
            f"Boltz prediction completed successfully. Output in {expected_output_dir}"
        )
        return expected_output_dir


class MMSeqsProfileProcessor(Processor):
    """Processor for running MMseqs2 profile searches.

    This class wraps the MMseqs2 workflow to perform a profile-based search
    against a target database using a query FASTA.
    """

    def __init__(
        self,
        query_fasta_path_in_image: str,
        num_threads: int = 8,
        mmseqs_args: dict | None = None,
    ):
        """Initialize the MMSeqsProfileProcessor.

        Args:
            query_fasta_path_in_image: Path to the query FASTA file. This path is expected
                                       to be accessible within the execution environment (e.g.,
                                       packaged in a Docker image).
            num_threads: Number of threads to use for MMseqs2 commands.
            mmseqs_args: A dictionary of additional MMseqs2 parameters.
                         Expected keys: "memory_limit_gb", "evalue", "sensitivity",
                         "max_seqs_search", "min_seq_id_cluster", "max_seqs_profile_msa".
                         Defaults are used if not provided.
        """
        if not Path(query_fasta_path_in_image).is_file():
            raise FileNotFoundError(
                f"Query FASTA file not found at: {query_fasta_path_in_image}"
            )
        self.query_fasta_path = query_fasta_path_in_image
        self.num_threads = str(num_threads)  # MMseqs2 expects string for threads

        default_mmseqs_args = {
            "memory_limit_gb": "25",
            "evalue": "10",
            "sensitivity": "7.5",
            "max_seqs_search": "300",
            "min_seq_id_cluster": "0.8",
            "max_seqs_profile_msa": "1000",
        }
        if mmseqs_args:
            self.mmseqs_args = {**default_mmseqs_args, **mmseqs_args}
        else:
            self.mmseqs_args = default_mmseqs_args

        # Log dayhoff-tools version
        from dayhoff_tools import __version__

        logger.info(f"dayhoff-tools version: {__version__}")
        logger.info(
            f"MMSeqsProfileProcessor initialized with query: {self.query_fasta_path}"
        )
        logger.info(f"MMSeqs args: {self.mmseqs_args}")
        logger.info(f"Num threads: {self.num_threads}")

    def _run_mmseqs_command(
        self, command_parts: list[str], step_description: str, work_dir: Path
    ):
        """Runs an MMseqs2 command and logs its execution.

        Args:
            command_parts: A list of strings representing the command and its arguments.
            step_description: A human-readable description of the MMseqs2 step.
            work_dir: The working directory for the command.

        Raises:
            subprocess.CalledProcessError: If the MMseqs2 command returns a non-zero exit code.
        """
        full_command = " ".join(command_parts)
        logger.info(f"Running MMseqs2 step in {work_dir}: {step_description}")
        logger.info(f"Command: {full_command}")
        try:
            process = subprocess.run(
                command_parts,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=work_dir,  # Run command in the specified working directory
            )
            if process.stdout:
                logger.info(f"MMseqs2 stdout: {process.stdout.strip()}")
            if process.stderr:  # MMseqs often outputs informational messages to stderr
                logger.info(f"MMseqs2 stderr: {process.stderr.strip()}")
            logger.info(f"MMseqs2 step '{step_description}' completed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"MMseqs2 step '{step_description}' failed in {work_dir}.")
            if e.stdout:
                logger.error(f"MMseqs2 stdout: {e.stdout.strip()}")
            if e.stderr:
                logger.error(f"MMseqs2 stderr: {e.stderr.strip()}")
            raise

    def run(self, input_file: str) -> str:
        """Run MMseqs2 profile search.

        The input_file is the target FASTA. The query FASTA is provided
        during initialization.
        The method creates an output directory (e.g., {target_stem})
        which contains the result files, now named meaningfully using the target stem
        (e.g., {target_stem}_results.m8 and {target_stem}_hits.fasta).

        Args:
            input_file: Path to the input target FASTA file.

        Returns:
            Path to the output directory (e.g., {target_stem}) containing
            the meaningfully named result files.

        Raises:
            subprocess.CalledProcessError: If any MMseqs2 command fails.
            FileNotFoundError: If the input_file is not found.
        """
        if not Path(input_file).is_file():
            raise FileNotFoundError(f"Input target FASTA file not found: {input_file}")

        input_file_path = Path(input_file).resolve()  # Ensure absolute path
        target_fasta_filename = input_file_path.name
        target_fasta_stem = input_file_path.stem  # Get stem for naming

        # Create a unique base directory for this run's outputs and temp files
        # This directory will be returned and subsequently uploaded by the Operator
        run_base_dir_name = f"{target_fasta_stem}"  # Use stem as the dir name
        run_base_dir = Path(run_base_dir_name).resolve()
        run_base_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created run base directory: {run_base_dir}")

        # Define local paths within the run_base_dir
        local_target_file = run_base_dir / target_fasta_filename
        # Copy the target file into the run directory to keep inputs and outputs together
        shutil.copy(input_file_path, local_target_file)
        logger.info(f"Copied target file {input_file_path} to {local_target_file}")

        # Query file is already specified by self.query_fasta_path (path in image)
        local_query_file = Path(self.query_fasta_path).resolve()

        # Temporary directory for MMseqs2 intermediate files, created inside run_base_dir
        mmseqs_temp_dir = run_base_dir / "mmseqs_tmp"
        mmseqs_temp_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created MMseqs2 temporary directory: {mmseqs_temp_dir}")

        # Define INTERMEDIATE output file paths within mmseqs_temp_dir
        intermediate_results_m8_file = mmseqs_temp_dir / "results.m8"
        intermediate_results_as_csv_file = mmseqs_temp_dir / "results_as.csv"

        # Define FINAL output file paths within run_base_dir, using target stem
        final_results_csv_file = run_base_dir / f"{target_fasta_stem}.csv"
        final_hits_txt_file = run_base_dir / f"{target_fasta_stem}.txt"

        # --- MMseqs2 Workflow Paths (intermediate files in mmseqs_temp_dir) ---
        query_db = mmseqs_temp_dir / "queryDB"
        target_db = mmseqs_temp_dir / "targetDB"
        # Ensure local_target_file is used for creating targetDB
        target_db_input_file = local_target_file

        query_db_cluster = mmseqs_temp_dir / "queryDB_cluster"
        query_db_rep = mmseqs_temp_dir / "queryDB_rep"
        aln_db = mmseqs_temp_dir / "alnDB"
        profile_db = mmseqs_temp_dir / "profileDB"
        result_db = mmseqs_temp_dir / "resultDB"

        try:
            # 1. Create query database
            self._run_mmseqs_command(
                ["mmseqs", "createdb", str(local_query_file), str(query_db)],
                "Create query DB",
                run_base_dir,  # Working directory for the command
            )

            # 2. Create target database
            self._run_mmseqs_command(
                ["mmseqs", "createdb", str(target_db_input_file), str(target_db)],
                "Create target DB",
                run_base_dir,
            )

            # 3. Cluster query sequences
            self._run_mmseqs_command(
                [
                    "mmseqs",
                    "cluster",
                    str(query_db),
                    str(query_db_cluster),
                    str(
                        mmseqs_temp_dir / "tmp_cluster"
                    ),  # MMseqs needs a temp dir for cluster
                    "--min-seq-id",
                    self.mmseqs_args["min_seq_id_cluster"],
                    "--threads",
                    self.num_threads,
                ],
                "Cluster query sequences",
                run_base_dir,
            )

            # 4. Create representative set from query clusters
            self._run_mmseqs_command(
                [
                    "mmseqs",
                    "createsubdb",
                    str(query_db_cluster),
                    str(query_db),
                    str(query_db_rep),
                ],
                "Create representative query set",
                run_base_dir,
            )

            # 5. Create MSA for profile generation
            self._run_mmseqs_command(
                [
                    "mmseqs",
                    "search",
                    str(query_db_rep),
                    str(query_db),  # Search representative against full query DB
                    str(aln_db),
                    str(mmseqs_temp_dir / "tmp_search_msa"),  # Temp for this search
                    "--max-seqs",
                    self.mmseqs_args["max_seqs_profile_msa"],
                    "--threads",
                    self.num_threads,
                ],
                "Create MSA for profile",
                run_base_dir,
            )

            # 6. Create profile database
            self._run_mmseqs_command(
                [
                    "mmseqs",
                    "result2profile",
                    str(query_db_rep),  # Use query_db_rep as input for profile
                    str(query_db),  # Full query DB as second arg
                    str(aln_db),
                    str(profile_db),
                    "--threads",  # Added threads option
                    self.num_threads,
                ],
                "Create profile DB",
                run_base_dir,
            )

            # 7. Perform profile search
            self._run_mmseqs_command(
                [
                    "mmseqs",
                    "search",
                    str(profile_db),
                    str(target_db),
                    str(result_db),
                    str(mmseqs_temp_dir / "tmp_search_profile"),  # Temp for this search
                    "--split-memory-limit",
                    f"{self.mmseqs_args['memory_limit_gb']}G",
                    "-e",
                    self.mmseqs_args["evalue"],
                    "--max-seqs",
                    self.mmseqs_args["max_seqs_search"],
                    "--threads",
                    self.num_threads,
                    "-s",
                    self.mmseqs_args["sensitivity"],
                ],
                "Perform profile search",
                run_base_dir,
            )

            # 8. Convert results to tabular format (M8) -> to intermediate file
            self._run_mmseqs_command(
                [
                    "mmseqs",
                    "convertalis",
                    str(profile_db),  # Query DB used for search (profileDB)
                    str(target_db),
                    str(result_db),
                    str(intermediate_results_m8_file),  # Output M8 file to temp dir
                    "--threads",
                    self.num_threads,
                ],
                "Convert results to M8",
                run_base_dir,
            )

            # 8.5 Convert M8 to CSV with headers
            logger.info(
                f"Converting M8 results to CSV: {intermediate_results_m8_file} -> {intermediate_results_as_csv_file}"
            )
            csv_headers = [
                "query_id",
                "target_id",
                "percent_identity",
                "alignment_length",
                "mismatches",
                "gap_openings",
                "query_start",
                "query_end",
                "target_start",
                "target_end",
                "e_value",
                "bit_score",
            ]
            try:
                if not intermediate_results_m8_file.exists():
                    logger.warning(
                        f"M8 results file {intermediate_results_m8_file} not found. CSV will be empty."
                    )
                    # Create an empty CSV with headers if M8 is missing
                    with open(
                        intermediate_results_as_csv_file, "w", newline=""
                    ) as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(csv_headers)
                else:
                    with (
                        open(intermediate_results_m8_file, "r") as m8file,
                        open(
                            intermediate_results_as_csv_file, "w", newline=""
                        ) as csvfile,
                    ):
                        writer = csv.writer(csvfile)
                        writer.writerow(csv_headers)
                        for line in m8file:
                            writer.writerow(line.strip().split("\t"))
            except Exception as e:
                logger.error(f"Error converting M8 to CSV: {e}", exc_info=True)
                # Ensure an empty csv is created on error to prevent downstream issues
                if not intermediate_results_as_csv_file.exists():
                    with open(
                        intermediate_results_as_csv_file, "w", newline=""
                    ) as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(csv_headers)  # write headers even on error

            # 9. Extract hit sequence IDs from M8 results for the TXT file
            hit_sequence_ids = set()
            logger.info(
                f"Extracting hit IDs from {intermediate_results_m8_file} for TXT output."
            )
            try:
                if intermediate_results_m8_file.exists():
                    with open(intermediate_results_m8_file, "r") as m8_file:
                        for line in m8_file:
                            if line.strip():  # Check if line is not empty
                                columns = line.strip().split("\t")
                                if len(columns) >= 2:
                                    hit_sequence_ids.add(
                                        columns[1]
                                    )  # Add target_accession
                    logger.info(
                        f"Found {len(hit_sequence_ids)} unique hit IDs in M8 file."
                    )
                else:
                    logger.warning(
                        f"Intermediate M8 file {intermediate_results_m8_file} not found. Hit TXT file will be empty."
                    )
            except Exception as e:
                logger.error(
                    f"Error reading M8 file {intermediate_results_m8_file} for hit ID extraction: {e}",
                    exc_info=True,
                )
                # Proceed even if M8 reading fails, TXT will be empty

            # 10. Write the set of hit sequence IDs to the final .txt file
            logger.info(
                f"Writing {len(hit_sequence_ids)} hit sequence IDs to {final_hits_txt_file}"
            )
            try:
                with open(final_hits_txt_file, "w") as txt_out:
                    # Sort IDs for consistent output
                    for seq_id in sorted(list(hit_sequence_ids)):
                        txt_out.write(f"{seq_id}\n")
                logger.info(f"Successfully wrote hit IDs to {final_hits_txt_file}")
            except Exception as e:
                logger.error(
                    f"Failed to write hit IDs to {final_hits_txt_file}: {e}",
                    exc_info=True,
                )
                # Ensure the file exists even if writing fails
                if not final_hits_txt_file.exists():
                    final_hits_txt_file.touch()

            logger.info(
                f"PROCESSOR: MMseqs2 workflow and FASTA/TXT generation completed successfully. Intermediate outputs in {mmseqs_temp_dir}"
            )

            # Move and rename final output files from mmseqs_temp_dir to run_base_dir
            if intermediate_results_as_csv_file.exists():
                shutil.move(
                    str(intermediate_results_as_csv_file), str(final_results_csv_file)
                )
                logger.info(
                    f"Moved and renamed M8 results to CSV: {final_results_csv_file}"
                )
            else:
                logger.warning(
                    f"Intermediate CSV file {intermediate_results_as_csv_file} not found. Creating empty target CSV file."
                )
                final_results_csv_file.touch()  # Create empty file in run_base_dir if not found

            logger.info(
                f"MMSeqsProfileProcessor run completed for {input_file}. Output CSV: {final_results_csv_file}"
            )

        except Exception as e:
            logger.error(
                f"MMSeqsProfileProcessor failed for {input_file}: {e}", exc_info=True
            )
            raise
        finally:
            # --- Cleanup --- #
            logger.info(f"Cleaning up temporary directory: {mmseqs_temp_dir}")
            if mmseqs_temp_dir.exists():
                shutil.rmtree(mmseqs_temp_dir)
            if local_target_file.exists() and local_target_file != Path(input_file):
                logger.info(
                    f"Cleaning up local copy of target file: {local_target_file}"
                )
                local_target_file.unlink()
            logger.info("MMSeqsProfileProcessor cleanup finished.")

        return str(run_base_dir)  # Return the path to the directory containing outputs
