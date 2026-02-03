# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Setup

This is a uv-managed Python project using Python 3.13.

### Environment Setup

The project uses a virtual environment in `.venv/`:
```bash
# Activate the virtual environment
source .venv/bin/activate

# Or use uv run to execute commands without activating
uv run python main.py
```

### Dependency Management

```bash
# Add a new dependency
uv add <package-name>

# Add a development dependency
uv add --dev <package-name>

# Sync dependencies
uv sync
```

### Running the Project

```bash
# Load and display PMMS data
uv run python pmms.py data/historicalweeklydata.xlsx
```

## Data

The main data file is `data/historicalweeklydata.xlsx`, which contains historical weekly data. This may be used as input for data analysis, reporting, or other processing tasks.

## Project Structure

- `pmms.py`: PMMS data loading module
  - `read_pmms(filename)`: Reads PMMS Excel data, skips first 7 rows, loads first 2 columns as 'date' and 'rate', removes disclaimer rows
  - `plot_pmms(df, output_file='pmms.html')`: Creates interactive Plotly chart with two subplots:
    - Top: Rate over time with range slider
    - Bottom: Rate changes (bar chart with green for increases, red for decreases)
      - Dropdown selector to choose period: Weekly, Monthly, Quarterly, or Annual
    - Both plots have independent range sliders
  - Can be run as a script to display head/tail of data
- `pyproject.toml`: Project configuration and dependencies
- `data/`: Data directory
  - `historicalweeklydata.xlsx`: Historical weekly data
- `pmms.html`: Generated interactive plot (created by plot_pmms)
