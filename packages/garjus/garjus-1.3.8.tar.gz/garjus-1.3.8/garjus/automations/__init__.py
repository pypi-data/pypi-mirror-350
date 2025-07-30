"""

Garjus automations.

Automation names correspond to folder name.

"""
import logging
import importlib
import tempfile

from ..utils_redcap import download_file, field2events

from . import etl_nihexaminer


# TODO: move slice timing to redcap


logger = logging.getLogger('garjus.automations')


D3_SLICE_TIMING = [
    0.00, 0.80, 0.08, 0.88, 0.16, 0.96, 0.24, 1.04, 0.32, 1.12,
    1.52, 0.72, 1.44, 0.64, 1.36, 0.56, 1.28, 0.48, 1.20, 0.40,
    0.00, 0.80, 0.08, 0.88, 0.16, 0.96, 0.24, 1.04, 0.32, 1.12,
    1.52, 0.72, 1.44, 0.64, 1.36, 0.56, 1.28, 0.48, 1.20, 0.40,
    0.00, 0.80, 0.08, 0.88, 0.16, 0.96, 0.24, 1.04, 0.32, 1.12,
    1.52, 0.72, 1.44, 0.64, 1.36, 0.56, 1.28, 0.48, 1.20, 0.40]

DM2_SLICE_TIMING = [
    0.0, 0.65, 0.065, 0.7150000000000001, 0.13, 0.78, 0.195, 0.845, 0.26, 0.91,
    1.235, 0.585, 1.17, 0.52, 1.105, 0.455, 1.04, 0.39, 0.9750000000000001,
    0.325,
    0.0, 0.65, 0.065, 0.7150000000000001, 0.13, 0.78, 0.195, 0.845, 0.26, 0.91,
    1.235, 0.585, 1.17, 0.52, 1.105, 0.455, 1.04, 0.39, 0.9750000000000001,
    0.325,
    0.0, 0.65, 0.065, 0.7150000000000001, 0.13, 0.78, 0.195, 0.845, 0.26, 0.91,
    1.235, 0.585, 1.17, 0.52, 1.105, 0.455, 1.04, 0.39, 0.9750000000000001,
    0.325]

REMBRANDT_SLICE_TIMING = [
    0.00, 0.80, 0.08, 0.88, 0.16, 0.96, 0.24, 1.04, 0.32, 1.12,
    1.52, 0.72, 1.44, 0.64, 1.36, 0.56, 1.28, 0.48, 1.20, 0.40,
    0.00, 0.80, 0.08, 0.88, 0.16, 0.96, 0.24, 1.04, 0.32, 1.12,
    1.52, 0.72, 1.44, 0.64, 1.36, 0.56, 1.28, 0.48, 1.20, 0.40,
    0.00, 0.80, 0.08, 0.88, 0.16, 0.96, 0.24, 1.04, 0.32, 1.12,
    1.52, 0.72, 1.44, 0.64, 1.36, 0.56, 1.28, 0.48, 1.20, 0.40]


def update(garjus, projects, autos_include=None, autos_exclude=None):
    """Update project progress."""
    for p in projects:
        logging.debug(f'updating automations:{p}')
        update_project(garjus, p, autos_include, autos_exclude)


def update_project(garjus, project, autos_include=None, autos_exclude=None):
    """Update automations for project."""

    # These can run without xnat, for now
    etl_autos = garjus.etl_automations(project)

    if garjus.xnat_enabled():
        scan_autos = garjus.scan_automations(project)
    else:
        logging.debug(f'no xnat, disable scan automations')
        scan_autos = []

    edat_autos = garjus.edat_automation_choices()

    if autos_include:
        # Apply include filter
        scan_autos = [x for x in scan_autos if x in autos_include]
        etl_autos = [x for x in etl_autos if x in autos_include]
        edat_autos = [x for x in edat_autos if x in autos_include]

    if autos_exclude:
        # Apply exclude filter
        scan_autos = [x for x in scan_autos if x not in autos_exclude]
        etl_autos = [x for x in etl_autos if x not in autos_exclude]
        edat_autos = [x for x in edat_autos if x not in autos_exclude]

    if scan_autos:
        logging.debug(f'running scan automations:{project}:{scan_autos}')
        _run_scan_automations(scan_autos, garjus, project)

    for a in etl_autos:
        logging.debug(f'running automation:{project}:{a}')
        _run_etl_automation(a, garjus, project)

    if edat_autos:
        _run_edat_automations(edat_autos, garjus, project)


def _run_edat_automations(automations, garjus, project):
    results = []
    edats = garjus.edat_protocols(project)
    scanp = garjus.scanning_protocols(project)
    primary_redcap = garjus.primary(project)
    limbo = garjus.project_setting(project, 'limbodir')
    scans = []
    convertdir = garjus.project_setting(project, 'convertdir')
    event2sess = {}

    if primary_redcap is None:
        logger.debug(f'primary redcap not found, check keys:{project}')
        return

    if garjus.xnat_enabled():
        scans = garjus.scans(projects=[project]).to_dict('records')

    # Only MRI
    logger.debug(f'{scanp=}')
    scanp = [x for x in scanp if x['scanning_modality'] == '1']
    logger.debug(f'{scanp=}')

    for p in scanp:
        s = p['scanning_xnatsuffix']
        _events = [x.strip() for x in p['scanning_events'].split(',')]
        for e in _events:
            event2sess[e] = s

    # load the automations
    try:
        edat_limbo2redcap = importlib.import_module(
            f'garjus.automations.edat_limbo2redcap')
        edat_convert2tab = importlib.import_module(
            f'garjus.automations.edat_convert2tab')
        edat_redcap2xnat = importlib.import_module(
            f'garjus.automations.edat_redcap2xnat')
    except ModuleNotFoundError as err:
        logger.error(f'error loading modules:{err}')
        return

    for e in edats:
        edat_autos = [
            k.split('edat_autos___')[1]
            for k, v in e.items() if k.startswith('edat_autos') and v == '1']

        # Apply filter
        edat_autos = [x for x in edat_autos if x in automations]

        _events = [x.strip() for x in e['edat_events'].split(',')]
        _nums = [x.strip() for x in e['edat_eventnums'].split(',')]
        _event2num = dict(zip(_events, _nums))

        if 'edat_limbo2redcap' in edat_autos:
            results += edat_limbo2redcap.process_project(
                primary_redcap,
                _events,
                e['edat_rawfield'],
                e['edat_convfield'],
                e['edat_fileprefix'],
                limbo,
                event2sess=_event2num)

        if 'edat_convert2tab' in edat_autos and convertdir:
            results += edat_convert2tab.process_project(
                primary_redcap,
                _events,
                e['edat_rawfield'],
                e['edat_convfield'],
                convertdir)

        if 'edat_redcap2xnat' in edat_autos and garjus.xnat_enabled():
            results += edat_redcap2xnat.process_project(
                garjus.xnat(),
                primary_redcap,
                _events,
                e['edat_convfield'],
                event2sess,
                scans,
                e['edat_scantype'],
                'EDAT')

        if 'edat_etl' in edat_autos:
            if e['edat_convfield'] == 'tat_conv':
                # Trait Adjective Task
                try:
                    etl_traitadjtask = importlib.import_module(
                        'garjus.automations.etl_traitadjtask')

                    logger.debug(f'{project}:ETL Trait Adjective Task')
                    results += etl_traitadjtask.process_project(primary_redcap)
                except ModuleNotFoundError as err:
                    logger.error(f'error loading modules:{err}')

            elif e['edat_convfield'] == 'tat_recall_conv':
                # Trait Adjective Recall
                try:
                    etl_traitadjrecall = importlib.import_module(
                        'garjus.automations.etl_traitadjrecall')
                    logger.debug(f'{project}:ETL Trait Adjective Recall')
                    results += etl_traitadjrecall.process_project(primary_redcap)
                except ModuleNotFoundError as err:
                    logger.error(f'error loading modules:{err}')
                    return

    # Upload results to garjus
    for r in results:
        r.update({'project': project})
        garjus.add_activity(**r)


def _parse_scanmap(scanmap):
    """Parse scan map stored as string into map."""
    # Parse multiline string of delimited key value pairs into dictionary
    scanmap = dict(x.strip().split(':', 1) for x in scanmap.split('\n'))

    # Remove extra whitespace from keys and values
    scanmap = {k.strip(): v.strip() for k, v in scanmap.items()}

    return scanmap


def _parse_map(mapstring):
    """Parse map stored as string into dictionary."""

    parsed_map = mapstring.replace('=', ':')

    # Parse multiline string of delimited key value pairs into dictionary
    parsed_map = dict(x.strip().split(':', 1) for x in parsed_map.split('\n'))

    # Remove extra whitespace from keys and values
    parsed_map = {k.strip(): v.strip() for k, v in parsed_map.items()}

    return parsed_map


def _run_etl_automation(automation, garjus, project):
    """Load the project primary redcap."""
    results = []

    project_redcap = garjus.primary(project)
    if not project_redcap:
        logger.debug(f'primary redcap not found:{project}')
        return

    if automation == 'etl_arcdata':
        arc_dir = garjus.project_setting(project, 'arcdatadir')
        results = _run_etl_arcdata(project_redcap, arc_dir)
    elif automation == 'etl_gaitrite':
        results = _run_etl_gaitrite(project_redcap)
    elif automation == 'etl_nihexaminer':
        if 'nih_dot_total' in project_redcap.field_names:
            limbo = garjus.project_setting(project, 'limbodir')
            _dir = f'{limbo}/{project}_EXAMINER/data'
            e2s = garjus.project_setting(project, 'examinermap')
            e2s = _parse_map(e2s)
            results = etl_nihexaminer.file2redcap(project_redcap, _dir, e2s)
        else:
            results = []

        results += etl_nihexaminer.run(project_redcap)
    elif automation == 'etl_nihtoolbox_drtaylor':
        results = _run_etl_nihtoolbox_drtaylor(project_redcap)
    else:
        # load the automation
        try:
            m = importlib.import_module(f'garjus.automations.{automation}')
        except ModuleNotFoundError as err:
            logger.error(f'error loading module:{automation}:{err}')
            return

        # Run it
        try:
            results = m.process_project(project_redcap)
        except Exception as err:
            logger.error(f'{project}:{automation}:failed to run:{err}')
            return

    # Upload results to garjus
    for r in results:
        r.update({'project': project, 'category': automation})
        r.update({'description': r.get('description', automation)})
        garjus.add_activity(**r)


def _run_etl_fitbit(project):
    '''project is a pycap redcap project that contains data to process'''
    results = []
    file_field = 'fitbit_summary_worn'
    def_field = project.def_field
    done_field = 'fitbit_daysworn'
    fields = [def_field, file_field, done_field]
    id2subj = {}

    # load the automation
    try:
        fitbit = importlib.import_module(f'garjus.automations.etl_fitbit')
    except ModuleNotFoundError as err:
        logger.error(f'error loading module:{err}')
        return

    events = field2events(project, file_field)
    sec_field = project.export_project_info()['secondary_unique_field']
    if sec_field:
        rec = project.export_records(fields=[def_field, sec_field])
        id2subj = {x[def_field]: x[sec_field] for x in rec if x[sec_field]}
    else:
        rec = project.export_records(fields=[def_field])
        id2subj = {x[def_field]: x[def_field] for x in rec if x[def_field]}

    # Get records
    rec = project.export_records(fields=fields, events=events)

    # Process each record
    for r in rec:
        record_id = r[def_field]
        event_id = r['redcap_event_name']
        subj = id2subj.get(record_id)

        if r[done_field]:
            logger.debug(f'already ETL:{record_id}:{event_id}')
            continue

        # Check for converted file
        if not r[file_field]:
            logging.debug(f'no file found:{record_id}:{subj}:{event_id}:{file_field}')
            continue

        if r[file_field] == 'CONVERT_FAILED.txt':
            logging.debug(f'found CONVERT_FAILED')
            continue

        if r[file_field] == 'MISSING_DATA.txt':
            logging.debug(f'found MISSING_DATA')
            continue

        # Do the ETL
        with tempfile.TemporaryDirectory() as tmpdir:
            data_file = f'{tmpdir}/TimeFBWorn.csv'

            # Download files from redcap
            logger.debug(f'downloading file:{data_file}')
            download_file(
                project, record_id, file_field, data_file, event_id=event_id)

            # Extract and Transform
            data = etl_fitbit.process(data_file)

        # Load data back to redcap
        _load(project, record_id, event_id, data)

        results.append({
            'result': 'COMPLETE',
            'category': 'etl_fitbit',
            'description': 'etl_fitbit',
            'subject': subj,
            'event': event_id,
            'field': file_field})

    return results


def _run_etl_nihtoolbox_drtaylor(project):
    data = {}
    results = []
    events = []
    fields = []
    records = []
    reg_field = 'toolbox_regdata'
    score_field = 'toolbox_cogscores'
    done_field = 'toolbox_pin'

    # load the automation
    try:
        toolbox = importlib.import_module(
            f'garjus.automations.etl_nihtoolbox_drtaylor')
    except ModuleNotFoundError as err:
        logger.error(f'error loading module:{err}')
        return

    events = field2events(project, reg_field)

    fields = [project.def_field, done_field, reg_field, score_field]

    records = project.export_records(fields=fields, events=events)

    for r in records:
        data = {}
        record_id = r[project.def_field]
        event_id = r['redcap_event_name']

        if r[done_field]:
            logger.debug(f'already ETL:{record_id}:{event_id}')
            continue

        if not r[score_field]:
            logger.debug(f'no data file:{record_id}:{event_id}')
            continue

        logger.debug(f'running ETL:{record_id}:{event_id}')
        results.append({'subject': record_id, 'event': event_id})

        with tempfile.TemporaryDirectory() as tmpdir:
            reg_file = f'{tmpdir}/regfile.csv'
            score_file = f'{tmpdir}/scorefile.csv'

            # Download files from redcap
            logger.debug(f'downloading file:{reg_file}')
            download_file(
                project, record_id, reg_field, reg_file, event_id=event_id)
            logger.debug(f'downloading file:{score_file}')
            download_file(
                project, record_id, score_field, score_file, event_id=event_id)

            data = toolbox.process(reg_file, score_file)

        # Load data back to redcap
        _load(project, record_id, event_id, data)
        results.append({'subject': record_id, 'event': event_id})

    return results


def _run_etl_arcdata(project, datadir):

    # load the automation
    try:
        mod = importlib.import_module(f'garjus.automations.etl_arcdata')
    except ModuleNotFoundError as err:
        logger.error(f'error loading module:{err}')
        return

    return mod.process(project, datadir)


def _run_etl_gaitrite(project):
    data = {}
    results = []
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
        data = {}
        record_id = r[project.def_field]
        event_id = r['redcap_event_name']

        if not r[file_field]:
            logger.debug(f'no data file:{record_id}:{event_id}')
            continue

        if counts[(record_id, event_id)] > 0:
            logger.debug(f'already done:{record_id}:{event_id}')
            continue

        logger.debug(f'etl_gaitrite:{record_id}:{event_id}')

        with tempfile.TemporaryDirectory() as tmpdir:
            data_file = f'{tmpdir}/gaitrite.xlsx'

            # Download files from redcap
            logger.debug(f'downloading file:{data_file}')
            download_file(
                project, record_id, file_field, data_file, event_id=event_id)

            # Process downloaded file to extract data
            data = mod.process(data_file)

        # Load data back to redcap
        results.append({'subject': record_id, 'event': event_id})
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


def _run_etl_nihexaminer(project):
    """Process examiner files from REDCap and upload results."""
    data = {}
    results = []
    events = []
    fields = []
    records = []
    flank_field = 'flanker_file'
    nback_field = 'nback_upload'
    shift_field = 'set_shifting_file'
    cpt_field = 'cpt_upload'
    done_field = 'flanker_score'

    # load the automation
    try:
        examiner = importlib.import_module(f'garjus.automations.etl_nihexaminer')
    except ModuleNotFoundError as err:
        logger.error(f'error loading module:examiner:{err}')
        return

    if 'flanker_summfile' in project.field_names:
        # Alternate file field names
        flank_field = 'flanker_summfile'
        nback_field = 'nback_summfile'
        shift_field = 'set_shifting_summfile'
        cpt_field = 'cpt_summfile'

    # Get the fields
    fields = [
        project.def_field,
        done_field,
        cpt_field,
        nback_field,
        shift_field,
        flank_field,
        'dot_count_tot',
        'anti_trial_1',
        'anti_trial_2',
        'correct_f',
        'correct_l',
        'correct_animal',
        'correct_veg',
        'repetition_f',
        'rule_vio_f',
        'repetition_l',
        'rule_vio_l',
        'repetition_animal',
        'rule_vio_animal',
        'repetition_veg',
        'rule_vio_veg',
        'brs_1',
        'brs_2',
        'brs_3',
        'brs_4',
        'brs_5',
        'brs_6',
        'brs_7',
        'brs_8',
        'brs_9',
    ]

    if 'correct_s' in project.field_names:
        fields.extend([
            'correct_s', 'rule_vio_s', 'repetition_s',
            'correct_t', 'rule_vio_t', 'repetition_t',
            'correct_fruit', 'rule_vio_fruit', 'repetition_fruit',
            'correct_r', 'rule_vio_r', 'repetition_r',
            'correct_m', 'rule_vio_m', 'repetition_m',
            'correct_cloth', 'rule_vio_cloth', 'repetition_cloth',
        ])

    # Determine events
    events = field2events(project, cpt_field)

    # Get records for those events and fields
    records = project.export_records(fields=fields, events=events)

    for r in records:
        data = {}
        record_id = r[project.def_field]
        event_id = r['redcap_event_name']

        if r[done_field]:
            logger.debug(f'already ETL:{record_id}:{event_id}')
            continue

        if not r[cpt_field]:
            logger.debug(f'no data file:{record_id}:{event_id}')
            continue

        # Check for blanks
        has_blank = False
        check_fields = [
            flank_field,
            nback_field,
            shift_field,
            cpt_field,
            'dot_count_tot',
            'anti_trial_1',
            'anti_trial_2',
            'correct_f',
            'correct_l',
            'correct_animal',
            'correct_veg',
            'repetition_f',
            'rule_vio_f',
            'repetition_l',
            'rule_vio_l',
            'repetition_animal',
            'rule_vio_animal',
            'repetition_veg',
            'rule_vio_veg',
            'brs_1',
            'brs_2',
            'brs_3',
            'brs_4',
            'brs_5',
            'brs_6',
            'brs_7',
            'brs_8',
            'brs_9']

        for k in check_fields:
            if r[k] == '' and k != done_field:
                logger.debug(f'blank value:{record_id}:{event_id}:{k}')
                has_blank = True
                break

        if has_blank:
            continue

        logger.debug(f'running nihexaminer ETL:{record_id}:{event_id}')

        # Get values needed for scoring
        manual_values = {
            'dot_total': int(r['dot_count_tot']),
            'anti_trial_1': int(r['anti_trial_1']),
            'anti_trial_2': int(r['anti_trial_2']),
            'cf1_corr': int(r['correct_animal']),
            'cf1_rep': int(r['repetition_animal']),
            'cf1_rv': int(r['rule_vio_animal']),
            'brs_1': int(r['brs_1']),
            'brs_2': int(r['brs_2']),
            'brs_3': int(r['brs_3']),
            'brs_4': int(r['brs_4']),
            'brs_5': int(r['brs_5']),
            'brs_6': int(r['brs_6']),
            'brs_7': int(r['brs_7']),
            'brs_8': int(r['brs_8']),
            'brs_9': int(r['brs_9']),
        }

        if r['correct_f']:
            # examiner version 0
            manual_values.update({
                'vf1_corr': int(r['correct_f']),
                'vf1_rep': int(r['repetition_f']),
                'vf1_rv': int(r['rule_vio_f']),
                'vf2_corr': int(r['correct_l']),
                'vf2_rep': int(r['repetition_l']),
                'vf2_rv': int(r['rule_vio_l']),
                'cf2_corr': int(r['correct_veg']),
                'cf2_rep': int(r['repetition_veg']),
                'cf2_rv': int(r['rule_vio_veg'])
            })
        elif r['correct_t']:
            # examiner version 1
            manual_values.update({
                'vf1_corr': int(r['correct_t']),
                'vf1_rep': int(r['repetition_t']),
                'vf1_rv': int(r['rule_vio_t']),
                'vf2_corr': int(r['correct_s']),
                'vf2_rep': int(r['repetition_s']),
                'vf2_rv': int(r['rule_vio_s']),
                'cf2_corr': int(r['correct_fruit']),
                'cf2_rep': int(r['repetition_fruit']),
                'cf2_rv': int(r['rule_vio_fruit'])
            })
        else:
            # examiner version 2
            manual_values.update({
                'vf1_corr': int(r['correct_r']),
                'vf1_rep': int(r['repetition_r']),
                'vf1_rv': int(r['rule_vio_r']),
                'vf2_corr': int(r['correct_m']),
                'vf2_rep': int(r['repetition_m']),
                'vf2_rv': int(r['rule_vio_m']),
                'cf2_corr': int(r['correct_cloth']),
                'cf2_rep': int(r['repetition_cloth']),
                'cf2_rv': int(r['rule_vio_cloth'])
            })

        with tempfile.TemporaryDirectory() as tmpdir:
            # Get files needed
            flank_file = f'{tmpdir}/flanker.csv'
            cpt_file = f'{tmpdir}/cpt.csv'
            nback_file = f'{tmpdir}/nback.csv'
            shift_file = f'{tmpdir}/shift.csv'

            try:
                # Download files from redcap
                logger.debug(f'download files:{record_id}:{event_id}:{flank_file}')
                download_file(project, record_id, flank_field, flank_file, event_id=event_id)
                logger.debug(f'download NBack:{record_id}:{event_id}:{nback_field}')
                download_file(project, record_id, nback_field, nback_file, event_id=event_id)
                logger.debug(f'download Shift:{record_id}:{event_id}:{shift_field}')
                download_file(project, record_id, shift_field, shift_file, event_id=event_id)
                logger.debug(f'download CPT:{record_id}:{event_id}:{cpt_field}')
                download_file(project, record_id, cpt_field, cpt_file, event_id=event_id)
            except Exception as err:
                logger.error(f'downloading files:{record_id}:{event_id}')
                continue

            try:
                # Process inputs
                data = examiner.process(
                    manual_values,
                    flank_file,
                    cpt_file,
                    nback_file,
                    shift_file)
            except Exception as err:
                logger.error(f'processing examiner:{record_id}:{event_id}:{err}')
                continue

        # Load data back to redcap
        _load(project, record_id, event_id, data)
        results.append({'subject': record_id, 'event': event_id})

    return results


def _run_scan_automations(automations, garjus, project):
    results = []
    proj_scanmap = garjus.project_setting(project, 'scanmap')
    sess_replace = garjus.project_setting(project, 'relabelreplace').split(',')
    scan_data = garjus.scanning_protocols(project)
    site_data = garjus.sites(project)
    protocols = garjus.scanning_protocols(project)
    project_redcap = garjus.primary(project)

    # Add slice timing
    if project in ['REMBRANDT', 'COGD']:
        logger.debug(f'running add_slicetiming:{project}')

        slicetiming = importlib.import_module(
            'garjus.automations.xnat_add_slicetiming')
        results += slicetiming.process_project(
            garjus,
            project,
            D3_SLICE_TIMING,
            ['fMRI_REST1', 'fMRI_REST2'],
            sites=['VUMC'],
        )
    elif project == 'D3':
        logger.debug(f'running add_slicetiming:{project}')

        slicetiming = importlib.import_module(
            'garjus.automations.xnat_add_slicetiming')
        results += slicetiming.process_project(
            garjus,
            project,
            D3_SLICE_TIMING,
            ['fMRI_REST1', 'fMRI_REST2'],
            sites=['VUMC'],
        )
    elif project in ['DepMIND2', 'DepMIND3']:
        logger.debug(f'running add_slicetiming:{project}')

        slicetiming = importlib.import_module(
            'garjus.automations.xnat_add_slicetiming')
        results += slicetiming.process_project(
            garjus,
            project,
            DM2_SLICE_TIMING,
            ['fMRI_REST1', 'fMRI_REST2', 'fMRI_REST3'],
            sites=['VUMC'],
        )

    # load the automations
    try:
        xnat_auto_archive = importlib.import_module(
            f'garjus.automations.xnat_auto_archive')
        xnat_relabel_sessions = importlib.import_module(
            f'garjus.automations.xnat_relabel_sessions')
        xnat_relabel_scans = importlib.import_module(
            f'garjus.automations.xnat_relabel_scans')
        xnat_dcm2niix = importlib.import_module(
            f'garjus.automations.xnat_dcm2niix')
        xnat_ma3stats2voltxt = importlib.import_module(
            'garjus.automations.xnat_ma3stats2voltxt')
        logger.debug('modules loaded')
    except ModuleNotFoundError as err:
        logger.error(f'error loading scan automations:{err}')
        return

    if 'xnat_auto_archive' in automations and project_redcap and garjus.has_dcm2niix():
        # Apply autos to each scanning protocol
        for p in protocols:
            date_field = p['scanning_datefield']
            sess_field = p['scanning_srcsessfield']
            sess_suffix = p['scanning_xnatsuffix']
            src_project = p['scanning_srcproject']
            alt_primary = p['scanning_altprimary']

            # Get events list
            events = None
            if p.get('scanning_events', False):
                events = [x.strip() for x in p['scanning_events'].split(',')]

            # Make the scan table that links what's entered at the scanner with
            # what we want to label the scans
            if alt_primary:
                scan_redcap = garjus.alternate(alt_primary)
            else:
                scan_redcap = project_redcap

            scan_table = _make_scan_table(
                scan_redcap,
                events,
                date_field,
                sess_field,
                sess_suffix)

            # Run
            logger.debug(f'running xnat_auto_archive:{project}:{events}')
            results += xnat_auto_archive.process_project(
                garjus, scan_table, src_project, project)

    # Apply relabeling
    if 'xnat_relabel_sessions' in automations:
        # Build the session relabling
        sess_relabel = _session_relabels(scan_data, site_data)

        # Run it
        logger.debug(f'{project}:running session relabel')
        results += xnat_relabel_sessions.process_project(
            garjus.xnat(), project, sess_relabel, sess_replace)

    if 'xnat_relabel_scans' in automations and proj_scanmap:
        # Parse scan map
        proj_scanmap = _parse_scanmap(proj_scanmap)

        # Run it
        logger.debug(f'{project}:running scan relabel:{proj_scanmap}')
        results += xnat_relabel_scans.process_project(
            garjus.xnat(), project, proj_scanmap)

    # MA3 stats 2 vol txt
    if 'xnat_ma3stats2voltxt' in automations:
        logger.debug(f'running ma3stats2voltxt:{project}')
        assessors = garjus.assessors(
            projects=[project], proctypes=['Multi_Atlas_v3'])
        xnat = garjus.xnat()

        # Add resource information, note takes a minute to load resources
        _resources = garjus.assessor_resources(project, 'Multi_Atlas_v3')
        assessors['RESOURCES'] = assessors.apply(
            lambda x: _resources.get(x.ASSR, ''), axis=1)

        # Run it
        results += xnat_ma3stats2voltxt.process_project(
            xnat,
            project,
            assessors)

    # d2n
    if garjus.has_dcm2niix() and 'dcm2niix' in automations:
        logger.debug(f'{project}:running dcm2niix')
        results += xnat_dcm2niix.process_project(garjus, project)

    # Upload results to garjus
    for r in results:
        r['project'] = project
        garjus.add_activity(**r)


def _make_scan_table(
    project,
    events,
    date_field,
    sess_field,
    scan_suffix,
):
    """Make the scan table, linking source to destination subject/session."""
    data = []
    id2subj = {}

    # Shortcut
    def_field = project.def_field

    # Handle secondary ID
    sec_field = project.export_project_info()['secondary_unique_field']
    if sec_field:
        rec = project.export_records(fields=[def_field, sec_field])
        id2subj = {x[def_field]: x[sec_field] for x in rec if x[sec_field]}
    else:
        rec = project.export_records(fields=[def_field])
        id2subj = {x[def_field]: x[def_field] for x in rec if x[def_field]}

    # Get mri records from redcap
    fields = [date_field, sess_field, def_field]
    try:
        rec = project.export_records(fields=fields, events=events)
    except Exception as err:
        logger.error(err)
        return []

    # Only if date is entered
    rec = [x for x in rec if x[date_field]]

    # Only if entered
    rec = [x for x in rec if x[sess_field]]

    # Set the subject and session
    for r in rec:
        d = {}
        try:
            d['dst_subject'] = id2subj.get(r[def_field])
        except KeyError:
            logger.warn(f'blank subject number:{r[def_field]}')
            continue

        if not d['dst_subject']:
            logger.warn(f'blank subject number:{r[def_field]}')
            continue

        d['src_session'] = r[sess_field].strip()
        d['src_subject'] = d['src_session']
        d['dst_session'] = d['dst_subject'] + scan_suffix
        data.append(d)

    return data


def _session_relabels(scan_data, site_data):
    """Build session relabels."""
    relabels = []

    # Build the session relabeling from scan_autos and sites
    for rec in scan_data:
        relabels.append((
            'session_label',
            '*' + rec['scanning_xnatsuffix'],
            'session_type',
            rec['scanning_xnattype']))

    for rec in site_data:
        relabels.append((
            'session_label',
            rec['site_sessmatch'],
            'site',
            rec['site_shortname']))

    return relabels


def _load(project, record_id, event_id, data):
    data[project.def_field] = record_id
    data['redcap_event_name'] = event_id
    data = {k: str(v) for k, v in data.items()}

    try:
        response = project.import_records([data])
        assert 'count' in response
        logger.debug(f'uploaded:{record_id}:{event_id}')
    except AssertionError as e:
        logger.error('error uploading', record_id, e)
