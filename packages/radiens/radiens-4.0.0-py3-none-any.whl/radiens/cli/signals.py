"""
radiens CLI
"""
from datetime import datetime
from pathlib import Path
from pprint import pprint

import click
import pandas as pd
from radiens.utils.constants import PRIMARY_CACHE_STREAM_GROUP_ID
from radiens.utils.enums import ClientType
from radiens.utils.util import make_time_range, time_now


@ click.group(short_help='signals commands')
@ click.pass_context
def signals(ctx):
    '''
    Signals commands. 

    This command group has sub-commands for interacting with signals. 
    '''


@ signals.command('snapshot', short_help='get and plot a signals snapshot')
@ click.pass_context
@ click.option('-idx', '--index',  type=click.INT, default=None, help='dataset index from table (Allego n/a)', show_default=True)
@ click.option('-id', '--dset_id',  type=click.STRING, default=None, help='dataset ID from table (Allego n/a)', show_default=True)
@ click.option('-p', '--path',  type=click.STRING, default=None, help='path and base name of Radiens file set', show_default=True)
@ click.option('-h', '--hub',  type=click.STRING, default='default', help='Radiens hub (Allego n/a)', show_default=True)
def snapshot(ctx, index, dset_id, path, hub):
    '''
    Gets a signals snapshot and optionally plot it or save to file. 

    '''
    cmd_app = ClientType.parse(ctx.obj['cmd_app'])
    try:
        if cmd_app.is_videre():
            dsource = ctx.obj['videre_client'].get_data_file_metadata(
                dataset_idx=index, dataset_id=dset_id, path=path, fail_hard=True)
            ctx.obj['videre_client'].signal_metrics().clear(
                dataset_metadata=dsource)
            msg_id = dsource.id
        else:
            click.Echo('not implemented yet for Allego')
            msg_id = PRIMARY_CACHE_STREAM_GROUP_ID
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    click.echo('{} ({}) : cleared signal metrics at {}'.format(
        cmd_app.name, msg_id, time_now()))


@ signals.command('psd', short_help='calculate power spectral density')
@ click.pass_context
@ click.option('-ts', '--tstart',  type=click.FLOAT, default=None, help='time start (sec)', show_default=True)
@ click.option('-dur', '--dur',  type=click.FLOAT, default=None, help='time end (sec)', show_default=True)
@ click.option('-idx', '--index',  type=click.INT, default=None, help='dataset index from table (Allego n/a)', show_default=True)
@ click.option('-id', '--dset_id',  type=click.STRING, default=None, help='dataset ID from table (Allego n/a)', show_default=True)
@ click.option('-p', '--path',  type=click.STRING, default=None, help='path and base name of Radiens file set', show_default=True)
@ click.option('-f', '--file',  type=click.STRING, default=None, help='save to file', show_default=True)
@ click.option('-h', '--hub',  type=click.STRING, default='default', help='Radiens hub (Allego n/a)', show_default=True)
def psd(ctx, tstart, dur, index, dset_id, path, file, hub):
    '''
    Calculates the power spectral density of the requested signals and optionally plots the result and/or saves it to file. 
    '''
    cmd_app = ClientType.parse(ctx.obj['cmd_app'])
    try:
        if cmd_app.is_videre():
            dsource = ctx.obj['videre_client'].get_data_file_metadata(
                dataset_idx=index, dataset_id=dset_id, path=path, fail_hard=True)
            tstart = tstart if tstart is not None else dsource.time_range.sec[0]
            dur = dur if dur is not None else 0.250
            ctx.obj['videre_client'].signals().get_psd(
                time_range=make_time_range(
                    time_range=[tstart, tstart+dur], fs=dsource.time_range.fs),
                file=str(Path(file).expanduser().absolute()) if file else None,
                data=False,
                dataset_metadata=dsource)
            msg_id = dsource.id
        else:
            click.Echo('not implemented yet for Allego')
            msg_id = PRIMARY_CACHE_STREAM_GROUP_ID
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    click.echo('{} ({}) : calculated PSD heatmap at {}'.format(
        cmd_app.name, msg_id, time_now()))
    if file:
        click.echo('          saved to {}'.format(file))


# @ signals.command('dashboard', short_help='launch signals dashboard')
# @ click.pass_context
# @ click.option('-idx', '--index',  type=click.INT, default=None, help='dataset index from table', show_default=True)
# @ click.option('-id', '--dset_id',  type=click.STRING, default=None, help='dataset ID from table', show_default=True)
# @ click.option('-p', '--path',  type=click.STRING, default=None, help='path and base name of Radiens file set', show_default=True)
# @ click.option('-d', '--dash',  type=click.Choice(['metrics', 'psd', 'snapshot'], case_sensitive=False), default='metrics', help='dashboard name', show_default=True)
# @ click.option('-s', '--style',  type=click.Choice(['dark', '538', 'fast', 'seaborn'], case_sensitive=False), default='dark', help='dashboard style', show_default=True)
# @ click.option('-did', '--dash_id',  type=click.STRING, default=None, help='radiens-py dash ID', show_default=True)
# @ click.option('-h', '--hub',  type=click.STRING, default='default', help='Radiens hub', show_default=True)
# def dashboard(ctx, index, dset_id, path, dash, style, dash_id, hub):
#     '''
#     Launch a dashboard for a data source linked to the Radiens hub.
#     '''
#     try:
#         dash_enum = DASHBOARD(['metrics', 'psd', 'snapshot'].index(dash))
#         style_enum = DASHBOARD_STYLE(['dark', '538', 'fast', 'seaborn'].index(style))
#         dsource = ctx.obj['videre_client'].get_data_file_metadata(dataset_idx=index, dataset_id=dset_id, path=path, fail_hard=True)
#         ctx.obj['videre_client'].signals().launch_dashboard(dsource, dash_enum, dash_style=style_enum, dash_id=dash_id)
#     except Exception as ex:
#         click.echo('Error: {}'.format(ex))
#         return
#     click.echo('Launching {} dashboard in {} style...'.format(dash_enum.name, style_enum.name))
