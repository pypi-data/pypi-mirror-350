# `DamplyDirs`: Simplified Data Science Directory Management

Data science projects often involve complex directory structures to organize raw data, processed data, results, and code. Managing these directories manually can be error-prone and time-consuming. The `damply.dmpdirs` module solves this problem by providing standardized access to these directories through a simple, consistent interface.

## The Problem

As data scientists, we face several challenges when working with project directories:

- **Inconsistent Naming**: Different team members might use different directory names
- **Path Construction**: Building paths can be error-prone across operating systems
- **Missing Directories**: Time wasted creating directories that should already exist
- **Environment Variables**: Need to use the same paths in Python, R, and shell scripts
- **Project Transfer**: Moving projects between systems requires path adjustments

## Solution with `DamplyDirs`

DamplyDirs provides intuitive, standardized access to common data science project directories with environment variable support:

```python
from damply import dirs

# Access directory paths easily
data_file = dirs.RAWDATA / "dataset.csv"

# Write outputs to standard locations
results_file = dirs.RESULTS / "analysis_results.csv"

# Get a nice visual representation of your directories
print(dirs)
# DamplyDirs<Strict Mode: OFF>
# Project Root: /private/tmp/ctrpv2-treatmentresponse-snakemake
# CONFIG       : ├── config
# LOGS         : ├── logs
# METADATA     : ├── metadata
# NOTEBOOKS    : ├── workflow/notebooks
# PROCDATA     : ├── data/procdata
# RAWDATA      : ├── data/rawdata
# RESULTS      : ├── data/results
# SCRIPTS      : └── workflow/scripts
```

## Directory Resolution

`DamplyDirs` resolves directory paths in the following order:

1. **Environment Variables(RECOMMENDED)**: If an environment variable with the same name exists (e.g., `RAWDATA`), its value is used
2. **Default Structure**: Otherwise, falls back to a standard directory structure

### Default Directory Structure

When environment variables aren't set, `DamplyDirs` uses this standard structure:

```console
project_root/
├── config/         # Configuration files
├── data/           # All data in one parent directory
│   ├── procdata/   # Processed/intermediate data
│   ├── rawdata/    # Raw input data
│   └── results/    # Analysis outputs
├── logs/           # Log files
├── metadata/       # Dataset descriptions
└── workflow/       # Code organization
    ├── notebooks/  # Jupyter notebooks
    └── scripts/    # Analysis scripts
```

## Recommended Environment Variable Integration

`DamplyDirs` seamlessly integrates with environment variables, making it perfect for projects using tools like `pixi`:

```toml
# Example pixi.toml configuration
[activation]
# convenient variables which can be used in scripts
env.CONFIG = "${PIXI_PROJECT_ROOT}/config"
env.METADATA = "${PIXI_PROJECT_ROOT}/metadata"
env.LOGS = "${PIXI_PROJECT_ROOT}/logs"
env.RAWDATA = "${PIXI_PROJECT_ROOT}/data/rawdata"
env.PROCDATA = "${PIXI_PROJECT_ROOT}/data/procdata"
env.RESULTS = "${PIXI_PROJECT_ROOT}/data/results"
env.SCRIPTS = "${PIXI_PROJECT_ROOT}/workflow/scripts"
```

This will automatically set these environment variables when you activate your
project environment via `pixi shell` or `pixi run`.

With this setup, your paths will be consistent across:

- Python scripts using `DamplyDirs`
- R scripts using environment variables
- Shell scripts and commands
- Snakemake workflows
- Any other tools that can access environment variables

## Getting Started

### Basic Usage

```python
from damply import dirs

# Access paths directly
config_path = dirs.CONFIG / "analysis_config.yaml"
data_path = dirs.RAWDATA / "experiment_1" / "samples.csv"
results_path = dirs.RESULTS / "figures" / "figure1.png"
```

### Auto-Directory Creation

By default, `DamplyDirs` operates in non-strict mode, which automatically creates missing directories when they are accessed. This behavior helps get you started quickly without having to manually create all directories first:

```python
# Accessing this path will create the directory if it doesn't exist
missing_dir = dirs.RESULTS / "new_analysis"

# You can enable strict mode if you prefer to get errors for missing directories
dirs.set_strict_mode(True)

# Now this will raise DirectoryNameNotFoundError if the directory doesn't exist
try:
    missing_dir = dirs.RESULTS / "another_analysis"
except DirectoryNameNotFoundError:
    print("Directory doesn't exist and won't be created in strict mode")
```

When not in strict mode, you'll see informative log messages when directories are created automatically.

## Advanced Usage

### Project Root Discovery

`DamplyDirs` finds your project root in the following order:

1. From `DMP_PROJECT_ROOT` environment variable
2. From `PIXI_PROJECT_ROOT` environment variable
3. Current working directory as fallback (**not recommended as this won't work in jupyter notebooks**)

Set the environment variable to ensure consistent behavior across scripts:

```bash
export DMP_PROJECT_ROOT=/path/to/my/project
```

## Using in Other Languages and Tools

!!! note
    Assuming you have set the environment variables as shown in the `pixi.toml`
    example, you can access these directories in various languages and tools.

=== "Python"
    ```python
    from damply import dirs

    # Access directories using environment variables
    raw_data_path = dirs.RAWDATA / "dataset.csv"
    results_path = dirs.RESULTS / "analysis_results.csv"

    # Read data and save results
    import pandas as pd
    data = pd.read_csv(raw_data_path)
    data.to_csv(results_path, index=False)
    ```

=== "R Scripts"
    ```r
    # Access the same directories in R
    RAWDATA <- Sys.getenv("RAWDATA")
    RESULTS <- Sys.getenv("RESULTS")

    # Read data and save results using those paths
    data <- read.csv(file.path(RAWDATA, "dataset.csv"))
    write.csv(results, file.path(RESULTS, "analysis_results.csv"))
    ```

=== "Shell Scripts"
    ```bash
    # Access the same directories in shell scripts
    echo $RAWDATA
    ls $RAWDATA/dataset.csv
    cp $RAWDATA/dataset.csv $PROCDATA/processed_dataset.csv
    ```

=== "Snakemake"
    ```python
    # Snakemake is a python superset, so you can use damply.dmpdirs directly!
    from damply import dirs
    rule all:
        input:
            dirs.RESULTS / "final_results.txt"
    rule process_data:
        input:
            dirs.RAWDATA / "dataset.csv"
        output:
            dirs.PROCDATA / "processed_data.csv"
        shell:
            "${dirs.SCRIPTS}/process_data.sh {input} > {output}"
    ```

## Real-World Examples

### Data Processing Workflow

```python
from damply import dirs
import pandas as pd

# Load input data
input_file = dirs.RAWDATA / "experiment_2023" / "samples.csv"
data = pd.read_csv(input_file)

# Process data
processed_data = data.groupby('sample_id').mean()

# Save intermediate result
interim_file = dirs.PROCDATA / "aggregated_samples.csv"
processed_data.to_csv(interim_file)

# Generate and save visualization
output_file = dirs.RESULTS / "sample_means.png"
processed_data.plot(kind='bar').figure.savefig(output_file)
print(f"Results saved to {output_file}")
# Results saved to /path/to/project_root/data/results/sample_means.png
```

### Configuration Management

```python
from damply import dirs
import yaml

# Load configuration
config_file = dirs.CONFIG / "analysis_params.yaml"
with open(config_file, 'r') as f:
    config = yaml.safe_load(f)

# Use configuration in analysis
threshold = config['filtering']['threshold']
print(f"Using threshold: {threshold}")
```

## Troubleshooting

### "Directory Not Found" Errors

If you get a `DirectoryNameNotFoundError`:

1. Check that you're in the correct project root
2. Verify that the directory exists or the environment variable is set
3. Consider setting `dirs.set_strict_mode(False)` to auto-create directories

### Environment Variable Not Set

If you get an `EnvironmentVariableNotSetError` or see a warning log about falling back to default paths:

1. Make sure your environment is activated and you have [set the environment variables](#recommended-environment-variable-integration)
   in your `pixi.toml`!
2. Check that the variable is set correctly (try `echo $VARNAME`)

## Best Practices

- Use `DamplyDirs` consistently across all project scripts
- Set environment variables in your project configuration (`pixi.toml`, etc.)
- Keep a clear separation between raw data, processed data, and results
- Monitor the logs - they provide useful information about directory creation and fallbacks

By using `DamplyDirs` with environment variables, you ensure that your data science projects remain organized, portable, and consistent across languages, tools, and team members.

## Strict Mode and Environment Variables

When using environment variables with `DamplyDirs`, the behavior depends on the strict mode setting:

1. **In Strict Mode** (`dirs.set_strict_mode(True)`):
   - If an environment variable for a directory is not set, an `EnvironmentVariableNotSetError` is raised
   - If a directory doesn't exist (even with environment variable), a `DirectoryNameNotFoundError` is raised

2. **In Non-Strict Mode** (`dirs.set_strict_mode(False)`, the default):
   - If an environment variable isn't set, falls back to default paths with a warning log message
   - If a directory doesn't exist, it's automatically created with an info log message

This behavior gives you flexibility to enforce environment variable usage in production while allowing more permissive behavior during development:

```python
# In development: auto-create missing directories (default behavior)
dirs.set_strict_mode(False)
data_path = dirs.RAWDATA / "my_data.csv"  # Will use default path if env var not set

# In production: enforce that environment variables are properly set
dirs.set_strict_mode(True)
try:
    data_path = dirs.RAWDATA / "my_data.csv"
except EnvironmentVariableNotSetError:
    print("RAWDATA environment variable must be set!")
```
