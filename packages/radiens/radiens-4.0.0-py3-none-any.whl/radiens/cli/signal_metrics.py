"""
radiens CLI
"""
from datetime import datetime
from pathlib import Path
from pprint import pprint

import click
import pandas as pd
# from radiens.lib.graphics.graphics import plot_sig_metrics
from radiens.utils.constants import PRIMARY_CACHE_STREAM_GROUP_ID
from radiens.utils.enums import ClientType
from radiens.utils.util import time_now


@click.group(short_help="signal metrics commands")
@click.pass_context
def metrics(ctx):
    """
    Signal metrics commands.

    This command group has sub-commands for specifying, controlling, and accessing signal metrics.
    """


@metrics.command("clear", short_help="clear signal metrics")
@click.pass_context
@click.option(
    "-idx",
    "--index",
    type=click.INT,
    default=None,
    help="dataset index from table (Allego n/a)",
    show_default=True,
)
@click.option(
    "-id",
    "--dset_id",
    type=click.STRING,
    default=None,
    help="dataset ID from table (Allego n/a)",
    show_default=True,
)
@click.option(
    "-h",
    "--hub",
    type=click.STRING,
    default="default",
    help="Radiens hub (Allego n/a)",
    show_default=True,
)
def clear(ctx, index, dset_id, hub):
    """
    Clears the signal metrics for the requested linked dataset.

    """
    cmd_app = ClientType.parse(ctx.obj["cmd_app"])
    try:
        if cmd_app.is_videre():
            dsource = ctx.obj["videre_client"].get_data_file_metadata(
                dataset_idx=index, dataset_id=dset_id, fail_hard=True
            )
            ctx.obj["videre_client"].signal_metrics().clear(
                dataset_metadata=dsource)
            msg_id = dsource.id
        else:
            click.Echo("not implemented yet for Allego")
            msg_id = PRIMARY_CACHE_STREAM_GROUP_ID
    except Exception as ex:
        click.echo("Error: {}".format(ex))
        return
    click.echo(
        "{} ({}) : cleared signal metrics at {}".format(
            cmd_app.name, msg_id, time_now()
        )
    )


@metrics.command("calculate", short_help="calculates signal metrics")
@click.pass_context
@click.option(
    "-idx",
    "--index",
    type=click.INT,
    default=None,
    help="dataset index from table (Allego n/a)",
    show_default=True,
)
@click.option(
    "-id",
    "--dset_id",
    type=click.STRING,
    default=None,
    help="dataset ID from table (Allego n/a)",
    show_default=True,
)
@click.option(
    "-cmd",
    "--command",
    type=click.Choice(["standard", "custom"], case_sensitive=False),
    default="standard",
    help="calculate command",
    show_default=True,
)
@click.option(
    "-h",
    "--hub",
    type=click.STRING,
    default="default",
    help="Radiens hub (Allego n/a)",
    show_default=True,
)
def calc(ctx, index, dset_id, command, hub):
    """
    Calculates the signal metrics for the requested linked data set.
    """
    cmd_app = ClientType.parse(ctx.obj["cmd_app"])
    try:
        if cmd_app.is_videre():
            dsource = ctx.obj["videre_client"].get_data_file_metadata(
                dataset_idx=index, dataset_id=dset_id, fail_hard=True
            )
            ctx.obj["videre_client"].signal_metrics().calculate(
                dataset_metadata=dsource,
                cmd=command,
                hub_name=hub,
            )
            msg_id = dsource.id
        else:
            click.Echo("not implemented yet for Allego")
            msg_id = PRIMARY_CACHE_STREAM_GROUP_ID
    except Exception as ex:
        click.echo("Error: {}".format(ex))
        return
    click.echo(
        "{} ({}) : (re-)calculated signal metrics at {}".format(
            cmd_app.is_videre(), msg_id, time_now()
        )
    )


@metrics.command("status", short_help="prints the status of the signal metrics service")
@click.pass_context
@click.option(
    "-idx",
    "--index",
    type=click.INT,
    default=None,
    help="dataset index from table (Allego n/a)",
    show_default=True,
)
@click.option(
    "-id",
    "--dset_id",
    type=click.STRING,
    default=None,
    help="dataset ID from table (Allego n/a)",
    show_default=True,
)
@click.option(
    "-h",
    "--hub",
    type=click.STRING,
    default="default",
    help="Radiens hub (Allego n/a)",
    show_default=True,
)
def status(ctx, index, dset_id, hub):
    """
    Prints the status of the stream metrics service.
    """

    cmd_app = ClientType.parse(ctx.obj["cmd_app"])
    try:
        if cmd_app.is_videre():
            dsource = ctx.obj["videre_client"].get_data_file_metadata(
                dataset_idx=index, dataset_id=dset_id, fail_hard=True
            )
            resp = (
                ctx.obj["videre_client"]
                .signal_metrics()
                .get_metrics_status(dataset_metadata=dsource)
            )
            msg_id = dsource.id
        else:
            click.Echo("not implemented yet for Allego")
            msg_id = PRIMARY_CACHE_STREAM_GROUP_ID
    except Exception as ex:
        click.echo("Error: {}".format(ex))
        return
    click.echo(
        "{} ({}) : status at {}".format(
            cmd_app.name, msg_id, time_now())
    )
    resp.print()


@metrics.command("params", short_help="prints the signal metrics parameters")
@click.pass_context
@click.option(
    "-idx",
    "--index",
    type=click.INT,
    default=None,
    help="dataset index from table (Allego n/a)",
    show_default=True,
)
@click.option(
    "-id",
    "--dset_id",
    type=click.STRING,
    default=None,
    help="dataset ID from table (Allego n/a)",
    show_default=True,
)
@click.option(
    "-h",
    "--hub",
    type=click.STRING,
    default="default",
    help="Radiens hub (Allego n/a)",
    show_default=True,
)
def params(ctx, index, dset_id, hub):
    """
    Prints the status of the stream metrics service.
    """
    cmd_app = ClientType.parse(ctx.obj["cmd_app"])
    try:
        if cmd_app.is_videre():
            dsource = ctx.obj["videre_client"].get_data_file_metadata(
                dataset_idx=index, dataset_id=dset_id, fail_hard=True
            )
            resp = (
                ctx.obj["videre_client"]
                .signal_metrics()
                .get_params(dataset_metadata=dsource)
            )
            msg_id = dsource.id
        else:
            click.Echo("not implemented yet for Allego")
            msg_id = PRIMARY_CACHE_STREAM_GROUP_ID
    except Exception as ex:
        click.echo("Error: {}".format(ex))
        return
    click.echo(
        "{} ({}) : parameters at {}".format(
            cmd_app.name, msg_id, time_now()
        )
    )
    print(resp)


@metrics.command("plot", short_help="plots the signal metrics")
@click.option(
    "-idx",
    "--index",
    type=click.INT,
    default=None,
    help="dataset index from table (Allego n/a)",
    show_default=True,
)
@click.option(
    "-id",
    "--dset_id",
    type=click.STRING,
    default=None,
    help="dataset ID from table (Allego n/a)",
    show_default=True,
)
@click.option(
    "-h",
    "--hub",
    type=click.STRING,
    default="default",
    help="Radiens hub (Allego n/a)",
    show_default=True,
)
@click.pass_context
def plot(ctx, index, dset_id, hub):
    """
    Plots the requested signal metrics.
    """
    cmd_app = ClientType.parse(ctx.obj["cmd_app"])
    try:
        if cmd_app.is_videre():
            dsource = ctx.obj["videre_client"].get_data_file_metadata(
                dataset_idx=index, dataset_id=dset_id, fail_hard=True
            )
            resp = (
                ctx.obj["videre_client"]
                .signal_metrics()
                .get_metrics(dataset_metadata=dsource)
            )
            msg_id = dsource.id
        else:
            click.Echo("not implemented yet for Allego")
            msg_id = PRIMARY_CACHE_STREAM_GROUP_ID
    except Exception as ex:
        click.echo("Error: {}".format(ex))
        return
    raise NotImplementedError("plotting not implemented in this package")
    # plot_sig_metrics(resp)
    click.echo(
        "{} ({}) : plotted at {}".format(
            cmd_app.name, msg_id, time_now())
    )


@metrics.group("set", short_help="sets the mutable signal metrics settings")
@click.pass_context
def metrics_set(ctx):
    """
    Sets signal metrics settings.

    This command group has sub-commands to set various signal metrics settings
    """


@metrics_set.command(
    "threshold", short_help="sets event threshold level(s) and activation state"
)
@click.pass_context
@click.option(
    "-nl",
    "--neg_thr_level",
    type=click.FLOAT,
    default=None,
    help="negative threshold level",
    show_default=True,
)
@click.option(
    "-pl",
    "--pos_thr_level",
    type=click.FLOAT,
    default=None,
    help="positive threshold level",
    show_default=True,
)
@click.option(
    "-s",
    "--scale",
    type=click.Choice(["uV", "sd"], case_sensitive=False),
    default="uV",
    help="threshold scale in uV or SD",
    show_default=True,
)
@click.option(
    "-na",
    "--neg_thr_act",
    type=click.BOOL,
    default=None,
    help="negative threshold activation state",
    show_default=True,
)
@click.option(
    "-pa",
    "--pos_thr_act",
    type=click.BOOL,
    default=None,
    help="positive threshold activation state",
    show_default=True,
)
@click.option(
    "-i",
    "--idxs",
    type=click.INT,
    default=None,
    help="requested channels (-1-> all channels)",
    show_default=True,
)
@click.option(
    "-w",
    "--weak_thr",
    type=click.BOOL,
    default=False,
    help="use True to set the weak threshold",
    show_default=True,
)
@click.option(
    "-idx",
    "--index",
    type=click.INT,
    default=None,
    help="dataset index from table (Allego n/a)",
    show_default=True,
)
@click.option(
    "-id",
    "--dset_id",
    type=click.STRING,
    default=None,
    help="dataset ID from table (Allego n/a)",
    show_default=True,
)
@click.option(
    "-h",
    "--hub",
    type=click.STRING,
    default="default",
    help="Radiens hub (Allego n/a)",
    show_default=True,
)
def metrics_set_threshold(
    ctx,
    neg_thr_level,
    pos_thr_level,
    scale,
    neg_thr_act,
    pos_thr_act,
    idxs,
    weak_thr,
    index,
    dset_id,
    hub,
):
    """
    Sets threshold levels and activation states
    """
    msg_id = PRIMARY_CACHE_STREAM_GROUP_ID
    idxs = None if idxs == -1 else idxs
    try:
        level_msg = (
            ctx.obj["allego_client"]
            .spike_sorter()
            .set_threshold_level(
                neg_thr=neg_thr_level,
                pos_thr=pos_thr_level,
                scale=scale,
                ntv_idxs=idxs,
                weak_thr=weak_thr,
                channel_meta=None,
            )
        )
        activate_msg = (
            ctx.obj["allego_client"]
            .spike_sorter()
            .set_threshold(
                neg_thr=neg_thr_act,
                pos_thr=pos_thr_act,
                ntv_idxs=idxs,
                weak_thr=weak_thr,
                channel_meta=None,
            )
        )
    except Exception as ex:
        click.echo("Error: {}".format(ex))
        return
    click.echo(
        "{} ({}) : set thresholds at {}".format(
            ctx.obj["cmd_app"].upper(), msg_id, time_now()
        )
    )
    click.echo("set thresholds : {}".format(level_msg))
    click.echo("                 {}".format(activate_msg))


@metrics_set.command("window", short_help="sets event detection window")
@click.pass_context
@click.option(
    "-pre",
    "--pre_thr_ms",
    type=click.FLOAT,
    default=None,
    help="pre-threshold time [ms]",
    show_default=True,
)
@click.option(
    "-pl",
    "--post_thr_ms",
    type=click.FLOAT,
    default=None,
    help="post-threshold time [ms]",
    show_default=True,
)
@click.option(
    "-idx",
    "--index",
    type=click.INT,
    default=None,
    help="dataset index from table (Allego n/a)",
    show_default=True,
)
@click.option(
    "-id",
    "--dset_id",
    type=click.STRING,
    default=None,
    help="dataset ID from table (Allego n/a)",
    show_default=True,
)
@click.option(
    "-h",
    "--hub",
    type=click.STRING,
    default="default",
    help="Radiens hub (Allego n/a)",
    show_default=True,
)
def metrics_set_window(ctx, pre_thr_ms, post_thr_ms, index, dset_id, hub):
    """
    Sets the event detection window
    """

    msg_id = PRIMARY_CACHE_STREAM_GROUP_ID
    try:
        msg = (
            ctx.obj["allego_client"]
            .spike_sorter()
            .set_spike_window(pre_thr_ms=pre_thr_ms, post_thr_ms=post_thr_ms)
        )
    except Exception as ex:
        click.echo("Error: {}".format(ex))
        return
    click.echo(
        "{} ({}) : set window at {}".format(
            ctx.obj["cmd_app"].upper(), msg_id, time_now()
        )
    )
    click.echo("set window  : {}".format(msg))


@metrics_set.command("shadow", short_help="sets shadow window")
@click.pass_context
@click.option(
    "-s",
    "--shadow_ms",
    type=click.FLOAT,
    default=None,
    help="shadow  time [ms]",
    show_default=True,
)
@click.option(
    "-idx",
    "--index",
    type=click.INT,
    default=None,
    help="dataset index from table (Allego n/a)",
    show_default=True,
)
@click.option(
    "-id",
    "--dset_id",
    type=click.STRING,
    default=None,
    help="dataset ID from table (Allego n/a)",
    show_default=True,
)
@click.option(
    "-h",
    "--hub",
    type=click.STRING,
    default="default",
    help="Radiens hub (Allego n/a)",
    show_default=True,
)
def metrics_set_shadow(ctx, shadow_ms, index, dset_id, hub):
    """
    Sets the event detection shadow window
    """
    msg_id = PRIMARY_CACHE_STREAM_GROUP_ID
    cmd_app = ClientType.parse(ctx.obj["cmd_app"])
    try:
        msg = (
            ctx.obj["allego_client"]
            .spike_sorter()
            .set_spike_shadow(shadow_ms=shadow_ms)
        )
    except Exception as ex:
        click.echo("Error: {}".format(ex))
        return
    click.echo(
        "{} ({}) : set shadow windowq at {}".format(
            cmd_app.name, msg_id, time_now()
        )
    )
    click.echo("set shadow  : {}".format(msg))
