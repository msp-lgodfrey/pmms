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
        DataFrame with 'date', 'rate_30yr', and 'rate_15yr' columns, with disclaimer rows removed
        Note: 15-year rates begin on 8/30/91
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
                usecols=[0, 1, 3],
                header=None,
                skiprows=7,
                names=['date', 'rate_30yr', 'rate_15yr']
            )
    else:
        df = pd.read_excel(
            filename,
            usecols=[0, 1, 3],
            header=None,
            skiprows=7,
            names=['date', 'rate_30yr', 'rate_15yr']
        )
    # Remove rows with missing 30-year rate values (disclaimers)
    df = df.dropna(subset=['rate_30yr'])
    return df


def plot_pmms(df, output_file='pmms.html'):
    """
    Plot PMMS rate data over time using Plotly with two subplots:
    1. Rate over time (30-year and 15-year)
    2. Rate changes (weekly, monthly, quarterly, or annual - selectable via dropdown)

    Args:
        df: DataFrame with 'date', 'rate_30yr', and 'rate_15yr' columns
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
        df_period = df_indexed.resample(resample_rule)[['rate_30yr', 'rate_15yr']].last().reset_index()
        df_period['rate_change_30yr'] = df_period['rate_30yr'].diff()
        df_period['rate_change_15yr'] = df_period['rate_15yr'].diff()
        period_data[name] = df_period

    # Create subplots with extra spacing to accommodate rangeslider
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Freddie Mac PMMS<br><sub>Mortgage Rates</sub>', 'Rate Change'),
        vertical_spacing=0.38,
        row_heights=[0.52, 0.48]
    )

    # Add rate over time plots for both 30-year and 15-year
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['rate_30yr'],
            mode='lines',
            name='30-year',
            line=dict(color='blue'),
            hovertemplate='30-year: %{y:.2f}%<extra></extra>'
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['rate_15yr'],
            mode='lines',
            name='15-year',
            line=dict(color='green'),
            hovertemplate='15-year: %{y:.2f}%<extra></extra>'
        ),
        row=1, col=1
    )

    # Add rate change plots for each period (both 30-year and 15-year)
    for idx, (name, df_period) in enumerate(period_data.items()):
        # 30-year changes
        colors_30yr = ['#0066cc' if x >= 0 else '#ff3333' for x in df_period['rate_change_30yr'].fillna(0)]

        fig.add_trace(
            go.Bar(
                x=df_period['date'],
                y=df_period['rate_change_30yr'],
                name='30-year',
                marker=dict(color=colors_30yr),
                visible=(name == 'Quarterly'),
                offsetgroup=0,
                showlegend=False
            ),
            row=2, col=1
        )

        # 15-year changes
        colors_15yr = ['#00aa00' if x >= 0 else '#cc0000' for x in df_period['rate_change_15yr'].fillna(0)]

        fig.add_trace(
            go.Bar(
                x=df_period['date'],
                y=df_period['rate_change_15yr'],
                name='15-year',
                marker=dict(color=colors_15yr),
                visible=(name == 'Quarterly'),
                offsetgroup=1,
                showlegend=False
            ),
            row=2, col=1
        )

    # Create dropdown menu for period selection
    buttons = []
    for idx, name in enumerate(period_data.keys()):
        # Calculate which traces should be visible
        # Traces 0-1 are the rate plots (always visible)
        # Traces 2+ are the period change plots (2 per period: 30yr and 15yr)
        visible = [True, True]  # Top plot traces always visible

        # Add visibility for each period's traces
        for i in range(len(period_data)):
            if i == idx:
                visible.extend([True, True])  # Show both 30yr and 15yr for selected period
            else:
                visible.extend([False, False])

        buttons.append(
            dict(
                label=name,
                method='update',
                args=[
                    {'visible': visible},
                    {'annotations[1].text': f'{name} Rate Change'}
                ]
            )
        )

    # Update layout
    fig.update_layout(
        hovermode='x unified',
        showlegend=True,
        height=1200,
        barmode='group',
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

    # Update axes with explicit range to show all data
    # Add a small buffer to ensure the last data point is fully visible
    date_buffer = pd.Timedelta(days=7)
    fig.update_xaxes(
        title_text='Date',
        row=1, col=1,
        rangeslider=dict(visible=True),
        hoverformat='%m/%d/%Y',
        range=[df['date'].min(), df['date'].max() + date_buffer]
    )
    fig.update_xaxes(
        title_text='Date',
        row=2, col=1,
        rangeslider=dict(visible=True),
        hoverformat='%m/%d/%Y'
    )
    fig.update_yaxes(title_text='Rate (%)', row=1, col=1)
    fig.update_yaxes(title_text='Rate Change (%)', row=2, col=1)

    # Add source attribution below the range slider
    fig.add_annotation(
        text='Data Source: Freddie Mac Primary Mortgage Market Survey',
        xref='paper',
        yref='paper',
        x=0.5,
        y=-0.33,
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

    print("\nGenerating plot...")
    plot_pmms(df)
