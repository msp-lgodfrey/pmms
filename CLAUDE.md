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
# Load and display PMMS data from Freddie Mac
uv run python pmms.py

# Or specify a custom file/URL
uv run python pmms.py path/to/file.xlsx
```

## Data

The app reads data directly from Freddie Mac's online source:
https://www.freddiemac.com/pmms/docs/historicalweeklydata.xlsx

This ensures you always have the most up-to-date mortgage rate data.

## Project Structure

- `pmms.py`: PMMS data loading module
  - `read_pmms(filename)`: Reads PMMS Excel data from URL or file path, skips first 7 rows, loads first 2 columns as 'date' and 'rate', removes disclaimer rows
  - `plot_pmms(df, output_file='pmms.html')`: Creates interactive Plotly chart with two subplots:
    - Top: Rate over time with range slider
    - Bottom: Rate changes (bar chart with green for increases, red for decreases)
      - Dropdown selector to choose period: Monthly, Quarterly, or Annually
    - Both plots have independent range sliders
  - Can be run as a script to display head/tail of data
- `pyproject.toml`: Project configuration and dependencies
- `pmms.html`: Generated interactive plot (created by plot_pmms)
