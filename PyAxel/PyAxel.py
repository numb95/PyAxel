# coding: utf-8
#
# ==========================================
# Developed by Mehdy Khoshnoody           =
# Contact @ mehdy.khoshnoody@gmail.com    =
# More info @ http://mehdy.net            =
# ==========================================
#
__author__ = 'mehdy'
__name__ = 'PyAxel'
__version__ = '0.1'

# import the packages
import sys
import subprocess
import urllib2

import os
import click


def version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version {0}'.format(__version__))
    ctx.exit()


@click.command()
@click.option('-a', '--alternate', is_flag=True, help="Alternate progress indicator")
@click.option('-H', '--header', type=click.STRING, help="Add header string")
@click.option('-l', '--from-list', type=click.File('rw+'), multiple=True,
              help="Download a list of links")  # new added option
@click.option('-n', '--num-connections', type=int, help="Specify maximum number of connections")
@click.option('-N', '--no-proxy', is_flag=True, help="Just don't use any proxy server")
@click.option('-o', '--output', type=click.STRING, help="Specify local output file")
@click.option('-p', '--password', required=False, help="HTTP password")
@click.option('-q', '--quiet', is_flag=True, help="Leave stdout alone")
@click.option('-s', '--max-speed', type=int, help="Specify maximum speed (bytes per second)")
@click.option('-S', '--search', type=click.STRING,
              help="Search for mirrors and download from x servers")  # TODO: not sure about type
@click.option('-u', '--username', type=click.STRING, required=False, help="HTTP username")
@click.option('-U', '--user-agent', type=str, help="Set user agent")  # TODO: not sure about type
@click.option('-v', '--verbose', is_flag=True, help="More status information")
@click.option('-V', '--version', is_flag=True, callback=version, expose_value=False, is_eager=True,
              help="Version information")
@click.argument('url', required=False, nargs=-1)
def generate(alternate, header, from_list, num_connections, no_proxy, output, quiet, max_speed, search, user_agent,
             verbose, url, username, password):
    """
    An Improvement of axel download accelerator.
    """
    cmd = 'axel '
    if alternate: cmd += '-a '
    if header: cmd += '-H ' + header + ' '
    if num_connections: cmd += '-n {0} '.format(str(num_connections))
    if no_proxy: cmd += '-N '
    if output: cmd += '-o ' + output + ' '
    if quiet: cmd += '=q '
    if max_speed: cmd += '-s ' + str(max_speed) + ' '
    if search: cmd += '-S ' + search + ' '
    if user_agent: cmd += '-U ' + user_agent + ' '
    if verbose: cmd += '-v '
    if url:
        for item in url:
            if username and password:
                item = list(item.partition('://'))
                item.insert(2, username + ':' + password + '@')
                item = ''.join(item)
            elif username or password:
                click.echo('Please enter both username and password if you wish do authentication for your requests')
            if not os.path.isfile(urllib2.unquote(item.split('/')[-1])) or os.path.isfile(
                            urllib2.unquote(item.split('/')[-1]) + '.st'):
                click.echo('======================================================================================')
                click.echo(item)
                click.echo('======================================================================================')
                execute(cmd + '"' + item + '"')
            else:
                click.echo('======================================================================================')
                click.echo('The file "%s" exists' % unicode(urllib2.unquote(item.split('/')[-1])) +
                           ' in the downloading directory.\nif you are sure this is something else,' +
                           ' please download it to somewhere else or move the existing file')
                click.echo('======================================================================================')
    # Download for a list of urls
    if from_list:
        for item in from_list:
            file_generic = item.open()
            file_list = file_generic.read().split('\n')
            write_list = list(file_list)
            for url in file_list:
                if username and password:
                    url = list(url.partition('://'))
                    url.insert(2, username + ':' + password + '@')
                    url = ''.join(url)
                elif username or password:
                    click.echo(
                        'Please enter both username and password if you wish do authentication for your requests')
                if not os.path.isfile(urllib2.unquote(url.split('/')[-1])) or os.path.isfile(
                                urllib2.unquote(url.split('/')[-1]) + '.st'):
                    click.echo('======================================================================================')
                    click.echo(url)
                    click.echo('======================================================================================')
                    execute(cmd + '"' + url + '"')
                    write_list.remove(url)
                    file_generic.seek(0)
                    file_generic.truncate()
                    file_generic.flush()
                    file_generic.writelines('\n'.join(write_list))
                    file_generic.flush()
                else:
                    click.echo('======================================================================================')
                    click.echo('The file "%s" exists' % unicode(urllib2.unquote(url.split('/')[-1])) +
                               ' in the downloading directory.\nif you are sure this is something else,' +
                               ' please download it to somewhere else or move the existing file')
                    click.echo('======================================================================================')
                # TODO: return help in no arguments


def execute(cmd):
    """
    Executing generated axel commands

    :param cmd: an axel command to run
    :return:
    """
    proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    while True:
        try:
            out = proc.stderr.read(1)
        except KeyboardInterrupt:
            sys.stdout.flush()
            print ('\nInterrupted by user.\nyou can continue it later.')
            exit()
        if out == '' and proc.poll() is not None:
            print ('\nDownloaded the link successfully')
        if out != '' and out is str:
            sys.stdout.write(out)
            sys.stdout.flush()
        else:
            break

