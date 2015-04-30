# Copyright Amaret, Inc 2011-2015. All rights reserved.
''' Wind Docker Container Util '''

import os
import time
import json
from subprocess import call
from windutil.argparser import parse
from windutil.scrlogger import ScrLogger

LOG = ScrLogger()

DEFAULT_CONTAINER_CONFIG = [
    {
        'name': 'redis',
        'priority': 0,
        'run': 'docker run --name wind_redis -p 6379 : 6379 -d redis',
        'image': 'redis'
    }
]

CONFIG_FILE_PATH = os.path.expanduser('~') + '/.wutilrc'


def _read_config():
    ''' look up config, if not found init '''
    rcfile = os.path.expanduser('~') + '/.wutilrc'
    if not os.path.exists(rcfile):
        wutilrc = open(CONFIG_FILE_PATH, 'w')
        LOG.debug("writing config to %s" % CONFIG_FILE_PATH)
        wutilrc.write(
            json.dumps(
                DEFAULT_CONTAINER_CONFIG,
                sort_keys=True,
                indent=4,
                separators=(',', ': ')))
        wutilrc.close()
        return DEFAULT_CONTAINER_CONFIG

    LOG.debug("reading config from %s" % CONFIG_FILE_PATH)
    wutilrc = open(CONFIG_FILE_PATH, 'r')
    json_str = wutilrc.read()
    wutilrc.close()
    return json.loads(json_str)


def _load_config():
    '''store by name for key'''
    info = {}
    for cntr in CONTAINER_CONFIG:
        info[cntr['name']] = cntr
    return info

CONTAINER_CONFIG = _read_config()
CONTAINER_INFO = _load_config()


def _rm(pargs):
    '''rm'''
    if pargs.use_all:
        _container_command('rm', _sorted_config_names())
    else:
        _container_command('rm', pargs.containers)


def _start(pargs):
    '''start'''
    if pargs.use_all:
        _container_command('start', _sorted_config_names())
    else:
        _container_command('start', pargs.containers)


def _stop(pargs):
    '''stop'''
    if pargs.use_all:
        _container_command('stop', _reversed_config_names())
    else:
        _container_command('stop', pargs.containers)


def _container_command(command, names):
    '''command'''
    LOG.debug(command + "(ing) ")
    for container in names:
        LOG.debug(command + " " + container)
        call(["docker", command, container])
        if 'delay' in CONTAINER_INFO[container]:
            secs = CONTAINER_INFO[container]['delay']
            LOG.debug("sleeping %s seconds" % (secs))
            time.sleep(secs)


def _run(pargs):
    '''run'''
    LOG.debug("run(ing)")
    names = []
    if pargs.use_all:
        names = _sorted_config_names()
    else:
        names = pargs.containers
    for container in names:
        LOG.debug("run " + container)
        arglist = CONTAINER_INFO[container]['run'].split()
        call(arglist)
        if 'delay' in CONTAINER_INFO[container]:
            secs = CONTAINER_INFO[container]['delay']
            LOG.debug("sleeping %s seconds" % (secs))
            time.sleep(secs)


def _pull(pargs):
    '''run'''
    LOG.debug("pull(ing)")
    names = []
    if pargs.use_all:
        names = _sorted_config_names()
    else:
        names = pargs.containers
    for container in names:
        LOG.debug("pull " + container)
        img = CONTAINER_INFO[container]['image']
        call(['docker', 'pull', img])


def _upgrade(pargs):
    '''upgrade'''
    if pargs.local is False:
        _pull(pargs)
    _stop(pargs)
    _rm(pargs)
    _run(pargs)


def _ps(pargs):
    '''ps'''
    option = '-a'
    from subprocess import Popen, PIPE
    process = Popen(["docker", "ps", option], stdout=PIPE)
    (output, _) = process.communicate()
    process.wait()
    import string
    lines = string.split(output, '\n')
    status_idx = lines[0].index('STATUS')
    print lines[0][status_idx:]
    keys = CONTAINER_INFO.keys()
    for line in lines[1:]:
        if len(line) > 0:
            cname = line[status_idx:].split()[-1]
            if pargs.all or cname in keys:
                print line[status_idx:]


def _reversed_config_names():
    '''reverse list'''
    return [x for x in reversed(_sorted_config_names())]


def _sorted_config_names():
    '''manage dependencies'''
    newlist = sorted(CONTAINER_INFO.values(), key=lambda x: x['priority'],
                     reverse=False)
    return [x['name'] for x in newlist]


def main():
    '''main entry point'''
    # pylint: disable=too-many-branches
    try:
        cmd, pargs = parse()
        pargs.use_all = 'containers' in pargs and pargs.containers[0] == 'all'
        if cmd is 'init':
            print "Initialized"
            return
        if cmd is 'ps':
            _ps(pargs)
            return
        if cmd is 'start':
            _start(pargs)
        if cmd is 'login':
            print "login command"
        if cmd is 'pull':
            _pull(pargs)
        if cmd is 'rm':
            _rm(pargs)
        if cmd is 'run':
            _run(pargs)
        if cmd is 'stop':
            _stop(pargs)
        if cmd is 'upgrade':
            _upgrade(pargs)

    # pylint: disable=broad-except
    except Exception, ex:
        LOG.error(ex)
        import traceback
        trace = traceback.format_exc()
        LOG.trace(trace)
