# TODO:
# - C(XX)FLAGS for innodb subdirs are overriden by ./configure!
# - http://bugs.mysql.com/bug.php?id=16470
#
# Conditional build:
%bcond_without	big_tables	# Support tables with more than 4G rows even on 32 bit platforms
%bcond_without	federated	# Federated storage engine support
%bcond_without	innodb		# InnoDB storage engine support
%bcond_without	raid		# Without raid
%bcond_without	ssl		# Without OpenSSL
%bcond_without	tcpd		# Without libwrap (tcp_wrappers) support
%bcond_with	bdb		# Berkeley DB support
%bcond_without	sphinx		# Sphinx storage engine support
#
%include	/usr/lib/rpm/macros.perl
#define	_snap	20060111
Summary:	MySQL: a very fast and reliable SQL database engine
Summary(de.UTF-8):	MySQL: ist eine SQL-Datenbank
Summary(fr.UTF-8):	MySQL: un serveur SQL rapide et fiable
Summary(pl.UTF-8):	MySQL: bardzo szybka i niezawodna baza danych (SQL)
Summary(pt_BR.UTF-8):	MySQL: Um servidor SQL rápido e confiável
Summary(ru.UTF-8):	MySQL - быстрый SQL-сервер
Summary(uk.UTF-8):	MySQL - швидкий SQL-сервер
Summary(zh_CN.UTF-8):	MySQL数据库服务器
Name:		mysql
Version:	5.0.68
Release:	0.1
License:	GPL + MySQL FLOSS Exception
Group:		Applications/Databases
#Source0:	ftp://ftp.mysql.com/pub/mysql/src/%{name}-%{version}.tar.gz
#Source0:	http://ftp.gwdg.de/pub/misc/mysql/Downloads/MySQL-5.0/%{name}-%{version}.tar.gz
#Source0:	http://mysql.he.net/Downloads/MySQL-5.0/%{name}-%{version}.tar.gz
Source0:	http://mirror.provenscaling.com/mysql/enterprise/source/5.0/%{name}-%{version}.tar.gz
# Source0-md5:	b3351d755bd62fd203bae777a77ccfef
Source100:	http://www.sphinxsearch.com/downloads/sphinx-0.9.8.tar.gz
# Source100-md5:	347e547b79b733778d7553ede34e0aac
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Source4:	%{name}d.conf
Source5:	%{name}-clusters.conf
Source7:	%{name}-ndb.init
Source8:	%{name}-ndb.sysconfig
Source9:	%{name}-ndb-mgm.init
Source10:	%{name}-ndb-mgm.sysconfig
Source11:	%{name}-ndb-cpc.init
Source12:	%{name}-ndb-cpc.sysconfig
Source13:	%{name}-client.conf
Patch0:		%{name}-libs.patch
Patch1:		%{name}-sphinx.patch
Patch2:		%{name}-c++.patch
Patch3:		%{name}-info.patch
Patch4:		%{name}-sql-cxx-pic.patch
Patch5:		%{name}-noproc.patch
Patch6:		%{name}-fix_privilege_tables.patch
Patch7:		%{name}-align.patch
Patch8:		%{name}-client-config.patch
Patch9:		%{name}-build.patch
Patch10:	%{name}-alpha.patch
Patch11:	%{name}-ndb-ldflags.patch
Patch12:	%{name}-bug-20153.patch
Patch13:	%{name}-bug-34192.patch
Patch14:	%{name}-bug-16470.patch
Patch15:	%{name}-system-users.patch
Patch16:	%{name}-bug-39021.patch
# Percona patches, http://www.percona.com/percona-lab.html
Patch17:	%{name}-control_flush_and_merge_and_read.patch
Patch18:	%{name}-control_io-threads.patch
Patch19:	%{name}-microslow_innodb.patch
Patch21:	%{name}-show_patches.patch
Patch22:	%{name}-split_buf_pool_mutex_fixed_optimistic_safe.patch
Patch23:	%{name}-userstats-testsuite.patch
Patch24:	%{name}-userstats.patch
#Patch25:	%{name}-acc-pslist.patch
URL:		http://www.mysql.com/products/database/mysql/community_edition.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
%{?with_bdb:BuildRequires:	db3-devel}
BuildRequires:	flex
BuildRequires:	libstdc++-devel >= 5:3.0
BuildRequires:	libtool
%{?with_tcpd:BuildRequires:	libwrap-devel}
BuildRequires:	ncurses-devel >= 4.2
%{?with_ssl:BuildRequires:	openssl-devel >= 0.9.7d}
BuildRequires:	perl-DBI
BuildRequires:	perl-devel >= 1:5.6.1
BuildRequires:	readline-devel >= 4.2
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.268
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
Requires:	%{name}-charsets = %{version}-%{release}
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
# CFLAGS for innodb are altered
%undefine	configure_cache

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

%description -l fr.UTF-8
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

%description -l pl.UTF-8
MySQL to prawdziwie wieloużytkownikowy, wielowątkowy serwer baz danych
SQL. SQL jest najpopularniejszym na świecie językiem używanym do baz
danych. MySQL to implementacja klient/serwer składająca się z demona
mysqld i wielu różnych programów i bibliotek klienckich.

Głównymi celami MySQL-a są szybkość, potęga i łatwość użytkowania.
MySQL oryginalnie był tworzony, ponieważ autorzy w Tcx potrzebowali
serwera SQL do obsługi bardzo dużych baz danych z szybkością o wiele
większą, niż mogli zaoferować inni producenci baz danych. Używają go
od 1996 roku w środowisku z ponad 40 bazami danych, 10 000 tabel, z
których ponad 500 zawiera ponad 7 milionów rekordów - w sumie około
50GB krytycznych danych.

Baza, na której oparty jest MySQL, składa się ze zbioru procedur,
które były używane w bardzo wymagającym środowisku produkcyjnym przez
wiele lat. Pomimo, że MySQL jest ciągle rozwijany, już oferuje bogaty
i użyteczny zbiór funkcji.

%description -l de.UTF-8
MySQL ist eine SQL-Datenbank. Allerdings ist sie im Gegensatz zu
Oracle, DB2 oder PostgreSQL keine relationale Datenbank. Die Daten
werden zwar in zweidimensionalen Tabellen gespeichert und können mit
einem Primärschlüssel versehen werden. Es ist aber keine Definition
eines Fremdschlüssels möglich. Der Benutzer ist somit bei einer
MySQL-Datenbank völlig allein für die (referenzielle) Integrität der
Daten verantwortlich. Allein durch die Nutzung externer
Tabellenformate, wie InnoDB bzw Berkeley DB wird eine Relationalität
ermöglicht. Diese Projekte sind aber getrennt von MySQL zu betrachten.

%description -l pt_BR.UTF-8
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

%description -l ru.UTF-8
MySQL - это SQL (Structured Query Language) сервер базы данных. MySQL
была написана Michael'ом (monty) Widenius'ом. См. файл CREDITS в
дистрибутиве на предмет других участников проекта и прочей информации
о MySQL.

%description -l uk.UTF-8
MySQL - це SQL (Structured Query Language) сервер бази даних. MySQL
було написано Michael'ом (monty) Widenius'ом. Див. файл CREDITS в
дистрибутиві для інформації про інших учасників проекту та іншої
інформації.

%package charsets
Summary:	MySQL - character sets definitions
Summary(pl.UTF-8):	MySQL - definicje kodowań znaków
Group:		Applications/Databases

%description charsets
This package contains character sets definitions needed by both client
and server.

%description charsets -l pl.UTF-8
Ten pakiet zawiera definicje kodowań znaków potrzebne dla serwera i
klienta.

%package extras
Summary:	MySQL additional utilities
Summary(pl.UTF-8):	Dodatkowe narzędzia do MySQL
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description extras
MySQL additional utilities except Perl scripts (they may be found in
%{name}-extras-perl package).

%description extras -l pl.UTF-8
Dodatkowe narzędzia do MySQL - z wyjątkiem skryptów Perla (które są w
pakiecie %{name}-extras-perl).

%package extras-perl
Summary:	MySQL additional utilities written in Perl
Summary(pl.UTF-8):	Dodatkowe narzędzia do MySQL napisane w Perlu
Group:		Applications/Databases
Requires:	%{name}-extras = %{version}-%{release}
Requires:	perl(DBD::mysql)

%description extras-perl
MySQL additional utilities written in Perl.

%description extras-perl -l pl.UTF-8
Dodatkowe narzędzia do MySQL napisane w Perlu.

%package client
Summary:	MySQL - Client
Summary(pl.UTF-8):	MySQL - Klient
Summary(pt.UTF-8):	MySQL - Cliente
Summary(ru.UTF-8):	MySQL клиент
Summary(uk.UTF-8):	MySQL клієнт
Group:		Applications/Databases
Requires:	%{name}-charsets = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	MySQL-client

%description client
This package contains the standard MySQL clients.

%description client -l fr.UTF-8
Ce package contient les clients MySQL standards.

%description client -l pl.UTF-8
Standardowe programy klienckie MySQL.

%description client -l pt_BR.UTF-8
Este pacote contém os clientes padrão para o MySQL.

%description client -l ru.UTF-8
Этот пакет содержит только клиент MySQL.

%description client -l uk.UTF-8
Цей пакет містить тільки клієнта MySQL.

%package libs
Summary:	Shared libraries for MySQL
Summary(pl.UTF-8):	Biblioteki dzielone MySQL
Group:		Libraries
Obsoletes:	libmysql10
Obsoletes:	mysql-doc < 4.1.12

%description libs
Shared libraries for MySQL.

%description libs -l pl.UTF-8
Biblioteki dzielone MySQL.

%package devel
Summary:	MySQL - Development header files and libraries
Summary(pl.UTF-8):	MySQL - Pliki nagłówkowe i biblioteki dla programistów
Summary(pt.UTF-8):	MySQL - Medições de desempenho
Summary(ru.UTF-8):	MySQL - хедеры и библиотеки разработчика
Summary(uk.UTF-8):	MySQL - хедери та бібліотеки програміста
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%{?with_ssl:Requires:	openssl-devel}
Requires:	zlib-devel
Obsoletes:	MySQL-devel
Obsoletes:	libmysql10-devel

%description devel
This package contains the development header files and libraries
necessary to develop MySQL client applications.

%description devel -l fr.UTF-8
Ce package contient les fichiers entetes et les librairies de
developpement necessaires pour developper des applications clientes
MySQL.

%description devel -l pl.UTF-8
Pliki nagłówkowe i biblioteki konieczne do kompilacji aplikacji
klienckich MySQL.

%description devel -l pt_BR.UTF-8
Este pacote contém os arquivos de cabeçalho (header files) e
bibliotecas necessárias para desenvolver aplicações clientes do MySQL.

%description devel -l ru.UTF-8
Этот пакет содержит хедеры и библиотеки разработчика, необходимые для
разработки клиентских приложений.

%description devel -l uk.UTF-8
Цей пакет містить хедери та бібліотеки програміста, необхідні для
розробки програм-клієнтів.

%package static
Summary:	MySQL static libraries
Summary(pl.UTF-8):	Biblioteki statyczne MySQL
Summary(ru.UTF-8):	MySQL - статические библиотеки
Summary(uk.UTF-8):	MySQL - статичні бібліотеки
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	MySQL-static

%description static
MySQL static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne MySQL.

%description static -l ru.UTF-8
Этот пакет содержит статические библиотеки разработчика, необходимые
для разработки клиентских приложений.

%description static -l uk.UTF-8
Цей пакет містить статичні бібліотеки програміста, необхідні для
розробки програм-клієнтів.

%package bench
Summary:	MySQL - Benchmarks
Summary(pl.UTF-8):	MySQL - Programy testujące szybkość działania bazy
Summary(pt.UTF-8):	MySQL - Medições de desempenho
Summary(ru.UTF-8):	MySQL - бенчмарки
Summary(uk.UTF-8):	MySQL - бенчмарки
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-client
Requires:	perl(DBD::mysql)
Obsoletes:	MySQL-bench

%description bench
This package contains MySQL benchmark scripts and data.

%description bench -l pl.UTF-8
Programy testujące szybkość serwera MySQL.

%description bench -l pt_BR.UTF-8
Este pacote contém medições de desempenho de scripts e dados do MySQL.

%description bench -l ru.UTF-8
Этот пакет содержит скрипты и данные для оценки производительности
MySQL.

%description bench -l uk.UTF-8
Цей пакет містить скрипти та дані для оцінки продуктивності MySQL.

%package doc
Summary:	MySQL manual
Summary(pl.UTF-8):	Podręcznik użytkownika MySQL
Group:		Applications/Databases

%description doc
This package contains manual in HTML format.

%description doc -l pl.UTF-8
Podręcznik MySQL-a w formacie HTML.

%package ndb
Summary:	MySQL - NDB Storage Engine Daemon
Summary(pl.UTF-8):	MySQL - demon silnika przechowywania danych NDB
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description ndb
This package contains the standard MySQL NDB Storage Engine Daemon.

%description ndb -l pl.UTF-8
Ten pakiet zawiera standardowego demona silnika przechowywania danych
NDB.

%package ndb-client
Summary:	MySQL - NDB Clients
Summary(pl.UTF-8):	MySQL - programy klienckie NDB
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description ndb-client
This package contains the standard MySQL NDB Clients.

%description ndb-client -l pl.UTF-8
Ten pakiet zawiera standardowe programy klienckie MySQL NDB.

%package ndb-mgm
Summary:	MySQL - NDB Management Daemon
Summary(pl.UTF-8):	MySQL - demon zarządzający NDB
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description ndb-mgm
This package contains the standard MySQL NDB Management Daemon.

%description ndb-mgm -l pl.UTF-8
Ten pakiet zawiera standardowego demona zarządzającego MySQL NDB.

%package ndb-cpc
Summary:	MySQL - NDB CPC Daemon
Summary(pl.UTF-8):	MySQL - demon NDB CPC
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description ndb-cpc
This package contains the standard MySQL NDB CPC Daemon.

%description ndb-cpc -l pl.UTF-8
Ten pakiet zawiera standardowego demona MySQL NDB CPC.

%prep
%setup -q %{?_snap:-n %{name}-%{version}-nightly-%{_snap}} %{?with_sphinx:-a100}
%patch0 -p1
%if %{with sphinx}
mv sphinx-*/mysqlse sql/sphinx
%patch1 -p1
%endif
%patch2 -p1
%patch3 -p1
%ifarch alpha
# this is strange: mysqld functions for UDF modules are not explicitly defined,
# so -rdynamic is used; in such case gcc3+ld on alpha doesn't like C++ vtables
# in objects compiled without -fPIC
%patch4 -p1
# gcc 3.3.x ICE
%patch10 -p1
%endif
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
#%patch25 -p1

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
	%{?with_sphinx:--with-sphinx-storage-engine} \
	%{?with_federated:--with-federated-storage-engine} \
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
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,rc.d/init.d,sysconfig,mysql,pki/mysql} \
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
touch $RPM_BUILD_ROOT/var/log/mysql/{err,log,update}

# remove innodb directives from mysqld.conf if mysqld is configured without
%if !%{with innodb}
	echo "BASE_TABLETYPE=MyISAM" >> $RPM_BUILD_ROOT/etc/sysconfig/mysql
	cp mysqld.conf mysqld.tmp
	awk 'BEGIN { RS="\n\n" } !/innodb/ { printf("%s\n\n", $0) }' < mysqld.tmp > mysqld.conf
%endif

# remove berkeley-db directives from mysqld.conf if mysqld is configured without
%if !%{with bdb}
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
sed -i -e 's,%{_libdir}/mysql,%{_libdir},' $RPM_BUILD_ROOT{%{_libdir}/libmysqlclient{,_r}.la,%{_bindir}/mysql_config}

# remove known unpackaged files
rm -rf $RPM_BUILD_ROOT%{_prefix}/mysql-test

# rename not to be so generic name
mv $RPM_BUILD_ROOT%{_bindir}/{,mysql_}comp_err
mv $RPM_BUILD_ROOT%{_bindir}/{,mysql_}resolve_stack_dump
mv $RPM_BUILD_ROOT%{_mandir}/man1/{,mysql_}resolve_stack_dump.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/{,mysql_}comp_err.1

# not useful without -debug build
%{!?debug:rm -f $RPM_BUILD_ROOT%{_bindir}/mysql_resolve_stack_dump}
%{!?debug:rm -f $RPM_BUILD_ROOT%{_mandir}/man1/mysql_resolve_stack_dump.1}
# generate symbols file, so one can generate backtrace using it
# mysql_resolve_stack_dump -s %{_datadir}/mysql/mysqld.sym -n mysqld.stack.
# http://dev.mysql.com/doc/refman/5.0/en/using-stack-trace.html
%{?debug:nm -n $RPM_BUILD_ROOT%{_sbindir}/mysqld > $RPM_BUILD_ROOT%{_datadir}/mysql/mysqld.sym}

# functionality in initscript / rpm / other os
rm $RPM_BUILD_ROOT%{_bindir}/mysql_install_db
rm $RPM_BUILD_ROOT%{_bindir}/mysqld_safe
rm $RPM_BUILD_ROOT%{_bindir}/mysqld_multi
rm $RPM_BUILD_ROOT%{_mandir}/man1/mysqld_{multi,safe}*
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/mysql-log-rotate
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/mysql.server
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/binary-configure
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/errmsg.txt
rm $RPM_BUILD_ROOT%{_bindir}/mysql_waitpid
rm $RPM_BUILD_ROOT%{_mandir}/man1/mysql.server*
rm $RPM_BUILD_ROOT%{_mandir}/man1/safe_mysqld*
rm $RPM_BUILD_ROOT%{_mandir}/man1/mysqlman.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/make_win_bin_dist.1
rm $RPM_BUILD_ROOT%{_mandir}/man1/mysql_install_db.1
rm $RPM_BUILD_ROOT%{_mandir}/man1/mysql_waitpid.1
rm $RPM_BUILD_ROOT%{_mandir}/man1/make_win_src_distribution.1
rm $RPM_BUILD_ROOT%{_datadir}/mysql/mysqld_multi.server

# no package for tests
rm $RPM_BUILD_ROOT%{_mandir}/man1/mysql-stress-test.pl.1
rm $RPM_BUILD_ROOT%{_mandir}/man1/mysql-test-run.pl.1
rm $RPM_BUILD_ROOT%{_mandir}/man1/mysql_client_test_embedded.1

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
%service mysql restart

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
%service mysql-ndb restart "mysql NDB engine"

%preun ndb
if [ "$1" = "0" ]; then
	%service mysql-ndb stop
	/sbin/chkconfig --del mysql-ndb
fi

%post ndb-mgm
/sbin/chkconfig --add mysql-ndb-mgm
%service mysql-ndb-mgm restart "mysql NDB management node"

%preun ndb-mgm
if [ "$1" = "0" ]; then
	%service mysql-ndb-mgm stop
	/sbin/chkconfig --del mysql-ndb-mgm
fi

%post ndb-cpc
/sbin/chkconfig --add mysql-ndb-cpc
%service mysql-ndb-cpc restart "mysql NDB CPC"

%preun ndb-cpc
if [ "$1" = "0" ]; then
	%service mysql-ndb-cpc stop
	/sbin/chkconfig --del mysql-ndb-cpc
fi

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%triggerpostun -- mysql < 4.0.20-2.4
# For clusters in /etc/mysql/clusters.conf
if [ -f /etc/sysconfig/mysql ]; then
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

%triggerpostun -- mysql < 4.1.1
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
	If you want to use new help tables in MySQL 4.1.x then You'll need to import the help data:
	mysql -u mysql mysql < %{_datadir}/%{name}/fill_help_tables.sql
EOF
#'

%files
%defattr(644,root,root,755)
%doc support-files/*.cnf support-files/*.ini ChangeLog
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/mysql
%attr(754,root,root) /etc/rc.d/init.d/mysql
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mysql
%dir /etc/pki/mysql
%attr(640,root,mysql) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mysql/clusters.conf
%attr(755,root,root) %{_bindir}/innochecksum
%attr(755,root,root) %{_bindir}/myisamchk
%attr(755,root,root) %{_bindir}/myisamlog
%attr(755,root,root) %{_bindir}/myisampack
%attr(755,root,root) %{_bindir}/mysql_fix_privilege_tables
%attr(755,root,root) %{_bindir}/my_print_defaults
%attr(755,root,root) %{_bindir}/mysql_upgrade
%attr(755,root,root) %{_bindir}/mysql_upgrade_shell
%attr(755,root,root) %{_sbindir}/mysqld
%{_mandir}/man1/mysql_fix_privilege_tables.1*
%{_mandir}/man1/my_print_defaults.1*
%{_mandir}/man1/myisamchk.1*
%{_mandir}/man1/myisamlog.1*
%{_mandir}/man1/myisampack.1*
%{_mandir}/man1/mysql_upgrade.1*
%{_mandir}/man1/innochecksum.1*
%{_mandir}/man8/mysqld.8*

%if %{?debug:1}0
%attr(755,root,root) %{_bindir}/*resolve_stack_dump
%{_datadir}/mysql/mysqld.sym
%{_mandir}/man1/*resolve_stack_dump.1*
%endif

%attr(700,mysql,mysql) %{_mysqlhome}
# root:root is proper here for AC mysql.rpm while mysql:mysql is potential security hole
%attr(751,root,root) /var/lib/mysql
%attr(750,mysql,mysql) %dir /var/log/mysql
%attr(750,mysql,mysql) %dir /var/log/archiv/mysql
%attr(640,mysql,mysql) %ghost /var/log/mysql/*

%{_infodir}/mysql.info*
# This is template for configuration file which is created after 'service mysql init'
%{_datadir}/mysql/mysqld.conf

%{_datadir}/mysql/fill_help_tables.sql
%{_datadir}/mysql/mysql_fix_privilege_tables.sql
%{_datadir}/mysql/mysql_system_tables.sql
%{_datadir}/mysql/mysql_system_tables_data.sql
%{_datadir}/mysql/mysql_test_data_timezone.sql

%{_datadir}/mysql/english
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

%files charsets
%defattr(644,root,root,755)
%dir %{_datadir}/mysql
%{_datadir}/mysql/charsets

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
%{_mandir}/man1/myisam_ftdump.1*
%{_mandir}/man1/mysql_secure_installation.1*
%{_mandir}/man1/mysql_tzinfo_to_sql.1*
%{_mandir}/man1/mysqlcheck.1*
%{_mandir}/man1/perror.1*
%{_mandir}/man1/replace.1*
%{_mandir}/man1/resolveip.1*

%files extras-perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysql_convert_table_format
%attr(755,root,root) %{_bindir}/mysql_explain_log
%attr(755,root,root) %{_bindir}/mysql_find_rows
%attr(755,root,root) %{_bindir}/mysql_fix_extensions
%attr(755,root,root) %{_bindir}/mysql_setpermission
%attr(755,root,root) %{_bindir}/mysql_tableinfo
%attr(755,root,root) %{_bindir}/mysql_zap
%attr(755,root,root) %{_bindir}/mysqlaccess
%attr(755,root,root) %{_bindir}/mysqldumpslow
%attr(755,root,root) %{_bindir}/mysqlhotcopy
%{_mandir}/man1/mysql_explain_log.1*
%{_mandir}/man1/mysql_zap.1*
%{_mandir}/man1/mysqlaccess.1*
%{_mandir}/man1/mysqlhotcopy.1*
%{_mandir}/man1/mysql_setpermission.1*
%{_mandir}/man1/mysql_tableinfo.1*
%{_mandir}/man1/mysql_fix_extensions.1*
%{_mandir}/man1/mysql_find_rows.1*
%{_mandir}/man1/mysql_convert_table_format.1*

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
%{_mandir}/man1/mysql.1*
%{_mandir}/man1/mysqladmin.1*
%{_mandir}/man1/mysqldump.1*
%{_mandir}/man1/mysqlshow.1*
%{_mandir}/man1/mysqlbinlog.1*
%{_mandir}/man1/mysqlimport.1*
%{_mandir}/man1/mysqlmanager*.1*
%{_mandir}/man8/mysqlmanager.8*

%files libs
%defattr(644,root,root,755)
%doc EXCEPTIONS-CLIENT
%attr(755,root,root) %{_libdir}/libmysqlclient.so.*.*
%attr(755,root,root) %{_libdir}/libmysqlclient_r.so.*.*
%attr(755,root,root) %{_libdir}/libndbclient.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libmysqlclient.so.15
%attr(755,root,root) %ghost %{_libdir}/libmysqlclient_r.so.15
%attr(755,root,root) %ghost %{_libdir}/libndbclient.so.2
%attr(751,root,root) %dir %{_sysconfdir}/mysql
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mysql/mysql-client.conf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysql_config
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_bindir}/*comp_err
%{_libdir}/lib*.la
%{_libdir}/lib*[!tr].a
%{_includedir}/mysql
%{_mandir}/man1/mysql_config.1*
%{_mandir}/man1/*comp_err.1*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*[tr].a

%files bench
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysql_client_test
%attr(755,root,root) %{_bindir}/mysqltest
%attr(755,root,root) %{_bindir}/mysqltestmanager
%attr(755,root,root) %{_bindir}/mysqltestmanager-pwgen
%attr(755,root,root) %{_bindir}/mysqltestmanagerc
%dir %{_datadir}/sql-bench
%{_datadir}/sql-bench/[CDRl]*
%attr(755,root,root) %{_datadir}/sql-bench/[bcgirst]*
# wrong dir?
%{_datadir}/mysql/mi_test_all.res
%attr(755,root,root) %{_datadir}/mysql/mi_test_all
%{_mandir}/man1/mysqlbug.1*
%{_mandir}/man1/mysqltest*.1*
%{_mandir}/man1/mysql_client_test.1*

#%files doc
#%defattr(644,root,root,755)
#%doc Docs/manual.html Docs/manual_toc.html

%files ndb
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ndbd
%attr(754,root,root) /etc/rc.d/init.d/mysql-ndb
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mysql-ndb
%{_mandir}/man8/ndbd.8*

%files ndb-client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ndb_*
%attr(755,root,root) %{_datadir}/mysql/ndb_size.tmpl
%{_mandir}/man1/ndb_*.1*
%exclude %{_mandir}/man8/ndb_mgmd.8*

%files ndb-mgm
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ndb_mgmd
%attr(754,root,root) /etc/rc.d/init.d/mysql-ndb-mgm
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mysql-ndb-mgm
%{_mandir}/man8/ndb_mgmd.8*

%files ndb-cpc
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ndb_cpcd
%attr(754,root,root) /etc/rc.d/init.d/mysql-ndb-cpc
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mysql-ndb-cpc
%{_mandir}/man1/ndb_cpcd.1*
