# Capillary-Utils


## Build

```bash
docker build . --tag capillary-web:latest
```

## Usage

### Run Server

```bash
docker run --rm -v $(pwd)/app:/app -p 8501:8501 capillary-web:latest ./start_server.sh
```

### Run cli

※ Add `docker run --rm -v $(pwd)/app:/app apillary-web:latest` if you want using Docker to run

```bash
# Call Help
python capillary_cli.py -h

# Convert to fasta
python capillary_cli.py convert -f <path_to_abi> -o <output_dir> --to fasta

# Convert to fastq
python capillary_cli.py convert -f <path_to_abi> -o <output_dir> --to fastq

# if you want to select dir
python capillary_cli.py convert -d <path_to_abi_dir> -o <output_dir> --to fastq

# You can choose all option. Including html report.
python capillary_cli.py all -f <path_to_abi> -o <output_dir>
```
