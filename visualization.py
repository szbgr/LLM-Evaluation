import plotly.graph_objects as go
import pandas as pd


def get_color(rating):
    colors = [
        'rgba(135, 206, 250, 0.6)',  # Light blue for '1'
        'rgba(100, 149, 237, 0.6)',  # Blue for '2'
        'rgba(64, 224, 208, 0.6)',   # Turquoise for '3'
        'rgba(255, 156, 143, 0.6)',  # Light coral for '4'
        'rgba(255, 182, 193, 0.6)'   # Pink for '5'
    ]
    return colors[rating - 1]


def get_description(rating):
    descriptions = {
        1: 'Misinterpreted',
        2: 'Incorrect',
        3: 'Partially Correct',
        4: 'Mostly Correct',
        5: 'Completely Correct'
    }
    return descriptions[rating]


def extract_ratings(data):
    """Extract ratings from the data."""
    return [entry['rating'] for entry in data if 'rating' in entry]


def ratings_to_df(ratings, category_name):
    """Convert a list of ratings into a DataFrame with the specified category name as the column."""
    return pd.DataFrame(ratings, columns=[category_name])
def plot_data(ratings_df):
    fig = go.Figure()

    ratings = ratings_df.iloc[:, 0].dropna().astype(int)
    counts = ratings.value_counts().sort_index()

    # Total number of ratings, which will be used to calculate percentages
    total_ratings = len(ratings)

    # Initialize a list to keep track of the order of bars
    ordered_bars = []

    # Adding actual traces for the ratings
    for rating in [2, 1]:  # Reverse order for the negative side
        count = counts.get(rating, 0)
        percent = count / total_ratings * 100
        color = get_color(rating)

        # Append a trace for the negative side
        ordered_bars.append(go.Bar(
            x=[-percent],
            y=["Ratings"],
            name=f"{rating}: {get_description(rating)}",
            orientation='h',
            marker=dict(color=color),
            hoverinfo='text',
            hovertext=f"{rating}: {count} ({percent:.1f}%)",
        ))

    for rating in [3, 4, 5]:  # Keep the order for the positive side
        count = counts.get(rating, 0)
        percent = count / total_ratings * 100
        color = get_color(rating)

        # Append a trace for the positive side
        ordered_bars.append(go.Bar(
            x=[percent],
            y=["Ratings"],
            name=f"{rating}: {get_description(rating)}",
            orientation='h',
            marker=dict(color=color),
            hoverinfo='text',
            hovertext=f"{rating}: {count} ({percent:.1f}%)",
        ))

    # Add all traces to the figure in the correct order
    for bar in ordered_bars:
        fig.add_trace(bar)

    # Update layout
    fig.update_layout(
        barmode='relative',
        title='Ratings Distribution',
        xaxis=dict(title='Percentage', range=[-100, 100], tickvals=list(range(-100, 110, 10))),
        yaxis=dict(title='Ratings', showticklabels=False),
        plot_bgcolor='rgba(248, 248, 255, 0.6)',
        paper_bgcolor='rgba(248, 248, 255, 0.6)',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig
