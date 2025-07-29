from chibi_atlas import Chibi_atlas
from chibi_hybrid.chibi_hybrid import Chibi_hybrid
from chibi_command import Command, Command_result


class Cp( Command ):
    command = 'cp'
    captive = False
    args = [ '-v' ]


class Exit( Command ):
    command = 'exit'
    captive = False


class Ping_result( Command_result ):
    def parse_result( self ):
        lines = self.result.split( '\n' )
        lines = list( filter( bool, lines ) )
        lines.pop( 0 )
        totals = lines[-2].split( ',' )
        self.count = int( totals[0].split( ' ', 1 )[0] )
        self.received = int( totals[1].strip().split( ' ', 1 )[0] )
        self.loss = totals[1].split( ' ', 1 )[0]
        self.pings = []
        for i in range( self.count ):
            line = lines[i]
            numbers = line.rsplit( ':', 1 )[1]
            numbers = list( filter( bool, numbers.split( ' ' ) ) )
            numbers.pop()
            ping = Chibi_atlas()
            self.pings.append( ping )
            for item in numbers:
                k, v = item.split( '=' )
                if k == 'time':
                    ping[ k ] = float( v )
                else:
                    ping[ k ] = int( v )

    def __str__( self ):
        return (
            f"avg = {self.total}/{self.count} = {self.avg}"
        )

    def __repr__( self ):
        return (
            f"ping: avg = {self.total}/{self.count} = {self.avg}"
        )

    @property
    def total( self ):
        return sum( ping.time for ping in self.pings )

    @property
    def avg( self ):
        return self.total / self.count


class Ping( Command ):
    command = 'ping'
    captive = True
    result_class = Ping_result

    @Chibi_hybrid
    def count( cls, amount ):
        return cls( '-c', amount)

    @count.instancemethod
    def count( self, amount ):
        self.add_args( '-c', amount )
        return self

    def build_tuple( self, *args, **kw ):
        if not self.args:
            self.count( 8 )
        return super().build_tuple( *args, **kw )
