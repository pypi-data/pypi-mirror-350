import logging
import os
import pandas as pd

from ....garjus import Garjus


logger = logging.getLogger('dashboard.processors.data')


def get_filename():
    datadir = f'{Garjus().userdir()}/DATA'
    filename = f'{datadir}/processorsdata.pkl'

    try:
        os.makedirs(datadir)
    except FileExistsError:
        pass

    return filename


def run_refresh(filename, projects):
    df = get_data(projects)

    save_data(df, filename)

    return df


def load_options():
    garjus = Garjus()
    proj_options = garjus.projects()

    return proj_options


def load_data(projects, refresh=False):
    filename = get_filename()

    if refresh or not os.path.exists(filename):
        run_refresh(filename, projects)

    logger.info('reading data from file:{}'.format(filename))
    return read_data(filename)


def read_data(filename):
    df = pd.read_pickle(filename)
    return df


def save_data(df, filename):
    # save to cache
    df.to_pickle(filename)


def get_data(projects):
    g = Garjus()

    if not g.rcq_enabled():
        logger.debug('rcq not enabled, no processing data')
        return pd.DataFrame(columns=g.column_names('processing'))

    # Load
    df = g.processing_protocols(projects)

    df['FILE'] = df['FILE'].apply(os.path.basename)

    df = df.sort_values(['PROJECT', 'FILE'])

    return df


def filter_data(df):
    # TBD

    return df
