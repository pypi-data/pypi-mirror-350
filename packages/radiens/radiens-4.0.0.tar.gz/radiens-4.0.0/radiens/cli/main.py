"""
radiens functional testing CLI
"""

import multiprocessing
import os
import subprocess
from pathlib import Path

import click
# https://matplotlib.org/stable/users/explain/backends.html
from click_shell import shell
from radiens.allego_client import AllegoClient
from radiens.cli.allego import allego
from radiens.cli.file_sys import filesys
from radiens.cli.sys import system
from radiens.cli.videre import videre
from radiens.file_sys_client import FileSystemClient
from radiens.videre_client import VidereClient


@shell(prompt='radiens > ', intro='Starting RADIENS utility (use `> help usage` for usage information)')
@ click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    if 'fsys_client' not in ctx.obj:
        ctx.obj['fsys_client'] = FileSystemClient()
        ctx.obj['allego_client'] = AllegoClient()
        ctx.obj['videre_client'] = VidereClient()
        ctx.obj['cmd_app'] = ''


@ cli.command(short_help='usage information')
@ click.pass_context
def usage(ctx):
    ''' RADIENS CLI utility

        Notes:
        (1) See `readme.md` for instructions.
    '''


@ cli.command('os', short_help='run OS command')
@ click.argument('cmd', nargs=-1)
@ click.pass_context
def os_cmd(ctx, cmd):
    ''' Shell out to run OS command.

        If the command line includes flags, then wrap `cmd` in quotes. 
    '''
    if len(cmd) == 0:
        return
    if cmd[0] in ['cd']:
        if len(cmd) == 2:
            os.chdir(Path(cmd[1]).expanduser().absolute())
        subprocess.run('pwd', shell=True)
        return
    subprocess.run(' '.join(cmd), shell=True)


cli.add_command(filesys)
cli.add_command(system)
cli.add_command(allego)
cli.add_command(videre)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    cli(obj={})
