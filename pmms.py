import argparse
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def read_pmms(filename):
    """
    Read PMMS data from an Excel file.

    Args:
        filename: Path to the Excel file

    Returns:
        DataFrame with 'date' and 'rate' columns, with disclaimer rows removed
    """
    df = pd.read_excel(
        filename,
        usecols=[0, 1],
        header=None,
        skiprows=7,
        names=['date', 'rate']
    )
    # Remove rows with missing rate values (disclaimers)
    df = df.dropna(subset=['rate'])
    return df


def plot_pmms(df, output_file='pmms.html'):
    """
    Plot PMMS rate data over time using Plotly with two subplots:
    1. Rate over time
    2. Quarterly rate changes

    Args:
        df: DataFrame with 'date' and 'rate' columns
        output_file: Path to save the HTML file (default: 'pmms.html')
    """
    # Ensure date column is datetime
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])

    # Calculate quarterly data (last rate of each quarter)
    df_quarterly = df.set_index('date').resample('QE')['rate'].last().reset_index()

    # Calculate quarter-over-quarter change
    df_quarterly['rate_change'] = df_quarterly['rate'].diff()

    # Create subplots with extra spacing to accommodate rangeslider
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Rate Over Time', 'Quarterly Rate Change'),
        vertical_spacing=0.32,
        row_heights=[0.52, 0.48]
    )

    # Add rate over time plot
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['rate'],
            mode='lines',
            name='Rate',
            line=dict(color='blue')
        ),
        row=1, col=1
    )

    # Add quarterly change plot with color based on positive/negative
    colors = ['green' if x >= 0 else 'red' for x in df_quarterly['rate_change'].fillna(0)]

    fig.add_trace(
        go.Bar(
            x=df_quarterly['date'],
            y=df_quarterly['rate_change'],
            name='Quarterly Change',
            marker=dict(color=colors)
        ),
        row=2, col=1
    )

    # Update layout
    fig.update_layout(
        title={
            'text': 'Freddie Mac PMMS<br><sub>30-Year Mortgage Rate</sub><br><br><br>',
            'x': 0.5,
            'xanchor': 'center'
        },
        hovermode='x unified',
        showlegend=True,
        height=950
    )

    # Adjust subplot title positions slightly downward to avoid overlap with subtitle
    for annotation in fig['layout']['annotations']:
        annotation['y'] = annotation['y'] - 0.005

    # Update axes
    fig.update_xaxes(title_text='Date', row=1, col=1, rangeslider=dict(visible=True))
    fig.update_xaxes(title_text='Date', row=2, col=1, rangeslider=dict(visible=True))
    fig.update_yaxes(title_text='Rate', row=1, col=1)
    fig.update_yaxes(title_text='Rate Change', row=2, col=1)

    fig.write_html(output_file)
    print(f"Plot saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read and display PMMS data from an Excel file")
    parser.add_argument("filename", help="Path to the Excel file")
    args = parser.parse_args()

    df = read_pmms(args.filename)

    print("Head of the data:")
    print(df.head())
    print("\nTail of the data:")
    print(df.tail())
