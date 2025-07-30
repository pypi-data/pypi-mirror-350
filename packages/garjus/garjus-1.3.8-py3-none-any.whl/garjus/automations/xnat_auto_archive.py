"""Archive scans in XNAT."""
import logging

# Copy session from project named for PI to primary project.
# Session ID generated from event 2 session mapping in project settings
# This method allows the PI project on XNAT to be set to auto-archive and
# skips the prearchive to avoid timeout problems moving large sessions.


logger = logging.getLogger('garjus.automations.xnat_auto_archive')


def process_project(
    garjus,
    scan_table,
    source_project,
    destination_project
):
    """Copy from src to dst as needed."""
    results = []
    src_proj = source_project
    dst_proj = destination_project
    src_labels = garjus.session_labels(src_proj)
    dst_labels = garjus.session_labels(dst_proj)

    # Process each record
    for r in scan_table:
        logger.debug(f'xnat_auto_archive:{r}')
        src_subj = r['src_subject']
        src_sess = r['src_session']
        dst_subj = r['dst_subject']
        dst_sess = r['dst_session']

        # Remove leading and trailing whitespace that keeps showing up
        src_sess = src_sess.strip()

        if destination_project == 'D3':
            # Hard code this to avoid duplicates
            dst_subj = dst_subj.replace('v', 'V')
            dst_sess = dst_sess.replace('v', 'V')

        # Check if session already exists in destination project
        if dst_sess in dst_labels:
            # Note that we don't check the other values in redcap
            logger.debug(f'session exists on XNAT:{dst_sess}')
            continue

        # Check that session does exist in source project
        if src_sess not in src_labels:
            logger.debug(f'session not on XNAT:{src_sess}:{dst_subj}')
            continue

        logger.info('copying:{0}/{1}/{2}:{3}/{4}/{5}'.format(
            src_proj,
            src_subj,
            src_sess,
            dst_proj,
            dst_subj,
            dst_sess,
        ))

        garjus._copy_session(
            src_proj,
            src_subj,
            src_sess,
            dst_proj,
            dst_subj,
            dst_sess)

        results.append({
            'result': 'COMPLETE',
            'description': f'{src_sess}',
            'subject': dst_subj,
            'session': dst_sess})

    return results
