Amaret Wind Util
--------

A command-line utility to manage docker containers comprising the Wind cloud application.

TODO: the command will have options to:

1. start all
2. restart all
3. stop all
4. upgrade all
5. ps (like docker ps -a + top)

## INSTALL

during development, you must clone this repo and from within the repo dir run:

`sudo pip install -e .`

add 'wind' to your /etc/hosts pointing to the ip address of your container
runner, ie: `boot2docker ip`

example:

`192.168.59.103 wind`

## TODO

_If we Open Source enough of the Wind stack so that users can run compiles
on their own environment, we should merge this tool into the pip pollen
command._

