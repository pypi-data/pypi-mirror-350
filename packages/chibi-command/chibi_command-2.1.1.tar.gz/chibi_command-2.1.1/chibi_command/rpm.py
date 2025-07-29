from chibi_command import Command
from chibi_hybrid.chibi_hybrid import Chibi_hybrid


class RPM( Command ):
    command = 'rpm'
    captive = False
    kw_format = '--{key} {value}'

    @classmethod
    def rpm_import( cls, repository ):
        return cls( **{ 'import': repository } )()

    @Chibi_hybrid
    def query( cls ):
        return cls( '-q', captive=True )

    @query.instancemethod
    def query( self ):
        self.add_args( '-q' )
        return self

    @Chibi_hybrid
    def changelog( cls ):
        return cls( '--changelog' )

    @changelog.instancemethod
    def changelog( self ):
        self.add_args( '--changelog' )
        return self
