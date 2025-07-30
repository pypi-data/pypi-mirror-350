"""Creates report PDF with zip."""
import logging
import io
import re
import os
import shutil
import itertools
from datetime import datetime, date, timedelta
import tempfile
import math

import numpy as np
import pydot
import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.subplots
import plotly.express as px
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from PIL import Image


logger = logging.getLogger('garjus.progress.report')


# These are used to set colors of graphs
RGB_DKBLUE = 'rgb(59,89,152)'
RGB_BLUE = 'rgb(66,133,244)'
RGB_GREEN = 'rgb(15,157,88)'
RGB_YELL = 'rgb(244,160,0)'
RGB_RED = 'rgb(219,68,55)'
RGB_PURP = 'rgb(160,106,255)'
RGB_GREY = 'rgb(200,200,200)'
RGB_PINK = 'rgb(255,182,193)'
RGB_LIME = 'rgb(17, 180, 101)'

# Give each status a color to display
QASTATUS2COLOR = {
    'PASS': RGB_GREEN,
    'NQA': RGB_LIME,
    'NPUT': RGB_YELL,
    'FAIL': RGB_RED,
    'NONE': RGB_GREY,
    'JOBF': RGB_PINK,
    'JOBR': RGB_BLUE}

STATUS2RGB = dict(zip(
    ['WAITING', 'PENDING', 'RUNNING', 'COMPLETE', 'FAILED', 'UNKNOWN', 'JOBF'],
    [RGB_GREY, RGB_YELL, RGB_GREEN, RGB_BLUE, RGB_RED, RGB_PURP, RGB_PINK]))

# These are used to make progress reports
ASTATUS2COLOR = {
    'PASS': RGB_GREEN,
    'NPUT': RGB_YELL,
    'FAIL': RGB_RED,
    'NQA': RGB_LIME,
    'NONE': RGB_GREY,
    'COMPLETE': RGB_BLUE,
    'UNKNOWN': RGB_PURP}

SESSCOLS = ['SESSION', 'SUBJECT', 'PROJECT', 'DATE', 'SESSTYPE', 'SITE', 'MODALITY']

HIDECOLS = [
    'assessor_label',
    'PROJECT',
    'SESSION',
    'SUBJECT',
    'AGE',
    'SEX',
    'DEPRESS',
    'TYPE',
    'SITE',
    'SESSTYPE',
    'DATE',
    'ASSR',
    'PROCSTATUS',
    'QCSTATUS',
    'INPUTS',
    'MODALITY',
    'XSITYPE',
    'PROCTYPE',
    'full_path',
    'case',
]

ACOLS = [
    'ASSR',
    'PROJECT',
    'SUBJECT',
    'SESSION',
    'SESSTYPE',
    'SITE',
    'DATE',
    'PROCTYPE',
]


class MYPDF(FPDF):
    """Custom PDF."""

    def set_filename(self, filename):
        """Set the filename."""
        self.filename = filename

    def set_project(self, project, enable_monthly=False):
        """Set the project name."""
        self.project = project
        today = datetime.now().strftime("%Y-%m-%d")
        self.date = today

        if enable_monthly:
            self.title = f'{project} Monthly Report'
            self.subtitle = '{}'.format(datetime.now().strftime("%B %Y"))
        else:
            self.title = f'{project} Report'
            self.subtitle = '{}'.format(datetime.now().strftime("%B %d, %Y"))
            

    def footer(self):
        """Return the custom footer."""
        self.set_y(-0.35)
        self.set_x(0.5)

        # Write date, title, page number
        self.set_font('helvetica', size=10)
        self.set_text_color(100, 100, 100)
        self.set_draw_color(100, 100, 100)
        self.line(x1=0.2, y1=10.55, x2=8.3, y2=10.55)
        self.cell(w=1, text=self.date)
        self.cell(w=5, align='C', text=self.title)
        self.cell(w=2.5, align='C', text=str(self.page_no()))


def blank_letter():
    """Blank letter sized PDF."""
    p = MYPDF(orientation="P", unit='in', format='letter')
    p.set_top_margin(0.5)
    p.set_left_margin(0.5)
    p.set_right_margin(0.5)

    return p


def _draw_counts(pdf, sessions, rangetype=None, groupby='site'):
    # Counts of each session type with sums
    # sessions column names are: SESSION, PROJECT, DATE, SESSTYPE, SITE
    type_list = sessions.SESSTYPE.unique()
    site_list = sorted(sessions.SITE.unique())
    group_list = sessions.GROUP.unique()
    indent_width = max(2.5 - len(type_list) * 0.5, 0.3)

    # Get the data
    df = sessions.copy()

    if rangetype == 'lastmonth':
        pdf.set_fill_color(114, 172, 77)

        # Get the dates of lst month
        _end = date.today().replace(day=1) - timedelta(days=1)
        _start = date.today().replace(day=1) - timedelta(days=_end.day)

        # Get the name of last month
        lastmonth = _start.strftime("%B")

        # Filter the data to last month
        df = df[df.DATE >= _start.strftime('%Y-%m-%d')]
        df = df[df.DATE <= _end.strftime('%Y-%m-%d')]

        # Create the lastmonth header
        _txt = 'Session Counts ({})'.format(lastmonth)

    else:
        pdf.set_fill_color(94, 156, 211)
        _txt = 'Session Counts (all)'

    # Draw heading
    pdf.set_font('helvetica', size=14)
    pdf.cell(w=7.5, h=0.5, text=_txt, align='C', border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Header Formatting
    pdf.cell(w=1.0)
    pdf.set_text_color(245, 245, 245)
    pdf.set_line_width(0.01)
    _kwargs = {'w': 1.0, 'h': 0.7, 'border': 1, 'align': 'C', 'fill': True}

    # Column header for each type
    pdf.cell(indent_width)
    for cur_type in type_list:
        _txt = cur_type
        if len(_txt) > 6:
            pdf.set_font('helvetica', size=12)

        pdf.cell(**_kwargs, text=_txt)

    # Got to next line
    pdf.ln()

    # Row formatting
    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(0, 0, 0)
    _kwargs = {'w': 1.0, 'h': 0.5, 'border': 1, 'align': 'C', 'fill': False}
    _kwargs_s = {'w': 1.0, 'h': 0.5, 'border': 1, 'align': 'C', 'fill': False}
    _kwargs_t = {'w': 0.7, 'h': 0.5, 'border': 1, 'align': 'C', 'fill': False}

    pdf.set_font('helvetica', size=18)

    if groupby == 'site':

        # Row for each site
        for cur_site in site_list:
            pdf.cell(w=indent_width)

            dfs = df[df.SITE == cur_site]
            _txt = cur_site

            if len(_txt) > 9:
                pdf.set_font('helvetica', size=11)

            pdf.cell(**_kwargs_s, text=_txt)

            pdf.set_font('helvetica', size=18)

            # Count each type for this site
            for cur_type in type_list:
                cur_count = str(len(dfs[dfs.SESSTYPE == cur_type]))
                pdf.cell(**_kwargs, text=cur_count)

            if len(type_list) > 1:
                # Total for site
                cur_count = str(len(dfs))
                pdf.cell(**_kwargs_t, text=cur_count, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            else:
                pdf.cell(**{'w': 1.0, 'h': 0.5, 'border': 0}, text='', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        if len(site_list) > 1:
            # TOTALS row
            pdf.cell(w=indent_width)
            pdf.cell(w=1.0)
            for cur_type in type_list:
                pdf.set_font('helvetica', size=18)
                cur_count = str(len(df[df.SESSTYPE == cur_type]))
                pdf.cell(**_kwargs, text=cur_count)

            # Grandtotal
            pdf.cell(**_kwargs_t, text=str(len(df)))

    else:
        # Row for each group
        for cur_group in group_list:
            pdf.cell(w=indent_width)

            dfg = df[df.GROUP == cur_group]

            # Show the group
            _txt = cur_group

            if len(_txt) > 6:
                pdf.set_font('helvetica', size=12)

            pdf.cell(**_kwargs_s, text=_txt)

            # Count each type for this group
            pdf.set_font('helvetica', size=18)
            for cur_type in type_list:
                cur_count = str(len(dfg[dfg.SESSTYPE == cur_type]))
                pdf.cell(**_kwargs, text=cur_count)

            if len(type_list) > 1:
                # Total for group
                cur_count = str(len(dfg))
                pdf.cell(**_kwargs_t, text=cur_count, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            else:
                #pdf.cell(w=0, h=0, border=0, text='', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.ln()

        if len(group_list) > 1:
            # TOTALS row
            pdf.cell(w=indent_width)
            pdf.cell(w=1.0)
            for cur_type in type_list:
                pdf.set_font('helvetica', size=18)
                cur_count = str(len(df[df.SESSTYPE == cur_type]))
                pdf.cell(**_kwargs, text=cur_count)

            # Grandtotal
            if len(type_list) > 1:
                pdf.cell(**_kwargs_t, text=str(len(df)))

    # End by going to next line
    pdf.ln()

    return pdf

def _exclude_maps(scantypes):
    return [x for x in scantypes if not 'FIELDMAP' in x.replace('_', '').upper() and not 'FSA' in x.replace('_', '').upper()]

def _draw_scan_counts(pdf, scans, groupby='site'):
    # Counts of each scan type by sess type by site/group
    scantypes = sorted(scans.SCANTYPE.unique())
    sesstypes = sorted(scans.SESSTYPE.unique())
    sitetypes = sorted(scans.SITE.unique())
    grouptypes = sorted(scans.GROUP.unique())

    scantypes = _exclude_maps(scantypes)

    if groupby == 'site':
        indent_width = max(2.0 - len(sitetypes) * 0.5, 0.3)
    else:
        indent_width = max(2.0 - len(grouptypes) * 0.5, 0.3)

    # Get the data
    df = scans.copy()

    pdf.set_fill_color(94, 156, 211)
    _txt = 'Scan Counts'

    # Draw heading
    pdf.set_font('helvetica', size=14)
    pdf.cell(w=7.5, h=0.5, text=_txt, align='C', border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Header Formatting
    pdf.cell(w=1.0)
    pdf.set_text_color(245, 245, 245)
    pdf.set_line_width(0.01)

    if len(sitetypes) > 4:
        _kwargs = {'w': 0.5, 'h': 0.5, 'border': 1, 'align': 'C', 'fill': True}
    else:
        _kwargs = {'w': 1.0, 'h': 0.5, 'border': 1, 'align': 'C', 'fill': True}

    # Column header for each type 

    if groupby == 'site':
        if len(sitetypes) > 4:
            pdf.cell(w=indent_width + 1.2)
        else:
            pdf.cell(w=indent_width + 2.0)

        for cur_type in sitetypes:
            _txt = cur_type
            if len(_txt) > 6:
                pdf.set_font('helvetica', size=12)

            if len(sitetypes) > 4:
                _txt = _txt[:4]

            pdf.cell(**_kwargs, text=_txt)
    
    else:
        pdf.cell(w=indent_width + 2.0)

        for cur_type in grouptypes:
            _txt = cur_type
            if len(_txt) > 6:
                pdf.set_font('helvetica', size=12)

            pdf.cell(**_kwargs, text=cur_type)

    # Next line
    pdf.ln()

    # Row formatting
    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(0, 0, 0)

    if len(sitetypes) > 4:
        _kwargs = {'w': 0.5, 'h': 0.4, 'border': 1, 'align': 'C', 'fill': False}
        _kwargs_s = {'w': 0.5, 'h': 0.4, 'border': 1, 'align': 'C', 'fill': False}
        _kwargs_x = {'w': 1.5, 'h': 0.4, 'border': 1, 'align': 'C', 'fill': False}
        _kwargs_t = {'w': 0.7, 'h': 0.4, 'border': 1, 'align': 'C', 'fill': False}
    else:
        _kwargs = {'w': 1.0, 'h': 0.4, 'border': 1, 'align': 'C', 'fill': False}
        _kwargs_s = {'w': 1.0, 'h': 0.4, 'border': 1, 'align': 'C', 'fill': False}
        _kwargs_x = {'w': 2.0, 'h': 0.4, 'border': 1, 'align': 'C', 'fill': False}
        _kwargs_t = {'w': 1.0, 'h': 0.4, 'border': 1, 'align': 'C', 'fill': False}

    pdf.set_font('helvetica', size=12)

    # First grouping by scan type
    #print(f'{indent_width=}')
    for cur_scan in scantypes:
        # Reset our cursor and indent
        pdf.cell(**{'w': 0, 'h': 0, 'border': 0}, text='', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(w=(indent_width))

        # Show the scan type
        pdf.set_font('helvetica', size=12, style='B')
        _txt = cur_scan
        pdf.cell(**_kwargs_x, text=_txt)

        # Row for each session type
        for cur_sess in sesstypes:
            # Show the session type
            pdf.set_font('helvetica', size=12)
            _txt = cur_sess
            #pdf.cell(**_kwargs_s, text=_txt)
            pdf.cell(**_kwargs_t, text=_txt)

            pdf.set_font('helvetica', size=16)
            if groupby == 'site':
                # Show count for each site
                for cur_site in sitetypes:
                    _txt = str(len(df[(df.SESSTYPE == cur_sess) & (df.SCANTYPE == cur_scan) & (df.SITE == cur_site)]))
                    pdf.cell(**_kwargs_s, text=_txt)
            else:
                # Show count for each group
                for cur_group in grouptypes:
                    _txt = str(len(df[(df.SESSTYPE == cur_sess) & (df.SCANTYPE == cur_scan) & (df.GROUP == cur_group)]))
                    pdf.cell(**_kwargs, text=_txt)

            # Fill then next line and indent
            pdf.cell(**{'w': 1.0, 'h': 0.4, 'border': 0}, text='', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            if len(sitetypes) > 4:
                pdf.cell(w=indent_width + 1.5)
            else:
                pdf.cell(w=indent_width + 2.0)

    # End by going to next line
    pdf.ln()

    return pdf


def plot_timeline(df, startdate=None, enddate=None):
    """Plot timeline of data."""
    palette = itertools.cycle(px.colors.qualitative.Plotly)
    type_list = df.SESSTYPE.unique()
    mod_list = df.MODALITY.unique()
    fig = plotly.subplots.make_subplots(rows=1, cols=1)
    fig.update_layout(margin=dict(l=40, r=40, t=40, b=40))

    for mod, sesstype in itertools.product(mod_list, type_list):
        # Get subset for this session type
        dfs = df[(df.SESSTYPE == sesstype) & (df.MODALITY == mod)]
        if dfs.empty:
            continue

        # Advance color here, before filtering by time
        _color = next(palette)

        if startdate:
            dfs = dfs[dfs.DATE >= startdate.strftime('%Y-%m-%d')]

        if enddate:
            dfs = dfs[dfs.DATE <= enddate.strftime('%Y-%m-%d')]

        # Nothing to plot so go to next session type
        if dfs.empty:
            logger.debug('nothing to plot:{}:{}'.format(mod, sesstype))
            continue

        # markers symbols, see https://plotly.com/python/marker-style/
        if mod == 'MR':
            symb = 'circle-dot'
        elif mod == 'PET':
            symb = 'diamond-wide-dot'
        else:
            symb = 'diamond-tall-dot'

        # Convert hex to rgba with alpha of 0.5
        if _color.startswith('#'):
            _rgba = 'rgba({},{},{},{})'.format(
                int(_color[1:3], 16),
                int(_color[3:5], 16),
                int(_color[5:7], 16),
                0.7)
        else:
            _r, _g, _b = _color[4:-1].split(',')
            _a = 0.7
            _rgba = 'rgba({},{},{},{})'.format(_r, _g, _b, _a)

        # Plot this session type
        try:
            _row = 1
            _col = 1
            fig.append_trace(
                go.Box(
                    name='{} {} ({})'.format(sesstype, mod, len(dfs)),
                    x=dfs['DATE'],
                    y=dfs['SITE'],
                    boxpoints='all',
                    jitter=0.7,
                    text=dfs['SESSION'],
                    pointpos=0.5,
                    orientation='h',
                    marker={
                        'symbol': symb,
                        'color': _rgba,
                        'size': 12,
                        'line': dict(width=2, color=_color)
                    },
                    line={'color': 'rgba(0,0,0,0)'},
                    fillcolor='rgba(0,0,0,0)',
                    hoveron='points',
                ),
                _row,
                _col)
        except Exception as err:
            logger.error(err)
            return None

    # show lines so we can better distinguish categories
    fig.update_yaxes(showgrid=True)

    # Set the size
    fig.update_layout(width=900)

    # Export figure to image
    _png = fig.to_image(format="png")
    image = Image.open(io.BytesIO(_png))
    return image


def plot_activity(df, pivot_index):
    """Plot activity data."""
    status2rgb = ASTATUS2COLOR

    fig = plotly.subplots.make_subplots(rows=1, cols=1)
    fig.update_layout(margin=dict(l=40, r=40, t=40, b=40))

    # Draw bar for each status, these will be displayed in order
    dfp = pd.pivot_table(
        df, index=pivot_index, values='ID', columns=['STATUS'],
        aggfunc='count', fill_value=0)

    for status, color in status2rgb.items():
        ydata = sorted(dfp.index)
        if status not in dfp:
            xdata = [0] * len(dfp.index)
        else:
            xdata = dfp[status]

        fig.append_trace(go.Bar(
            x=ydata,
            y=xdata,
            name='{} ({})'.format(status, sum(xdata)),
            marker=dict(color=color),
            opacity=0.9), 1, 1)

    # Customize figure
    fig['layout'].update(barmode='stack', showlegend=True, width=900)

    # Export figure to image
    _png = fig.to_image(format="png")
    image = Image.open(io.BytesIO(_png))
    return image


def _add_count_pages(pdf, sessions, enable_monthly=False, groupby='site'):
    mr_sessions = sessions[sessions.MODALITY == 'MR'].copy()

    # Start the page with titles
    pdf.add_page()
    pdf.set_font('helvetica', size=22)
    pdf.cell(w=7.5, h=0.4, align='C', text=pdf.title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(w=7.5, h=0.4, align='C', text=pdf.subtitle, border='B', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(0.25)

    # Show all MRI session counts
    pdf.set_font('helvetica', size=18)
    pdf.cell(w=7.5, h=0.4, align='C', text=f'MRI by {groupby}')
    pdf.ln(0.25)
    _draw_counts(pdf, mr_sessions, groupby=groupby)
    pdf.ln(1)

    if enable_monthly:
        if len(mr_sessions.SITE.unique()) > 3:
            # Start a new page so it fits
            pdf.add_page()

        # Show MRI session counts in date range
        pdf.cell(w=7.5, h=0.4, align='C', text='MRI')
        pdf.ln(0.25)
        _draw_counts(pdf, mr_sessions, rangetype='lastmonth', groupby=groupby)
        pdf.ln(1)
        pdf.add_page()

    # Add other Modalities, counts for each session type
    logger.debug('adding other counts')
    _add_others(pdf, sessions, enable_monthly=enable_monthly, groupby=groupby)

    return pdf

def _add_scan_count_pages(pdf, scans, groupby='site'):
    mr_scans = scans[scans.MODALITY == 'MR'].copy()

    # Start the page
    pdf.add_page()

    # Show all MRI scan counts
    pdf.set_font('helvetica', size=18)
    pdf.cell(w=7.5, h=0.4, align='C', text=f'MRI by {groupby}')
    pdf.ln(0.25)
    _draw_scan_counts(pdf, mr_scans, groupby=groupby)
    pdf.ln(1)

    return pdf


def _add_graph_page(pdf, info):
    scantypes = info['scantypes']
    proctypes = info['proctypes']

    pdf.add_page()
    pdf.set_font('helvetica', size=18)
    pdf.cell(w=7.5, align='C', text='Processing Graph', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('helvetica', size=9)

    # MR Scan are orange
    pdf.set_fill_color(255, 166, 0)
    pdf.cell(h=0.3, text='MR Scan', fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # PET Scan are chocolate
    pdf.set_fill_color(210, 105, 30)
    pdf.cell(h=0.3, text='PET Scan', fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # EDAT are pink
    pdf.set_fill_color(238, 130, 238)
    pdf.cell(h=0.3, text='EDAT', fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Processing with stats are green
    pdf.set_fill_color(144, 238, 144)
    pdf.cell(h=0.3, text='Processing with stats', fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Processing without stats are blue
    pdf.set_fill_color(173, 216, 230)
    pdf.cell(h=0.3, text='Processing without stats', fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(0.5)

    # Build the graph
    graph = pydot.Dot(graph_type='digraph')
    graph.set_node_defaults(
        color='lightblue',
        style='filled',
        shape='box',
        fontname='Courier',
        fontsize='12')

    for scan in scantypes:
        if scan == 'CTAC':
            if 'FEOBVQA_v2' in proctypes:
                graph.add_node(pydot.Node('FEOBV', color='chocolate'))

            if 'AMYVIDQA_v2' in proctypes:
                graph.add_node(pydot.Node('AMYVID', color='chocolate'))
        else:
            graph.add_node(pydot.Node(scan, color='orange'))

    print(proctypes)

    if 'centiloids_pib_v1' in proctypes:
        graph.add_node(pydot.Node('PiB', color='chocolate'))
        graph.add_node(pydot.Node('AMYLOIDQA_v4', color='lightgreen'))
        graph.add_node(pydot.Node('centiloids_pib_v1', color='lightgreen'))
        graph.add_edge(pydot.Edge('PiB', 'AMYLOIDQA_v4'))
        graph.add_edge(pydot.Edge('FS7_v1', 'AMYLOIDQA_v4'))
        graph.add_edge(pydot.Edge('PiB', 'centiloids_pib_v1'))
        graph.add_edge(pydot.Edge('T1', 'centiloids_pib_v1'))

    if 'fMRI_NBACK' in scantypes:
        graph.add_node(pydot.Node('NBACK', color='violet'))

    if 'NMQA_v1' in proctypes:
        graph.add_node(pydot.Node('NMQA_v1', color='lightblue'))
        graph.add_edge(pydot.Edge('NM', 'NMQA_v1'))
        graph.add_edge(pydot.Edge('T1', 'NMQA_v1'))

    if 'fMRI_EEfRT1' in scantypes:
        graph.add_node(pydot.Node('EEfRT', color='violet'))
        graph.add_node(pydot.Node('fmriqa_v4', color='lightgreen'))
        graph.add_edge(pydot.Edge('fMRI_EEfRT1', 'fmriqa_v4'))
        graph.add_edge(pydot.Edge('fMRI_EEfRT2', 'fmriqa_v4'))
        graph.add_edge(pydot.Edge('fMRI_EEfRT3', 'fmriqa_v4'))

    if 'fMRI_MIDT1' in scantypes:
        graph.add_node(pydot.Node('MIDT', color='violet'))
        graph.add_edge(pydot.Edge('fMRI_MIDT1', 'fmriqa_v4'))
        graph.add_edge(pydot.Edge('fMRI_MIDT2', 'fmriqa_v4'))

    # Default proctypes
    graph.add_node(pydot.Node('FS7_v1', color='lightgreen'))
    graph.add_node(pydot.Node('FS7HPCAMG_v1', color='lightgreen'))
    graph.add_node(pydot.Node('LST_v1', color='lightgreen'))
    graph.add_node(pydot.Node('SAMSEG_v1', color='lightgreen'))
    graph.add_node(pydot.Node('DnSeg_v1', color='lightgreen'))
    graph.add_node(pydot.Node('FS7sclimbic_v0', color='lightgreen'))
    graph.add_node(pydot.Node('FS7hypothal_v1', color='lightgreen'))

    graph.add_edge(pydot.Edge('T1', 'DnSeg_v1'))
    graph.add_edge(pydot.Edge('T1', 'LST_v1'))
    graph.add_edge(pydot.Edge('T1', 'FS7_v1'))
    graph.add_edge(pydot.Edge('FS7_v1', 'SAMSEG_v1'))
    graph.add_edge(pydot.Edge('FS7_v1', 'FS7HPCAMG_v1'))
    graph.add_edge(pydot.Edge('FLAIR', 'LST_v1'))
    graph.add_edge(pydot.Edge('FLAIR', 'SAMSEG_v1'))
    graph.add_edge(pydot.Edge('FS7_v1', 'FS7sclimbic_v0'))
    graph.add_edge(pydot.Edge('FS7_v1', 'FS7hypothal_v1'))

    if 'fmri_msit_v4' in proctypes:
        graph.add_node(pydot.Node('EDAT', color='violet'))
        graph.add_edge(pydot.Edge('EDAT', 'fmri_msit_v4'))
        graph.add_edge(pydot.Edge('T1', 'fmri_msit_v4'))
        graph.add_node(pydot.Node('fmri_msit_v4', color='lightgreen'))
        graph.add_edge(pydot.Edge('fMRI_MSIT', 'fmri_msit_v4'))

    if 'fmri_bct_v2' in proctypes:
        graph.add_node(pydot.Node('struct_preproc_v1', color='lightgreen'))
        graph.add_edge(pydot.Edge('T1', 'struct_preproc_v1'))
        graph.add_edge(pydot.Edge('FLAIR', 'struct_preproc_v1'))
        graph.add_edge(pydot.Edge('struct_preproc_v1', 'fmri_rest_v4'))
        graph.add_edge(pydot.Edge('fMRI_REST1', 'fmri_rest_v4'))
        graph.add_edge(pydot.Edge('fMRI_REST2', 'fmri_rest_v4'))
        graph.add_edge(pydot.Edge('fmri_rest_v4', 'fmri_roi_v2'))
        graph.add_edge(pydot.Edge('fmri_roi_v2', 'fmri_bct_v2'))
        graph.add_node(pydot.Node('fmri_bct_v2', color='lightgreen'))

    if 'struct_preproc_noflair_v1' in proctypes:
        graph.add_edge(pydot.Edge(
            'struct_preproc_noflair_v1', 'fmri_rest_v4', style='dashed'))
        graph.add_edge(pydot.Edge(
            'T1', 'struct_preproc_noflair_v1', style='dashed'))

    if 'BFC_v2' in proctypes:
        graph.add_edge(pydot.Edge('T1', 'BFC_v2'))
        graph.add_node(pydot.Node('BFC_v2', color='lightgreen'))

    if 'FEOBVQA_v2' in proctypes:
        graph.add_edge(pydot.Edge('FEOBV', 'FEOBVQA_v2'))
        graph.add_edge(pydot.Edge('FS7_v1', 'FEOBVQA_v2'))
        graph.add_node(pydot.Node('FEOBVQA_v2', color='lightgreen'))

    if 'AMYVIDQA_v2' in proctypes:
        graph.add_edge(pydot.Edge('AMYVID', 'AMYVIDQA_v2'))
        graph.add_edge(pydot.Edge('FS7_v1', 'AMYVIDQA_v2'))
        graph.add_node(pydot.Node('AMYVIDQA_v2', color='lightgreen'))

    if 'BrainAgeGap_v2' in proctypes:
        graph.add_node(pydot.Node('Multi_Atlas_v3', color='lightgreen'))
        graph.add_node(pydot.Node('BrainAgeGap_v2', color='lightgreen'))
        graph.add_edge(pydot.Edge('T1', 'Multi_Atlas_v3'))
        graph.add_edge(pydot.Edge('Multi_Atlas_v3', 'BrainAgeGap_v2'))

    if 'dtiQA_synb0_v7' in proctypes:
        graph.add_node(pydot.Node('dtiQA_synb0_v7', color='lightgreen'))
        graph.add_node(pydot.Node('francois_schaefer200_v1', color='lightblue'))
        graph.add_edge(pydot.Edge('T1', 'dtiQA_synb0_v7'))
        graph.add_edge(pydot.Edge('DTI_2min_b1000', 'dtiQA_synb0_v7'))
        graph.add_edge(pydot.Edge('DTI_2min_b2000', 'dtiQA_synb0_v7'))
        graph.add_edge(pydot.Edge('dtiQA_synb0_v7', 'francois_schaefer200_v1'))
        graph.add_edge(pydot.Edge('FS7_v1', 'francois_schaefer200_v1'))

    # Make the graph, draw to pdf
    image = Image.open(io.BytesIO(graph.create_png()))
    pdf.image(image, x=0.5, y=3, w=7.5)

    return pdf


def _add_others(pdf, sessions, enable_monthly=False, groupby='site'):
    # Get non-MRI sessions
    other_sessions = sessions[sessions.MODALITY != 'MR'].copy()

    if len(other_sessions) == 0:
        logger.debug('no other modalities sessions, skipping page')
        return

    # Show all session counts
    pdf.set_font('helvetica', size=18)
    pdf.cell(w=7.5, h=0.4, align='C', text=f'Other Modalities by {groupby}')
    pdf.ln(0.25)
    _draw_counts(pdf, other_sessions, groupby=groupby)
    pdf.ln(1)

    if enable_monthly:
        # Show session counts in date range
        pdf.cell(w=7.5, h=0.4, align='C', text='Other Modalities')
        pdf.ln(0.25)
        _draw_counts(pdf, other_sessions, rangetype='lastmonth', groupby=groupby)
        pdf.ln(1)

    return pdf


def _add_wml_page(pdf, info):

    # Transform the data to row per session with columsn for LST, SAMSEG wml
    stats = info['stats']

    if stats.empty:
        logger.info('no stats found')
        return

    lst_data = stats[stats.PROCTYPE == 'LST_v1']
    sam_data = stats[stats.PROCTYPE == 'SAMSEG_v1']

    if lst_data.empty:
        logger.info('no LST data')
        return

    if sam_data.empty:
        logger.info('no SAMSEG data')
        return

    df = pd.merge(lst_data, sam_data, left_on='SESSION', right_on='SESSION')

    pdf.add_page()
    pdf.cell(text='LST vs SAMSEG', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    fig = plotly.subplots.make_subplots(rows=1, cols=1)

    fig.append_trace(
        go.Scatter(
            x=df['wml_volume_x'].astype(float),
            y=df['samseg_lesions_y'].astype(float) / 1000.0,
            mode='markers',
        ), 1, 1)

    _max = max(
        df['wml_volume_x'].astype(float).max(),
        df['samseg_lesions_y'].astype(float).max() / 1000.0,
    )
    _max = max(_max, 50)

    fig.add_trace(
        go.Scatter(
            x=[0, _max],
            y=[0, _max],
            mode='lines',
            name='',
            line_color='grey'), 1, 1)

    fig.update_yaxes(autorange=True)
    fig.update_layout(showlegend=False)
    fig.update_layout(
        xaxis_title="LST wml (mL)",
        yaxis_title="SAMSEG lesions (mL)")

    # Draw to figure as image on PDF
    _image = Image.open(io.BytesIO(fig.to_image(format="png")))
    pdf.image(_image, x=0.75, w=7)

    return pdf


def _add_stats_fmriqa(pdf, stats, info):
    # get the stats data by scan type using inputs field to map to scan

    scans = info['scans']

    assessors = info['assessors'].copy()
    assessors = assessors[assessors.PROCTYPE == 'fmriqa_v4']

    # Extract scan fmri value into a column
    assessors['scan_fmri'] = assessors.apply(
        lambda row: row['INPUTS'].get('scan_fmri'), axis=1)

    df = pd.merge(
        assessors[['ASSR', 'scan_fmri']],
        scans[['full_path', 'SCANTYPE']],
        how='inner',
        left_on='scan_fmri',
        right_on='full_path')

    df = pd.merge(
        stats,
        df[['ASSR', 'SCANTYPE']],
        how='inner',
        left_on='ASSR',
        right_on='ASSR')

    for t in sorted(df.SCANTYPE.unique()):
        if t in ['fMRI_rest', 'fMRI_REST_FSA']:
            continue

        pdf.set_font('helvetica', size=10)
        _add_stats(pdf, df[df.SCANTYPE == t], plot_title=f'Scan Type: {t}')


def _add_stats(pdf, stats, plot_title=None):

    # this returns a PIL Image object
    image = plot_stats(stats, plot_title)
    tot_width, tot_height = image.size

    # Split horizontal image into chunks of width to fit on
    # letter-sized page with crop((left, top, right, bottom))
    chunk_h = 500
    chunk_w = 998
    rows_per_page = 3  # 3 rows per page
    page_count = math.ceil(tot_width / (rows_per_page * chunk_w))

    for p in range(page_count):
        for c in range(rows_per_page):
            # Calculate the starting x for this chunk
            chunk_x = (c * chunk_w) + (p * chunk_w * rows_per_page)
            if chunk_x > tot_width - 10:
                # out of bounds
                continue

            # Get the image from the cropped section
            _img = image.crop((chunk_x, 0, chunk_x + chunk_w, chunk_h))

            # Draw the image on the PDF
            pdf.image(_img, x=0.75, h=3.1)

    return pdf


def _add_qa_page(pdf, scandata, assrdata, sesstype):
    scan_image = plot_qa(scandata)
    assr_image = plot_qa(assrdata)

    if not scan_image and not assr_image:
        # skip this page b/c there's nothing to plot
        logger.debug('skipping page, nothing to plot:{}'.format(sesstype))
        return pdf

    pdf.add_page()
    pdf.set_font('helvetica', size=18)
    pdf.ln(0.5)
    pdf.cell(w=5, align='C', text='Scans by Type ({} Only)'.format(sesstype))

    if scan_image:
        pdf.image(scan_image, x=0.5, y=1.3, w=7.5)
        pdf.ln(4.7)

    if assr_image:
        pdf.cell(w=5, align='C', text=f'Assessors by Type ({sesstype} Only)')
        pdf.image(assr_image, x=0.5, y=6, w=7.5)

    return pdf


def _add_timeline_page(pdf, info, enable_monthly=False):
    # Get the data for all
    df = info['sessions'].copy()

    pdf.add_page()

    pdf.set_font('helvetica', size=18)

    # Draw all timeline
    _txt = 'Sessions Timeline'
    if enable_monthly:
        _txt += ' (all)'

    pdf.cell(w=7.5, align='C', text=_txt)
    image = plot_timeline(df)
    pdf.image(image, x=0.5, y=0.75, w=7.5)
    pdf.ln(5)

    if enable_monthly:
        # Get the dates of last month
        enddate = date.today().replace(day=1) - timedelta(days=1)
        startdate = date.today().replace(day=1) - timedelta(days=enddate.day)

        # Get the name of last month
        lastmonth = startdate.strftime("%B")
        _txt = 'Sessions Timeline ({})'.format(lastmonth)
        image = plot_timeline(df, startdate=startdate, enddate=enddate)
        pdf.cell(w=7.5, align='C', text=_txt)
        pdf.image(image, x=0.5, y=5.75, w=7.5)
        pdf.ln()
        pdf.add_page()

    return pdf


def _add_nda_page(pdf, info):
    pdf.add_page()

    pdf.cell(text='NDA', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(1)

    return pdf

def _add_analyses_page(pdf, info):
    pdf.add_page()

    pdf.cell(text='ANALYSES', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    analyses = info['analyses']

    #print(analyses)

    for i, a in analyses.iterrows():
        #PROJECT
        #ID
        #NAME
        #STATUS
        #EDIT
        #NOTES
        #SUBJECTS
        #PROCESSOR
        #INVESTIGATOR
        #OUTPUT

        _txt = f'{a.PROJECT}-A{a.ID} {a.NAME}'
        pdf.cell(text=_txt, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        _txt = f'STATUS:{a.STATUS} OUTPUT:{a.OUTPUT}'
        pdf.cell(text=_txt, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        _txt = f'NOTES:{a.NOTES}'
        pdf.cell(text=_txt, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.ln(0.3)


    return pdf

def _add_settings_page(pdf, info):
    pdf.add_page()

    pdf.set_font('helvetica', size=18)
    pdf.cell(w=7.5, align='C', text='Project Settings', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Add some space
    pdf.ln(0.5)

    # Main Settings
    pdf.set_font('helvetica', size=14, style='B')
    pdf.cell(text='REDCap Projects:', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('helvetica', size=10)
    pdf.cell(h=0.2, text=f'Primary PID:{info["primary_redcap"]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(h=0.2, text=f'Secondary PID:{info["secondary_redcap"]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(h=0.2, text=f'Stats PID:{info["stats_redcap"]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(0.3)

    if info.get('xnat_scanmap', False):
        # Scan Map
        pdf.set_font('helvetica', size=14, style='B')
        pdf.cell(text='XNAT Scan Map', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font('helvetica', size=10)
        _txt = _transform_scanmap(info['xnat_scanmap'])
        pdf.multi_cell(w=5.0, h=0.2, text=_txt, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(0.3)

    if info.get('nda_scanmap', False):
        # NDA Scan Map
        pdf.set_font('helvetica', size=14, style='B')
        pdf.cell(text='NDA Scan Map', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font('helvetica', size=11)
        _txt = info['nda_scanmap']
        pdf.multi_cell(w=5.0, h=0.2, text=_txt, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(0.3)

    if info.get('nda_expmap', False):
        # NDA Experiment Map
        pdf.set_font('helvetica', size=14, style='B')
        pdf.cell(text='NDA Experiment Map', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font('helvetica', size=11)
        _txt = info['nda_expmap']
        pdf.multi_cell(w=5.0, h=0.2, text=_txt, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(0.3)

    if info.get('scan_protocols', False):
        # Scanning Protocols
        pdf.set_font('helvetica', size=14, style='B')
        pdf.cell(text='Scanning Protocols', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font('helvetica', size=11)
        _txt = '\n'.join([x['scanning_eventname'] for x in info['scan_protocols']])
        pdf.multi_cell(w=5.0, h=0.2, text=_txt, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(0.3)

    if info.get('edat_protocols', False):
        # EDAT Protocols
        pdf.set_font('helvetica', size=14, style='B')
        pdf.cell(text='EDAT Protocols', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font('helvetica', size=11)
        _txt = '\n'.join([x['edat_name'] for x in info['edat_protocols']])
        pdf.multi_cell(w=5.0, h=0.2, text=_txt, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(0.2)

    return pdf


def _add_proclib_page(pdf, info):
    pdf.add_page()

    # Get the proclib for enabled proctypes
    proclib = info['proclib']
    proclib = {k: v for k, v in proclib.items() if k in info['proctypes']}

    # Display each proctype
    for k, v in proclib.items():
        # Show the proctype
        pdf.set_font('helvetica', size=16)
        pdf.cell(text=k, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Build the description
        _text = v.get('short_descrip', '') + '\n'
        _text += 'Inputs: ' + v.get('inputs_descrip', '') + '\n'
        _text += v.get('procurl', '') + '\n'

        # show stats
        for s, t in info['statlib'].get(k, {}).items():
            _text += f'{s}: {t}\n'

        # Show the description
        pdf.set_font('helvetica', size=12)
        pdf.multi_cell(0, 0.3, _text, border='LBTR', align="L", new_x=XPos.RIGHT, new_y=YPos.NEXT)

        # Add some space between proc types
        pdf.ln(0.2)

    return pdf


def _add_phantoms(pdf, info, enable_monthly=False):
    # Get the data for all
    df = info['phantoms'].copy()

    # Draw all timeline
    _txt = 'Phantoms (all)'
    pdf.set_font('helvetica', size=18)
    pdf.cell(w=7.5, align='C', text=_txt, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    image = plot_timeline(df)
    pdf.image(image, x=0.5, w=7.5)
    pdf.ln(5)

    if enable_monthly:
        # Get the dates of last month
        enddate = date.today().replace(day=1) - timedelta(days=1)
        startdate = date.today().replace(day=1) - timedelta(days=enddate.day)

        # Get the name of last month
        lastmonth = startdate.strftime("%B")

        _txt = 'Phantoms ({})'.format(lastmonth)
        image = plot_timeline(df, startdate=startdate, enddate=enddate)
        pdf.cell(w=7.5, align='C', text=_txt)
        pdf.image(image, x=0.5, y=5.75, w=7.5)
        pdf.ln()

    return pdf


def _add_activity_page(pdf, info):
    pdf.add_page()
    pdf.set_font('helvetica', size=16)

    # top third is jobs section
    df = info['recentjobs'].copy()
    image = plot_activity(df, 'CATEGORY')
    pdf.image(image, x=1.6, y=0.2, h=3.3)
    pdf.ln(0.5)
    pdf.multi_cell(1.5, 0.3, text='Jobs\n')

    # middle third is activity section
    df = info['activity'].copy()
    image = plot_activity(df, 'CATEGORY')
    pdf.image(image, x=1.6, y=3.5, h=3.3)
    pdf.ln(3)
    pdf.multi_cell(1.5, 0.3, text='Autos')

    # bottom third is issues
    df = info['issues'].copy()
    image = plot_activity(df, 'CATEGORY')
    pdf.image(image, x=1.6, y=7.0, h=3.3)
    pdf.ln(3)
    pdf.multi_cell(1.5, 0.3, text='Issues\n')

    return pdf


def plot_qa(dfp):
    """Plot QA bars."""
    for col in dfp.columns:
        if col in ('SESSION', 'PROJECT', 'DATE', 'MODALITY'):
            # don't mess with these columns
            continue

        # Change each value from the multiple values in concatenated
        # characters to a single overall status
        dfp[col] = dfp[col].apply(get_metastatus)

    # Initialize a figure
    fig = plotly.subplots.make_subplots(rows=1, cols=1)
    fig.update_layout(margin=dict(l=40, r=40, t=40, b=40))

    # Check for empty data
    if len(dfp) == 0:
        logger.debug('dfp empty data')
        return None

    # use pandas melt function to unpivot our pivot table
    df = pd.melt(
        dfp,
        id_vars=(
            'SESSION',
            'SUBJECT',
            'PROJECT',
            'DATE',
            'SITE',
            'SESSTYPE',
            'MODALITY'),
        value_name='STATUS')

    # Check for empty data
    if len(df) == 0:
        logger.debug('df empty data')
        return None

    # We use fill_value to replace nan with 0
    dfpp = df.pivot_table(
        index='TYPE',
        columns='STATUS',
        values='SESSION',
        aggfunc='count',
        fill_value=0)

    scan_type = []
    assr_type = []
    for cur_type in dfpp.index:
        # Use a regex to test if name ends with _v and a number, then assr
        if re.search('_v\d+$', cur_type):
            assr_type.append(cur_type)
        else:
            scan_type.append(cur_type)

    newindex = scan_type + assr_type
    dfpp = dfpp.reindex(index=newindex)

    # Draw bar for each status, these will be displayed in order
    # ydata should be the types, xdata should be count of status
    # for each type
    for cur_status, cur_color in QASTATUS2COLOR.items():
        ydata = dfpp.index
        if cur_status not in dfpp:
            xdata = [0] * len(dfpp.index)
        else:
            xdata = dfpp[cur_status]

        cur_name = '{} ({})'.format(cur_status, sum(xdata))

        _width = (len(xdata) * 0.1) + 0.1
        _width = min(_width, 0.8)
        fig.append_trace(
            go.Bar(
                x=ydata,
                y=xdata,
                name=cur_name,
                marker=dict(color=cur_color),
                opacity=0.9,
                width=_width,
            ),
            1, 1)

    # Customize figure
    fig['layout'].update(barmode='stack', showlegend=True, width=900)

    # Export figure to image
    _png = fig.to_image(format="png")
    image = Image.open(io.BytesIO(_png))

    return image


def _plottable(var):
    try:
        _ = var.astype(str).replace('', np.nan).dropna().str.strip('%').astype(float)
        return True
    except Exception:
        return False


def plot_stats(df, plot_title=None):
    """Plot stats, one boxlplot per var."""
    box_width = 250
    min_box_count = 4

    logger.debug('plot_stats:{}'.format(len(df)))

    # Check for empty data
    if len(df) == 0:
        logger.debug('empty data, using empty figure')
        fig = go.Figure()
        _png = fig.to_image(format="png")
        image = Image.open(io.BytesIO(_png))
        return image

    # Filter var list to only include those that have data
    var_list = [x for x in df.columns if not pd.isnull(df[x]).all()]

    # Filter var list to only stats variables
    var_list = [x for x in var_list if x not in HIDECOLS]

    # Filter var list to only stats can be plotted as float
    var_list = [x for x in var_list if _plottable(df[x])]

    # skip vars
    var_list = [x for x in var_list if not x.endswith('pathlength')]

    # Determine how many boxplots we're making, depends on how many vars, use
    # minimum so graph doesn't get too small
    box_count = len(var_list)
    site_count = len(df['SITE'].unique())

    if box_count < 3:
        box_width = 500
        min_box_count = 2
    elif box_count < 6:
        box_width = 333
        min_box_count = 3

    if site_count > 3:
        box_width = 500
        min_box_count = 2

    if box_count < min_box_count:
        box_count = min_box_count

    graph_width = box_width * box_count

    # Horizontal spacing cannot be greater than (1 / (cols - 1))
    hspacing = 1 / (box_count * 4)

    logger.debug(f'{box_count}, {min_box_count}, {graph_width}, {hspacing}')

    # Make the figure with 1 row and a column for each var we are plotting
    var_titles = [x[:22] for x in var_list]
    fig = plotly.subplots.make_subplots(
        rows=1,
        cols=box_count,
        horizontal_spacing=hspacing,
        subplot_titles=var_titles)

    # Add box plot for each variable
    for i, var in enumerate(var_list):

        # Create boxplot for this var and add to figure
        logger.debug('plotting var:{}'.format(var))

        _row = 1
        _col = i + 1

        fig.append_trace(
            go.Box(
                y=df[var].astype(str).replace('', np.nan).dropna().str.strip('%').astype(float),
                x=df['SITE'],
                boxpoints='all',
                text=df['ASSR'],
                boxmean=True,
            ),
            _row,
            _col)

        # Plot horizontal line at median
        _median = df[var].astype(str).replace('', np.nan).dropna().str.strip('%').astype(float).median()
        fig.add_trace(
            go.Scatter(
                x=df['SITE'],
                y=[_median] * len(df),
                mode='lines',
                name='',
                fillcolor='red',
                line_color='grey'),
            _row, _col)

        fig.update_yaxes(autorange=True)

        if var.startswith('con_') or var.startswith('inc_'):
            logger.debug('setting beta range:{}'.format(var))
            _yaxis = 'yaxis{}'.format(i + 1)
            fig['layout'][_yaxis].update(range=[-1, 1], autorange=False)
        else:
            pass

    # Move the subtitles to bottom instead of top of each subplot
    if len(df['SITE'].unique()) < 4:
        for i in range(len(fig.layout.annotations)):
            fig.layout.annotations[i].update(y=-.15)

    if plot_title:
        fig.update_layout(
            title={'text': plot_title, 'x': 0.5, 'xanchor': 'center'})

    # Customize figure to hide legend and fit the graph
    fig.update_layout(
        showlegend=False,
        autosize=False,
        width=graph_width,
        margin=dict(l=20, r=40, t=40, b=80, pad=0))

    _png = fig.to_image(format="png")
    image = Image.open(io.BytesIO(_png))
    return image


def _add_stats_pages(pdf, info):
    proclib = info['proclib']
    stats = info['stats']
    stattypes = info['stattypes']

    for proctype in stattypes:
        # Limit the data to this proctype
        stat_data = stats[stats.PROCTYPE == proctype]

        if stat_data.empty:
            logger.debug(f'no stats for proctype:{proctype}')
            continue

        logger.debug(f'add stats page:{proctype}')

        # Get descriptions for this processing type
        proc_info = proclib.get(proctype, {})

        # use proclib to filter stats variable names
        _subset = proc_info.get('stats_subset', None)
        if _subset:
            try:
                stat_data = stat_data[_subset + ['SITE', 'ASSR']]
            except Exception as err:
                logger.error(f'subset failed:{_subset}, skipping page:{proctype}')
                return

        # Now make the page
        pdf.add_page()
        pdf.set_font('helvetica', size=16)
        pdf.cell(text=proctype, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        if proctype == 'fmriqa_v4':
            # stats by scan type using inputs field to map to scan
            _add_stats_fmriqa(pdf, stat_data, info)
        else:
            _add_stats(pdf, stat_data)

        # Build the description
        _text = proc_info.get('short_descrip', '') + '\n'
        _text += 'Inputs: ' + proc_info.get('inputs_descrip', '') + '\n'

        # Append stats descriptions
        for s, t in info['statlib'].get(proctype, {}).items():
            _text += f'{s}: {t}\n'

        # Show the descriptions
        pdf.set_font('helvetica', size=12)
        pdf.multi_cell(0, 0.25, _text, border='LBTR', align="L", new_x=XPos.RIGHT, new_y=YPos.NEXT)

        _url = proc_info.get('procurl', '')
        if _url:
            pdf.set_font('helvetica', size=10)
            pdf.cell(text=_url, link=_url)


def make_pdf(info, filename):
    enable_monthly = info['enable_monthly']
    multi_group = info['multi_group']

    """Make PDF from info, save to filename."""
    logger.debug('making PDF')

    # Initialize a new PDF letter size and shaped
    pdf = blank_letter()
    pdf.set_filename(filename)
    pdf.set_project(info['project'], enable_monthly=enable_monthly)

    # Add first page showing MRIs
    logger.debug('adding first page')
    _add_count_pages(pdf, info['sessions'], enable_monthly=enable_monthly, groupby='site')

    # Show group pages only when multiple groups found
    if multi_group:
        _add_count_pages(pdf, info['sessions'], enable_monthly=enable_monthly, groupby='group')

    # Add per scan counts
    logger.debug('adding per scan count pages')
    _add_scan_count_pages(pdf, info['scans'], groupby='site')
    if multi_group:
        _add_scan_count_pages(pdf, info['scans'], groupby='group')

    # Timeline
    logger.debug('adding timeline page')
    _add_timeline_page(pdf, info, enable_monthly=enable_monthly)

    # Phantom pages
    if len(info['phantoms']) > 0:
        logger.debug('adding phantom page')
        _add_phantoms(pdf, info, enable_monthly=enable_monthly)
    else:
        logger.debug('no phantom page')

    # Add stats pages
    if info['stats'].empty:
        logger.debug('without stats')
    else:
        logger.debug('adding stats pages')
        _add_stats_pages(pdf, info)

    # Session type pages - counts per scans, counts per assessor
    logger.debug('adding MR qa pages')

    mr_sessions = info['sessions'].copy()
    mr_sessions = mr_sessions[mr_sessions.MODALITY == 'MR']

    for curtype in mr_sessions.SESSTYPE.unique():
        logger.debug('add_qa_page:{}'.format(curtype))

        # Get the scan and assr data
        scandf = info['scanqa'].copy()
        assrdf = info['assrqa'].copy()

        # Limit to the current session type
        scandf = scandf[scandf.SESSTYPE == curtype]
        assrdf = assrdf[assrdf.SESSTYPE == curtype]

        # Drop columns that are all empty
        scandf = scandf.dropna(axis=1, how='all')
        assrdf = assrdf.dropna(axis=1, how='all')

        # Add the page for this session type
        _add_qa_page(pdf, scandf, assrdf, curtype)

    # LST vs SAMSEG
    _add_wml_page(pdf, info)

    # QA/Jobs/Issues counts
    if info['enable_monthly']:
        _add_activity_page(pdf, info)

    # Directed Graph of processing
    # TODO: only run if graphviz/dot are installed
    # TODO: build the graph dynamically using same logic as dashboard autofilter
    # to find used scan types, then list unused to the side with counts
    # and then do the for proc types based on enabled in processing or not
    _add_graph_page(pdf, info)

    # Settings
    _add_settings_page(pdf, info)

    # NDA
    if False:
        _add_nda_page(pdf, info)

    # Analyses
    _add_analyses_page(pdf, info)


    # Save to file
    logger.debug('saving PDF to file:{}'.format(pdf.filename))
    try:
        pdf.output(pdf.filename)
    except Exception as err:
        logger.error('error while saving PDF:{}:{}'.format(pdf.filename, err))

    return True


def _scanqa(scans, scantypes=None):
    dfp = _scan_pivot(scans).reset_index()

    if not scantypes:
        scantypes = scans.SCANTYPE.unique()

    # Filter columns to include
    include_list = SESSCOLS.copy()
    if scantypes:
        include_list += scantypes
    include_list = [x for x in include_list if x in dfp.columns]
    include_list = list(set(include_list))
    dfp = dfp[include_list]

    # Drop columns that are all empty
    dfp = dfp.dropna(axis=1, how='all')

    return dfp


def _assrqa(assessors, proctypes=None):
    # Load that data
    dfp = _assr_pivot(assessors).reset_index()

    # Filter columns to include
    include_list = SESSCOLS + proctypes
    include_list = [x for x in include_list if x in dfp.columns]
    include_list = list(set(include_list))
    dfp = dfp[include_list]

    return dfp


def _scan_pivot(df):
    _index = ('SESSION', 'SUBJECT', 'PROJECT', 'DATE', 'SESSTYPE', 'SITE', 'MODALITY')
    df['TYPE'] = df['SCANTYPE']
    df['STATUS'] = df['QUALITY']
    dfp = df.pivot_table(
        index=_index,
        columns='TYPE',
        values='STATUS',
        aggfunc=lambda x: ''.join(x))

    return dfp


def _assr_pivot(df):
    _index = ('SESSION', 'SUBJECT', 'PROJECT', 'DATE', 'SESSTYPE', 'SITE', 'MODALITY')
    df['TYPE'] = df['PROCTYPE']
    df['STATUS'] = df['PROCSTATUS']
    dfp = df.pivot_table(
        index=_index,
        columns='TYPE',
        values='STATUS',
        aggfunc=lambda x: ''.join(x))

    return dfp


def get_metastatus(status):
    if not status or pd.isnull(status):  # np.isnan(status):
        # empty so it's none
        metastatus = 'NONE'
    elif 'P' in status:
        # at least one passed, so PASSED
        metastatus = 'PASS'
    elif 'Q' in status:
        # any are still needs qa, then 'NEEDS_QA'
        metastatus = 'NQA'
    elif 'N' in status:
        # if any jobs are still running, then NEEDS INPUTS?
        metastatus = 'NPUT'
    elif 'F' in status:
        # at this point if one failed, then they all failed, so 'FAILED'
        metastatus = 'FAIL'
    elif 'X' in status:
        metastatus = 'JOBF'
    elif 'R' in status:
        metastatus = 'JOBR'
    elif 'usable' in status:
        metastatus = 'PASS'
    elif 'questionable' in status:
        metastatus = 'NQA'
    elif 'unusable' in status:
        metastatus = 'FAIL'
    else:
        # whatever else is UNKNOWN, grey
        metastatus = 'NONE'

    return metastatus


def _filter_scantypes(scantypes):

    # Try to filter out junk
    scantypes = [x for x in scantypes if not x.startswith('[')]
    scantypes = [x for x in scantypes if 'survey' not in x.lower()]
    scantypes = [x for x in scantypes if x.lower() != 'cor']
    scantypes = [x for x in scantypes if x.lower() != 'unknown']
    scantypes = [x for x in scantypes if x.lower() != 'fmri_rest_fsa']
    scantypes = [x for x in scantypes if not x.lower().startswith('screen')]
    scantypes = [x for x in scantypes if not x.startswith('Low Dose CT')]
    scantypes = [x for x in scantypes if not x.startswith('VWIP')]
    scantypes = [x for x in scantypes if not x.startswith('3DFRP')]
    scantypes = [x for x in scantypes if not x.startswith('TOPUP')]
    scantypes = [x for x in scantypes if not x.startswith('localizer')]
    scantypes = [x for x in scantypes if not x.startswith('Calibration')]
    scantypes = [x for x in scantypes if not x.endswith('PhysioLog')]
    scantypes = [x for x in scantypes if not x.endswith('SBRef')]
    scantypes = [x for x in scantypes if not x.endswith('FSA')]
    scantypes = [x for x in scantypes if not x.startswith('Cor_')]
    scantypes = [x for x in scantypes if not x.startswith('Ax_')]
    scantypes = [x for x in scantypes if not x.startswith('AXIIAL')]
    scantypes = [x for x in scantypes if not x.startswith('DTI_1_')]
    scantypes = [x for x in scantypes if 'MDDW' not in x]
    scantypes = [x for x in scantypes if not x.startswith('3-Plane')]
    scantypes = [x for x in scantypes if not x.startswith('DTI_96d')]
    scantypes = [x for x in scantypes if not x.startswith('Head-Low')]
    scantypes = [x for x in scantypes if not x.startswith('MultiP')]
    scantypes = [x for x in scantypes if not x.startswith('MPRAGE A')]
    scantypes = [x for x in scantypes if not x.startswith('CTAC2mm')]
    scantypes = [x for x in scantypes if not x.startswith('ORIG')]
    scantypes = [x for x in scantypes if not x.startswith('Phoenix')]
    scantypes = [x for x in scantypes if not x.startswith('SpinEcho')]
    scantypes = [x for x in scantypes if not x.startswith('rsfMRI')]
    scantypes = [x for x in scantypes if not x.startswith('Sagittal_3D_F')]
    scantypes = [x for x in scantypes if not x.startswith('fMRI_rest')]
    scantypes = [x for x in scantypes if not x.startswith('DTI_2min_b1000a')]
    scantypes = [x for x in scantypes if not x.startswith('DTI_2min_b1000a')]
    scantypes = [x for x in scantypes if not x.startswith('DTI_b0')]

    return scantypes


def make_project_report(
    garjus,
    project,
    pdfname,
    zipname=None,
    monthly=False
):
    """"Make the project report PDF and zip files"""
    proclib = garjus.processing_library()
    statlib = garjus.stats_library()
    activity = garjus.activity(project)
    issues = garjus.issues(project)
    analyses = garjus.analyses([project], download=False)

    # Load types for this project
    proctypes = garjus.proctypes(project)
    scantypes = garjus.scantypes(project)
    stattypes = garjus.stattypes(project)

    # Loads scans/assessors with type filters applied
    scans = garjus.scans(projects=[project], scantypes=scantypes)
    scans.SESSTYPE = scans.SESSTYPE.replace('', 'UNKNOWN')
    scans.SITE = scans.SITE.replace('', 'UNKNOWN')
    scans.MODALITY = scans.MODALITY.replace('', 'UNKNOWN')
    scans.DATE = scans.DATE.fillna(datetime.now())

    scantypes = list(scans.SCANTYPE.unique())
    scantypes = _filter_scantypes(scantypes)

    # Truncate names for display
    scantypes = list(set([x[:15].strip() for x in scantypes if x]))
    scantypes = sorted(scantypes)

    assessors = garjus.assessors(projects=[project], proctypes=proctypes)
    assessors.SESSTYPE = assessors.SESSTYPE.replace('', 'UNKNOWN')
    assessors.SITE = assessors.SITE.replace('', 'UNKNOWN')
    assessors.MODALITY = assessors.MODALITY.replace('', 'UNKNOWN')
    assessors.DATE = assessors.DATE.fillna(datetime.now())

    phantoms = garjus.phantoms(project)
    phantoms = phantoms[SESSCOLS].drop_duplicates().sort_values('SESSION')

    # Extract sessions from scans/assessors
    sessions = pd.concat([scans[SESSCOLS], assessors[SESSCOLS]])
    sessions = sessions.drop_duplicates().sort_values('SESSION')

    # Merge in group from subjects
    subjects = garjus.subjects(project).reset_index()
    sessions = pd.merge(
        sessions,
        subjects[['ID', 'PROJECT', 'GROUP']],
        left_on=('SUBJECT', 'PROJECT'),
        right_on=('ID', 'PROJECT'),
        how='left',
    )

    if project == 'REMBRANDT':
        sessions['GROUP'] = sessions['GROUP'].fillna('Depress')
    else:
        sessions['GROUP'] = sessions['GROUP'].fillna('UNKNOWN')

    scans = pd.merge(
        scans,
        subjects[['ID', 'PROJECT', 'GROUP']],
        left_on=('SUBJECT', 'PROJECT'),
        right_on=('ID', 'PROJECT'),
        how='left'
    )

    if project == 'REMBRANDT':
        scans['GROUP'] = scans['GROUP'].fillna('Depress')
    else:
        scans['GROUP'] = scans['GROUP'].fillna('UNKNOWN')

    # Load stats with extra assessor columns
    stats = garjus.stats(project, assessors)

    # Make the info dictionary for PDF
    info = {}
    info['scans'] = scans
    info['assessors'] = assessors
    info['proclib'] = proclib
    info['statlib'] = statlib
    info['project'] = project
    info['stattypes'] = stattypes
    info['scantypes'] = scantypes
    info['proctypes'] = proctypes
    info['sessions'] = sessions
    info['activity'] = activity
    info['issues'] = issues
    info['analyses'] = analyses
    info['recentjobs'] = _recent_jobs(assessors)
    info['recentqa'] = _recent_qa(assessors)
    info['stats'] = stats
    info['scanqa'] = _scanqa(scans, scantypes)
    info['assrqa'] = _assrqa(assessors, proctypes)
    info['phantoms'] = phantoms
    info['enable_monthly'] = monthly
    info['xnat_scanmap'] = garjus.project_setting(project, 'scanmap')
    info['nda_expmap'] = garjus.project_setting(project, 'xst2nei')
    info['nda_scanmap'] = garjus.project_setting(project, 'xst2nst')
    info['scan_protocols'] = garjus.scanning_protocols(project)
    info['edat_protocols'] = garjus.edat_protocols(project)
    info['settings_redcap'] = garjus.project_setting(project, 'redcap')
    info['primary_redcap'] = garjus.project_setting(project, 'primary')
    info['secondary_redcap'] = garjus.project_setting(project, 'secondary')
    info['stats_redcap'] = garjus.project_setting(project, 'stats')

    if len(sessions['GROUP'].unique()) > 1:
        info['multi_group'] = True
    else:
        info['multi_group'] = False

    # Save the PDF report to file
    make_pdf(info, pdfname)

    # Save the stats to zip file
    if zipname:
        # TODO: include a QA.csv and a subjects.csv with demographics
        subjects = garjus.subjects(project)
        data2zip(subjects, stats, zipname)


def data2zip(subjects, stats, filename):
    """Convert stats dict to zip of csv files, one csv per proctype."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Prep output dir
        data_dir = os.path.join(tmpdir, 'data')
        zip_file = os.path.join(tmpdir, 'data.zip')
        os.mkdir(data_dir)

        # Save subjects csv
        csv_file = os.path.join(data_dir, f'subjects.csv')
        logger.info(f'saving subjects csv:{csv_file}')
        subjects.to_csv(csv_file)

        # Save a csv for each proc type
        for proctype in stats.PROCTYPE.unique():
            # Get the data for this processing type
            dft = stats[stats.PROCTYPE == proctype]

            dft = dft.dropna(axis=1, how='all')

            dft = dft.sort_values('ASSR')

            # Save file for this type
            csv_file = os.path.join(data_dir, f'{proctype}.csv')
            logger.info(f'saving csv:{proctype}:{csv_file}')
            dft.to_csv(csv_file, index=False)

        # Create zip file of dir of csv files
        shutil.make_archive(data_dir, 'zip', data_dir)

        # Save it outside of temp dir
        logger.info(f'saving zip:{filename}')
        shutil.copy(zip_file, filename)


def _last_month():
    from dateutil.relativedelta import relativedelta
    return (datetime.today() - relativedelta(months=1)).strftime('%Y-%m-%d')


def _recent_jobs(assessors, startdate=None):
    """Get recent jobs, assessors on XNAT with job date since startdate."""
    if startdate is None:
        startdate = _last_month()

    df = assessors.copy()

    # Filter by jobstartdate date, include anything with job running
    df = df[(df['JOBDATE'] >= startdate) | (df['PROCSTATUS'] == 'JOB_RUNNING')]

    # Relabel as jobs
    df['LABEL'] = df['ASSR']
    df['CATEGORY'] = df['PROCTYPE']
    df['STATUS'] = df['PROCSTATUS'].map({
        'COMPLETE': 'COMPLETE',
        'JOB_FAILED': 'FAIL',
        'JOB_RUNNING': 'NPUT'}).fillna('UNKNOWN')
    df['CATEGORY'] = df['PROCTYPE']
    df['DESCRIPTION'] = 'JOB' + ':' + df['LABEL']
    df['DATETIME'] = df['JOBDATE']
    df['ID'] = df.index

    return df


def _recent_qa(assessors, startdate=None):
    if startdate is None:
        startdate = _last_month()

    df = assessors.copy()

    # Filter by qc date
    df = df[df['QCDATE'] >= startdate]

    # Relabel as qa
    df['LABEL'] = df['ASSR']
    df['CATEGORY'] = df['PROCTYPE']
    df['STATUS'] = df['QCSTATUS'].map({
        'Failed': 'FAIL',
        'Passed': 'PASS'}).fillna('UNKNOWN')
    df['CATEGORY'] = df['PROCTYPE']
    df['DESCRIPTION'] = 'QA' + ':' + df['LABEL']
    df['DATETIME'] = df['QCDATE']
    df['ID'] = df.index

    return df


def _transform_scanmap(scanmap):
    """Parse scan map stored as string into map."""
    # Parse multiline string of delimited key value pairs into dictionary
    scanmap = dict(x.strip().split(':', 1) for x in scanmap.split('\n'))

    # Remove extra whitespace from keys and values
    scanmap = {k.strip(): v.strip() for k, v in scanmap.items()}
    scanmap = '\n'.join(f'{k} -> {v}' for k, v in scanmap.items())

    return scanmap
