import logging
import sys
import redcap
from garjus.automations.etl_arcapp import process_project


api_url = 'https://redcap.vanderbilt.edu/api/'


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s:%(module)s:%(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info('connecting to redcap')
    api_key = sys.argv[1]  # this is a test copy of REM
    rc = redcap.Project(api_url, api_key)

    logging.info('Running it')
    results = process_project(rc)

    logging.info(results)
    logging.info('Done!')
