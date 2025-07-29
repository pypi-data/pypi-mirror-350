import functools
import itertools
from chibi_command import Command, Command_result
from chibi_hybrid.chibi_hybrid import Chibi_hybrid


class Wmctrl_window:
    def __init__( self, *args ):
        self.id = args[0]
        self.gravity = int( args[1] )
        self.pid = args[2]
        self.x = int( args[3] )
        self.y = int( args[4] )
        self.w = int( args[5] )
        self.h = int( args[6] )
        self.program = args[7]
        self.host = args[8]
        self.title = args[9]

    def __str__( self ):
        return (
            f"{self.id} {self.column} "
            f"{self.row} {self.program} {self.title}"
        )

    @property
    def can_move( self ):
        return self.gravity >= 0

    @property
    def row( self ):
        desktop = self.get_desktop()
        y, r_y = desktop.dg_y, ( desktop.vp_y + self.y )
        size_y = desktop.dg_y / desktop.rows
        if r_y < size_y:
            return 0
        return y // r_y

    @property
    def column( self ):
        desktop = self.get_desktop()
        try:
            return desktop.dg_x // ( desktop.vp_x + self.x )
        except ZeroDivisionError:
            return 0

    @functools.cache
    def get_desktop( self ):
        result = list( Wmctrl.desktop().run() )
        return result[0]

    @property
    def select( self ):
        return Wmctrl.select( self.id )

    def remove( self, *flags ):
        return self.select.remove( *flags )

    def move( self, x, y, w, h ):
        return self.select.move( 0, x, y, w, h )


class Wmctrl_desktop_obj:
    def __init__( self, *args ):
        self.id = args[0]
        self.is_principal = args[1]
        self.dg = args[2]
        self.dg_value = args[3]
        self.dg_x, self.dg_y = self.dg_value.split( 'x' )
        self.dg_x, self.dg_y = int( self.dg_x ), int( self.dg_y )
        self.vp = args[4]
        self.vp_value = args[5]
        self.vp_x, self.vp_y = self.vp_value.split( ',' )
        self.vp_x, self.vp_y = int( self.vp_x ), int( self.vp_y )
        self.wa = args[6]
        self.wa_value = args[7]
        self.resolution = args[8]
        self.resolution_x, self.resolution_y = self.resolution.split( 'x' )
        self.resolution_x, self.resolution_y = (
            int( self.resolution_x ), int( self.resolution_y ) )
        self.title = args[9]

    @property
    def current_column( self ):
        try:
            return self.dg_x // self.vp_x
        except ZeroDivisionError:
            return 0

    @property
    def current_row( self ):
        try:
            return self.dg_y // self.vp_y
        except ZeroDivisionError:
            return 0

    @property
    def columns( self ):
        return self.dg_x // self.resolution_x

    @property
    def rows( self ):
        return self.dg_y // self.resolution_y

    def __str__( self ):
        return f"{self.id} {self.dg_value} {self.resolution}"


class Wmctrl_list( Command_result ):
    def parse_result( self ):
        lines = self.result.splitlines()
        split = functools.partial( str.split, maxsplit=9)
        lines = map( split, lines )
        lines = itertools.starmap( Wmctrl_window, lines )
        self.result = lines

    def __iter__( self ):
        return iter( self.result )


class Wmctrl_desktop( Command_result ):
    def parse_result( self ):
        lines = self.result.splitlines()
        split = functools.partial( str.split, maxsplit=9)
        lines = map( split, lines )
        lines = itertools.starmap( Wmctrl_desktop_obj, lines )
        self.result = lines

    def __iter__( self ):
        return iter( self.result )


class Wmctrl( Command ):
    command = 'wmctrl'
    captive = True
    result_class = Wmctrl_list

    @Chibi_hybrid
    def list( cls ):
        return cls( '-lGpx', )

    @list.instancemethod
    def list( self ):
        self.add_args( '-lGpx' )
        return self

    @Chibi_hybrid
    def desktop( cls ):
        return cls( '-d', result_class=Wmctrl_desktop, )

    @Chibi_hybrid
    def select( cls, window_id ):
        return cls( '-i', '-r', window_id )

    @Chibi_hybrid
    def toggle( cls, *flags ):
        parameter = ",".join( [ 'toggle', *flags ] )
        return cls( '-b', parameter )

    @toggle.instancemethod
    def toggle( self, *flags ):
        parameter = ",".join( [ 'toggle', *flags ] )
        self.add_args( '-b', parameter )
        return self

    @Chibi_hybrid
    def remove( cls, *flags ):
        parameter = ",".join( [ 'remove', *flags ] )
        return cls( '-b', parameter )

    @remove.instancemethod
    def remove( self, *flags ):
        parameter = ",".join( [ 'remove', *flags ] )
        self.add_args( '-b', parameter )
        return self

    @Chibi_hybrid
    def move( cls, gravity, x, y, w, h ):
        return cls( '-e', f"{gravity},{x},{y},{w},{h}" )  # noqa

    @move.instancemethod
    def move( self, gravity, x, y, w, h ):
        self.add_args( '-e', f"{gravity},{x},{y},{w},{h}" )
        return self
