import logging

import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.subplots
from dash import Input, Output, callback, dcc, html, dash_table as dt
import dash_bootstrap_components as dbc

from .. import utils
from ..shared import STATUS2RGB
from . import data


logger = logging.getLogger('dashboard.queue')

# STATUS2EMO???


STATUSES = [
    'FAILED',
    'COMPLETE',
    'COMPLETED',
    'UPLOADING',
    'RUNNING',
    'PENDING',
    'WAITING',
    'QUEUED',
    'UNKNOWN',
]


def get_graph_content(df):
    status2rgb = {k: STATUS2RGB[k] for k in STATUSES}

    # Make a 1x1 figure
    fig = plotly.subplots.make_subplots(rows=1, cols=1)

    dfp = pd.pivot_table(
        df,
        index='PROCTYPE',
        values='LABEL',
        columns=['STATUS'],
        aggfunc='count',
        fill_value=0)

    for status, color in status2rgb.items():
        ydata = sorted(dfp.index)
        if status not in dfp:
            xdata = [0] * len(dfp.index)
        else:
            xdata = dfp[status]

        fig.append_trace(
            go.Bar(
                x=xdata,
                y=ydata,
                name='{} ({})'.format(status, sum(xdata)),
                marker=dict(color=color),
                opacity=0.9, orientation='h'),
            1,
            1
        )

    fig['layout'].update(barmode='stack', showlegend=True)

    graph = dcc.Graph(figure=fig)

    return dbc.Spinner(id="loading-queue-graph", children=[graph])


def get_content():
    COLUMNS = [
        'ID',
        'LABEL',
        'STATUS',
        'WALLTIME',
        'MEMREQ',
        'PROJECT',
        'PROCESSOR',
        'USER',
    ]

    columns = utils.make_columns(COLUMNS)

    # Format columns with links as markdown text
    for i, c in enumerate(columns):
        if c['name'] in ['ID']:
            columns[i]['type'] = 'text'
            columns[i]['presentation'] = 'markdown'

    content = [
        dbc.Row([
            dbc.Col(
                dbc.Button(
                    'Refresh Data',
                    id='button-queue-refresh',
                    outline=True,
                    color='primary',
                    size='sm',
                ),
            ),
            dbc.Col(
                dbc.Switch(
                    id='switch-queue-graph',
                    label='Graph',
                    value=False,
                ),
                align='center',
            ),
        ]),
        dbc.Row([
            dbc.Col(
                [
                    dbc.Stack([
                        dcc.Dropdown(
                            id='dropdown-queue-proj',
                            multi=True,
                            placeholder='Select Projects',
                        ),
                        dcc.Dropdown(
                            id='dropdown-queue-proc',
                            multi=True,
                            placeholder='Select Processing Types',
                        ),
                        dcc.Dropdown(
                            id='dropdown-queue-user',
                            multi=True,
                            placeholder='Select Users',
                        ),
                    ]),
                ],
                width=3
            ),
            dbc.Col(html.Div(id='container-queue-graph', children=[])),
        ]),
        dbc.Spinner(id="loading-queue-table", children=[
            dbc.Label('Loading...', id='label-queue-rowcount1'),
        ]),
        dt.DataTable(
            cell_selectable=False,
            columns=columns,
            data=[],
            page_action='none',
            sort_action='native',
            id='datatable-queue',
            style_cell={
                'textAlign': 'center',
                'padding': '5px 5px 0px 5px',
            #    'width': '30px',
            #    'overflow': 'hidden',
            #    'textOverflow': 'ellipsis',
            #    'height': 'auto',
            #    'minWidth': '40',
            #    'maxWidth': '60'
            },
            style_data_conditional=[
                {'if': {'column_id': 'LABEL'}, 'textAlign': 'left'},
            #    {'if': {'filter_query': '{STATUS} = "QUEUED"'},  'backgroundColor': STATUS2HEX['WAITING']},
            #    {'if': {'filter_query': '{STATUS} = "RUNNING"'},  'backgroundColor': STATUS2HEX['RUNNING']},
            #    {'if': {'filter_query': '{STATUS} = "WAITING"'},  'backgroundColor': STATUS2HEX['WAITING']},
            #    {'if': {'filter_query': '{STATUS} = "PENDING"'},  'backgroundColor': STATUS2HEX['PENDING']},
            #    {'if': {'filter_query': '{STATUS} = "UNKNOWN"'},  'backgroundColor': STATUS2HEX['UNKNOWN']},
            #    {'if': {'filter_query': '{STATUS} = "FAILED"'},   'backgroundColor': STATUS2HEX['FAILED']},
            #    {'if': {'filter_query': '{STATUS} = "COMPLETE"'}, 'backgroundColor': STATUS2HEX['COMPLETE']},
            #    {'if': {'column_id': 'STATUS', 'filter_query': '{STATUS} = ""'}, 'backgroundColor': 'white'}
            ],
            style_header={
                'fontWeight': 'bold',
                'padding': '5px 15px 0px 10px',
            },
            export_format='xlsx',
            export_headers='names',
            export_columns='visible',
        ),
        dbc.Label('Get ready...', id='label-queue-rowcount2'),
    ]

    return content


def load_data(refresh=False, hidedone=True):
    return data.load_data(refresh=refresh, hidedone=hidedone)


def load_options(df):
    options = {}

    for k in ['PROCTYPE', 'USER', 'PROJECT']:
        # Get a unique list of strings with blanks removed
        koptions = df[k].unique()
        koptions = [str(x) for x in koptions]
        koptions = [x for x in koptions if x]
        options[k] = sorted(koptions)

    return options


def filter_data(df, selected_proj, selected_proc, selected_user):
    return data.filter_data(
        df, selected_proj, selected_proc, selected_user)


@callback(
    [Output('dropdown-queue-proc', 'options'),
     Output('dropdown-queue-proj', 'options'),
     Output('dropdown-queue-user', 'options'),
     Output('datatable-queue', 'data'),
     Output('container-queue-graph', 'children'),
     Output('label-queue-rowcount1', 'children'),
     Output('label-queue-rowcount2', 'children'),
    ],
    [
     Input('dropdown-queue-proc', 'value'),
     Input('dropdown-queue-proj', 'value'),
     Input('dropdown-queue-user', 'value'),
     Input('switch-queue-graph', 'value'),
     Input('button-queue-refresh', 'n_clicks'),
    ]
)
def update_queue(
    selected_proc,
    selected_proj,
    selected_user,
    selected_graph,
    n_clicks
):
    refresh = False
    graph_content = []

    logger.debug('update_queue')

    # Load data
    if utils.was_triggered('button-queue-refresh'):
        # Refresh data if refresh button clicked
        logger.debug('queue refresh:clicks={}'.format(n_clicks))
        refresh = True

    logger.debug('loading data')
    df = load_data(refresh=refresh)

    # Update lists of possible options for dropdowns (could have changed)
    # make these lists before we filter what to display
    options = load_options(df)
    proj = utils.make_options(options['PROJECT'])
    proc = utils.make_options(options['PROCTYPE'])
    user = utils.make_options(options['USER'])

    # Filter data based on dropdown values
    df = filter_data(
        df,
        selected_proj,
        selected_proc,
        selected_user)

    if selected_graph:
        graph_content = get_graph_content(df)

    # Get the table data
    records = df.reset_index().to_dict('records')

    # Format records
    for r in records:
         # Make log a link
        _link = r['IDLINK']
        _text = r['ID']
        r['ID'] = f'[{_text}]({_link})'

    # Count how many rows are in the table
    if len(records) > 1:
        rowcount = '{} rows'.format(len(records))
    else:
        rowcount = ''

    return [proc, proj, user, records, graph_content, rowcount, rowcount]
