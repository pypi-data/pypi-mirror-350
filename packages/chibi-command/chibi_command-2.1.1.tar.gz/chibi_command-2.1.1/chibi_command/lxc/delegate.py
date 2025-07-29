from chibi_command.nix.systemd_run import System_run
from . import lxc


class LXC( lxc.LXC ):
    delegate = System_run


class Create( lxc.Create ):
    delegate = System_run


class Attach( lxc.Attach ):
    delegate = System_run


class Start( lxc.Start ):
    delegate = System_run


class Stop( lxc.Stop ):
    delegate = System_run


class Destroy( lxc.Destroy ):
    delegate = System_run


class Info( lxc.Info ):
    pass
