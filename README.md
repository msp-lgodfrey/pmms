# PMMS - Primary Mortgage Market Survey Visualization

A Python tool for analyzing and visualizing Freddie Mac's Primary Mortgage Market Survey (PMMS) data, tracking both 30-year and 15-year fixed-rate mortgage rates over time.

## Overview

This project provides tools to load, analyze, and visualize historical mortgage rate data from Freddie Mac's weekly survey. The data includes 30-year rates from April 2, 1971 to present and 15-year rates from August 30, 1991 to present, offering insights into long-term mortgage rate trends and quarterly changes.

## Features

- **Data Loading**: Read and clean PMMS data from Excel files
  - Automatic removal of disclaimer rows and invalid data
  - Proper date parsing and data type handling

- **Interactive Visualizations**: Dual-subplot charts with Plotly
  - **Top Plot**: Historical 30-year and 15-year mortgage rates over time with full timeline view
  - **Bottom Plot**: Grouped bar chart comparing rate changes for both loan types (color-coded by increase/decrease)
    - Dropdown selector to choose: Monthly, Quarterly, or Annual changes
  - Independent range sliders on both plots for detailed time period analysis
  - Full date format (mm/dd/yyyy) in hover tooltips

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
# Read from Freddie Mac's online source
uv run python pmms.py
```

This displays the first and last 5 rows of the dataset.

### Generate Visualization

```python
from pmms import read_pmms, plot_pmms

# Load data from Freddie Mac URL (default)
df = read_pmms('https://www.freddiemac.com/pmms/docs/historicalweeklydata.xlsx')

# Or from any local file or URL
df = read_pmms('path/to/your/file.xlsx')

# Create interactive plot
plot_pmms(df)  # Saves to pmms.html
```

Open `pmms.html` in a web browser to interact with the visualization.

## Data Source

The app reads data directly from Freddie Mac's Primary Mortgage Market Survey:
https://www.freddiemac.com/pmms/docs/historicalweeklydata.xlsx

This ensures you always have access to the most current mortgage rate data.

### Data Attribution

The mortgage rate data is provided by Freddie Mac and is subject to their terms of use. This software license (MIT) applies only to the code and visualization tools, not to the data itself. Users access the data directly from Freddie Mac's servers.

## Project Structure

```
pmms/
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

MIT License - see [LICENSE](LICENSE) file for details.

The software is licensed under MIT, but the mortgage rate data is provided by Freddie Mac and subject to their terms.
