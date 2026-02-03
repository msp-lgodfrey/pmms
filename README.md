# PMMS - Primary Mortgage Market Survey Visualization

A Python tool for analyzing and visualizing Freddie Mac's Primary Mortgage Market Survey (PMMS) data, specifically tracking 30-year fixed-rate mortgage rates over time.

## Overview

This project provides tools to load, analyze, and visualize historical mortgage rate data from Freddie Mac's weekly survey. The data spans from 1971 to present, offering insights into long-term mortgage rate trends and quarterly changes.

## Features

- **Data Loading**: Read and clean PMMS data from Excel files
  - Automatic removal of disclaimer rows and invalid data
  - Proper date parsing and data type handling

- **Interactive Visualizations**: Dual-subplot charts with Plotly
  - **Top Plot**: Historical mortgage rates over time with full timeline view
  - **Bottom Plot**: Rate changes with selectable time periods (color-coded: green for increases, red for decreases)
    - Dropdown selector to choose: Weekly, Monthly, Quarterly, or Annual changes
  - Independent range sliders on both plots for detailed time period analysis

- **Command-Line Interface**: Easy data exploration from the terminal
  - Display head and tail of data
  - Generate interactive HTML visualizations

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management and requires Python 3.13.

```bash
# Clone the repository
git clone <repository-url>
cd pmms

# The virtual environment and dependencies are already configured
# Activate the virtual environment
source .venv/bin/activate

# Or use uv run to execute without activating
uv run python pmms.py data/historicalweeklydata.xlsx
```

## Usage

### View Data Summary

```bash
# Read from Freddie Mac's online source (default)
uv run python pmms.py

# Or use a local file
uv run python pmms.py data/historicalweeklydata.xlsx
```

This displays the first and last 5 rows of the dataset.

### Generate Visualization

```python
from pmms import read_pmms, plot_pmms

# Load data from URL (default)
df = read_pmms('https://www.freddiemac.com/pmms/docs/historicalweeklydata.xlsx')

# Or from local file
df = read_pmms('data/historicalweeklydata.xlsx')

# Create interactive plot
plot_pmms(df)  # Saves to pmms.html
```

Open `pmms.html` in a web browser to interact with the visualization.

## Data Source

By default, the app reads data directly from Freddie Mac's Primary Mortgage Market Survey:
https://www.freddiemac.com/pmms/docs/historicalweeklydata.xlsx

A local copy is also available in the `data/` directory for offline use or testing.

## Project Structure

```
pmms/
├── data/
│   └── historicalweeklydata.xlsx  # Source data
├── pmms.py                         # Main module
├── pyproject.toml                  # Project configuration
├── CLAUDE.md                       # Development guide
└── README.md                       # This file
```

## Dependencies

- pandas >= 3.0.0
- plotly >= 6.5.2
- openpyxl >= 3.1.5

All dependencies are managed via uv and specified in `pyproject.toml`.

## License

[Add license information here]
