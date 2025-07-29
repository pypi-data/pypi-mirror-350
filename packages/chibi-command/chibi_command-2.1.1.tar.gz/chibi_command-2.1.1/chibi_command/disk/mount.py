from chibi_command import Command


class Mount( Command ):
    command = 'mount'
    captive = False


class Umount( Command ):
    command = 'umount'
    captive = False
