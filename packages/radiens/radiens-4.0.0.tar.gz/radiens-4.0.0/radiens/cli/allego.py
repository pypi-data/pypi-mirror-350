"""
radiens CLI
"""
from pathlib import Path

import click
import pandas as pd
from radiens.cli.signal_metrics import metrics
from radiens.cli.spike_sorter import sorter
from radiens.utils.config import ERROR_COLOR_FG
from radiens.utils.util import time_now


@click.group(short_help="allego commands")
@click.pass_context
def allego(ctx):
    """
    ALLEGO command group

    This command group works concurrently with the ALLEGO app to control the data acquisition system.
    """
    ctx.obj["cmd_app"] = "allego"


allego.add_command(sorter)
allego.add_command(metrics)


@allego.command(short_help="control streaming or print the system status")
@click.pass_context
@click.argument("arg", type=click.STRING, nargs=-1)
@click.option(
    "-v",
    "--verbose",
    type=click.Choice(["brief", "all"], case_sensitive=False),
    default="brief",
    help="detail of status",
    show_default=True,
)
def stream(ctx, arg, verbose):
    """
    Turns streaming on or off or prints the stream status.

    arg: [[on | off]], no argument will print status
    """
    if len(arg) == 0:
        status(ctx, verbose)
        return
    if arg[0] not in ["on", "off"]:
        click.echo(click.style(
            "`arg` must be `on` or `off`", fg=ERROR_COLOR_FG))
        return
    try:
        ctx.obj["allego_client"].set_streaming(arg[0])
    except Exception as ex:
        click.echo("Error: {}".format(ex))
        return
    click.echo("ALLEGO stream set to {} at {}".format(arg[0], time_now()))


@allego.command(short_help="prints system status")
@click.pass_context
@click.option(
    "-v",
    "--verbose",
    type=click.Choice(["brief", "all"], case_sensitive=False),
    default="brief",
    help="detail of status",
    show_default=True,
)
def status(ctx, verbose):
    """
    Copy one Radiens-aware data file set to a 'dest' data file set.
    """
    try:
        resp = ctx.obj["allego_client"].get_status()
    except Exception as ex:
        click.echo("Error: {}".format(ex))
        return
    resp.print(verbose)


@allego.command(short_help="control recording or print system status")
@click.pass_context
@click.argument("arg", type=click.STRING, nargs=-1)
@click.option(
    "-v",
    "--verbose",
    type=click.Choice(["brief", "all"], case_sensitive=False),
    default="brief",
    help="detail of status",
    show_default=True,
)
def record(ctx, arg, verbose):
    """
    Turns recording on or off or prints the stream status.

    arg: [[on | off]], no argument will print status

    Notes:
        1. streaming is always turned on when recording is started.
    """
    if len(arg) == 0:
        status(ctx, verbose)
        return
    if arg[0] not in ["on", "off"]:
        click.echo(click.style(
            "`arg` must be `on` or `off`", fg=ERROR_COLOR_FG))
        return
    try:
        ctx.obj["allego_client"].set_recording(arg[0])
    except Exception as ex:
        click.echo("Error: {}".format(ex))
        return
    stat = ctx.obj["allego_client"].get_status()
    if arg[0] in ["on"]:
        click.echo(
            "ALLEGO recording {} ({}); Saving to {}".format(
                arg[0], time_now(), Path(stat.recording.path,
                                         stat.recording.file_name)
            )
        )
    else:
        click.echo(
            "ALLEGO recording {} ({}); Recorded {:.3f} sec to {}".format(
                arg[0],
                time_now(),
                stat.recording.dur_sec,
                Path(stat.recording.path, stat.recording.file_name),
            )
        )


@allego.command(short_help="restart allego with hardware or simulator")
@click.pass_context
@click.option(
    "-sys",
    "--system",
    type=click.Choice(
        [
            "sbpro",
            "sbpro-sinaps-256",
            "sbpro-sinaps-1024" "sbclassic",
            "sim-sine",
            "sim-spikes",
            "open-ephys_usb2",
            "open-ephys_usb3",
            "intan1024",
            "intan512",
            "xdaq-one-rec",
            "xdaq-one-stim",
            "xdaq-core-rec",
            "xdaq-core-stim",
        ],
        case_sensitive=False,
    ),
    default="sim-spikes",
    help="allego system type",
    show_default=True,
)
def restart(ctx, system):
    """
    Restart Allego for specified hardware or simulator system.
    """
    try:
        ctx.obj["allego_client"].restart(system)
    except Exception as ex:
        click.echo("Error: {}".format(ex))
        return
    stat = ctx.obj["allego_client"].get_status()
    print("allego restarted using {}".format(stat.system_mode))


@allego.group(short_help="set allego settings")
@click.pass_context
def set(ctx):
    """
    Set Allego settings

    This command group has sub-commands to set various types of system settings
    """


@set.command("system", short_help="set basic system settings")
@click.pass_context
@click.option(
    "-fs",
    "--samp_freq",
    type=click.INT,
    default=-1,
    help="system sample frequency [samples/sec]",
    show_default=True,
)
def set_system(ctx, samp_freq):
    """
    Sets the basic system settings.

    """
    try:
        if samp_freq > 0:
            ctx.obj["allego_client"].set_sampling_freq(float(samp_freq))
    except Exception as ex:
        click.echo("Error: {}".format(ex))
        return
    stat = ctx.obj["allego_client"].get_status()
    if samp_freq > 0:
        print("new sampling freq = {}".format(stat.sample_freq))


@set.command("record", short_help="set recording parameters")
@click.pass_context
@click.option(
    "-p", "--path", type=click.STRING, default="", help="path", show_default=True
)
@click.option(
    "-n",
    "--name",
    type=click.STRING,
    default="",
    help="base name for composed file name",
    show_default=True,
)
@click.option(
    "-i",
    "--index",
    type=click.INT,
    default=-1,
    help="index for composed file name",
    show_default=True,
)
@click.option(
    "-t",
    "--timestamp",
    type=click.Choice(["-1", "0", "1"]),
    default="-1",
    help="timestamp for file name",
    show_default=True,
)
def set_record(ctx, path, name, index, timestamp):
    """
    Sets the recording settings.

    \b
    --path option value:
        any: path for saving the recording file
        '' : no change
    \b
    --timestamp option value:
        0:  do not include timestamp in composed file name
        1:  do include timestamp in composed file name
        -1: no change

    \b
    --index option value:
        idx >= 0:  index value to include in composed file name
        -1: no change
    """
    try:
        stat = ctx.obj["allego_client"].get_status()
        path = (
            str(Path(path).expanduser().absolute().parent)
            if len(path) > 0
            else stat.recording.path
        )
        name = name if len(name) > 0 else stat.recording.base_name
        index = index if index >= 0 else stat.recording.index
        if timestamp in ["0"]:
            _ts = False
        elif timestamp in ["1"]:
            _ts = True
        else:
            _ts = False if len(stat.recording.timestamp) == 0 else True
        ctx.obj["allego_client"].set_recording_config(path, name, index, _ts)

    except Exception as ex:
        click.echo("Error: {}".format(ex))
        return
    stat = ctx.obj["allego_client"].get_status()
    click.echo("new recording file {}".format(stat.recording.file_name))


@set.command("record", short_help="set recording parameters")
@click.pass_context
@click.option(
    "-p", "--path", type=click.STRING, default="", help="path", show_default=True
)
@click.option(
    "-n",
    "--name",
    type=click.STRING,
    default="",
    help="base name for composed file name",
    show_default=True,
)
@click.option(
    "-i",
    "--index",
    type=click.INT,
    default=-1,
    help="index for composed file name",
    show_default=True,
)
@click.option(
    "-t",
    "--timestamp",
    type=click.Choice(["-1", "0", "1"]),
    default="-1",
    help="timestamp for file name",
    show_default=True,
)
def set_record_params(ctx, path, name, index, timestamp):
    """
    Sets the recording settings.

    \b
    --path option value:
        any: path for saving the recording file
        '' : no change
    \b
    --timestamp option value:
        0:  do not include timestamp in composed file name
        1:  do include timestamp in composed file name
        -1: no change

    \b
    --index option value:
        idx >= 0:  index value to include in composed file name
        -1: no change
    """
    try:
        stat = ctx.obj["allego_client"].get_status()
        path = (
            str(Path(path).expanduser().absolute().parent)
            if len(path) > 0
            else stat.recording.path
        )
        name = name if len(name) > 0 else stat.recording.base_name
        index = index if index >= 0 else stat.recording.index
        if timestamp in ["0"]:
            _ts = False
        elif timestamp in ["1"]:
            _ts = True
        else:
            _ts = False if len(stat.recording.timestamp) == 0 else True
        ctx.obj["allego_client"].set_recording_config(path, name, index, _ts)

    except Exception as ex:
        click.echo("Error: {}".format(ex))
        return
    stat = ctx.obj["allego_client"].get_status()
    click.echo("new recording file {}".format(stat.recording.file_name))
