# TODO:
# - http://bugs.mysql.com/bug.php?id=16470
# - innodb are dynamic (= as plugins) ?
# - missing have_archive, have_merge
# - is plugin_dir lib64 safe?
# - Using NDB Cluster... could not find sci transporter in /{include, lib}
# - configure: WARNING: unrecognized options: --with-innodb, --with-raid, --with-archive-storage-engine, --with-federated-storage-engine, --with-vio, --without-ndbcluster
# - !!! Makefiles for libmysqld.so !!!
# - segfaults on select from non-mysql user (caused by builder environment):
#     https://bugs.launchpad.net/pld-linux/+bug/381904
#     (profiling disabled temporaily to workaround this)
#
# Conditional build:
%bcond_without	innodb		# InnoDB storage engine support
%bcond_without	big_tables	# Support tables with more than 4G rows even on 32 bit platforms
%bcond_without	federated	# Federated storage engine support
%bcond_without	raid		# RAID support
%bcond_without	ssl		# OpenSSL support
%bcond_without	tcpd		# libwrap (tcp_wrappers) support
%bcond_with	autodeps	# BR packages needed only for resolving deps
%bcond_with	sphinx		# Sphinx storage engine support
%bcond_with	tests		# FIXME: don't run correctly
%bcond_with	ndb		# NDB is now a separate product, this here is broken, so disable it
#
%include	/usr/lib/rpm/macros.perl
Summary:	MySQL: a very fast and reliable SQL database engine
Summary(de.UTF-8):	MySQL: ist eine SQL-Datenbank
Summary(fr.UTF-8):	MySQL: un serveur SQL rapide et fiable
Summary(pl.UTF-8):	MySQL: bardzo szybka i niezawodna baza danych (SQL)
Summary(pt_BR.UTF-8):	MySQL: Um servidor SQL rápido e confiável
Summary(ru.UTF-8):	MySQL - быстрый SQL-сервер
Summary(uk.UTF-8):	MySQL - швидкий SQL-сервер
Summary(zh_CN.UTF-8):	MySQL数据库服务器
Name:		mysql
Version:	5.1.41
Release:	3
License:	GPL + MySQL FLOSS Exception
Group:		Applications/Databases
#Source0Download: http://dev.mysql.com/downloads/mysql/5.1.html#source
Source0:	http://mysql.easynet.be/Downloads/MySQL-5.1/%{name}-%{version}.tar.gz
# Source0-md5:	b5d39e8789174753f3c782959729e68c
Source100:	http://www.sphinxsearch.com/downloads/sphinx-0.9.7.tar.gz
# Source100-md5:	32f2b7e98d8485c86108851d52c5cef4
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
Source14:	my.cnf
Patch0:		%{name}-libs.patch
Patch1:		%{name}-libwrap.patch
Patch2:		%{name}-c++.patch
Patch3:		%{name}-info.patch
Patch4:		%{name}-sql-cxx-pic.patch
Patch5:		%{name}-noproc.patch
Patch6:		%{name}-system-users.patch
Patch7:		%{name}-bug-34192.patch
Patch8:		%{name}-client-config.patch
Patch9:		%{name}-build.patch
Patch10:	%{name}-alpha.patch
Patch11:	%{name}-upgrade.patch
Patch12:	%{name}-config.patch
Patch13:	%{name}-errorlog-no-rename.patch
Patch14:	%{name}-bug-43594.patch
Patch15:	plugin-avoid-version.patch
Patch16:	%{name}-fix-dummy-thread-race-condition.patch
# <percona patches, http://www.percona.com/percona-lab.html>
Patch100:	%{name}-userstats.patch
Patch101:	%{name}-microslow.patch
Patch102:	%{name}-acc-pslist.patch
Patch103:	%{name}-split_buf_pool_mutex_fixed_optimistic_safe.patch
Patch104:	%{name}-innodb_rw_lock.patch
# </percona>
URL:		http://www.mysql.com/products/database/mysql/community_edition.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	doxygen
BuildRequires:	libstdc++-devel >= 5:3.0
BuildRequires:	libtool
%{?with_tcpd:BuildRequires:	libwrap-devel}
BuildRequires:	ncurses-devel >= 4.2
%{?with_ssl:BuildRequires:	openssl-devel >= 0.9.7d}
%{?with_autodeps:BuildRequires:	perl-DBI}
BuildRequires:	perl-devel >= 1:5.6.1
BuildRequires:	readline-devel >= 4.2
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.414
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
Requires:	%{name}-libs = %{version}-%{release}
Requires:	/usr/bin/setsid
Requires:	rc-scripts >= 0.2.0
Suggests:	mysql-client
%{?with_tcpd:Suggests:	tcp_wrappers}
Provides:	MySQL-server
Provides:	group(mysql)
Provides:	msqlormysql
Provides:	user(mysql)
Obsoletes:	MySQL
Obsoletes:	mysql-server
Conflicts:	logrotate < 3.7-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_sbindir}
%define		_localstatedir	/var/lib/mysql
%define		_mysqlhome	/home/services/mysql

%define		_noautoreqdep	'perl(DBD::mysql)'

# readline/libedit detection goes wrong
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

%package -n mysqlhotcopy
Summary:	mysqlhotcopy - A MySQL database backup program
Summary(pl.UTF-8):	mysqlhotcopy - program do tworzenia kopii zapasowych baz MySQL
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}
Requires:	perl-DBD-mysql

%description -n mysqlhotcopy
mysqlhotcopy uses LOCK TABLES, FLUSH TABLES, and cp or scp to make a
database backup quickly. It is the fastest way to make a backup of the
database or single tables, but it can be run only on the same machine
where the database directories are located. mysqlhotcopy works only
for backing up MyISAM and ARCHIVE tables.

See innobackup package to backup InnoDB tables.

%description -n mysqlhotcopy -l pl.UTF-8
mysqlhotcopy wykorzystuje LOCK TABLES, FLUSH TABLES oraz cp i scp do
szybkiego tworzenia kopii zapasowych baz danych. Jest to najszybszy
sposób wykonania kopii zapasowej bazy danych lub pojedynczych tabel,
ale może działać tylko na maszynie, na której znajdują się katalogi z
bazą danych. mysqlhotcopy działa tylko dla tabel typu MyISAM i
ARCHIVE.

Narzędzie do tworzenia kopii tabel InnoDB znajduje się w pakiecie
innobackup.

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
# this is just for the sake of smooth upgrade, not to break systems
Requires:	mysqlhotcopy = %{version}-%{release}
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
%setup -q %{?with_sphinx:-a100}
%if %{with sphinx}
mv sphinx-*/mysqlse storage/sphinx
%endif
%patch0 -p1
#%{?with_tcpd:%patch1 -p1}  # WHATS PURPOSE OF THIS PATCH?
#%patch2 -p1 # NEEDS CHECK, which exact program needs -lc++
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
%patch14 -p0
%patch15 -p1
%patch16 -p1
# <percona %patches>
%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
# </percona>

%build
%{__libtoolize}
%{__aclocal} -I config/ac-macros
%{__automake}
%{__autoconf}

# The compiler flags are as per their "official" spec ;)
CXXFLAGS="%{rpmcxxflags} -fPIC -fno-implicit-templates -fno-rtti -fno-exceptions"
CFLAGS="%{rpmcflags} -fPIC"
CPPFLAGS="%{rpmcppflags}"

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
	--with%{!?with_innodb:out}-innodb \
	--with%{!?with_raid:out}-raid \
	--with%{!?with_ssl:out}-ssl=/usr \
	--with%{!?with_tcpd:out}-libwrap \
	%{?with_big_tables:--with-big-tables} \
	--with-comment="PLD Linux Distribution MySQL RPM" \
	--with%{!?debug:out}-debug%{?debug:=full} \
	--with-embedded-server \
	--with-extra-charsets=all \
	--with-low-memory \
	--with-mysqld-user=mysql \
	--with-named-curses-libs="-lncurses" \
	--with-named-thread-libs="-lpthread" \
	--with-unix-socket-path=/var/lib/mysql/mysql.sock \
	--with-archive-storage-engine \
	--with-plugins=max \
	%{?with_federated:--with-federated-storage-engine} \
	--with-fast-mutexes \
	--with-vio \
	--without-readline \
	--without-libedit \
%if %{with ndb}
	--with%{!?debug:out}-ndb-debug \
	--with-ndbcluster \
	--with-ndb-docs \
%else
	--without-ndbcluster \
%endif
	--with-docs

#--with-error-inject

# NOTE that /var/lib/mysql/mysql.sock is symlink to real sock file
# (it defaults to first cluster but user may change it to whatever
# cluster it wants)

echo -e "all:\ninstall:\nclean:\nlink_sources:\n" > libmysqld/examples/Makefile

%{__make} \
	benchdir=$RPM_BUILD_ROOT%{_datadir}/sql-bench

%{__make} -C Docs mysql.info

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,rc.d/init.d,sysconfig,mysql,skel} \
	   $RPM_BUILD_ROOT/var/{log/{archive,}/mysql,lib/mysql} \
	   $RPM_BUILD_ROOT{%{_infodir},%{_mysqlhome}}

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
touch $RPM_BUILD_ROOT/var/log/mysql/{mysqld,query,slow}.log

# remove innodb directives from mysqld.conf if mysqld is configured without
%if %{without innodb}
	cp mysqld.conf mysqld.tmp
	awk 'BEGIN { RS="\n\n" } !/innodb/ { printf("%s\n\n", $0) }' < mysqld.tmp > mysqld.conf
%endif

# remove berkeley-db directives from mysqld.conf if mysqld is configured without
cp mysqld.conf mysqld.tmp
awk 'BEGIN { RS="\n\n" } !/bdb/ { printf("%s\n\n", $0) }' < mysqld.tmp > mysqld.conf

install mysqld.conf $RPM_BUILD_ROOT%{_datadir}/mysql/mysqld.conf
cp -a %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/mysql/mysql-client.conf
cp -a %{SOURCE14} $RPM_BUILD_ROOT/etc/skel/.my.cnf

# NDB
%if %{with ndb}
install %{SOURCE7} $RPM_BUILD_ROOT/etc/rc.d/init.d/mysql-ndb
install %{SOURCE8} $RPM_BUILD_ROOT/etc/sysconfig/mysql-ndb
install %{SOURCE9} $RPM_BUILD_ROOT/etc/rc.d/init.d/mysql-ndb-mgm
install %{SOURCE10} $RPM_BUILD_ROOT/etc/sysconfig/mysql-ndb-mgm
install %{SOURCE11} $RPM_BUILD_ROOT/etc/rc.d/init.d/mysql-ndb-cpc
install %{SOURCE12} $RPM_BUILD_ROOT/etc/sysconfig/mysql-ndb-cpc
%endif

mv -f $RPM_BUILD_ROOT%{_libdir}/mysql/lib* $RPM_BUILD_ROOT%{_libdir}
sed -i -e 's,%{_libdir}/mysql,%{_libdir},' $RPM_BUILD_ROOT{%{_libdir}/libmysqlclient{,_r}.la,%{_bindir}/mysql_config}
sed -i -e '/libs/s/$ldflags//' $RPM_BUILD_ROOT%{_bindir}/mysql_config

# remove known unpackaged files
rm -rf $RPM_BUILD_ROOT%{_prefix}/mysql-test

# remove .txt variants for .sys messages
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/*/*.txt

# rename not to be so generic name
mv $RPM_BUILD_ROOT%{_bindir}/{,mysql_}resolve_stack_dump
mv $RPM_BUILD_ROOT%{_mandir}/man1/{,mysql_}resolve_stack_dump.1

# not useful without -debug build
%{!?debug:rm -f $RPM_BUILD_ROOT%{_bindir}/mysql_resolve_stack_dump}
%{!?debug:rm -f $RPM_BUILD_ROOT%{_mandir}/man1/mysql_resolve_stack_dump.1}
# generate symbols file, so one can generate backtrace using it
# mysql_resolve_stack_dump -s %{_datadir}/mysql/mysqld.sym -n mysqld.stack.
# http://dev.mysql.com/doc/refman/5.0/en/using-stack-trace.html
%{?debug:nm -n $RPM_BUILD_ROOT%{_sbindir}/mysqld > $RPM_BUILD_ROOT%{_datadir}/mysql/mysqld.sym}

# do not clobber users $PATH
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/mysql_upgrade
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/innochecksum
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/myisamchk
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/myisamlog
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/myisampack
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/mysql_fix_privilege_tables
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/my_print_defaults
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/mysqlcheck

# functionality in initscript / rpm
rm $RPM_BUILD_ROOT%{_bindir}/mysql_install_db
rm $RPM_BUILD_ROOT%{_mandir}/man1/mysql_install_db.1*
rm $RPM_BUILD_ROOT%{_bindir}/mysqld_safe
rm $RPM_BUILD_ROOT%{_bindir}/mysqld_multi
rm $RPM_BUILD_ROOT%{_mandir}/man1/mysqld_{multi,safe}*
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/mysql-log-rotate
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/mysql.server
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/binary-configure
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/errmsg.txt
rm $RPM_BUILD_ROOT%{_bindir}/mysql_waitpid
rm $RPM_BUILD_ROOT%{_mandir}/man1/mysql_waitpid.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/mysql.server*
rm $RPM_BUILD_ROOT%{_mandir}/man1/mysqlman.1*
rm $RPM_BUILD_ROOT%{_bindir}/resolveip
rm $RPM_BUILD_ROOT%{_mandir}/man1/resolveip.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/comp_err.1*
rm $RPM_BUILD_ROOT%{_datadir}/mysql/ChangeLog

# we don't package those (we have no -test or -testsuite pkg) and some of them just segfault
rm $RPM_BUILD_ROOT%{_bindir}/mysql_client_test
rm $RPM_BUILD_ROOT%{_datadir}/mysql/mi_test_all
rm $RPM_BUILD_ROOT%{_datadir}/mysql/mi_test_all.res
rm $RPM_BUILD_ROOT%{_datadir}/mysql/mysqld_multi.server
rm $RPM_BUILD_ROOT%{_mandir}/man1/mysql_client_test.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/mysql_client_test_embedded.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/mysql-stress-test.pl.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/mysql-test-run.pl.1*

# in %doc
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/*.{ini,cnf}

# not needed
rm -f $RPM_BUILD_ROOT%{_libdir}/mysql/plugin/ha_*.{a,la}
rm -f $RPM_BUILD_ROOT%{_libdir}/mysql/plugin/ha_example.*

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

%triggerpostun -- mysql < 5.1.0
configs=""
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
		echo >&2 "ERROR: Can't find real config file for $config! Please report this (with above errors, if any) to http://bugs.pld-linux.org/"
		continue
	fi
	configs="$configs $config_file"
done

(
echo 'You should run MySQL upgrade script *after* restarting MySQL server for all MySQL clusters.'
echo 'Thus, you should invoke:'
for config in $configs; do
	datadir=$(awk -F= '!/^#/ && $1 ~ /datadir/{print $2}' $config | xargs)
	echo "# mysql_upgrade --datadir=$datadir"
done
) | %banner -e %{name}-5.1

%files
%defattr(644,root,root,755)
%doc support-files/*.cnf support-files/*.ini ChangeLog
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/mysql
%attr(754,root,root) /etc/rc.d/init.d/mysql
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mysql
%attr(640,root,mysql) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mysql/clusters.conf
%attr(755,root,root) %{_sbindir}/innochecksum
%attr(755,root,root) %{_sbindir}/my_print_defaults
%attr(755,root,root) %{_sbindir}/myisamchk
%attr(755,root,root) %{_sbindir}/myisamlog
%attr(755,root,root) %{_sbindir}/myisampack
%attr(755,root,root) %{_sbindir}/mysql_fix_privilege_tables
%attr(755,root,root) %{_sbindir}/mysql_upgrade
%attr(755,root,root) %{_sbindir}/mysqlcheck
%attr(755,root,root) %{_sbindir}/mysqld
%dir %{_libdir}/mysql
%dir %{_libdir}/mysql/plugin
%attr(755,root,root) %{_libdir}/mysql/plugin/ha_innodb_plugin.so
%{_mandir}/man1/innochecksum.1*
%{_mandir}/man1/my_print_defaults.1*
%{_mandir}/man1/myisamchk.1*
%{_mandir}/man1/myisamlog.1*
%{_mandir}/man1/myisampack.1*
%{_mandir}/man1/mysql_fix_privilege_tables.1*
%{_mandir}/man1/mysql_upgrade.1*
%{_mandir}/man1/mysqlcheck.1*
%{_mandir}/man8/mysqld.8*

%if %{?debug:1}0
%attr(755,root,root) %{_bindir}/*resolve_stack_dump
%{_datadir}/mysql/mysqld.sym
%{_mandir}/man1/*resolve_stack_dump.1*
%endif

%attr(700,mysql,mysql) %{_mysqlhome}
# root:root is proper here for mysql.rpm while mysql:mysql is potential security hole
%attr(751,root,root) /var/lib/mysql
%attr(750,mysql,mysql) %dir /var/log/mysql
%attr(750,mysql,mysql) %dir /var/log/archive/mysql
%attr(640,mysql,mysql) %ghost /var/log/mysql/*

%{_infodir}/mysql.info*
# This is template for configuration file which is created after 'service mysql init'
%{_datadir}/mysql/mysqld.conf
%{_datadir}/mysql/mysql_system_tables.sql
%{_datadir}/mysql/mysql_system_tables_data.sql
%{_datadir}/mysql/mysql_test_data_timezone.sql

%{_datadir}/mysql/english
%{_datadir}/mysql/fill_help_tables.sql
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
%attr(755,root,root) %{_bindir}/perror
%attr(755,root,root) %{_bindir}/replace
%{_mandir}/man1/msql2mysql.1*
%{_mandir}/man1/myisam_ftdump.1*
%{_mandir}/man1/mysql_secure_installation.1*
%{_mandir}/man1/mysql_tzinfo_to_sql.1*
%{_mandir}/man1/perror.1*
%{_mandir}/man1/replace.1*

%files -n mysqlhotcopy
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysqlhotcopy
%{_mandir}/man1/mysqlhotcopy.1*

%files extras-perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysql_convert_table_format
%attr(755,root,root) %{_bindir}/mysql_find_rows
%attr(755,root,root) %{_bindir}/mysql_fix_extensions
%attr(755,root,root) %{_bindir}/mysql_setpermission
%attr(755,root,root) %{_bindir}/mysql_zap
%attr(755,root,root) %{_bindir}/mysqlaccess
%attr(755,root,root) %{_bindir}/mysqldumpslow
%{_mandir}/man1/mysql_convert_table_format.1*
%{_mandir}/man1/mysql_find_rows.1*
%{_mandir}/man1/mysql_fix_extensions.1*
%{_mandir}/man1/mysql_setpermission.1*
%{_mandir}/man1/mysql_zap.1*
%{_mandir}/man1/mysqlaccess.1*
%{_mandir}/man1/mysqldumpslow.1*

%files client
%defattr(644,root,root,755)
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/skel/.my.cnf
%attr(755,root,root) %{_bindir}/mysql
%attr(755,root,root) %{_bindir}/mysqladmin
%attr(755,root,root) %{_bindir}/mysqlbinlog
%attr(755,root,root) %{_bindir}/mysqlbug
%attr(755,root,root) %{_bindir}/mysqldump
%attr(755,root,root) %{_bindir}/mysqlimport
%attr(755,root,root) %{_bindir}/mysqlshow
%attr(755,root,root) %{_sbindir}/mysqlmanager
%{_mandir}/man1/mysql.1*
%{_mandir}/man1/mysqladmin.1*
%{_mandir}/man1/mysqlbinlog.1*
%{_mandir}/man1/mysqlbug.1*
%{_mandir}/man1/mysqldump.1*
%{_mandir}/man1/mysqlimport.1*
%{_mandir}/man1/mysqlshow.1*
%{_mandir}/man8/mysqlmanager.8*

%files libs
%defattr(644,root,root,755)
%doc EXCEPTIONS-CLIENT
%attr(751,root,root) %dir %{_sysconfdir}/mysql
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mysql/mysql-client.conf
%attr(755,root,root) %{_libdir}/libmysqlclient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmysqlclient.so.16
%attr(755,root,root) %{_libdir}/libmysqlclient_r.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmysqlclient_r.so.16
%if %{with ndb}
%attr(755,root,root) %{_libdir}/libndbclient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libndbclient.so.3
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysql_config
%attr(755,root,root) %{_libdir}/libmysqlclient.so
%attr(755,root,root) %{_libdir}/libmysqlclient_r.so
%if %{with ndb}
%attr(755,root,root) %{_libdir}/libndbclient.so
%{_libdir}/libndbclient.la
%endif
%{_libdir}/libmysqlclient.la
%{_libdir}/libmysqlclient_r.la
# static-only
%{_libdir}/libdbug.a
%{_libdir}/libheap.a
%{_libdir}/libmyisam.a
%{_libdir}/libmyisammrg.a
%{_libdir}/libmysqld.a
%{_libdir}/libmystrings.a
%{_libdir}/libmysys.a
%{_libdir}/libvio.a
%{_includedir}/mysql
%{_aclocaldir}/mysql.m4
%{_mandir}/man1/mysql_config.1*

%files static
%defattr(644,root,root,755)
%{_libdir}/libmysqlclient.a
%{_libdir}/libmysqlclient_r.a
%if %{with ndb}
%{_libdir}/libndbclient.a
%endif

%files bench
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysqlslap
%attr(755,root,root) %{_bindir}/mysqltest
%dir %{_datadir}/sql-bench
%{_datadir}/sql-bench/[CDRl]*
%attr(755,root,root) %{_datadir}/sql-bench/[bcgirst]*
%{_mandir}/man1/mysqlslap.1*
%{_mandir}/man1/mysqltest.1*
%{_mandir}/man1/mysqltest_embedded.1*

#%files doc
#%defattr(644,root,root,755)
#%doc Docs/manual.html Docs/manual_toc.html

%if %{with ndb}
%files ndb
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ndbd
%attr(754,root,root) /etc/rc.d/init.d/mysql-ndb
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mysql-ndb
%{_mandir}/man1/ndbd_redo_log_reader.1*
%{_mandir}/man8/ndbd.8*

%files ndb-client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ndb_config
%attr(755,root,root) %{_bindir}/ndb_delete_all
%attr(755,root,root) %{_bindir}/ndb_desc
%attr(755,root,root) %{_bindir}/ndb_drop_index
%attr(755,root,root) %{_bindir}/ndb_drop_table
%attr(755,root,root) %{_bindir}/ndb_error_reporter
%attr(755,root,root) %{_bindir}/ndb_mgm
%attr(755,root,root) %{_bindir}/ndb_print_backup_file
%attr(755,root,root) %{_bindir}/ndb_print_schema_file
%attr(755,root,root) %{_bindir}/ndb_print_sys_file
%attr(755,root,root) %{_bindir}/ndb_restore
%attr(755,root,root) %{_bindir}/ndb_select_all
%attr(755,root,root) %{_bindir}/ndb_select_count
%attr(755,root,root) %{_bindir}/ndb_show_tables
%attr(755,root,root) %{_bindir}/ndb_size.pl
%attr(755,root,root) %{_bindir}/ndb_test_platform
%attr(755,root,root) %{_bindir}/ndb_waiter
%{_mandir}/man1/ndb_config.1*
%{_mandir}/man1/ndb_delete_all.1*
%{_mandir}/man1/ndb_desc.1*
%{_mandir}/man1/ndb_drop_index.1*
%{_mandir}/man1/ndb_drop_table.1*
%{_mandir}/man1/ndb_error_reporter.1*
%{_mandir}/man1/ndb_mgm.1*
%{_mandir}/man1/ndb_print_backup_file.1*
%{_mandir}/man1/ndb_print_schema_file.1*
%{_mandir}/man1/ndb_print_sys_file.1*
%{_mandir}/man1/ndb_restore.1*
%{_mandir}/man1/ndb_select_all.1*
%{_mandir}/man1/ndb_select_count.1*
%{_mandir}/man1/ndb_show_tables.1*
%{_mandir}/man1/ndb_size.pl.1*
%{_mandir}/man1/ndb_waiter.1*

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
%endif
