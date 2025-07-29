"""
radiens CLI
"""
import click
from datetime import datetime
from pprint import pprint

from radiens.api.api_utils.util import launch_server
from radiens.utils.util import (time_now)
import radiens.api.api_videre as api_videre


# ===================== server sub-command set

@ click.group()
@ click.option('--hub', default='default', help='radiens hub name')
@ click.pass_context
def server(ctx, hub):
    ''' pyradiens server command set
    '''
    pprint('in pyradiens server: hub={hub}, ctx={ctx}')


@ server.command()
@ click.option('--hub', default='default', help='radiens hub name')
@ click.pass_context
def start(ctx, hub):
    ''' start radiens-py server in the background
    '''
    try:
        uid = ctx.obj['videre_client']._pyradiens_register_process(addr, hub)
    except Exception as ex:
        print('failed to launch radiens-py server: ex={}'.format(ex))
        return
    print("launched radiens-py server on {} with UID={}".format(addr, uid))

# ===================== system command set


@ click.group()
@ click.option('--hub', default='default', help='radiens hub name')
@ click.pass_context
def system(ctx, hub):
    ''' RADIENS system commands
    '''


system.add_command(server)


@ system.command()
@ click.pass_context
def diag(ctx, hub):
    ''' RADIENS system diagnostics
    '''
    pprint('in system diag: hub={hub}, ctx={ctx}')


# @ system.command()
# @ click.option('--hub', default='default', help='radiens hub name')
# @ click.pass_context
# def register(ctx, hub):
#     ''' register radiens-py with Radiens apps.
#     '''
#     try:
#         ctx.obj['videre_client'].radiens_py_register(hub)
#     except Exception as ex:
#         print('failed to register radiens-py: '+ex)
#         return
#     print("registered radiens-py with Radiens apps at "+time_now())
