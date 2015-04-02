# Copyright Amaret, Inc 2011-2015. All rights reserved.

''' Pollen Cloud Compiler Client Arg Parser'''

import argparse

def _config_parent_args(parser):
    ''' add param rules'''
    help_str = ('Docker Containers.  Specify a space delimited list of ' \
                'containers.  ie: "wutil <start|stop|rm|run|pull> ' \
                'redis gateway" or ' \
                ' use "all", ie: "wutil <start|stop|rm|run|pull> all".')
    parser.add_argument('containers', nargs='+',
                        action='store', help=help_str)

def _config_login(subparsers, parent_parser):
    ''' configure login command'''
    help_str = 'Log into the docker hub'
    _config('login', help_str, subparsers, parent_parser)

def _config_start(subparsers, parent_parser):
    ''' configure start command '''
    help_str = 'Start containers.  Run this command with parameters \
                indicating what containers you wish to \
                start.  Run "wutil start --help" for \
                parameter help.'
    _config('start', help_str, subparsers, parent_parser)

def _config_stop(subparsers, parent_parser):
    ''' configure stop command '''
    help_str = 'Stop containers.  Run this command with parameters \
                indicating what containers you wish to \
                stop.  Run "wutil stop --help" for \
                parameter help.'
    _config('stop', help_str, subparsers, parent_parser)

def _config_rm(subparsers, parent_parser):
    ''' configure destroy command '''
    help_str = 'rm containers.  Run this command with parameters \
                indicating what containers you wish to \
                destroy. \
                "wutil destroy --help" for parameter help.'
    _config('rm', help_str, subparsers, parent_parser)

def _config_run(subparsers, parent_parser):
    ''' configure run command '''
    help_str = 'run containers.  Run this command with parameters \
                indicating what containers you wish to \
                run ("run" both creates AND starts). \
                "wutil run --help" for parameter help.'
    _config('run', help_str, subparsers, parent_parser)

def _config_upgrade(subparsers, parent_parser):
    ''' configure upgrade command '''
    help_str = 'upgrade containers.  Run this command with parameters \
                indicating what containers you wish to \
                upgrade (stop, rm, run). \
                "wutil upgrade --help" for parameter help.'
    parser = _config('upgrade', help_str, subparsers, parent_parser)

    help_str = 'set if you do not want to pull the latest image from ' \
               'Docker Hub.'
    parser.add_argument('-L', '--local', default=False,
                        action='store_true', help=help_str)

def _config_pull(subparsers, parent_parser):
    ''' configure pull command '''
    help_str = 'Upgrade images.  Run this command with parameters \
                indicating what containers you wish to \
                pull from the latest Docker images.  Run \
                "wutil pull --help" for parameter help.'
    _config('pull', help_str, subparsers, parent_parser)

def _config_untagged(subparsers):
    ''' configure untagged command '''
    help_str = 'rmi all orphans.'
    parser = subparsers.add_parser('untagged', help=help_str)
    def up_fun(parg):
        '''fun'''
        return 'untagged', parg
    parser.set_defaults(func=up_fun)

def _config_init(subparsers):
    ''' configure init command '''
    help_str = 'Initialize the ~/.wutilrc file.  Use this command ' \
                'if you need to modify container names and/or parameters.'
    parser = subparsers.add_parser('init', help=help_str)
    def up_fun(parg):
        '''fun'''
        return 'init', parg
    parser.set_defaults(func=up_fun)

def _config_ps(subparsers):
    ''' configure ps command '''
    help_str = 'Get a terse view of statuses of running containers ' \
               'configured in your ~/.wutilrc file'
    parser = subparsers.add_parser('ps', help=help_str)
    def up_fun(parg):
        '''fun'''
        return 'ps', parg
    parser.set_defaults(func=up_fun)
    help_str = 'show ALL containers, not just ~/.wutilrc configured ones.'
    parser.add_argument('-a', '--all', default=False,
                        action='store_true', help=help_str)

def _config(command, help_str, subparsers, parent_parser):
    ''' configure command '''
    parser = subparsers.add_parser(command, help=help_str,
                                   parents=[parent_parser])
    def up_fun(parg):
        '''fun'''
        return command, parg
    parser.set_defaults(func=up_fun)
    # return parser so that caller can optionally perform additional
    # add_parameter calls on it
    return parser

def parse():
    ''' run arg object'''

    parent_parser = argparse.ArgumentParser(add_help=False)
    _config_parent_args(parent_parser)

    # run the top-level parser
    root_parser = argparse.ArgumentParser(prog='wutil')
    root_help_msg = 'Run "wutil SUB-COMMAND --help" for sub-command-specific \
                     help. For example: "wutil start --help"'
    subparsers = root_parser.add_subparsers(help=root_help_msg)

    #
    # config args
    #
    _config_login(subparsers, parent_parser)
    _config_start(subparsers, parent_parser)
    _config_stop(subparsers, parent_parser)
    _config_pull(subparsers, parent_parser)
    _config_rm(subparsers, parent_parser)
    _config_run(subparsers, parent_parser)
    _config_upgrade(subparsers, parent_parser)
    _config_init(subparsers)
    _config_untagged(subparsers)
    _config_ps(subparsers)
    #
    # process args
    #
    pargs = root_parser.parse_args()

    return pargs.func(pargs)

