=======
History
=======

2.1.1 ( 2025-05-22 )
--------------------

* usar el RPM.query() hace que el comando sea captivo

2.1.0 ( 2025-05-21 )
--------------------

* se agrego el snippet para saber la ip local Ip.get_my_local_ip()
* se agregaron los argumentos para queries de changelog de rpm RPM.query().changelog().run( 'some.rpm' )

2.0.0 ( 2025-05-15 )
--------------------

* se migro el uso de git a https://github.com/dem4ply/chibi_git

1.1.3 ( 2025-03-12 )
--------------------

* se agrego repr a los results de los comandos
* correcion con el f string que faltaba en un logger debug

1.1.0 ( 2024-10-18 )
--------------------

* comando ping

1.0.0 ( 2024-10-18 )
--------------------

* se cambio el comportamiento para que tire una excepcion cada vez que un comando falla

0.9.0 ( 2024-10-17 )
--------------------

* comando de ssh

0.8.0 ( 2024-10-17 )
--------------------

* se agrego comandos para archlinux ( pacman y yay )

0.6.0 (2020-02-19)
------------------

* se agrego cp en chibi_command.commnon

0.0.1 (2020-02-19)
------------------

* First release on PyPI.
