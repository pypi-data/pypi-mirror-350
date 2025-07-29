from chibi.snippet import regex
from chibi.atlas import Chibi_atlas
from chibi_command import Command, Command_result
from chibi_hybrid.chibi_hybrid import Chibi_hybrid


__all__ = [ 'Create', 'Start', 'Stop', 'Attach', 'Info', 'Destroy' ]

re_ipv6 = (
    r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|'
    r'([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:)'
    r'{1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1'
    r',5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}'
    r':){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{'
    r'1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA'
    r'-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a'
    r'-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0'
    r'-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,'
    r'4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}'
    r':){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9'
    r'])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0'
    r'-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]'
    r'|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]'
    r'|1{0,1}[0-9]){0,1}[0-9]))' )


class Info_result( Command_result ):
    def parse_result( self ):
        if not self:
            return
        result = Chibi_atlas()
        for line in self.result.split( '\n' ):
            line = line.strip()
            if not line:
                continue
            k, v = line.split( ':', 1 )
            v = v.strip()
            if ( 'ip' == k.lower()
                    and regex.test( re_ipv6, v ) ):
                k = f"{k}v6"
            result[k.lower()] = v.lower()
        self.result = result

    # lo dejare de usar
    @property
    def is_running( self ):
        return self and self.result.state == 'running'


class LXC( Command ):
    command = 'lxc'
    captive = False

    @Chibi_hybrid
    def name( cls, name ):
        return cls( '-n', name )

    @name.instancemethod
    def name( self, name ):
        self.add_args( '-n', name )
        return self


class Create( LXC ):
    command = 'lxc-create'
    captive = False

    @Chibi_hybrid
    def template( cls, template ):
        return cls( '-t', template )

    @template.instancemethod
    def template( self, template ):
        self.add_args( '-t', template )
        return self

    def parameters( self, *args ):
        self.add_args( '--', *args )
        return self


class Start( LXC ):
    command = 'lxc-start'
    captive = False

    @Chibi_hybrid
    def daemon( cls ):
        return cls( '-d' )

    @daemon.instancemethod
    def daemon( self ):
        self.add_args( '-d' )
        return self


class Stop( LXC ):
    command = 'lxc-stop'
    captive = False


class Attach( LXC ):
    command = 'lxc-attach'
    args = ( '--clear-env', )
    captive = False

    @Chibi_hybrid
    def set_var( cls, name, value ):
        return cls( '--set-var', f"{name}={value}" )

    @set_var.instancemethod
    def set_var( self, name, value ):
        self.add_args( '--set-var', f"{name}={value}" )
        return self

    def build_tuple( self, *args, **kw ):
        new_args = []
        for arg in args:
            if isinstance( arg, Command ):
                new_args += list( arg.build_tuple() )
            else:
                new_args.append( arg )
        if self.delegate:
            delegate_tuple = self.build_delegate()
            return (
                *delegate_tuple, self.command,
                *self.build_kw( **kw ), *self.args, '--', *new_args )
        return (
            self.command, *self.build_kw( **kw ), *self.args, '--', *new_args )


class Info( LXC ):
    command = 'lxc-info'
    captive = True
    args = ( '-H', )
    result_class = Info_result


class Destroy( LXC ):
    command = 'lxc-destroy'
    captive = False
