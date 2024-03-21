# TODO:
# - -DWITH_AUTHENTICATION_KERBEROS=ON (BR: MIT krb5)
# - -DWITH_AUTHENTICATION_FIDO=ON (using system libfido?)
# - mysqldump ... (invalid usage) prints to stdout not stderr (idiotic if you want to create dump and get usage in .sql)
# - http://bugs.mysql.com/bug.php?id=16470
# - innodb are dynamic (= as plugins) ?
# - missing have_archive, have_merge
# - is plugin_dir lib64 safe?
# - Using NDB Cluster... could not find sci transporter in /{include, lib}
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
%bcond_without	systemtap	# systemtap/dtrace probes
%bcond_without	tcpd		# libwrap (tcp_wrappers) support
%bcond_with	sphinx		# Sphinx storage engine support
# mysql needs boost 1.77.0 and doesn't support newer/older boost versions
%bcond_with	system_boost
%bcond_without	tests		# run test suite
%bcond_with	ndb		# NDB is now a separate product, this here is broken, so disable it
%bcond_without	ldap		# LDAP auth support (requires MIT Kerberos)

Summary:	MySQL: a very fast and reliable SQL database engine
Summary(de.UTF-8):	MySQL: ist eine SQL-Datenbank
Summary(fr.UTF-8):	MySQL: un serveur SQL rapide et fiable
Summary(pl.UTF-8):	MySQL: bardzo szybka i niezawodna baza danych (SQL)
Summary(pt_BR.UTF-8):	MySQL: Um servidor SQL rápido e confiável
Summary(ru.UTF-8):	MySQL - быстрый SQL-сервер
Summary(uk.UTF-8):	MySQL - швидкий SQL-сервер
Summary(zh_CN.UTF-8):	MySQL数据库服务器
%define majorver        8.0
Name:		mysql%{majorver}
# keep stable (and not "innovation") line here
Version:	8.0.36
Release:    1
License:	GPL v2 + MySQL FOSS License Exception
Group:		Applications/Databases
#Source0Download: https://dev.mysql.com/downloads/mysql/8.0.html#downloads
Source0:	http://cdn.mysql.com/Downloads/MySQL-%{majorver}/mysql-%{version}.tar.gz
# Source0-md5:	08bc8e4307246e77d013267e2cd8fa49
Source100:	http://www.sphinxsearch.com/files/sphinx-2.2.11-release.tar.gz
# Source100-md5:	5cac34f3d78a9d612ca4301abfcbd666
%if %{without system_boost}
Source101:	http://downloads.sourceforge.net/boost/boost_1_77_0.tar.bz2
# Source101-md5:	09dc857466718f27237144c6f2432d86
%endif
Source1:	mysql.init
Source2:	mysql.sysconfig
Source3:	mysql.logrotate
Source4:	mysqld.conf
Source5:	mysql-clusters.conf
Source7:	mysql-ndb.init
Source8:	mysql-ndb.sysconfig
Source9:	mysql-ndb-mgm.init
Source10:	mysql-ndb-mgm.sysconfig
Source11:	mysql-ndb-cpc.init
Source12:	mysql-ndb-cpc.sysconfig
Source13:	mysql-client.conf
Source14:	my.cnf
Patch0:		mysql-opt.patch
Patch1:		mysql-system-xxhash.patch

Patch17:	mysql-5.7-sphinx.patch
Patch18:	mysql-sphinx.patch

Patch24:	mysql-cmake.patch
Patch25:	mysql-readline.patch

Patch26:	mysqldumpslow-clusters.patch
URL:		http://www.mysql.com/products/community/
BuildRequires:	bison >= 1.875
%{?with_system_boost:BuildRequires:	boost-devel >= 1.77.0}
BuildRequires:	cmake >= 2.8.2
%{?with_ldap:BuildRequires:	cyrus-sasl-devel}
# for configure and tests
%{?with_ldap:BuildRequires:	cyrus-sasl-scram}
#%{?with_ldap:BuildRequires:	krb5-devel}
BuildRequires:	libaio-devel
BuildRequires:	libevent-devel
BuildRequires:	libhsclient-devel
BuildRequires:	libstdc++-devel >= 5:7.1
%{?with_tcpd:BuildRequires:	libwrap-devel}
BuildRequires:	lz4-devel
BuildRequires:	mecab-devel
BuildRequires:	ncurses-devel >= 4.2
%{?with_ssl:BuildRequires:	openssl-devel >= 1.1.1}
%{?with_ldap:BuildRequires:	openldap-devel}
BuildRequires:	pam-devel
BuildRequires:	perl-devel >= 1:5.6.1
BuildRequires:	protobuf-devel >= 2.5
BuildRequires:	python-modules
BuildRequires:	readline-devel >= 6.2
BuildRequires:	rpcsvc-proto
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	sed >= 4.0
%{?with_systemtap:BuildRequires:	systemtap-sdt-devel}
BuildRequires:	xxHash-devel
BuildRequires:	zlib-devel >= 1.2.12
BuildRequires:	zstd-devel
Requires(post):	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name}-charsets = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}
Requires:	/usr/bin/setsid
Requires:	rc-scripts >= 0.2.0
Suggests:	%{name}-client
%{?with_tcpd:Suggests:	tcp_wrappers}
Suggests:	vim-syntax-mycnf
Provides:	MySQL-server
Provides:	group(mysql)
Provides:	msqlormysql
Provides:	user(mysql)
Obsoletes:	MySQL < 3.22.27
Obsoletes:	mysql-server < 4
Conflicts:	logrotate < 3.8.0
BuildRoot:	%{tmpdir}/mysql-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_sbindir}
%define		_localstatedir	/var/lib/%{name}
%define		_mysqlhome	/home/services/%{name}

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
BuildArch:	noarch

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
Requires:	%{name}-client = %{version}-%{release}
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
Requires:	perl-DBD-mysql

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
Requires:	readline >= 6.2
Obsoletes:	MySQL-client < 3.22.27

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
Summary(pl.UTF-8):	Biblioteki współdzielone MySQL
Group:		Libraries
Requires:	zlib >= 1.2.12
Obsoletes:	libmysql10 < 4
Obsoletes:	mysql-doc < 4.1.12

%description libs
Shared libraries for MySQL.

%description libs -l pl.UTF-8
Biblioteki współdzielone MySQL.

%package devel
Summary:	MySQL - development header files and other files
Summary(pl.UTF-8):	MySQL - Pliki nagłówkowe i inne dla programistów
Summary(pt.UTF-8):	MySQL - Medições de desempenho
Summary(ru.UTF-8):	MySQL - хедеры и библиотеки разработчика
Summary(uk.UTF-8):	MySQL - хедери та бібліотеки програміста
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%{?with_ssl:Requires:	openssl-devel >= 1.1.1}
Requires:	zlib-devel >= 1.2.12
Obsoletes:	MySQL-devel < 3.22.27
Obsoletes:	libmysql10-devel < 4
Obsoletes:	webscalesql-devel

%description devel
This package contains the development header files and other files
necessary to develop MySQL client applications.

%description devel -l fr.UTF-8
Ce package contient les fichiers entetes et les librairies de
developpement necessaires pour developper des applications clientes
MySQL.

%description devel -l pl.UTF-8
Pliki nagłówkowe i inne pliki konieczne do kompilacji aplikacji
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
Obsoletes:	MySQL-static < 3.22.27

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
Requires:	perl-DBD-mysql
Obsoletes:	MySQL-bench < 3.22.27

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
%setup -q %{?with_sphinx:-a100} %{!?with_system_boost:-a101} -n mysql-%{version}

#%patch0 -p1
# FIXME
#%patch1 -p1

%if %{with sphinx}
# http://www.sphinxsearch.com/docs/manual-0.9.9.html#sphinxse-mysql51
%{__mv} sphinx-*/mysqlse storage/sphinx
%patch17 -p1
%patch18 -p1
%endif

%patch24 -p1
%patch25 -p1

#%patch26 -p1

# to get these files rebuild
[ -f sql/sql_yacc.cc ] && %{__rm} sql/sql_yacc.cc
[ -f sql/sql_yacc.h ] && %{__rm} sql/sql_yacc.h

# ensure sytstem lib
# need to keep xxhash.[ch]
# FIXME
#%{__rm} -rv extra/lz4/lz4**

%build
install -d build
cd build
# NOTE that /var/lib/mysql/mysql.sock is symlink to real sock file
# (it defaults to first cluster but user may change it to whatever
# cluster it wants)

CPPFLAGS="%{rpmcppflags}" \
%cmake .. \
%if "%{_lib}" != "lib64"
	-DUSE_LD_LLD=off \
%endif
        -DCMAKE_EXECUTABLE_SUFFIX=string:%{majorver} \
	-DCMAKE_BUILD_TYPE=%{!?debug:RelWithDebInfo}%{?debug:Debug} \
	-DCMAKE_C_FLAGS_RELWITHDEBINFO="%{rpmcflags} -DNDEBUG -fno-omit-frame-pointer -fno-strict-aliasing" \
	-DCMAKE_CXX_FLAGS_RELWITHDEBINFO="%{rpmcxxflags} -DNDEBUG -fno-omit-frame-pointer -fno-strict-aliasing" \
	-DCOMPILATION_COMMENT="PLD/Linux Distribution MySQL RPM" \
	-DCURSES_INCLUDE_PATH=/usr/include/ncurses \
	%{?with_systemtap:-DENABLE_DTRACE=ON} \
	-DFEATURE_SET="community" \
	-DINSTALL_LAYOUT=RPM \
	-DINSTALL_LIBDIR=%{_lib} \
        -DINSTALL_PRIV_LIBDIR=%{_libdir}/%{name}/private \
	-DINSTALL_MYSQLTESTDIR_RPM="" \
	-DINSTALL_PLUGINDIR=%{_lib}/%{name}/plugin \
        -DINSTALL_SECURE_FILE_PRIVDIR=/var/lib/%{name}-files \
	-DINSTALL_SQLBENCHDIR=%{_datadir} \
	-DINSTALL_SUPPORTFILESDIR=share/%{name}-support \
	-DINSTALL_MYSQLSHAREDIR=share/%{name} \
        -DROUTER_INSTALL_LIBDIR=%{_libdir}/%{name}router/private \
        -DROUTER_INSTALL_PLUGINDIR=%{_libdir}/%{name}router \
	-DMYSQL_UNIX_ADDR=/var/lib/%{name}/mysql.sock \
	%{?debug:-DWITH_DEBUG=ON} \
	-DWITHOUT_EXAMPLE_STORAGE_ENGINE=1 \
	%{!?with_ldap:-DWITH_AUTHENTICATION_LDAP=OFF} \
	-DWITH_LIBWRAP=%{?with_tcpd:ON}%{!?with_tcpd:OFF} \
	-DWITH_PERFSCHEMA_STORAGE_ENGINE=1 \
	-DWITH_PIC=ON \
	%{?with_ldap:-DWITH_LDAP=system} \
	-DWITH_KERBEROS=system \
	-DWITH_LIBEVENT=system \
	-DWITH_LZ4=system \
	-DWITH_PROTOBUF=system \
	-DWITH_SASL=system \
        -DWITH_UNIT_TESTS=%{?with_tests:ON}%{!?with_tests:OFF} \
	-DWITH_SSL=%{?with_ssl:system}%{!?with_ssl:no} \
	%{!?with_system_boost:-DWITH_BOOST="$(pwd)/$(ls -1d ../boost_*)"} \
	-DWITH_ZLIB=system \
	-DWITH_EDITLINE=system \
	-DWITH_MECAB=system \
	-DTMPDIR=/var/tmp

%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,rc.d/init.d,sysconfig,%{name},skel} \
	   $RPM_BUILD_ROOT/var/{log/{archive,}/%{name},lib/{%{name},%{name}-files}} \
	   $RPM_BUILD_ROOT%{_mysqlhome} \
	   $RPM_BUILD_ROOT%{_libdir}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

sed -e 's#{MYSQL_MAJOR}#%{majorver}#g' %{SOURCE1} > $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
sed -e 's#{MYSQL_MAJOR}#%{majorver}#g' %{SOURCE3} > $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
# This is template for configuration file which is created after 'service mysql init'
sed -e 's#{MYSQL_MAJOR}#%{majorver}#g' %{SOURCE4} > mysqld.conf
sed -e 's#{MYSQL_MAJOR}#%{majorver}#g' %{SOURCE5} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/clusters.conf
touch $RPM_BUILD_ROOT/var/log/%{name}/{mysqld,query,slow}.log

mv $RPM_BUILD_ROOT/etc/logrotate.d/{mysqlrouter,%{name}router}

# remove innodb directives from mysqld.conf if mysqld is configured without
%if %{without innodb}
	cp mysqld.conf mysqld.tmp
	awk 'BEGIN { RS="\n\n" } !/innodb/ { printf("%s\n\n", $0) }' < mysqld.tmp > mysqld.conf
%endif

# remove berkeley-db directives from mysqld.conf if mysqld is configured without
cp mysqld.conf mysqld.tmp
awk 'BEGIN { RS="\n\n" } !/bdb/ { printf("%s\n\n", $0) }' < mysqld.tmp > mysqld.conf

cp -a mysqld.conf $RPM_BUILD_ROOT%{_datadir}/%{name}/mysqld.conf
cp -a %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/mysql-client.conf
ln -s mysql-client.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/my.cnf
cp -a %{SOURCE14} $RPM_BUILD_ROOT/etc/skel/.my.cnf

# NDB
%if %{with ndb}
install -p %{SOURCE7} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-ndb
cp -a %{SOURCE8} $RPM_BUILD_ROOT/etc/sysconfig/%{name}-ndb
install -p %{SOURCE9} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-ndb-mgm
cp -a %{SOURCE10} $RPM_BUILD_ROOT/etc/sysconfig/%{name}-ndb-mgm
install -p %{SOURCE11} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-ndb-cpc
cp -a %{SOURCE12} $RPM_BUILD_ROOT/etc/sysconfig/%{name}-ndb-cpc
%endif

sed -i -e 's,/usr//usr,%{_prefix},g' $RPM_BUILD_ROOT%{_bindir}/mysql_config
sed -i -e '/libs/s/$ldflags//' $RPM_BUILD_ROOT%{_bindir}/mysql_config
sed -i -e '/libs/s/-lprobes_mysql//' $RPM_BUILD_ROOT%{_bindir}/mysql_config

# remove known unpackaged files
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}-support

# rename not to be so generic name

# not useful without -debug build
# generate symbols file, so one can generate backtrace using it
# mysql_resolve_stack_dump -s %{_datadir}/%{name}/mysqld.sym -n mysqld.stack.
# http://dev.mysql.com/doc/refman/5.0/en/using-stack-trace.html
%{?debug:nm -n $RPM_BUILD_ROOT%{_sbindir}/mysqld > $RPM_BUILD_ROOT%{_datadir}/%{name}/mysqld.sym}

# do not clobber users $PATH
%{__mv} $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/mysql_upgrade
%{__mv} $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/innochecksum
%{__mv} $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/myisamchk
%{__mv} $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/myisamlog
%{__mv} $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/myisampack
#%{__mv} $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/mysql_fix_privilege_tables
%{__mv} $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/my_print_defaults
%{__mv} $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/mysqlcheck

# delete - functionality in initscript / rpm
# note: mysql_install_db (and thus resolveip) are needed by digikam
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mysqld_safe
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mysqld_multi
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/mysqld_{multi,safe}*
#%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/mysql-log-rotate
#%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/mysql.server
#%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/binary-configure
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/mysql.server*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/mysqlman.1*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/comp_err.1*

# we don't package those (we have no -test or -testsuite pkg) and some of them just segfault
%{__rm} $RPM_BUILD_ROOT%{_bindir}/{mysql_client_test,mysqlxtest}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/plugin/test_udf_services.so
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/plugin/component_test_udf_services.so
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/mysql-test

# not needed
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/plugin/libdaemon_example.*
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/plugin/daemon_example.ini

# test plugins
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/plugin/libtest*.so
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/plugin/rewrite_example.so
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/plugin/test_security_context.so

# fix names for parallel coinstallation
for f in $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/* ; do
    fb=$(basename "$f")
    mv "${f}" "${f}%{majorver}"
    for m in $RPM_BUILD_ROOT%{_mandir}/man*; do
        mnr=$(echo -n $m | tail -c 1)
        if [ -f "${m}/${fb}.${mnr}" ]; then
            mv "${m}/${fb}.${mnr}" "$m/${fb}%{majorver}.${mnr}"
        fi
    done
done

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 89 mysql
%useradd -u 89 -d %{_mysqlhome} -s /bin/false -g mysql -c "%{name} Server" mysql

%post
/sbin/ldconfig
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%userremove mysql
	%groupremove mysql
fi

%post ndb
/sbin/chkconfig --add %{name}-ndb
%service %{name}-ndb restart "%{name} NDB engine"

%preun ndb
if [ "$1" = "0" ]; then
	%service %{name}-ndb stop
	/sbin/chkconfig --del %{name}-ndb
fi

%post ndb-mgm
/sbin/chkconfig --add %{name}-ndb-mgm
%service %{name}-ndb-mgm restart "%{name} NDB management node"

%preun ndb-mgm
if [ "$1" = "0" ]; then
	%service %{name}-ndb-mgm stop
	/sbin/chkconfig --del %{name}-ndb-mgm
fi

%post ndb-cpc
/sbin/chkconfig --add %{name}-ndb-cpc
%service %{name}-ndb-cpc restart "%{name} NDB CPC"

%preun ndb-cpc
if [ "$1" = "0" ]; then
	%service %{name}-ndb-cpc stop
	/sbin/chkconfig --del %{name}-ndb-cpc
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}router
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(640,root,mysql) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/clusters.conf
%attr(755,root,root) %{_bindir}/ibd2sdi%{majorver}
%attr(755,root,root) %{_bindir}/mysql_migrate_keyring%{majorver}
%attr(755,root,root) %{_bindir}/mysqlrouter%{majorver}
%attr(755,root,root) %{_bindir}/mysqlrouter_keyring%{majorver}
%attr(755,root,root) %{_bindir}/mysqlrouter_passwd%{majorver}
%attr(755,root,root) %{_bindir}/mysqlrouter_plugin_info%{majorver}
%attr(755,root,root) %{_sbindir}/innochecksum%{majorver}
%attr(755,root,root) %{_sbindir}/my_print_defaults%{majorver}
%attr(755,root,root) %{_sbindir}/myisamchk%{majorver}
%attr(755,root,root) %{_sbindir}/myisamlog%{majorver}
%attr(755,root,root) %{_sbindir}/myisampack%{majorver}
%attr(755,root,root) %{_sbindir}/mysql_upgrade%{majorver}
%attr(755,root,root) %{_sbindir}/mysqlcheck%{majorver}
%attr(755,root,root) %{_sbindir}/mysqld%{majorver}

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugin
%attr(755,root,root) %{_libdir}/%{name}/plugin/adt_null.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/auth.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/auth_socket.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/auth_test_plugin.so
#%attr(755,root,root) %{_libdir}/%{name}/plugin/authentication_fido_client.so
#%{?with_ldap:%attr(755,root,root) %{_libdir}/%{name}/plugin/authentication_ldap_sasl_client.so}
#%attr(755,root,root) %{_libdir}/%{name}/plugin/authentication_oci_client.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_audit_api_message_emit.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_keyring_file.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_log_filter_dragnet.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_log_sink_json.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_log_sink_syseventlog.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_mysqlbackup.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_mysqlx_global_reset.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_pfs_example.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_pfs_example_component_population.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_query_attributes.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_reference_cache.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_udf_*_func.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_validate_password.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/conflicting_variables.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/connection_control.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/ddl_rewriter.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/group_replication.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/ha_mock.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/keyring_file.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/keyring_udf.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libpluginmecab.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/locking_service.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/mypluglib.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/mysql_clone.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/mysql_no_login.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/qa_auth_client.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/qa_auth_interface.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/qa_auth_server.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/replication_observers_example_plugin.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/rewriter.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/semisync_master.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/semisync_replica.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/semisync_slave.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/semisync_source.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/validate_password.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/version_token.so
%if %{with sphinx}
%attr(755,root,root) %{_libdir}/%{name}/plugin/ha_sphinx.so
%endif
%dir %{_libdir}/%{name}/private
%{_libdir}/%{name}/private/icudt*l
%dir %{_libdir}/%{name}router
%attr(755,root,root) %{_libdir}/%{name}router/connection_pool.so
%attr(755,root,root) %{_libdir}/%{name}router/destination_status.so
%attr(755,root,root) %{_libdir}/%{name}router/http_auth_backend.so
%attr(755,root,root) %{_libdir}/%{name}router/http_auth_realm.so
%attr(755,root,root) %{_libdir}/%{name}router/http_server.so
%attr(755,root,root) %{_libdir}/%{name}router/io.so
%attr(755,root,root) %{_libdir}/%{name}router/keepalive.so
%attr(755,root,root) %{_libdir}/%{name}router/metadata_cache.so
%attr(755,root,root) %{_libdir}/%{name}router/rest_api.so
%attr(755,root,root) %{_libdir}/%{name}router/rest_connection_pool.so
%attr(755,root,root) %{_libdir}/%{name}router/rest_metadata_cache.so
%attr(755,root,root) %{_libdir}/%{name}router/rest_router.so
%attr(755,root,root) %{_libdir}/%{name}router/rest_routing.so
%attr(755,root,root) %{_libdir}/%{name}router/router_openssl.so
%attr(755,root,root) %{_libdir}/%{name}router/router_protobuf.so
%attr(755,root,root) %{_libdir}/%{name}router/routing.so
%dir %{_libdir}/%{name}router/private
%attr(755,root,root) %{_libdir}/%{name}router/private/libmysqlharness*.so*
%attr(755,root,root) %{_libdir}/%{name}router/private/libmysqlrouter*.so*
%{_mandir}/man1/ibd2sdi%{majorver}.1*
%{_mandir}/man1/innochecksum%{majorver}.1*
%{_mandir}/man1/my_print_defaults%{majorver}.1*
%{_mandir}/man1/myisamchk%{majorver}.1*
%{_mandir}/man1/myisamlog%{majorver}.1*
%{_mandir}/man1/myisampack%{majorver}.1*
%{_mandir}/man1/mysql_upgrade%{majorver}.1*
%{_mandir}/man1/mysqlcheck%{majorver}.1*
%{_mandir}/man1/mysqlrouter%{majorver}.1*
%{_mandir}/man1/mysqlrouter_passwd%{majorver}.1*
%{_mandir}/man1/mysqlrouter_plugin_info%{majorver}.1*
%{_mandir}/man8/mysqld%{majorver}.8*

%if %{?debug:1}0
%attr(755,root,root) %{_bindir}/*resolve_stack_dump
%{_datadir}/%{name}/mysqld.sym
%{_mandir}/man1/*resolve_stack_dump.1*
%endif

%attr(700,mysql,mysql) %{_mysqlhome}
# root:root is proper here for mysql.rpm while mysql:mysql is potential security hole
%attr(751,root,root) /var/lib/%{name}
%attr(750,mysql,mysql) %dir /var/lib/%{name}-files
%attr(750,mysql,mysql) %dir /var/log/%{name}
%attr(750,mysql,mysql) %dir /var/log/archive/%{name}
%attr(640,mysql,mysql) %ghost /var/log/%{name}/*

# This is template for configuration file which is created after 'service mysql init'
%{_datadir}/%{name}/mysqld.conf

%{_datadir}/%{name}/english
%{_datadir}/%{name}/dictionary.txt
%{_datadir}/%{name}/messages_to_clients.txt
%{_datadir}/%{name}/messages_to_error_log.txt
%{_datadir}/%{name}/install_rewriter.sql
%{_datadir}/%{name}/uninstall_rewriter.sql
# Don't mark these with %%lang. These are used depending
# on database client settings.
%{_datadir}/%{name}/bulgarian
%{_datadir}/%{name}/czech
%{_datadir}/%{name}/danish
%{_datadir}/%{name}/german
%{_datadir}/%{name}/greek
%{_datadir}/%{name}/spanish
%{_datadir}/%{name}/estonian
%{_datadir}/%{name}/french
%{_datadir}/%{name}/hungarian
%{_datadir}/%{name}/italian
%{_datadir}/%{name}/japanese
%{_datadir}/%{name}/korean
%{_datadir}/%{name}/dutch
%{_datadir}/%{name}/norwegian
%{_datadir}/%{name}/norwegian-ny
%{_datadir}/%{name}/polish
%{_datadir}/%{name}/portuguese
%{_datadir}/%{name}/romanian
%{_datadir}/%{name}/russian
%{_datadir}/%{name}/serbian
%{_datadir}/%{name}/slovak
%{_datadir}/%{name}/swedish
%{_datadir}/%{name}/ukrainian

%files charsets
%defattr(644,root,root,755)
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/charsets

%files extras
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/myisam_ftdump%{majorver}
%attr(755,root,root) %{_bindir}/mysql_secure_installation%{majorver}
%attr(755,root,root) %{_bindir}/mysql_ssl_rsa_setup%{majorver}
%attr(755,root,root) %{_bindir}/mysql_tzinfo_to_sql%{majorver}
%attr(755,root,root) %{_bindir}/perror%{majorver}
%{_mandir}/man1/myisam_ftdump%{majorver}.1*
%{_mandir}/man1/mysql_ssl_rsa_setup%{majorver}.1*
%{_mandir}/man1/mysql_secure_installation%{majorver}.1*
%{_mandir}/man1/mysql_tzinfo_to_sql%{majorver}.1*
%{_mandir}/man1/perror%{majorver}.1*

%files extras-perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysqldumpslow%{majorver}
%{_mandir}/man1/mysqldumpslow%{majorver}.1*

%files client
%defattr(644,root,root,755)
%attr(600,root,root) %config(noreplace,missingok) %verify(not md5 mtime size) /etc/skel/.my.cnf
%attr(755,root,root) %{_bindir}/mysql%{majorver}
%attr(755,root,root) %{_bindir}/mysqladmin%{majorver}
%attr(755,root,root) %{_bindir}/mysqlbinlog%{majorver}
%attr(755,root,root) %{_bindir}/mysql_config_editor%{majorver}
%attr(755,root,root) %{_bindir}/mysqldump%{majorver}
%attr(755,root,root) %{_bindir}/mysqlimport%{majorver}
%attr(755,root,root) %{_bindir}/mysqlpump%{majorver}
%attr(755,root,root) %{_bindir}/mysqlshow%{majorver}
%{_mandir}/man1/mysql%{majorver}.1*
%{_mandir}/man1/mysqladmin%{majorver}.1*
%{_mandir}/man1/mysqlbinlog%{majorver}.1*
%{_mandir}/man1/mysql_config_editor%{majorver}.1*
%{_mandir}/man1/mysqldump%{majorver}.1*
%{_mandir}/man1/mysqlimport%{majorver}.1*
%{_mandir}/man1/mysqlpump%{majorver}.1*
%{_mandir}/man1/mysqlshow%{majorver}.1*

%files libs
%defattr(644,root,root,755)
%attr(751,root,root) %dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/mysql-client.conf
%{_sysconfdir}/%{name}/my.cnf
%attr(755,root,root) %{_libdir}/libmysqlclient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmysqlclient.so.21
%if %{with ndb}
%attr(755,root,root) %{_libdir}/libndbclient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libndbclient.so.3
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysql_config%{majorver}
%attr(755,root,root) %{_libdir}/libmysqlclient.so
%if %{with ndb}
%attr(755,root,root) %{_libdir}/libndbclient.so
%endif
%{_pkgconfigdir}/mysqlclient.pc
%{_libdir}/libmysqlservices.a
%{_includedir}/mysql
%{_aclocaldir}/mysql.m4
%{_mandir}/man1/mysql_config%{majorver}.1*

%files static
%defattr(644,root,root,755)
%{_libdir}/libmysqlclient.a
%if %{with ndb}
%{_libdir}/libndbclient.a
%endif

# rename to test or split?
%files bench
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/comp_err%{majorver}
%attr(755,root,root) %{_bindir}/mysql_keyring_encryption_test%{majorver}
%attr(755,root,root) %{_bindir}/mysqlslap%{majorver}
%attr(755,root,root) %{_bindir}/mysqltest%{majorver}
%attr(755,root,root) %{_bindir}/mysqltest_safe_process%{majorver}
%attr(755,root,root) %{_bindir}/zlib_decompress%{majorver}
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_example_component1.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_example_component2.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_example_component3.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_log_sink_test.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_audit_api_message.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_backup_lock_service.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_component_deinit.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_host_application_signal.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_mysql_current_thread_reader.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_mysql_runtime_error.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_mysql_system_variable_set.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_pfs_notification.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_pfs_resource_group.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_sensitive_system_variables.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_status_var_service.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_status_var_service_int.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_status_var_service_reg_only.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_status_var_service_str.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_status_var_service_unreg_only.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_string_service.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_string_service_charset.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_string_service_long.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_sys_var_service.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_sys_var_service_int.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_sys_var_service_same.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_sys_var_service_str.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_system_variable_source.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_table_access.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/component_test_udf_registration.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/pfs_example_plugin_employee.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/test_services_host_application_signal.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/test_services_plugin_registry.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/udf_example.so
#%dir %{_datadir}/sql-bench
#%{_datadir}/sql-bench/[CDRl]*
#%attr(755,root,root) %{_datadir}/sql-bench/[bcgirst]*
%{_mandir}/man1/lz4_decompress.1*
%{_mandir}/man1/mysqlslap%{majorver}.1*
%{_mandir}/man1/zlib_decompress%{majorver}.1*

#%files doc
#%defattr(644,root,root,755)
#%doc Docs/manual.html Docs/manual_toc.html

%if %{with ndb}
%files ndb
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ndbd%{majorver}
%attr(754,root,root) /etc/rc.d/init.d/%{name}-ndb
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mysql-ndb
%{_mandir}/man1/ndbd_redo_log_reader%{majorver}.1*
%{_mandir}/man8/ndbd%{majorver}.8*

%files ndb-client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ndb_config%{majorver}
%attr(755,root,root) %{_bindir}/ndb_delete_all%{majorver}
%attr(755,root,root) %{_bindir}/ndb_desc%{majorver}
%attr(755,root,root) %{_bindir}/ndb_drop_index%{majorver}
%attr(755,root,root) %{_bindir}/ndb_drop_table%{majorver}
%attr(755,root,root) %{_bindir}/ndb_error_reporter%{majorver}
%attr(755,root,root) %{_bindir}/ndb_mgm%{majorver}
%attr(755,root,root) %{_bindir}/ndb_print_backup_file%{majorver}
%attr(755,root,root) %{_bindir}/ndb_print_schema_file%{majorver}
%attr(755,root,root) %{_bindir}/ndb_print_sys_file%{majorver}
%attr(755,root,root) %{_bindir}/ndb_restore%{majorver}
%attr(755,root,root) %{_bindir}/ndb_select_all%{majorver}
%attr(755,root,root) %{_bindir}/ndb_select_count%{majorver}
%attr(755,root,root) %{_bindir}/ndb_show_tables%{majorver}
%attr(755,root,root) %{_bindir}/ndb_size.pl%{majorver}
%attr(755,root,root) %{_bindir}/ndb_test_platform%{majorver}
%attr(755,root,root) %{_bindir}/ndb_waiter%{majorver}
%{_mandir}/man1/ndb_config%{majorver}.1*
%{_mandir}/man1/ndb_delete_all%{majorver}.1*
%{_mandir}/man1/ndb_desc%{majorver}.1*
%{_mandir}/man1/ndb_drop_index%{majorver}.1*
%{_mandir}/man1/ndb_drop_table%{majorver}.1*
%{_mandir}/man1/ndb_error_reporter%{majorver}.1*
%{_mandir}/man1/ndb_mgm%{majorver}.1*
%{_mandir}/man1/ndb_print_backup_file%{majorver}.1*
%{_mandir}/man1/ndb_print_schema_file%{majorver}.1*
%{_mandir}/man1/ndb_print_sys_file%{majorver}.1*
%{_mandir}/man1/ndb_restore%{majorver}.1*
%{_mandir}/man1/ndb_select_all%{majorver}.1*
%{_mandir}/man1/ndb_select_count%{majorver}.1*
%{_mandir}/man1/ndb_show_tables%{majorver}.1*
%{_mandir}/man1/ndb_size.pl%{majorver}.1*
%{_mandir}/man1/ndb_waiter%{majorver}.1*

%files ndb-mgm
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ndb_mgmd%{majorver}
%attr(754,root,root) /etc/rc.d/init.d/%{name}-ndb-mgm
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mysql-ndb-mgm
%{_mandir}/man8/ndb_mgmd%{majorver}.8*

%files ndb-cpc
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ndb_cpcd%{majorver}
%attr(754,root,root) /etc/rc.d/init.d/%{name}-ndb-cpc
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mysql-ndb-cpc
%{_mandir}/man1/ndb_cpcd%{majorver}.1*
%endif
