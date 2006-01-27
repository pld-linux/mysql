# TODO:
# - trigger that prepares system from pre-cluster into cluster
# - trigger /etc/mysqld.conf into /etc/mysql/mysqld.conf. Solve possible
#   conflict with /var/lib/mysql/mysqld.conf
# - C(XX)FLAGS for innodb subdirs are overriden by ./configre!
# - http://bugs.mysql.com/bug.php?id=16470
#
# Conditional build:
%bcond_with	bdb	# Berkeley DB support
%bcond_without	innodb	# Without InnoDB support
%bcond_without	raid	# Without raid
%bcond_without	ssl	# Without OpenSSL
%bcond_without	tcpd	# Without libwrap (tcp_wrappers) support
%bcond_without	big_tables	# Support tables with more than 4G rows even on 32 bit platforms
#
%include	/usr/lib/rpm/macros.perl
#define	_snap	20060111
Summary:	MySQL: a very fast and reliable SQL database engine
Summary(de):	MySQL: ist eine SQL-Datenbank
Summary(fr):	MySQL: un serveur SQL rapide et fiable
Summary(pl):	MySQL: bardzo szybka i niezawodna baza danych (SQL)
Summary(pt_BR):	MySQL: Um servidor SQL rápido e confiável
Summary(ru):	MySQL - ÂÙÓÔÒÙÊ SQL-ÓÅÒ×ÅÒ
Summary(uk):	MySQL - Û×ÉÄËÉÊ SQL-ÓÅÒ×ÅÒ
Summary(zh_CN):	MySQLÊı¾İ¿â·şÎñÆ÷
Name:		mysql
Version:	5.0.18
Release:	2
License:	GPL + MySQL FLOSS Exception
Group:		Applications/Databases
Source0:	http://ftp.gwdg.de/pub/misc/mysql/Downloads/MySQL-5.0/%{name}-%{version}.tar.gz
# Source0-md5:	f18153b0239aaa03fc5a751f2d82cb71
#Source0:	http://downloads.mysql.com/snapshots/mysql-5.0/%{name}-%{version}-nightly-%{_snap}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Source4:	%{name}d.conf
Source5:	%{name}-clusters.conf
Source6:	%{name}.monitrc
Source7:	%{name}-ndb.init
Source8:	%{name}-ndb.sysconfig
Source9:	%{name}-ndb-mgm.init
Source10:	%{name}-ndb-mgm.sysconfig
Source11:	%{name}-ndb-cpc.init
Source12:	%{name}-ndb-cpc.sysconfig
Source13:	%{name}-client.conf
Patch0:		%{name}-libs.patch
Patch1:		%{name}-libwrap.patch
Patch2:		%{name}-c++.patch
Patch3:		%{name}-info.patch
Patch4:		%{name}-sql-cxx-pic.patch
Patch5:		%{name}-noproc.patch
Patch6:		%{name}-fix_privilege_tables.patch
Patch7:		%{name}-align.patch
Patch8:		%{name}-client-config.patch
Patch9:		%{name}-build.patch
Patch10:	%{name}-alpha.patch
URL:		http://www.mysql.com/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_bdb:BuildRequires:	db3-devel}
BuildRequires:	libstdc++-devel >= 5:3.0
BuildRequires:	libtool
%{?with_tcpd:BuildRequires:	libwrap-devel}
BuildRequires:	ncurses-devel >= 4.2
%{?with_ssl:BuildRequires:	openssl-devel >= 0.9.7d}
BuildRequires:	perl-DBI
BuildRequires:	perl-devel >= 1:5.6.1
BuildRequires:	readline-devel >= 4.2
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	sed >= 4.0
BuildRequires:	texinfo
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(triggerpostun):	sed >= 4.0
Requires:	/usr/bin/setsid
Requires:	rc-scripts >= 0.2.0
Provides:	MySQL-server
Provides:	group(mysql)
Provides:	msqlormysql
Provides:	user(mysql)
Obsoletes:	MySQL
Obsoletes:	mysql-server
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_sbindir}
%define		_localstatedir	/var/lib/mysql
%define		_mysqlhome	/home/services/mysql

%define		_noautoreqdep	'perl(DBD::mysql)'

%description
MySQL is a true multi-user, multi-threaded SQL (Structured Query
Language) database server. SQL is the most popular database language
in the world. MySQL is a client/server implementation that consists of
a server daemon mysqld and many different client programs/libraries.

The main goals of MySQL are speed, robustness and easy to use. MySQL
was originally developed because we at Tcx needed a SQL server that
could handle very big databases with magnitude higher speed than what
any database vendor could offer to us. We have now been using MySQL
since 1996 in a environment with more than 40 databases, 10,000
tables, of which more than 500 have more than 7 million rows. This is
about 50G of mission critical data.

The base upon which MySQL is built is a set of routines that have been
used in a highly demanding production environment for many years.
While MySQL is still in development, it already offers a rich and
highly useful function set.

%description -l fr
MySQL est un serveur de bases de donnees SQL vraiment multi-usagers et
multi-taches. Le langage SQL est le langage de bases de donnees le
plus populaire au monde. MySQL est une implementation client/serveur
qui consiste en un serveur (mysqld) et differents
programmes/bibliotheques clientes.

Les objectifs principaux de MySQL sont: vitesse, robustesse et
facilite d'utilisation. MySQL fut originalement developpe parce que
nous, chez Tcx, avions besoin d'un serveur SQL qui pouvait gerer de
tres grandes bases de donnees avec une vitesse d'un ordre de magnitude
superieur a ce que n'importe quel vendeur pouvait nous offrir. Nous
utilisons MySQL depuis 1996 dans un environnement avec plus de 40
bases de donnees, 10000 tables, desquelles plus de 500 ont plus de 7
millions de lignes. Ceci represente environ 50G de donnees critiques.

A la base de la conception de MySQL, on retrouve une serie de routines
qui ont ete utilisees dans un environnement de production pendant
plusieurs annees. Meme si MySQL est encore en developpement, il offre
deja une riche et utile serie de fonctions.

%description -l pl
MySQL to prawdziwie wielou¿ytkownikowy, wielow±tkowy serwer baz danych
SQL. SQL jest najpopularniejszym na ¶wiecie jêzykiem u¿ywanym do baz
danych. MySQL to implementacja klient/serwer sk³adaj±ca siê z demona
mysqld i wielu ró¿nych programów i bibliotek klienckich.

G³ównymi celami MySQL-a s± szybko¶æ, potêga i ³atwo¶æ u¿ytkowania.
MySQL oryginalnie by³ tworzony, poniewa¿ autorzy w Tcx potrzebowali
serwera SQL do obs³ugi bardzo du¿ych baz danych z szybko¶ci± o wiele
wiêksz±, ni¿ mogli zaoferowaæ inni producenci baz danych. U¿ywaj± go
od 1996 roku w ¶rodowisku z ponad 40 bazami danych, 10 000 tabel, z
których ponad 500 zawiera ponad 7 milionów rekordów - w sumie oko³o
50GB krytycznych danych.

Baza, na której oparty jest MySQL, sk³ada siê ze zbioru procedur,
które by³y u¿ywane w bardzo wymagaj±cym ¶rodowisku produkcyjnym przez
wiele lat. Pomimo, ¿e MySQL jest ci±gle rozwijany, ju¿ oferuje bogaty
i u¿yteczny zbiór funkcji.

%description -l de
MySQL ist eine SQL-Datenbank. Allerdings ist sie im Gegensatz zu
Oracle, DB2 oder PostgreSQL keine relationale Datenbank. Die Daten
werden zwar in zweidimensionalen Tabellen gespeichert und können mit
einem Primärschlüssel versehen werden. Es ist aber keine Definition
eines Fremdschlüssels möglich. Der Benutzer ist somit bei einer
MySQL-Datenbank völlig allein für die (referenzielle) Integrität der
Daten verantwortlich. Allein durch die Nutzung externer
Tabellenformate, wie InnoDB bzw Berkeley DB wird eine Relationalität
ermöglicht. Diese Projekte sind aber getrennt von MySQL zu betrachten.

%description -l pt_BR
O MySQL é um servidor de banco de dados SQL realmente multiusuário e
multi-tarefa. A linguagem SQL é a mais popular linguagem para banco de
dados no mundo. O MySQL é uma implementação cliente/servidor que
consiste de um servidor chamado mysqld e diversos
programas/bibliotecas clientes. Os principais objetivos do MySQL são:
velocidade, robustez e facilidade de uso. O MySQL foi originalmente
desenvolvido porque nós na Tcx precisávamos de um servidor SQL que
pudesse lidar com grandes bases de dados e com uma velocidade muito
maior do que a que qualquer vendedor podia nos oferecer. Estamos
usando o MySQL desde 1996 em um ambiente com mais de 40 bases de dados
com 10.000 tabelas, das quais mais de 500 têm mais de 7 milhões de
linhas. Isto é o equivalente a aproximadamente 50G de dados críticos.
A base da construção do MySQL é uma série de rotinas que foram usadas
em um ambiente de produção com alta demanda por muitos anos. Mesmo o
MySQL estando ainda em desenvolvimento, ele já oferece um conjunto de
funções muito ricas e úteis. Veja a documentação para maiores
informações.

%description -l ru
MySQL - ÜÔÏ SQL (Structured Query Language) ÓÅÒ×ÅÒ ÂÁÚÙ ÄÁÎÎÙÈ. MySQL
ÂÙÌÁ ÎÁĞÉÓÁÎÁ Michael'ÏÍ (monty) Widenius'ÏÍ. óÍ. ÆÁÊÌ CREDITS ×
ÄÉÓÔÒÉÂÕÔÉ×Å ÎÁ ĞÒÅÄÍÅÔ ÄÒÕÇÉÈ ÕŞÁÓÔÎÉËÏ× ĞÒÏÅËÔÁ É ĞÒÏŞÅÊ ÉÎÆÏÒÍÁÃÉÉ
Ï MySQL.

%description -l uk
MySQL - ÃÅ SQL (Structured Query Language) ÓÅÒ×ÅÒ ÂÁÚÉ ÄÁÎÉÈ. MySQL
ÂÕÌÏ ÎÁĞÉÓÁÎÏ Michael'ÏÍ (monty) Widenius'ÏÍ. äÉ×. ÆÁÊÌ CREDITS ×
ÄÉÓÔÒÉÂÕÔÉ×¦ ÄÌÑ ¦ÎÆÏÒÍÁÃ¦§ ĞÒÏ ¦ÎÛÉÈ ÕŞÁÓÎÉË¦× ĞÒÏÅËÔÕ ÔÁ ¦ÎÛÏ§
¦ÎÆÏÒÍÁÃ¦§.

%package extras
Summary:	MySQL additional utilities
Summary(pl):	Dodatkowe narzêdzia do MySQL
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description extras
MySQL additional utilities except Perl scripts (they may be found in
%{name}-extras-perl package).

%description extras -l pl
Dodatkowe narzêdzia do MySQL - z wyj±tkiem skryptów Perla (które s± w
pakiecie %{name}-extras-perl).

%package extras-perl
Summary:	MySQL additional utilities written in Perl
Summary(pl):	Dodatkowe narzêdzia do MySQL napisane w Perlu
Group:		Applications/Databases
Requires:	%{name}-extras = %{version}-%{release}
Requires:	perl(DBD::mysql)

%description extras-perl
MySQL additional utilities written in Perl.

%description extras-perl -l pl
Dodatkowe narzêdzia do MySQL napisane w Perlu.

%package client
Summary:	MySQL - Client
Summary(pl):	MySQL - Klient
Summary(pt):	MySQL - Cliente
Summary(ru):	MySQL ËÌÉÅÎÔ
Summary(uk):	MySQL ËÌ¦¤ÎÔ
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	MySQL-client

%description client
This package contains the standard MySQL clients.

%description client -l fr
Ce package contient les clients MySQL standards.

%description client -l pl
Standardowe programy klienckie MySQL.

%description client -l pt_BR
Este pacote contém os clientes padrão para o MySQL.

%description client -l ru
üÔÏÔ ĞÁËÅÔ ÓÏÄÅÒÖÉÔ ÔÏÌØËÏ ËÌÉÅÎÔ MySQL.

%description client -l uk
ãÅÊ ĞÁËÅÔ Í¦ÓÔÉÔØ Ô¦ÌØËÉ ËÌ¦¤ÎÔÁ MySQL.

%package libs
Summary:	Shared libraries for MySQL
Summary(pl):	Biblioteki dzielone MySQL
Group:		Applications/Databases
Obsoletes:	libmysql10
Obsoletes:	mysql-doc < 4.1.12

%description libs
Shared libraries for MySQL.

%description libs -l pl
Biblioteki dzielone MySQL.

%package devel
Summary:	MySQL - Development header files and libraries
Summary(pl):	MySQL - Pliki nag³ówkowe i biblioteki dla programistów
Summary(pt):	MySQL - Medições de desempenho
Summary(ru):	MySQL - ÈÅÄÅÒÙ É ÂÉÂÌÉÏÔÅËÉ ÒÁÚÒÁÂÏÔŞÉËÁ
Summary(uk):	MySQL - ÈÅÄÅÒÉ ÔÁ Â¦ÂÌ¦ÏÔÅËÉ ĞÒÏÇÒÁÍ¦ÓÔÁ
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%{?with_ssl:Requires:	openssl-devel}
Requires:	zlib-devel
Obsoletes:	MySQL-devel
Obsoletes:	libmysql10-devel

%description devel
This package contains the development header files and libraries
necessary to develop MySQL client applications.

%description devel -l fr
Ce package contient les fichiers entetes et les librairies de
developpement necessaires pour developper des applications clientes
MySQL.

%description devel -l pl
Pliki nag³ówkowe i biblioteki konieczne do kompilacji aplikacji
klienckich MySQL.

%description devel -l pt_BR
Este pacote contém os arquivos de cabeçalho (header files) e
bibliotecas necessárias para desenvolver aplicações clientes do MySQL.

%description devel -l ru
üÔÏÔ ĞÁËÅÔ ÓÏÄÅÒÖÉÔ ÈÅÄÅÒÙ É ÂÉÂÌÉÏÔÅËÉ ÒÁÚÒÁÂÏÔŞÉËÁ, ÎÅÏÂÈÏÄÉÍÙÅ ÄÌÑ
ÒÁÚÒÁÂÏÔËÉ ËÌÉÅÎÔÓËÉÈ ĞÒÉÌÏÖÅÎÉÊ.

%description devel -l uk
ãÅÊ ĞÁËÅÔ Í¦ÓÔÉÔØ ÈÅÄÅÒÉ ÔÁ Â¦ÂÌ¦ÏÔÅËÉ ĞÒÏÇÒÁÍ¦ÓÔÁ, ÎÅÏÂÈ¦ÄÎ¦ ÄÌÑ
ÒÏÚÒÏÂËÉ ĞÒÏÇÒÁÍ-ËÌ¦¤ÎÔ¦×.

%package static
Summary:	MySQL static libraries
Summary(pl):	Biblioteki statyczne MySQL
Summary(ru):	MySQL - ÓÔÁÔÉŞÅÓËÉÅ ÂÉÂÌÉÏÔÅËÉ
Summary(uk):	MySQL - ÓÔÁÔÉŞÎ¦ Â¦ÂÌ¦ÏÔÅËÉ
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	MySQL-static

%description static
MySQL static libraries.

%description static -l pl
Biblioteki statyczne MySQL.

%description static -l ru
üÔÏÔ ĞÁËÅÔ ÓÏÄÅÒÖÉÔ ÓÔÁÔÉŞÅÓËÉÅ ÂÉÂÌÉÏÔÅËÉ ÒÁÚÒÁÂÏÔŞÉËÁ, ÎÅÏÂÈÏÄÉÍÙÅ
ÄÌÑ ÒÁÚÒÁÂÏÔËÉ ËÌÉÅÎÔÓËÉÈ ĞÒÉÌÏÖÅÎÉÊ.

%description static -l uk
ãÅÊ ĞÁËÅÔ Í¦ÓÔÉÔØ ÓÔÁÔÉŞÎ¦ Â¦ÂÌ¦ÏÔÅËÉ ĞÒÏÇÒÁÍ¦ÓÔÁ, ÎÅÏÂÈ¦ÄÎ¦ ÄÌÑ
ÒÏÚÒÏÂËÉ ĞÒÏÇÒÁÍ-ËÌ¦¤ÎÔ¦×.

%package bench
Summary:	MySQL - Benchmarks
Summary(pl):	MySQL - Programy testuj±ce szybko¶æ dzia³ania bazy
Summary(pt):	MySQL - Medições de desempenho
Summary(ru):	MySQL - ÂÅÎŞÍÁÒËÉ
Summary(uk):	MySQL - ÂÅÎŞÍÁÒËÉ
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-client
Requires:	perl(DBD::mysql)
Obsoletes:	MySQL-bench

%description bench
This package contains MySQL benchmark scripts and data.

%description bench -l pl
Programy testuj±ce szybko¶æ serwera MySQL.

%description bench -l pt_BR
Este pacote contém medições de desempenho de scripts e dados do MySQL.

%description bench -l ru
üÔÏÔ ĞÁËÅÔ ÓÏÄÅÒÖÉÔ ÓËÒÉĞÔÙ É ÄÁÎÎÙÅ ÄÌÑ ÏÃÅÎËÉ ĞÒÏÉÚ×ÏÄÉÔÅÌØÎÏÓÔÉ
MySQL.

%description bench -l uk
ãÅÊ ĞÁËÅÔ Í¦ÓÔÉÔØ ÓËÒÉĞÔÉ ÔÁ ÄÁÎ¦ ÄÌÑ ÏÃ¦ÎËÉ ĞÒÏÄÕËÔÉ×ÎÏÓÔ¦ MySQL.

%package doc
Summary:	MySQL manual
Summary(pl):	Podrêcznik u¿ytkownika MySQL
Group:		Applications/Databases

%description doc
This package contains manual in HTML format.

%description doc -l pl
Podrêcznik MySQL-a w formacie HTML.

%package ndb
Summary:	MySQL - NDB Storage Engine Daemon
Summary(pl):	MySQL - demon silnika przechowywania danych NDB
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description ndb
This package contains the standard MySQL NDB Storage Engine Daemon.

%description ndb -l pl
Ten pakiet zawiera standardowego demona silnika przechowywania danych
NDB.

%package ndb-client
Summary:	MySQL - NDB Clients
Summary(pl):	MySQL - programy klienckie NDB
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description ndb-client
This package contains the standard MySQL NDB Clients.

%description ndb-client -l pl
Ten pakiet zawiera standardowe programy klienckie MySQL NDB.

%package ndb-mgm
Summary:	MySQL - NDB Management Daemon
Summary(pl):	MySQL - demon zarz±dzaj±cy NDB
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description ndb-mgm
This package contains the standard MySQL NDB Management Daemon.

%description ndb-mgm -l pl
Ten pakiet zawiera standardowego demona zarz±dzaj±cego MySQL NDB.

%package ndb-cpc
Summary:	MySQL - NDB CPC Daemon
Summary(pl):	MySQL - demon NDB CPC
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description ndb-cpc
This package contains the standard MySQL NDB CPC Daemon.

%description ndb-cpc -l pl
Ten pakiet zawiera standardowego demona MySQL NDB CPC.

%prep
%setup -q %{?_snap:-n %{name}-%{version}-nightly-%{_snap}}
%patch0 -p1
%{?with_tcpd:%patch1 -p1}
%patch2 -p1
%patch3 -p1
%ifarch alpha
# this is strange: mysqld functions for UDF modules are not explicitly defined,
# so -rdynamic is used; in such case gcc3+ld on alpha doesn't like C++ vtables
# in objects compiled without -fPIC
%patch4 -p1
%patch10 -p1
%endif
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%{__perl} -pi -e 's@(ndb_bin_am_ldflags)="-static"@$1=""@' configure.in

%build
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}

# The compiler flags are as per their "official" spec ;)
CXXFLAGS="%{rpmcflags} -felide-constructors -fno-rtti -fno-exceptions %{!?debug:-fomit-frame-pointer}"
CFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"

# NOTE: the PS, FIND_PROC, KILL, CHECK_PID are not used by PLD Linux
# and therefore do not add BR on these. These are here just to satisfy
# configure.

%configure \
	PS='/bin/ps' \
	FIND_PROC='/bin/ps p $$PID' \
	KILL='/bin/kill' \
	CHECK_PID='/bin/kill -0 $$PID' \
	--enable-assembler \
	--enable-largefile=yes \
	--enable-shared \
	--enable-static \
	--enable-thread-safe-client \
	--with%{!?with_bdb:out}-berkeley-db \
	--with%{!?with_innodb:out}-innodb \
	--with%{!?with_raid:out}-raid \
	--with%{!?with_ssl:out}-openssl \
	--with%{!?with_tcpd:out}-libwrap \
	%{?with_big_tables:--with-big-tables} \
	--with-comment="PLD Linux Distribution MySQL RPM" \
	--with%{!?debug:out}-debug \
	--with%{!?debug:out}-ndb-debug \
	--with-embedded-server \
	--with-extra-charsets=all \
	--with-low-memory \
	--with-mysqld-user=mysql \
	--with-named-curses-libs="-lncurses" \
	--with-named-thread-libs="-lpthread" \
	--with-unix-socket-path=/var/lib/mysql/mysql.sock \
	--with-archive-storage-engine \
	--with-vio \
	--with-ndbcluster \
	--without-readline \
	--without-libedit \
	--without-docs
#	--with-mysqlfs
#	--with-ndb-test --with-ndb-docs

# NOTE that /var/lib/mysql/mysql.sock is symlink to real sock file
# (it defaults to first cluster but user may change it to whatever
# cluster it wants)

echo -e "all:\ninstall:\nclean:\nlink_sources:\n" > libmysqld/examples/Makefile

%{__make} \
	benchdir=$RPM_BUILD_ROOT%{_datadir}/sql-bench

%{__make} -C Docs mysql.info

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,rc.d/init.d,sysconfig,mysql,monit} \
	   $RPM_BUILD_ROOT/var/{log/{archiv,}/mysql,lib/mysql} \
	   $RPM_BUILD_ROOT{%{_infodir},%{_mysqlhome}}

%if %{with bdb}
install -d $RPM_BUILD_ROOT/var/lib/mysql/bdb/{log,tmp}
%endif

# Make install
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	benchdir=%{_datadir}/sql-bench \
	libsdir=/tmp
# libsdir is to avoid installing innodb static libs in $RPM_BUILD_ROOT../libs

install Docs/mysql.info $RPM_BUILD_ROOT%{_infodir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mysql
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/mysql
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/mysql
# This is template for configuration file which is created after 'service mysql init'
install %{SOURCE4} mysqld.conf
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/mysql/clusters.conf
install %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/monit
touch $RPM_BUILD_ROOT/var/log/mysql/{err,log,update}

# remove innodb directives from mysqld.conf if mysqld is configured without
%if %{without innodb}
	cp mysqld.conf mysqld.tmp
	awk 'BEGIN { RS="\n\n" } !/innodb/ { printf("%s\n\n", $0) }' < mysqld.tmp > mysqld.conf
%endif

# remove berkeley-db directives from mysqld.conf if mysqld is configured without
%if %{without bdb}
	cp mysqld.conf mysqld.tmp
	awk 'BEGIN { RS="\n\n" } !/bdb/ { printf("%s\n\n", $0) }' < mysqld.tmp > mysqld.conf
%endif

install mysqld.conf $RPM_BUILD_ROOT%{_datadir}/mysql/mysqld.conf
install %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/mysql/mysql-client.conf

# NDB
install %{SOURCE7} $RPM_BUILD_ROOT/etc/rc.d/init.d/mysql-ndb
install %{SOURCE8} $RPM_BUILD_ROOT/etc/sysconfig/mysql-ndb
install %{SOURCE9} $RPM_BUILD_ROOT/etc/rc.d/init.d/mysql-ndb-mgm
install %{SOURCE10} $RPM_BUILD_ROOT/etc/sysconfig/mysql-ndb-mgm
install %{SOURCE11} $RPM_BUILD_ROOT/etc/rc.d/init.d/mysql-ndb-cpc
install %{SOURCE12} $RPM_BUILD_ROOT/etc/sysconfig/mysql-ndb-cpc
# remove .txt variants for .sys messages
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/*/*.txt

mv -f $RPM_BUILD_ROOT%{_libdir}/mysql/lib* $RPM_BUILD_ROOT%{_libdir}
sed -i -e 's,%{_libdir}/mysql,%{_libdir},' $RPM_BUILD_ROOT%{_libdir}/libmysqlclient{,_r}.la

# remove known unpackaged files
rm -rf $RPM_BUILD_ROOT%{_prefix}/mysql-test

# rename not to be so generic name
mv $RPM_BUILD_ROOT%{_bindir}/{,mysql_}comp_err
mv $RPM_BUILD_ROOT%{_bindir}/{,mysql_}resolve_stack_dump

# not useful without -debug build
%{!?debug:rm -f $RPM_BUILD_ROOT%{_bindir}/mysql_resolve_stack_dump}
# generate symbols file, so one can generate backtrace using it
# mysql_resolve_stack_dump -s /usr/share/mysql/mysqld.sym -n mysqld.stack.
# http://dev.mysql.com/doc/refman/5.0/en/using-stack-trace.html
%{?debug:nm -n $RPM_BUILD_ROOT%{_sbindir}/mysqld > $RPM_BUILD_ROOT%{_datadir}/mysql/mysqld.sym}

# functionality in initscript / rpm
rm $RPM_BUILD_ROOT%{_bindir}/mysql_create_system_tables
rm $RPM_BUILD_ROOT%{_bindir}/mysql_install_db
rm $RPM_BUILD_ROOT%{_bindir}/mysqld_safe
rm $RPM_BUILD_ROOT%{_bindir}/mysqld_multi
rm $RPM_BUILD_ROOT%{_mandir}/man1/mysqld_{multi,safe}*
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/fill_help_tables.sql
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/mysql-log-rotate
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/mysql.server
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/binary-configure
rm $RPM_BUILD_ROOT%{_bindir}/mysql_waitpid
rm $RPM_BUILD_ROOT%{_mandir}/man1/mysql.server*
rm $RPM_BUILD_ROOT%{_mandir}/man1/safe_mysqld*

# in %doc
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/*.{ini,cnf}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 89 mysql
%useradd -u 89 -d %{_mysqlhome} -s /bin/sh -g mysql -c "MySQL Server" mysql

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/sbin/chkconfig --add mysql

if [ "$1" = 1 ]; then
	%banner -e %{name}-4.1.x <<-EOF
	If you want to use new help tables in mysql 4.1.x then you'll need to import the help data:
	zcat %{_docdir}/%{name}-%{version}/fill_help_tables.sql.gz | mysql mysql
EOF
#'
fi

%service mysql restart
exit 0

%preun
if [ "$1" = "0" ]; then
	%service -q mysql stop
	/sbin/chkconfig --del mysql
fi

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
if [ "$1" = "0" ]; then
	%userremove mysql
	%groupremove mysql
fi

%post ndb
/sbin/chkconfig --add mysql-ndb
if [ -f /var/lock/subsys/mysql-ndb ]; then
        /etc/rc.d/init.d/mysql-ndb restart >&2
else
        echo "Run \"/etc/rc.d/init.d/mysql-ndb start\" to start mysql NDB engine." >&2
fi

%preun ndb
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/mysql-ndb ]; then
                /etc/rc.d/init.d/mysql-ndb stop
        fi
        /sbin/chkconfig --del mysql-ndb
fi

%post ndb-mgm
/sbin/chkconfig --add mysql-ndb-mgm
if [ -f /var/lock/subsys/mysql-ndb-mgm ]; then
        /etc/rc.d/init.d/mysql-ndb-mgm restart >&2
else
        echo "Run \"/etc/rc.d/init.d/mysql-ndb-mgm start\" to start mysql NDB management node." >&2
fi

%preun ndb-mgm
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/mysql-ndb-mgm ]; then
                /etc/rc.d/init.d/mysql-ndb-mgm stop
        fi
        /sbin/chkconfig --del mysql-ndb-mgm
fi

%post ndb-cpc
/sbin/chkconfig --add mysql-ndb-cpc
if [ -f /var/lock/subsys/mysql-ndb-cpc ]; then
        /etc/rc.d/init.d/mysql-ndb-cpc restart >&2
else
        echo "Run \"/etc/rc.d/init.d/mysql-ndb-cpc start\" to start mysql NDB CPC." >&2
fi

%preun ndb-cpc
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/mysql-ndb-cpc ]; then
                /etc/rc.d/init.d/mysql-ndb-cpc stop
        fi
        /sbin/chkconfig --del mysql-ndb-cpc
fi

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%triggerpostun -- mysql <= 4.0.20-2
# For clusters in /etc/mysql/clusters.conf
if [ -f "/etc/sysconfig/mysql" ]; then
	. /etc/sysconfig/mysql
	if [ -n "$MYSQL_DB_CLUSTERS" ]; then
		for i in "$MYSQL_DB_CLUSTERS"; do
			echo "$i/mysqld.conf=$i" >> /etc/mysql/clusters.conf
		done
		echo "# Do not use **obsolete** option MYSQL_DB_CLUSTERS" >> /etc/sysconfig/mysql
		echo "# USE /etc/mysql/clusters.conf instead" >> /etc/sysconfig/mysql
		echo "Converted clusters from MYSQL_DB_CLUSTERS to /etc/mysql/clusters.conf."
		echo "You NEED to fix your /etc/sysconfig/mysql and verify /etc/mysql/clusters.conf."
	fi
fi

%triggerpostun -- mysql <= 4.1.1
# For better compatibility with prevoius versions:
for config in $(awk -F= '!/^#/ && /=/{print $1}' /etc/mysql/clusters.conf); do
	if echo "$config" | grep -q '^/'; then
		config_file="$config"
	elif [ -f "/etc/mysql/$config" ]; then
		config_file=/etc/mysql/$config
	else
		clusterdir=$(awk -F= "/^$config/{print \$2}" /etc/mysql/clusters.conf)
		if [ -z "$clusterdir" ]; then
			echo >&2 "Can't find cluster dir for $config!"
			echo >&2 "Please remove extra (leading) spaces from /etc/mysql/clusters.conf"
			exit 1
		fi
		config_file="$clusterdir/mysqld.conf"
	fi

	if [ ! -f "$config_file" ]; then
			echo >&2 "Lost myself! Please report this (with above errors, if any) to http://bugs.pld-linux.org/"
			exit 1
	fi
	echo "Adding option old-passwords to config: $config_file"
	echo "If you want to use new, better passwords - remove it"

	# sed magic to add 'old-passwords' to [mysqld] section
	sed -i -e '/./{H;$!d;};x;/\[mysqld\]/{
		a
		a; Compatibility options:
		aold-passwords
	}
	' $config_file
done

%banner -e %{name}-4.1.x <<-EOF
	If you want to use new help tables in mysql 4.1.x then you'll need to import the help data:
	zcat %{_docdir}/%{name}-%{version}/fill_help_tables.sql.gz | mysql mysql
EOF
#'

%files
%defattr(644,root,root,755)
%doc support-files/*.cnf support-files/*.ini scripts/fill_help_tables.sql
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/mysql
%attr(754,root,root) /etc/rc.d/init.d/mysql
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mysql
%attr(640,root,mysql) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mysql/clusters.conf
%attr(750,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/monit/*.monitrc
%attr(755,root,root) %{_bindir}/innochecksum
%attr(755,root,root) %{_bindir}/myisamchk
%attr(755,root,root) %{_bindir}/myisamlog
%attr(755,root,root) %{_bindir}/myisampack
%attr(755,root,root) %{_bindir}/mysql_fix_privilege_tables
%attr(755,root,root) %{_bindir}/my_print_defaults
%attr(755,root,root) %{_sbindir}/mysqld
%{_mandir}/man1/mysql_fix_privilege_tables.1*
%{_mandir}/man1/mysqld.1*
%{_mandir}/man1/myisamchk.1*
%{_mandir}/man1/myisamlog.1*
%{_mandir}/man1/myisampack.1*

%attr(700,mysql,mysql) %{_mysqlhome}
# root:root is proper here for AC mysql.rpm while mysql:mysql is potential security hole
%attr(751,root,root) /var/lib/mysql
%attr(750,mysql,mysql) %dir /var/log/mysql
%attr(750,mysql,mysql) %dir /var/log/archiv/mysql
%attr(640,mysql,mysql) %ghost /var/log/mysql/*

%{_infodir}/mysql.info*
%dir %{_datadir}/mysql
# This is template for configuration file which is created after 'service mysql init'
%{_datadir}/mysql/mysqld.conf
%{_datadir}/mysql/charsets
%{_datadir}/mysql/english
%{_datadir}/mysql/mysql_fix_privilege_tables.sql
%lang(cs) %{_datadir}/mysql/czech
%lang(da) %{_datadir}/mysql/danish
%lang(de) %{_datadir}/mysql/german
%lang(el) %{_datadir}/mysql/greek
%lang(es) %{_datadir}/mysql/spanish
%lang(et) %{_datadir}/mysql/estonian
%lang(fr) %{_datadir}/mysql/french
%lang(hu) %{_datadir}/mysql/hungarian
%lang(it) %{_datadir}/mysql/italian
%lang(ja) %{_datadir}/mysql/japanese
%lang(ko) %{_datadir}/mysql/korean
%lang(nl) %{_datadir}/mysql/dutch
%lang(nb) %{_datadir}/mysql/norwegian
%lang(nn) %{_datadir}/mysql/norwegian-ny
%lang(pl) %{_datadir}/mysql/polish
%lang(pt) %{_datadir}/mysql/portuguese
%lang(ro) %{_datadir}/mysql/romanian
%lang(ru) %{_datadir}/mysql/russian
%lang(sr) %{_datadir}/mysql/serbian
%lang(sk) %{_datadir}/mysql/slovak
%lang(sv) %{_datadir}/mysql/swedish
%lang(uk) %{_datadir}/mysql/ukrainian

%files extras
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/msql2mysql
%attr(755,root,root) %{_bindir}/myisam_ftdump
%attr(755,root,root) %{_bindir}/mysql_secure_installation
%attr(755,root,root) %{_bindir}/mysql_tzinfo_to_sql
%attr(755,root,root) %{_bindir}/mysqlcheck
%attr(755,root,root) %{_bindir}/perror
%attr(755,root,root) %{_bindir}/replace
%attr(755,root,root) %{_bindir}/resolveip
%{_mandir}/man1/msql2mysql.1*
%{_mandir}/man1/mysqlcheck.1*
%{_mandir}/man1/perror.1*
%{_mandir}/man1/replace.1*

%files extras-perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysql_convert_table_format
%attr(755,root,root) %{_bindir}/mysqldumpslow
%attr(755,root,root) %{_bindir}/mysqlhotcopy
%attr(755,root,root) %{_bindir}/mysql_setpermission
%attr(755,root,root) %{_bindir}/mysql_zap
%attr(755,root,root) %{_bindir}/mysql_find_rows
%attr(755,root,root) %{_bindir}/mysqlaccess
%attr(755,root,root) %{_bindir}/mysql_fix_extensions
%attr(755,root,root) %{_bindir}/mysql_explain_log
%attr(755,root,root) %{_bindir}/mysql_tableinfo
%{_mandir}/man1/mysql_zap.1*
%{_mandir}/man1/mysqlaccess.1*
%{_mandir}/man1/mysqlhotcopy.1*

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysql
%attr(755,root,root) %{_bindir}/mysqlbug
%attr(755,root,root) %{_bindir}/mysqldump
%attr(755,root,root) %{_bindir}/mysqlimport
%attr(755,root,root) %{_sbindir}/mysqlmanager*
%attr(755,root,root) %{_bindir}/mysqlshow
%attr(755,root,root) %{_bindir}/mysqlbinlog
%attr(755,root,root) %{_bindir}/mysqladmin
%attr(755,root,root) %{_bindir}/mysqltest*
%{_mandir}/man1/mysql.1*
%{_mandir}/man1/mysqladmin.1*
%{_mandir}/man1/mysqldump.1*
%{_mandir}/man1/mysqlshow.1*
%{_mandir}/man1/mysqlmanager.1*
%{_mandir}/man1/mysqlbinlog.1*
%{_mandir}/man1/mysqlimport.1*

%files libs
%defattr(644,root,root,755)
%doc EXCEPTIONS-CLIENT
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(751,root,root) %dir %{_sysconfdir}/mysql
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mysql/mysql-client.conf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysql_config
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_bindir}/*comp_err
%attr(755,root,root) %{_bindir}/*resolve_stack_dump
%{?debug:%{_datadir}/mysql/mysqld.sym}
%{_libdir}/lib*.la
%{_libdir}/lib*[!tr].a
%{_includedir}/mysql
%{_mandir}/man1/mysql_config.1*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*[tr].a

%files bench
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysqltest
%attr(755,root,root) %{_bindir}/mysql_client_test
%dir %{_datadir}/sql-bench
%{_datadir}/sql-bench/[CDRl]*
%attr(755,root,root) %{_datadir}/sql-bench/[bcgirst]*
# wrong dir?
%{_datadir}/mysql/mi_test_all.res
%attr(755,root,root) %{_datadir}/mysql/mi_test_all

#%files doc
#%defattr(644,root,root,755)
#%doc Docs/manual.html Docs/manual_toc.html

%files ndb
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ndbd
%attr(754,root,root) /etc/rc.d/init.d/mysql-ndb
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mysql-ndb

%files ndb-client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ndb_*

%files ndb-mgm
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ndb_mgmd
%attr(754,root,root) /etc/rc.d/init.d/mysql-ndb-mgm
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mysql-ndb-mgm

%files ndb-cpc
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ndb_cpcd
%attr(754,root,root) /etc/rc.d/init.d/mysql-ndb-cpc
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mysql-ndb-cpc
