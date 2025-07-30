import logging
import sys
import importlib
import tempfile

from garjus.utils_redcap import download_file, field2events


logger = logging.getLogger('test_gaitrite')


def run(project):
    data = []
    results = []
    events = []
    records = []
    file_field = 'gaitrite_upload'
    done_field = 'gaitrite_testrecord'

    # load the automation
    try:
        mod = importlib.import_module(f'garjus.automations.etl_gaitrite')
    except ModuleNotFoundError as err:
        logger.error(f'error loading module:{err}')
        return

    # records will include both the file record and the repeating records
    records = project.export_records(
        fields=[file_field, done_field],
        events=field2events(project, file_field)
    )

    # Get unique list of record/event
    recordevents = list(set(
        [(x[project.def_field], x['redcap_event_name']) for x in records]))

    # Initialize counts
    counts = {x: 0 for x in recordevents}

    # Count repeats
    repeats = [x for x in records if x['redcap_repeat_instance']]

    # Count total records for each id/event
    for r in repeats:
        record_id = r[project.def_field]
        event_id = r['redcap_event_name']
        counts[(record_id, event_id)] += 1

    # Process each record
    for r in [x for x in records if not x['redcap_repeat_instance']]:
        data = []
        record_id = r[project.def_field]
        event_id = r['redcap_event_name']

        if not r[file_field]:
            logger.debug(f'no data file:{record_id}:{event_id}')
            continue

        if counts[(record_id, event_id)] > 0:
            logger.debug(f'already done:{record_id}:{event_id}')
            continue

        logger.debug(f'etl_gaitrite:{record_id}:{event_id}')

        filename = r[file_field]

        if filename.endswith('.zip'):
            logger.debug('ignoring zip')
            continue

        with tempfile.TemporaryDirectory() as tmpdir:
            data_file = f'{tmpdir}/{filename}'

            try:
                # Download files from redcap
                logger.debug(f'downloading VUMC file:{data_file}')
                download_file(
                    project,
                    record_id,
                    file_field,
                    data_file,
                    event_id=event_id
                )

                # Process downloaded file to extract data
                data = mod.process(data_file)

            except Exception as err:
                logger.error(err)
                continue

        # Load data back to redcap
        results.append({'subject': record_id, 'event': event_id, 'field': 'gaitrite_upload'})
        for d in data:
            d[project.def_field] = record_id
            d['redcap_event_name'] = event_id
            d['redcap_repeat_instrument'] = 'gaitrite'
            d['redcap_repeat_instance'] = 'new'
            d['gaitrite_complete'] = '2'

        if len(data) > 0:
            try:
                response = project.import_records(data)
                assert 'count' in response
                logger.debug(f'uploaded:{record_id}:{event_id}')
            except AssertionError as e:
                logger.error('error uploading', record_id, e)

    return results


def run_upmc(project):
    data = []
    results = []
    events = []
    records = []
    file_field = 'gaitrite_file'
    done_field = 'gaitrite_comments'

    # load the automation
    try:
        mod = importlib.import_module(f'garjus.automations.etl_gaitrite')
    except ModuleNotFoundError as err:
        logger.error(f'error loading module:{err}')
        return

    records = project.export_records(
        fields=[file_field, done_field],
    )

    records = [x for x in records if x['redcap_repeat_instrument'] == 'gaitrite']

    # Process each record
    for r in records:
        data = []
        record_id = r[project.def_field]
        repeat_id = r['redcap_repeat_instance']
        event_id = r['redcap_event_name']

        if r[done_field]:
            logger.debug(f'already done:{record_id}:{event_id}:{repeat_id}')
            continue

        if not r[file_field]:
            logger.debug(f'no data file:{record_id}:{event_id}:{repeat_id}')
            continue


        logger.debug(f'etl_gaitrite:{record_id}:{event_id}:{repeat_id}')

        with tempfile.TemporaryDirectory() as tmpdir:
            data_file = f'{tmpdir}/{r.get(file_field)}'

            try:
                # Download file from redcap
                logger.debug(f'downloading UPMC file:{data_file}')
                download_file(
                    project,
                    record_id,
                    file_field,
                    data_file,
                    event_id=event_id,
                    repeat_id=repeat_id,
                )

                # Process downloaded file to extract data
                d = mod.process_upmc(data_file)

                try:
                    # Complete the record with identifiers
                    d[project.def_field] = record_id
                    d['redcap_event_name'] = event_id
                    d['redcap_repeat_instrument'] = 'gaitrite'
                    d['redcap_repeat_instance'] = str(repeat_id)
                    d['gaitrite_complete'] = '2'
                except Exception as err:
                    logger.error(err)

                # Add to list for redcap upload
                data.append(d)

                # Save history
                results.append({'subject': record_id, 'event': event_id, 'field': file_field})

            except Exception as err:
                logger.error(err)
                continue

        if len(data) > 0:
            # Load data back to redcap
            try:
                response = project.import_records(data)
                assert 'count' in response
                logger.debug(f'uploaded:{record_id}:{event_id}')
            except AssertionError as e:
                logger.error('error uploading', record_id, e)

    return results


if __name__ == "__main__":
    import redcap
    from garjus.automations.etl_gaitrite import process

    api_url = 'https://redcap.vanderbilt.edu/api/'
    api_key = sys.argv[1]
    rc = redcap.Project(api_url, api_key)

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s:%(module)s:%(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')

    results = run(rc)
    results += run_upmc(rc)
    print(results)
    print('Done!')
