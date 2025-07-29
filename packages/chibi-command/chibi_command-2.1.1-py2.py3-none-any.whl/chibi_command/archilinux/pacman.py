from chibi_command import Command


class Pacman( Command ):
    command = 'pacman'
    captive = False

    @classmethod
    def sync( cls ):
        return cls( '-Sy' )

    @classmethod
    def upgrade( cls ):
        return cls( '-Syu' )

    @classmethod
    def install( cls, *packages ):
        return cls( '-S', *packages )
