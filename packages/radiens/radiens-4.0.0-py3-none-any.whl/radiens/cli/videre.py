"""
radiens CLI
"""
from pathlib import Path

import click
import pandas as pd
from radiens.cli.signal_metrics import metrics
from radiens.cli.signals import signals
from radiens.cli.spike_sorter import sorter
from radiens.utils.enums import ClientType
from radiens.utils.util import time_now


@ click.group(short_help='videre commands')
@ click.pass_context
def videre(ctx):
    '''
    VIDERE command group

    This command group works concurrently with the VIDERE app to control the data acquisition system.
    '''
    ctx.obj['cmd_app'] = ClientType.VIDERE


videre.add_command(sorter)
videre.add_command(metrics)
videre.add_command(signals)


@ videre.command('link', short_help='link a data file to Radiens')
@ click.pass_context
@ click.argument('datafile', type=click.STRING)
@ click.option('-m', '--metrics',  type=click.BOOL, default=True, help='calculate signal metrics', show_default=True)
@ click.option('-f', '--force',  type=click.BOOL, default=False, help='force linking', show_default=True)
@ click.option('-h', '--hub',  type=click.STRING, default='default', help='Radiens hub', show_default=True)
def link_datasource(ctx, datafile, metrics, force, hub):
    '''
    Links the requested data source to the Radiens hub. 
    '''
    try:
        dsource = ctx.obj['videre_client'].link_data_file(
            datafile, calc_metrics=metrics, force=force)
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    click.echo('Linked {} (id={}) to Radiens hub {} at {}'.format(
        Path(datafile), dsource.id, hub, time_now()))


@ videre.command('metadata', short_help='prints meta data on a Radiens data file')
@ click.pass_context
@ click.option('-idx', '--index',  type=click.INT, default=None, help='dataset index from table', show_default=True)
@ click.option('-id', '--dset_id',  type=click.STRING, default=None, help='dataset ID from table', show_default=True)
@ click.option('-p', '--path',  type=click.STRING, default=None, help='path and base name of Radiens file set', show_default=True)
@ click.option('-h', '--hub',  type=click.STRING, default='default', help='Radiens hub', show_default=True)
def dsource_metadata(ctx, index, dset_id, path, hub):
    '''
    Prints table of meta data for one requested linked dataset or Radiens-compatible data file. If --path is specified
    then the requested data file is linked to the Radiens hub.  
    '''
    try:
        resp = ctx.obj['videre_client'].get_data_file_metadata(dataset_idx=index, dataset_id=dset_id,
                                                               path=path, fail_hard=True)
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    click.echo('Linked dataset meta data [hub {}]'.format(hub))
    print(resp.table)


@ videre.command('list', short_help='print table of linked data source on the Radiens hub')
@ click.pass_context
@ click.option('-h', '--hub',  type=click.STRING, default='default', help='Radiens hub', show_default=True)
def list_dsource(ctx, hub):
    '''
    Prints table of currently linked data sources on the Radiens hub
    '''
    try:
        df_table = ctx.obj['videre_client'].get_dataset_ids()
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    click.echo('Linked dataset table [hub {}, N={}]'.format(
        hub, len(df_table)))
    print(df_table)


@ videre.command('unlink', short_help='unlink a data file from the Radiens hub')
@ click.pass_context
@ click.option('-idx', '--index',  type=click.INT, default=None, help='dataset index from table', show_default=True)
@ click.option('-id', '--dset_id',  type=click.STRING, default=None, help='dataset ID from table', show_default=True)
@ click.option('-p', '--path',  type=click.STRING, default=None, help='path and base name of Radiens file set', show_default=True)
@ click.option('-h', '--hub',  type=click.STRING, default='default', help='Radiens hub', show_default=True)
def unlink_dsource(ctx, index, dset_id, path, hub):
    '''
    Unlinks one or more datasets of this Curate session from the Radiens hub.
    Use dataset_id='all' to clear all session datasets.
    '''
    try:
        num_unlinked, df_table = ctx.obj['videre_client'].clear_dataset(dataset_idx=index, dataset_id=dset_id,
                                                                        path=path, fail_hard=True)
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    click.echo('Unlinked {} datasets from hub {}'.format(num_unlinked, hub))
    click.echo('Linked dataset table [hub {}, N={}]'.format(
        hub, len(df_table)))
    print(df_table)


@ videre.command('dashboard', short_help='manage Videre dashboard(s)')
@ click.pass_context
@ click.option('-c', '--close',  type=click.BOOL, default=False, help='close all dashboards', show_default=True)
@ click.option('-h', '--hub',  type=click.STRING, default='default', help='Radiens hub', show_default=True)
def dash_new(ctx, close, hub):
    '''
    Launch a new dashboard or close all dashboards for the Radiens hub. 
    '''
    try:
        ctx.obj['videre_client'].dashboard(close=close, hub_name=hub)
    except Exception as ex:
        click.echo('Error: {}', ex)
        return
    if close:
        click.echo('Closing all dashboards')
    else:
        click.echo('Launching new dashboard...')
