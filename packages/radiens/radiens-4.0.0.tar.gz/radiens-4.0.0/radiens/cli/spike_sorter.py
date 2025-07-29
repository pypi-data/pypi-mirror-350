"""
radiens CLI
"""
from datetime import datetime
from pathlib import Path
from pprint import pprint

import click
import pandas as pd
from radiens.utils.config import ERROR_COLOR_FG
from radiens.utils.util import time_now


@ click.group(short_help='spike sorter commands')
@ click.pass_context
def sorter(ctx):
    '''
    Allego real-time spike sorter commands. 

    This command group has sub-commands to control the spike sorter and its data. 
    '''


@ sorter.command('sort', short_help='turn spike sorter on or off')
@ click.pass_context
@ click.argument('arg', type=click.STRING, nargs=-1)
@ click.option('-v', '--verbose',  type=click.Choice(['brief', 'all'], case_sensitive=False), default='brief', help='detail of status', show_default=True)
def sort(ctx, arg, verbose):
    '''
    Controls the spike sorter state. 

    arg: [[on | off]], no argument will print status
    '''
    if len(arg) == 0:
        sorter_status(ctx, verbose)
        return
    if arg[0] not in ['on', 'off']:
        click.echo(click.style(
            '`arg` must be `on` or `off`', fg=ERROR_COLOR_FG))
        return
    try:
        ctx.obj['allego_client'].spike_sorter().set_sorting(arg[0])
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    click.echo(
        'ALLEGO real-time spike sorter set {} at {}'.format(arg[0], time_now()))


@ sorter.command('initialize', short_help='initializes spike sorter')
@ click.pass_context
def init(ctx):
    '''
    Stops, clears, and initializes the spike sorter to its default parameters. 
    '''
    try:
        ctx.obj['allego_client'].spike_sorter().initialize()
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    click.echo(
        'ALLEGO real-time spike sorter initialized at {}'.format(time_now()))


@ sorter.command('rebase', short_help='rebases spike sorter')
@ click.pass_context
def rebase(ctx):
    '''
   Rebases the spike sorter, which clears all spike data and spike templates. 
    '''
    try:
        ctx.obj['allego_client'].spike_sorter().rebase()
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    click.echo('ALLEGO real-time spike sorter rebased at {}'.format(time_now()))


@ sorter.command('clear-spikes', short_help='clears spikes from spike sorter')
@ click.pass_context
def clear_spikes(ctx):
    '''
   Clears all spike data from the spike sorter, but does not clear it's sorting settings or spike templates.
    '''
    try:
        ctx.obj['allego_client'].spike_sorter().clear_spikes()
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    click.echo(
        'ALLEGO real-time spike sorter spikes cleared at {}'.format(time_now()))


@ sorter.command('status', short_help='prints spike sorter status')
@ click.pass_context
@ click.option('-v', '--verbose',  type=click.Choice(['brief', 'all'], case_sensitive=False), default='brief', help='detail of status', show_default=True)
def sorter_status(ctx, verbose):
    '''
    Prints the spike sorter status. 
    '''
    try:
        resp = ctx.obj['allego_client'].spike_sorter().get_state()
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    pprint(resp)


@ sorter.command('params', short_help='prints spike sorter channel parameters')
@ click.pass_context
@ click.option('-v', '--verbose',  type=click.Choice(['brief', 'all'], case_sensitive=False), default='brief', help='detail of parameters', show_default=True)
def sorter_params(ctx, verbose):
    '''
    Prints the spike sorter channel parameters, including threshold levels and threshold states for each channel and also the spike detection window and shadow window.  
    '''
    try:
        resp = ctx.obj['allego_client'].spike_sorter().get_params()
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    pprint(resp)


@ sorter.command('dashboard', short_help='prints spike sorter dashboard')
@ click.pass_context
@ click.option('-v', '--verbose',  type=click.Choice(['brief', 'all'], case_sensitive=False), default='brief', help='detail of dashboard', show_default=True)
def sorter_dash(ctx, verbose):
    '''
    Prints the spike sorter dashboard. 
    '''
    try:
        resp = ctx.obj['allego_client'].spike_sorter().get_dashboard()
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    click.echo('\nALLEGO spike sorter dashboard')
    if verbose in ['brief']:
        print(resp.general)
        print('\n')
        return
    if verbose in ['all']:
        click.echo('GENERAL ')
        print(resp.general)
        click.echo('\nSUMMARY STATISTICS \n')
        print(resp.summary_stats)
        click.echo('\nSTATE \n')
        print(resp.state)
        return


@ sorter.group('set', short_help='sets the mutable spike sorter settings')
@ click.pass_context
def sorter_set(ctx):
    '''
    Set Allego spike sorter settings

    This command group has sub-commands to set various types of spike sorter settings and parameters. 
    '''


@ sorter_set.command('threshold', short_help='sets threshold level(s) and activation state')
@ click.pass_context
@ click.option('-nl', '--neg_thr_level',  type=click.FLOAT, default=None, help='negative threshold level', show_default=True)
@ click.option('-pl', '--pos_thr_level',  type=click.FLOAT, default=None, help='positive threshold level', show_default=True)
@ click.option('-s', '--scale',  type=click.Choice(['uV', 'sd'], case_sensitive=False), default='uV', help='threshold scale in uV or SD', show_default=True)
@ click.option('-na', '--neg_thr_act',  type=click.BOOL, default=None, help='negative threshold activation state', show_default=True)
@ click.option('-pa', '--pos_thr_act',  type=click.BOOL, default=None, help='positive threshold activation state', show_default=True)
@ click.option('-i', '--idxs',  type=click.INT, default=None, help='requested channels (-1-> all channels)', show_default=True)
@ click.option('-w', '--weak_thr',  type=click.BOOL, default=False, help='use True to set the weak threshold', show_default=True)
def sorter_set_threshold(ctx, neg_thr_level, pos_thr_level, scale, neg_thr_act, pos_thr_act, idxs, weak_thr):
    '''
    Sets threshold levels and activation states
    '''
    idxs = None if idxs == -1 else idxs
    try:
        level_msg = ctx.obj['allego_client'].spike_sorter().set_threshold_level(
            neg_thr=neg_thr_level, pos_thr=pos_thr_level, scale=scale, ntv_idxs=idxs, weak_thr=weak_thr, channel_meta=None)
        activate_msg = ctx.obj['allego_client'].spike_sorter().set_threshold(
            neg_thr=neg_thr_act, pos_thr=pos_thr_act, ntv_idxs=idxs, weak_thr=weak_thr, channel_meta=None)
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    click.echo('set thresholds : {}'.format(level_msg))
    click.echo('                 {}'.format(activate_msg))


@ sorter_set.command('window', short_help='sets spike detection window')
@ click.pass_context
@ click.option('-pre', '--pre_thr_ms',  type=click.FLOAT, default=None, help='pre-threshold time [ms]', show_default=True)
@ click.option('-pl', '--post_thr_ms',  type=click.FLOAT, default=None, help='post-threshold time [ms]', show_default=True)
def sorter_set_window(ctx, pre_thr_ms, post_thr_ms):
    '''
    Sets the spike detection window
    '''
    try:
        msg = ctx.obj['allego_client'].spike_sorter().set_spike_window(
            pre_thr_ms=pre_thr_ms, post_thr_ms=post_thr_ms)
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    click.echo('set window  : {}'.format(msg))


@ sorter_set.command('shadow', short_help='sets shadow window')
@ click.pass_context
@ click.option('-s', '--shadow_ms',  type=click.FLOAT, default=None, help='shadow  time [ms]', show_default=True)
def sorter_set_shadow(ctx, shadow_ms):
    '''
    Sets the shadow window
    '''
    try:
        msg = ctx.obj['allego_client'].spike_sorter().set_spike_shadow(
            shadow_ms=shadow_ms)
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    click.echo('set shadow  : {}'.format(msg))
