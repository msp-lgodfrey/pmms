import argparse
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from urllib.request import Request, urlopen
from io import BytesIO


def read_pmms(filename):
    """
    Read PMMS data from an Excel file or URL.

    Args:
        filename: Path to Excel file or URL (e.g., Freddie Mac's online data)

    Returns:
        DataFrame with 'date' and 'rate' columns, with disclaimer rows removed
    """
    # If it's a URL, download with proper headers to avoid 403 errors
    if filename.startswith('http://') or filename.startswith('https://'):
        req = Request(
            filename,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; PMMS-Reader/1.0)'}
        )
        with urlopen(req) as response:
            content = response.read()
            df = pd.read_excel(
                BytesIO(content),
                usecols=[0, 1],
                header=None,
                skiprows=7,
                names=['date', 'rate']
            )
    else:
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
    2. Rate changes (weekly, monthly, quarterly, or annual - selectable via dropdown)

    Args:
        df: DataFrame with 'date' and 'rate' columns
        output_file: Path to save the HTML file (default: 'pmms.html')
    """
    # Ensure date column is datetime
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df_indexed = df.set_index('date')

    # Calculate rate changes for different periods
    period_data = {}

    # Resample to different periods
    periods = {
        'Monthly': 'ME',
        'Quarterly': 'QE',
        'Annually': 'YE'
    }

    for name, resample_rule in periods.items():
        df_period = df_indexed.resample(resample_rule)['rate'].last().reset_index()
        df_period['rate_change'] = df_period['rate'].diff()
        period_data[name] = df_period

    # Create subplots with extra spacing to accommodate rangeslider
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('', 'Rate Change'),
        vertical_spacing=0.38,
        row_heights=[0.52, 0.48]
    )

    # Add rate over time plot
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['rate'],
            mode='lines',
            name='30-year rate',
            line=dict(color='blue')
        ),
        row=1, col=1
    )

    # Add rate change plots for each period
    for idx, (name, df_period) in enumerate(period_data.items()):
        colors = ['green' if x >= 0 else 'red' for x in df_period['rate_change'].fillna(0)]

        fig.add_trace(
            go.Bar(
                x=df_period['date'],
                y=df_period['rate_change'],
                name=f'{name} Change',
                marker=dict(color=colors),
                visible=(name == 'Quarterly'),  # Only quarterly visible by default
                showlegend=False  # Don't show in legend
            ),
            row=2, col=1
        )

    # Create dropdown menu for period selection
    buttons = []
    for idx, name in enumerate(period_data.keys()):
        # Calculate which traces should be visible
        # Trace 0 is the rate plot (always visible)
        # Traces 1-4 are the period change plots
        visible = [True] + [i == idx for i in range(len(period_data))]

        buttons.append(
            dict(
                label=name,
                method='update',
                args=[
                    {'visible': visible},
                    {'annotations[1].text': f'{name} Rate Change'}  # Update subplot title
                ]
            )
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
        height=950,
        updatemenus=[
            dict(
                buttons=buttons,
                direction='down',
                showactive=True,
                active=1,  # Quarterly is the 2nd item (index 1)
                x=1.02,
                xanchor='left',
                y=0.295,
                yanchor='top'
            )
        ]
    )

    # Adjust subplot title positions slightly downward to avoid overlap with subtitle
    for annotation in fig['layout']['annotations']:
        annotation['y'] = annotation['y'] - 0.005

    # Update axes
    fig.update_xaxes(title_text='Date', row=1, col=1, rangeslider=dict(visible=True))
    fig.update_xaxes(title_text='Date', row=2, col=1, rangeslider=dict(visible=True))
    fig.update_yaxes(title_text='Rate', row=1, col=1)
    fig.update_yaxes(title_text='Rate Change', row=2, col=1)

    # Add source attribution at the bottom
    fig.add_annotation(
        text='Data Source: Freddie Mac Primary Mortgage Market Survey',
        xref='paper',
        yref='paper',
        x=0.5,
        y=-0.05,
        xanchor='center',
        yanchor='top',
        showarrow=False,
        font=dict(size=10, color='gray')
    )

    fig.write_html(output_file)
    print(f"Plot saved to {output_file}")


if __name__ == "__main__":
    DEFAULT_URL = "https://www.freddiemac.com/pmms/docs/historicalweeklydata.xlsx"

    parser = argparse.ArgumentParser(
        description="Read and display PMMS data from Freddie Mac"
    )
    parser.add_argument(
        "filename",
        nargs='?',
        default=DEFAULT_URL,
        help=f"Path to Excel file or URL (default: {DEFAULT_URL})"
    )
    args = parser.parse_args()

    print(f"Reading data from: {args.filename}")
    df = read_pmms(args.filename)

    print("\nHead of the data:")
    print(df.head())
    print("\nTail of the data:")
    print(df.tail())
