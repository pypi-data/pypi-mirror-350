import dash_bootstrap_components
from dash import html, dcc


def load_filter_table():
    """

    :param df:
    :return:
    """
    filter_elements = []

    # Liftover
    liftover = dcc.Dropdown(
        ["hg38/GRCh38", "hg19/GRCh37", "T2T/CHM13"], "hg38/GRCh38", style={"font-size":"14px"}
    )

    filter_elements.append(liftover)

    filter_table = dash_bootstrap_components.Row([
        dash_bootstrap_components.Col(
            html.Div(
                "Reference genome", style= {"font-size":"14px"})),
            dash_bootstrap_components.Col(
                filter_elements
            )
    ])
    return filter_table