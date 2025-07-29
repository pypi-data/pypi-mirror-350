from chibi_hybrid.chibi_hybrid import Chibi_hybrid
from chibi_command import Command


class Tar( Command ):
    """
    Examples
    ========
    >>>command = Tar.verbose().extract().file( 'file.tar' )
    >>>command = command.output_directory( '/tmp/' )
    >>>command.preview()
    tar -v -x -f file.tar -C /tmp/
    >>>command.run()
    #run command
    >>>command = Tar.verbose().create().file( 'file.tar' )
    >>>command = command.input_directory( '/tmp/' )
    >>>command.preview()
    tar -v -c -f file.tar /tmp/
    >>>command.run()
    """
    command = 'tar'

    @Chibi_hybrid
    def extract( cls ):
        return cls( '-x' )

    @extract.instancemethod
    def extract( self ):
        self.add_args( '-x' )
        return self

    @Chibi_hybrid
    def file( cls, tar_file ):
        return cls( '-f', tar_file )

    @file.instancemethod
    def file( self, tar_file ):
        self.add_args( '-f', tar_file )
        return self

    @Chibi_hybrid
    def verbose( cls ):
        return cls( '-v' )

    @verbose.instancemethod
    def verbose( self ):
        self.add_args( '-v' )
        return self

    @Chibi_hybrid
    def output_directory( cls, path ):
        return cls( '-C', path )

    @output_directory.instancemethod
    def output_directory( self, path ):
        self.add_args( '-C', path )
        return self

    @Chibi_hybrid
    def input_directory( cls, path ):
        return cls( path )

    @input_directory.instancemethod
    def input_directory( self, path ):
        self.add_args( path )
        return self

    @Chibi_hybrid
    def create( cls ):
        return cls( '-c' )

    @create.instancemethod
    def create( self ):
        self.add_args( '-c' )
        return self

    @Chibi_hybrid
    def compress( cls ):
        return cls( '-z' )

    @compress.instancemethod
    def compress( self ):
        self.add_args( '-z' )
        return self


class Bsdtar( Command ):
    command = 'bsdtar'
