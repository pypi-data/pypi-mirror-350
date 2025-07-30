import polars as pl
import plotly.graph_objects as go
from copy import deepcopy
import re

# Exposing it so anything that uses eval can convert
from .units import convert

def parse_keys(full_str: str, ):

    if ('{' and '}' not in full_str):
        return full_str

    keys =  re.findall(r"\{(.*?)\}", full_str)
    new_str = deepcopy(full_str)
    for key in keys:
        new_str = new_str.replace('{' + key + '}', f'pl.col("{key}")')
    
    return 'df.with_columns([( + ' + new_str + ').alias("' + full_str +'")])'


def graph_scatter_by_key(
    df: pl.DataFrame,
    x: str,
    y: str,
    x_title = None,
    y_title = '',
    title = '',
    color = None,
    mode = 'lines',
    group_name: str = None,
    options: dict = None,
    fig: go.Figure = None,
    axis = 1,
    theme = 'plotly_dark',
    alt_y_name = None,
):

    if options is None:
        options = {}

    if x_title is None:
        x_title = x

    if fig is None:
        fig = go.Figure()
    
    if alt_y_name is None:
        alt_y_name = y

    y_axis_info = dict(
        title=dict(text=y_title),
        anchor="free",
        overlaying="y",
        autoshift=True,
        side="left"
    )

    if color is not None:
        y_axis_info['color'] = color

    if y not in df:
        df_evaluated = eval(parse_keys(y))
    else:
        df_evaluated = df 

    # TODO: Fix these copies? 
    data = dict(
        x = df_evaluated[x].to_list(), 
        y = df_evaluated[y].to_list(),
        name = alt_y_name,
        mode = mode,
        legendgroup = group_name,
        legendgrouptitle_text = group_name,
        **options
    )

    if mode == 'lines':
        data['line'] = dict(color = color)
    elif mode == 'markers':
        data['marker'] = dict(color = color)
    elif mode == 'lines+markers':
        data['line'] = dict(color = color)
        data['marker'] = dict(color = color)

    if axis == 1:
        fig.add_trace(go.Scatter(
            **data
        ))
        fig.update_layout(yaxis=dict(title=dict(text=y_title)))
    elif axis == 2:
        fig.add_trace(go.Scatter(
            yaxis='y2',
            **data
        ))
        fig.update_layout(
            yaxis2=y_axis_info,
        )
    elif axis == 3:
        fig.add_trace(go.Scatter(
            yaxis='y3',
            **data
        ))
        fig.update_layout(
            yaxis3=y_axis_info,
        )
    elif axis == 4:
        fig.add_trace(go.Scatter(
            yaxis='y4',
            **data
        ))
        fig.update_layout(
            yaxis4=y_axis_info,
        )

    fig.update_xaxes(title = x_title)
    fig.update_layout(
        title = title,
        template = theme,
        showlegend = True,
        hovermode='x unified',
    )

    return fig

def graph_all(
    df: pl.DataFrame,
    x: str,
    x_title = None,
    y_title = '',
    title = '',
    color = None,
    mode = 'lines',
    group_name: str = None,
    options: dict = None,
    fig: go.Figure = None,
    axis = 1,
    theme = 'plotly_dark',
    alt_y_dict = None,
):
    keys = [key.name for key in df if key.name != x]

    if fig is None:
        fig = go.Figure()

    if alt_y_dict is None:
        alt_y_dict = {}

    for key in keys:
        graph_scatter_by_key(
            df = df,
            x = x,
            y = key,
            x_title = x_title,
            y_title = y_title,
            title = title,
            color = color,
            mode = mode,
            group_name = group_name,
            options = options,
            fig = fig,
            axis = axis,
            theme = theme,
            alt_y_name = alt_y_dict.get(key, key)
        )

    return fig