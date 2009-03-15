# TODO:
# - trigger that prepares system from pre-cluster into cluster
# - trigger /etc/mysqld.conf into /etc/mysql/mysqld.conf. Solve possible
#   conflict with /var/lib/mysql/mysqld.conf
# - what's the libwrapper constistent name, i see in specs 'libwrap', 'tcpd', 'tcp_wrappers'
# - hangs on memcpy() (even mysql client does that) when built on Th, probably some problems
#   with overlaping areas. Note that Ac binaries run fine on Th
#
# Conditional build:
%bcond_with	bdb	# Berkeley DB support
%bcond_without	innodb	# Without InnoDB support
%bcond_without	isam	# Without ISAM table format (used in mysql 3.22)
%bcond_without	raid	# Without raid
%bcond_without	ssl	# Without OpenSSL
%bcond_without	tcpd	# Without libwrap (tcp_wrappers) support
#
%include	/usr/lib/rpm/macros.perl
Summary:	MySQL: a very fast and reliable SQL database engine
Summary(fr):	MySQL: un serveur SQL rapide et fiable
Summary(pl):	MySQL: bardzo szybka i niezawodna baza danych (SQL)
Summary(pt_BR):	MySQL: Um servidor SQL r·pido e confi·vel
Summary(ru):	MySQL - ¬Ÿ”‘“Ÿ  SQL-”≈“◊≈“
Summary(uk):	MySQL - €◊…ƒÀ…  SQL-”≈“◊≈“
Summary(zh_CN):	MySQL ˝æ›ø‚∑˛ŒÒ∆˜
Name:		mysql
Version:	4.0.30
Release:	3
License:	GPL + MySQL FLOSS Exception
Group:		Applications/Databases
Source0:	http://mirror.provenscaling.com/mysql/community/source/4.0/%{name}-%{version}.tar.gz
# Source0-md5:	35b838f40fa1f1d7feb9e65b42eea449
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Source4:	%{name}d.conf
Source5:	%{name}-clusters.conf
Source6:	%{name}.monitrc
Patch0:		%{name}-libs.patch
Patch1:		%{name}-libwrap.patch
Patch2:		%{name}-c++.patch
Patch3:		%{name}-_r-link.patch
Patch4:		%{name}-info.patch
Patch5:		%{name}-sql-cxx-pic.patch
Patch6:		%{name}-noproc.patch
Patch7:		%{name}-fix_privilege_tables.patch
Patch8:		%{name}-nptl.patch
Patch9:		%{name}-bug-27198.patch
Patch10:	%{name}-rename-table.patch
URL:		http://www.mysql.com/
BuildRequires:	/bin/ps
#BuildRequires:	ORBit-devel
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
BuildRequires:	rpmbuild(macros) >= 1.159
BuildRequires:	texinfo
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	/usr/bin/setsid
Requires:	rc-scripts >= 0.2.0
Provides:	MySQL-server
Provides:	group(mysql)
Provides:	msqlormysql
Provides:	user(mysql)
Obsoletes:	MySQL
Obsoletes:	mysql-server
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_libexecdir	%{_sbindir}
%define		_localstatedir	/var/lib/mysql
%define		_mysqlhome	/home/services/mysql

%define		_noautoreqdep	'perl(DBD::mysql)'
# workaround for buggy gcc 3.3.1
%define 	specflags_alpha  -mno-explicit-relocs

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
MySQL to prawdziwie wielouøytkownikowy, wielow±tkowy serwer baz danych
SQL. SQL jest najpopularniejszym na ∂wiecie jÍzykiem uøywanym do baz
danych. MySQL to implementacja klient/serwer sk≥adaj±ca siÍ z demona
mysqld i wielu rÛønych programÛw i bibliotek klienckich.

G≥Ûwnymi celami MySQL-a s± szybko∂Ê, potÍga i ≥atwo∂Ê uøytkowania.
MySQL oryginalnie by≥ tworzony, poniewaø autorzy w Tcx potrzebowali
serwera SQL do obs≥ugi bardzo duøych baz danych z szybko∂ci± o wiele
wiÍksz±, niø mogli zaoferowaÊ inni producenci baz danych. Uøywaj± go
od 1996 roku w ∂rodowisku z ponad 40 bazami danych, 10 000 tabel, z
ktÛrych ponad 500 zawiera ponad 7 milionÛw rekordÛw - w sumie oko≥o
50GB krytycznych danych.

Baza, na ktÛrej oparty jest MySQL, sk≥ada siÍ ze zbioru procedur,
ktÛre by≥y uøywane w bardzo wymagaj±cym ∂rodowisku produkcyjnym przez
wiele lat. Pomimo, øe MySQL jest ci±gle rozwijany, juø oferuje bogaty
i uøyteczny zbiÛr funkcji.

%description -l pt_BR
O MySQL È um servidor de banco de dados SQL realmente multiusu·rio e
multi-tarefa. A linguagem SQL È a mais popular linguagem para banco de
dados no mundo. O MySQL È uma implementaÁ„o cliente/servidor que
consiste de um servidor chamado mysqld e diversos
programas/bibliotecas clientes. Os principais objetivos do MySQL s„o:
velocidade, robustez e facilidade de uso. O MySQL foi originalmente
desenvolvido porque nÛs na Tcx precis·vamos de um servidor SQL que
pudesse lidar com grandes bases de dados e com uma velocidade muito
maior do que a que qualquer vendedor podia nos oferecer. Estamos
usando o MySQL desde 1996 em um ambiente com mais de 40 bases de dados
com 10.000 tabelas, das quais mais de 500 tÍm mais de 7 milhıes de
linhas. Isto È o equivalente a aproximadamente 50G de dados crÌticos.
A base da construÁ„o do MySQL È uma sÈrie de rotinas que foram usadas
em um ambiente de produÁ„o com alta demanda por muitos anos. Mesmo o
MySQL estando ainda em desenvolvimento, ele j· oferece um conjunto de
funÁıes muito ricas e ˙teis. Veja a documentaÁ„o para maiores
informaÁıes.

%description -l ru
MySQL - ‹‘œ SQL (Structured Query Language) ”≈“◊≈“ ¬¡⁄Ÿ ƒ¡ŒŒŸ». MySQL
¬ŸÃ¡ Œ¡–…”¡Œ¡ Michael'œÕ (monty) Widenius'œÕ. ÛÕ. ∆¡ Ã CREDITS ◊
ƒ…”‘“…¬’‘…◊≈ Œ¡ –“≈ƒÕ≈‘ ƒ“’«…» ’ﬁ¡”‘Œ…Àœ◊ –“œ≈À‘¡ … –“œﬁ≈  …Œ∆œ“Õ¡√……
œ MySQL.

%description -l uk
MySQL - √≈ SQL (Structured Query Language) ”≈“◊≈“ ¬¡⁄… ƒ¡Œ…». MySQL
¬’Ãœ Œ¡–…”¡Œœ Michael'œÕ (monty) Widenius'œÕ. ‰…◊. ∆¡ Ã CREDITS ◊
ƒ…”‘“…¬’‘…◊¶ ƒÃ— ¶Œ∆œ“Õ¡√¶ß –“œ ¶Œ€…» ’ﬁ¡”Œ…À¶◊ –“œ≈À‘’ ‘¡ ¶Œ€œß
¶Œ∆œ“Õ¡√¶ß.

%package extras
Summary:	MySQL additional utilities
Summary(pl):	Dodatkowe narzÍdzia do MySQL
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description extras
MySQL additional utilities except Perl scripts (they may be found in
%{name}-extras-perl package).

%description extras -l pl
Dodatkowe narzÍdzia do MySQL - z wyj±tkiem skryptÛw Perla (ktÛre s± w
pakiecie %{name}-extras-perl).

%package extras-perl
Summary:	MySQL additional utilities written in Perl
Summary(pl):	Dodatkowe narzÍdzia do MySQL napisane w Perlu
Group:		Applications/Databases
Requires:	%{name}-extras = %{version}-%{release}
Requires:	perl(DBD::mysql)

%description extras-perl
MySQL additional utilities written in Perl.

%description extras-perl -l pl
Dodatkowe narzÍdzia do MySQL napisane w Perlu.

%package client
Summary:	MySQL - Client
Summary(pl):	MySQL - Klient
Summary(pt):	MySQL - Cliente
Summary(ru):	MySQL ÀÃ…≈Œ‘
Summary(uk):	MySQL ÀÃ¶§Œ‘
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
Este pacote contÈm os clientes padr„o para o MySQL.

%description client -l ru
¸‘œ‘ –¡À≈‘ ”œƒ≈“÷…‘ ‘œÃÿÀœ ÀÃ…≈Œ‘ MySQL.

%description client -l uk
„≈  –¡À≈‘ Õ¶”‘…‘ÿ ‘¶ÃÿÀ… ÀÃ¶§Œ‘¡ MySQL.

%package libs
Summary:	Shared libraries for MySQL
Summary(pl):	Biblioteki dzielone MySQL
Group:		Applications/Databases
Obsoletes:	libmysql10
Obsoletes:	mysql-doc < 4.0.25-1

%description libs
Shared libraries for MySQL.

%description libs -l pl
Biblioteki dzielone MySQL.

%package devel
Summary:	MySQL - Development header files and libraries
Summary(pl):	MySQL - Pliki nag≥Ûwkowe i biblioteki dla programistÛw
Summary(pt):	MySQL - MediÁıes de desempenho
Summary(ru):	MySQL - »≈ƒ≈“Ÿ … ¬…¬Ã…œ‘≈À… “¡⁄“¡¬œ‘ﬁ…À¡
Summary(uk):	MySQL - »≈ƒ≈“… ‘¡ ¬¶¬Ã¶œ‘≈À… –“œ«“¡Õ¶”‘¡
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
Pliki nag≥Ûwkowe i biblioteki konieczne do kompilacji aplikacji
klienckich MySQL.

%description devel -l pt_BR
Este pacote contÈm os arquivos de cabeÁalho (header files) e
bibliotecas necess·rias para desenvolver aplicaÁıes clientes do MySQL.

%description devel -l ru
¸‘œ‘ –¡À≈‘ ”œƒ≈“÷…‘ »≈ƒ≈“Ÿ … ¬…¬Ã…œ‘≈À… “¡⁄“¡¬œ‘ﬁ…À¡, Œ≈œ¬»œƒ…ÕŸ≈ ƒÃ—
“¡⁄“¡¬œ‘À… ÀÃ…≈Œ‘”À…» –“…Ãœ÷≈Œ… .

%description devel -l uk
„≈  –¡À≈‘ Õ¶”‘…‘ÿ »≈ƒ≈“… ‘¡ ¬¶¬Ã¶œ‘≈À… –“œ«“¡Õ¶”‘¡, Œ≈œ¬»¶ƒŒ¶ ƒÃ—
“œ⁄“œ¬À… –“œ«“¡Õ-ÀÃ¶§Œ‘¶◊.

%package static
Summary:	MySQL static libraries
Summary(pl):	Biblioteki statyczne MySQL
Summary(ru):	MySQL - ”‘¡‘…ﬁ≈”À…≈ ¬…¬Ã…œ‘≈À…
Summary(uk):	MySQL - ”‘¡‘…ﬁŒ¶ ¬¶¬Ã¶œ‘≈À…
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	MySQL-static

%description static
MySQL static libraries.

%description static -l pl
Biblioteki statyczne MySQL.

%description static -l ru
¸‘œ‘ –¡À≈‘ ”œƒ≈“÷…‘ ”‘¡‘…ﬁ≈”À…≈ ¬…¬Ã…œ‘≈À… “¡⁄“¡¬œ‘ﬁ…À¡, Œ≈œ¬»œƒ…ÕŸ≈
ƒÃ— “¡⁄“¡¬œ‘À… ÀÃ…≈Œ‘”À…» –“…Ãœ÷≈Œ… .

%description static -l uk
„≈  –¡À≈‘ Õ¶”‘…‘ÿ ”‘¡‘…ﬁŒ¶ ¬¶¬Ã¶œ‘≈À… –“œ«“¡Õ¶”‘¡, Œ≈œ¬»¶ƒŒ¶ ƒÃ—
“œ⁄“œ¬À… –“œ«“¡Õ-ÀÃ¶§Œ‘¶◊.

%package bench
Summary:	MySQL - Benchmarks
Summary(pl):	MySQL - Programy testuj±ce szybko∂Ê dzia≥ania bazy
Summary(pt):	MySQL - MediÁıes de desempenho
Summary(ru):	MySQL - ¬≈ŒﬁÕ¡“À…
Summary(uk):	MySQL - ¬≈ŒﬁÕ¡“À…
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-client
Requires:	perl(DBD::mysql)
Obsoletes:	MySQL-bench

%description bench
This package contains MySQL benchmark scripts and data.

%description bench -l pl
Programy testuj±ce szybko∂Ê serwera MySQL.

%description bench -l pt_BR
Este pacote contÈm mediÁıes de desempenho de scripts e dados do MySQL.

%description bench -l ru
¸‘œ‘ –¡À≈‘ ”œƒ≈“÷…‘ ”À“…–‘Ÿ … ƒ¡ŒŒŸ≈ ƒÃ— œ√≈ŒÀ… –“œ…⁄◊œƒ…‘≈ÃÿŒœ”‘…
MySQL.

%description bench -l uk
„≈  –¡À≈‘ Õ¶”‘…‘ÿ ”À“…–‘… ‘¡ ƒ¡Œ¶ ƒÃ— œ√¶ŒÀ… –“œƒ’À‘…◊Œœ”‘¶ MySQL.

%package doc
Summary:	MySQL manual
Summary(pl):	PodrÍcznik uøytkownika MySQL
Group:		Applications/Databases

%description doc
This package contains manual in HTML format.

%description doc -l pl
PodrÍcznik MySQL-a w formacie HTML.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
# in 4.0.25 there is no source for info file
#%patch4 -p1
%ifarch alpha
# this is strange: mysqld functions for UDF modules are not explicitly defined,
# so -rdynamic is used; in such case gcc3+ld on alpha doesn't like C++ vtables
# in objects compiled without -fPIC
%patch5 -p1
%endif
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
# The compiler flags are as per their "official" spec ;)
CXXFLAGS="%{rpmcflags} -felide-constructors -fno-rtti -fno-exceptions %{!?debug:-fomit-frame-pointer}"
CFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"
%configure \
	PS='/bin/ps' \
	FIND_PROC='/bin/ps p $$PID' \
	KILL='/bin/kill' \
	CHECK_PID='/bin/kill -0 $$PID' \
	-C \
	--enable-assembler \
	--enable-shared \
	--enable-static \
	--enable-thread-safe-client \
	--with%{!?with_bdb:out}-berkeley-db \
	--with%{!?with_innodb:out}-innodb \
	--with%{!?with_isam:out}-isam \
	--with%{!?with_raid:out}-raid \
	--with%{!?with_ssl:out}-openssl \
	--with%{!?with_tcpd:out}-libwrap \
	--with-comment="PLD Linux Distribution MySQL RPM" \
	--with%{!?debug:out}-debug \
	--with-embedded-server \
	--with-extra-charsets=all \
	--with-low-memory \
	--with-mysqld-user=mysql \
	--with-named-curses-libs="-lncurses" \
	--with-pthread \
	--with-unix-socket-path=/var/lib/mysql/mysql.sock \
	--with-vio \
	--without-readline \
	--without-docs
#	--with-mysqlfs

# NOTE that /var/lib/mysql/mysql.sock is symlink to real sock file
# (it defaults to first cluster but user may change it to whatever
#  cluster it wants)

echo -e "all:\ninstall:\nclean:\nlink_sources:\n" > libmysqld/examples/Makefile

%{__make} benchdir=$RPM_BUILD_ROOT%{_datadir}/sql-bench
# workaround for missing files
(cd Docs; touch Images/cluster-components-1.txt Images/multi-comp-1.txt errmsg-table.texi cl-errmsg-table.texi)
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
install %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/mysql/mysqld.conf
install %{SOURCE4} mysqld.conf
install %{SOURCE5} $RPM_BUILD_ROOT/etc/mysql/clusters.conf
install %{SOURCE6} $RPM_BUILD_ROOT/etc/monit
touch $RPM_BUILD_ROOT/var/log/mysql/{err,log,update,isamlog.log}

# remove innodb directives from mysqld.conf if mysqld is configured without
%if !%{with innodb}
	cp mysqld.conf mysqld.tmp
	awk 'BEGIN { RS="\n\n" } !/innodb/ { printf("%s\n\n", $0) }' < mysqld.tmp > mysqld.conf
%endif

# remove berkeley-db directives from mysqld.conf if mysqld is configured without
%if !%{with bdb}
	cp mysqld.conf mysqld.tmp
	awk 'BEGIN { RS="\n\n" } !/bdb/ { printf("%s\n\n", $0) }' < mysqld.tmp > mysqld.conf
%endif

install mysqld.conf $RPM_BUILD_ROOT%{_datadir}/mysql/mysqld.conf

# remove mysqld's *.po files
find . $RPM_BUILD_ROOT%{_datadir}/%{name} -name \*.txt | xargs -n 100 rm -f
mv -f $RPM_BUILD_ROOT%{_libdir}/mysql/lib* $RPM_BUILD_ROOT%{_libdir}
%{__perl} -pi -e 's,%{_libdir}/mysql,%{_libdir},;' $RPM_BUILD_ROOT%{_libdir}/libmysqlclient.la

rm -rf $RPM_BUILD_ROOT%{_prefix}/mysql-test

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/usr/bin/getgid mysql`" ]; then
	if [ "`/usr/bin/getgid mysql`" != "89" ]; then
		echo "Error: group mysql doesn't have gid=89. Correct this before installing mysql." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 89 mysql
fi
if [ -n "`/bin/id -u mysql 2>/dev/null`" ]; then
	if [ "`/bin/id -u mysql`" != "89" ]; then
		echo "Error: user mysql doesn't have uid=89. Correct this before installing mysql." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 89 \
			-d %{_mysqlhome} -s /bin/sh -g mysql \
			-c "MySQL Server" mysql 1>&2
fi

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/sbin/chkconfig --add mysql
if [ -f /var/lock/subsys/mysql ]; then
	/etc/rc.d/init.d/mysql restart >&2
else
	echo "Run \"/etc/rc.d/init.d/mysql start\" to start mysql." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/mysql ]; then
		/etc/rc.d/init.d/mysql stop
	fi
	/sbin/chkconfig --del mysql
fi

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
if [ "$1" = "0" ]; then
	%userremove mysql
	%groupremove mysql
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

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/mysql
%attr(754,root,root) /etc/rc.d/init.d/mysql
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mysql
%attr(751,root,root) %dir /etc/mysql
%attr(640,root,mysql) %config(noreplace) %verify(not md5 mtime size) /etc/mysql/clusters.conf
%attr(750,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/monit/*.monitrc
%attr(755,root,root) %{_bindir}/isamchk
%attr(755,root,root) %{_bindir}/isamlog
%attr(755,root,root) %{_bindir}/myisamchk
%attr(755,root,root) %{_bindir}/myisamlog
%attr(755,root,root) %{_bindir}/myisampack
%attr(755,root,root) %{_bindir}/pack_isam
%attr(755,root,root) %{_sbindir}/mysqld
%{_mandir}/man1/isamchk.1*
%{_mandir}/man1/isamlog.1*
%{_mandir}/man8/mysqld.8*

%attr(700,mysql,mysql) %{_mysqlhome}
# root:root is proper here for AC mysql.rpm while mysql:mysql is potential security hole
%attr(751,root,root) /var/lib/mysql
%attr(750,mysql,mysql) %dir /var/log/mysql
%attr(750,mysql,mysql) %dir /var/log/archiv/mysql
%attr(640,mysql,mysql) %config(noreplace) %verify(not md5 mtime size) /var/log/mysql/*

%{_infodir}/mysql.info*
%dir %{_datadir}/mysql
# This is template for configuration file which is created after 'service mysql init'
%{_datadir}/mysql/mysqld.conf
%{_datadir}/mysql/charsets
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
%lang(sk) %{_datadir}/mysql/slovak
%lang(sv) %{_datadir}/mysql/swedish
%lang(uk) %{_datadir}/mysql/ukrainian

%files extras
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/msql2mysql
%attr(755,root,root) %{_bindir}/mysql_fix_privilege_tables
%attr(755,root,root) %{_bindir}/perror
%attr(755,root,root) %{_bindir}/my_print_defaults
%attr(755,root,root) %{_bindir}/replace
%attr(755,root,root) %{_bindir}/resolveip
%{_mandir}/man1/mysql_fix_privilege_tables.1*
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
%{_mandir}/man1/mysql_zap.1*
%{_mandir}/man1/mysqlaccess.1*

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysql
%attr(755,root,root) %{_bindir}/mysqlbug
%attr(755,root,root) %{_bindir}/mysqldump
%attr(755,root,root) %{_bindir}/mysqlimport
%attr(755,root,root) %{_bindir}/mysqlmanager*
%attr(755,root,root) %{_bindir}/mysqlshow
%attr(755,root,root) %{_bindir}/mysqlbinlog
%attr(755,root,root) %{_bindir}/mysqladmin
%attr(755,root,root) %{_bindir}/mysqltest
%{_mandir}/man1/mysql.1*
%{_mandir}/man1/mysqladmin.1*
%{_mandir}/man1/mysqldump.1*
%{_mandir}/man1/mysqlshow.1*

%files libs
%defattr(644,root,root,755)
%doc EXCEPTIONS-CLIENT
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysql_config
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/lib*[!tr].a
%{_includedir}/mysql

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*[tr].a

%files bench
%defattr(644,root,root,755)
%dir %{_datadir}/sql-bench
%{_datadir}/sql-bench/[CDRl]*
%attr(755,root,root) %{_datadir}/sql-bench/[bcgrst]*

#%files doc
#%defattr(644,root,root,755)
#%doc Docs/manual.html Docs/manual_toc.html
