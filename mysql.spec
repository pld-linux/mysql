#
# Conditional build:
# _with_bdb - Berkeley DB support
#
%include	/usr/lib/rpm/macros.perl
Summary:	MySQL: a very fast and reliable SQL database engine
Summary(fr):	MySQL: un serveur SQL rapide et fiable
Summary(pl):	MySQL: bardzo szybka i niezawodna baza danych (SQL)
Summary(pt_BR):	MySQL: Um servidor SQL rápido e confiável
Summary(ru):	MySQL - ÂÙÓÔÒÙÊ SQL-ÓÅÒ×ÅÒ
Summary(uk):	MySQL - Û×ÉÄËÉÊ SQL-ÓÅÒ×ÅÒ
Summary(zh_CN):	MySQLÊý¾Ý¿â·þÎñÆ÷
Name:		mysql
Group:		Applications/Databases
Version:	4.0.14
Release:	1
License:	GPL/LGPL
Source0:	http://sunsite.icm.edu.pl/mysql/Downloads/MySQL-4.0/mysql-%{version}.tar.gz
# Source0-md5:	9764f09c89692345d3b7800ab014f822
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Source4:	%{name}d.conf
Patch0:		%{name}-libs.patch
Patch1:		%{name}-libwrap.patch
Patch2:		%{name}-c++.patch
Patch3:		%{name}-_r-link.patch
Patch4:		%{name}-info.patch
Patch5:		%{name}-dump_quote_db_names.patch
Patch6:		%{name}-manfixes.patch
Patch7:		%{name}-sql-cxx-pic.patch
Patch8:		%{name}-noproc.patch
Icon:		mysql.gif
URL:		http://www.mysql.com/
#BuildRequires:	ORBit-devel
BuildRequires:	/bin/ps
BuildRequires:	autoconf
BuildRequires:	automake
%{?_with_bdb:BuildRequires:	db3-devel}
BuildRequires:	libstdc++-devel >= 5:3.0
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRequires:	ncurses-devel >= 4.2
BuildRequires:	openssl-devel
BuildRequires:	perl-DBI
BuildRequires:	perl-devel >= 5.6.1
BuildRequires:	readline-devel >= 4.2
BuildRequires:	rpm-perlprov
BuildRequires:	texinfo
BuildRequires:	zlib-devel
PreReq:		rc-scripts >= 0.2.0
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}
Provides:	MySQL-server
Provides:	msqlormysql
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	MySQL
Obsoletes:	mysql-server

%define		_libexecdir	%{_sbindir}
%define		_localstatedir	/var/lib/mysql
%define		_mysqlhome	/home/services/mysql

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
od 1996 roku w drodowisku z ponad 40 bazami danych, 10 000 tabel,
z których ponad 500 zawiera ponad 7 milionów rekordów - w sumie oko³o
50GB krytycznych danych.

Baza, na której oparty jest MySQL, sk³ada siê ze zbioru procedur,
które by³y u¿ywane w bardzo wymagaj±cym ¶rodowisku produkcyjnym przez
wiele lat. Pomimo, ¿e MySQL jest ci±gle rozwijany, ju¿ oferuje bogaty
i u¿yteczny zbiór funkcji.

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
ÂÙÌÁ ÎÁÐÉÓÁÎÁ Michael'ÏÍ (monty) Widenius'ÏÍ. óÍ. ÆÁÊÌ CREDITS ×
ÄÉÓÔÒÉÂÕÔÉ×Å ÎÁ ÐÒÅÄÍÅÔ ÄÒÕÇÉÈ ÕÞÁÓÔÎÉËÏ× ÐÒÏÅËÔÁ É ÐÒÏÞÅÊ ÉÎÆÏÒÍÁÃÉÉ
Ï MySQL.

%description -l uk
MySQL - ÃÅ SQL (Structured Query Language) ÓÅÒ×ÅÒ ÂÁÚÉ ÄÁÎÉÈ. MySQL
ÂÕÌÏ ÎÁÐÉÓÁÎÏ Michael'ÏÍ (monty) Widenius'ÏÍ. äÉ×. ÆÁÊÌ CREDITS ×
ÄÉÓÔÒÉÂÕÔÉ×¦ ÄÌÑ ¦ÎÆÏÒÍÁÃ¦§ ÐÒÏ ¦ÎÛÉÈ ÕÞÁÓÎÉË¦× ÐÒÏÅËÔÕ ÔÁ ¦ÎÛÏ§
¦ÎÆÏÒÍÁÃ¦§.

%package extras
Summary:	MySQL additional utilities
Summary(pl):	Dodatkowe narzêdzia do MySQL
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}

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
Requires:	%{name}-extras = %{version}
Requires:	perl(DBD::mysql)

%define		_noautoreqdep	"perl(DBD::mysql)"

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
Requires:	%{name}-libs = %{version}
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
üÔÏÔ ÐÁËÅÔ ÓÏÄÅÒÖÉÔ ÔÏÌØËÏ ËÌÉÅÎÔ MySQL.

%description client -l uk
ãÅÊ ÐÁËÅÔ Í¦ÓÔÉÔØ Ô¦ÌØËÉ ËÌ¦¤ÎÔÁ MySQL.

%package libs
Summary:	Shared libraries for MySQL
Summary(pl):	Biblioteki dzielone MySQL
Group:		Applications/Databases
Obsoletes:	libmysql10

%description libs
Shared libraries for MySQL.

%description libs -l pl
Biblioteki dzielone MySQL.

%package devel
Summary:	MySQL - Development header files and libraries
Summary(pl):	MySQL - Pliki nag³ówkowe i biblioteki dla programistów
Summary(pt):	MySQL - Medições de desempenho
Summary(ru):	MySQL - ÈÅÄÅÒÙ É ÂÉÂÌÉÏÔÅËÉ ÒÁÚÒÁÂÏÔÞÉËÁ
Summary(uk):	MySQL - ÈÅÄÅÒÉ ÔÁ Â¦ÂÌ¦ÏÔÅËÉ ÐÒÏÇÒÁÍ¦ÓÔÁ
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}
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
üÔÏÔ ÐÁËÅÔ ÓÏÄÅÒÖÉÔ ÈÅÄÅÒÙ É ÂÉÂÌÉÏÔÅËÉ ÒÁÚÒÁÂÏÔÞÉËÁ, ÎÅÏÂÈÏÄÉÍÙÅ ÄÌÑ
ÒÁÚÒÁÂÏÔËÉ ËÌÉÅÎÔÓËÉÈ ÐÒÉÌÏÖÅÎÉÊ.

%description devel -l uk
ãÅÊ ÐÁËÅÔ Í¦ÓÔÉÔØ ÈÅÄÅÒÉ ÔÁ Â¦ÂÌ¦ÏÔÅËÉ ÐÒÏÇÒÁÍ¦ÓÔÁ, ÎÅÏÂÈ¦ÄÎ¦ ÄÌÑ
ÒÏÚÒÏÂËÉ ÐÒÏÇÒÁÍ-ËÌ¦¤ÎÔ¦×.

%package static
Summary:	MySQL staic libraris
Summary(pl):	Biblioteki statyczne MySQL
Summary(ru):	MySQL - ÓÔÁÔÉÞÅÓËÉÅ ÂÉÂÌÉÏÔÅËÉ
Summary(uk):	MySQL - ÓÔÁÔÉÞÎ¦ Â¦ÂÌ¦ÏÔÅËÉ
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}
Obsoletes:	MySQL-static

%description static
MySQL static libraries.

%description static -l pl
Biblioteki statyczne MySQL.

%description static -l ru
üÔÏÔ ÐÁËÅÔ ÓÏÄÅÒÖÉÔ ÓÔÁÔÉÞÅÓËÉÅ ÂÉÂÌÉÏÔÅËÉ ÒÁÚÒÁÂÏÔÞÉËÁ, ÎÅÏÂÈÏÄÉÍÙÅ
ÄÌÑ ÒÁÚÒÁÂÏÔËÉ ËÌÉÅÎÔÓËÉÈ ÐÒÉÌÏÖÅÎÉÊ.

%description static -l uk
ãÅÊ ÐÁËÅÔ Í¦ÓÔÉÔØ ÓÔÁÔÉÞÎ¦ Â¦ÂÌ¦ÏÔÅËÉ ÐÒÏÇÒÁÍ¦ÓÔÁ, ÎÅÏÂÈ¦ÄÎ¦ ÄÌÑ
ÒÏÚÒÏÂËÉ ÐÒÏÇÒÁÍ-ËÌ¦¤ÎÔ¦×.

%package bench
Summary:	MySQL - Benchmarks
Summary(pl):	MySQL - Programy testuj±ce szybko¶æ dzia³ania bazy
Summary(pt):	MySQL - Medições de desempenho
Summary(ru):	MySQL - ÂÅÎÞÍÁÒËÉ
Summary(uk):	MySQL - ÂÅÎÞÍÁÒËÉ
Group:		Applications/Databases
Requires:	%{name} = %{version}
Requires:	%{name}-client
Obsoletes:	MySQL-bench

%description bench
This package contains MySQL benchmark scripts and data.

%description bench -l pl
Programy testuj±ce szybko¶æ serwera MySQL.

%description bench -l pt_BR
Este pacote contém medições de desempenho de scripts e dados do MySQL.

%description bench -l ru
üÔÏÔ ÐÁËÅÔ ÓÏÄÅÒÖÉÔ ÓËÒÉÐÔÙ É ÄÁÎÎÙÅ ÄÌÑ ÏÃÅÎËÉ ÐÒÏÉÚ×ÏÄÉÔÅÌØÎÏÓÔÉ
MySQL.

%description bench -l uk
ãÅÊ ÐÁËÅÔ Í¦ÓÔÉÔØ ÓËÒÉÐÔÉ ÔÁ ÄÁÎ¦ ÄÌÑ ÏÃ¦ÎËÉ ÐÒÏÄÕËÔÉ×ÎÏÓÔ¦ MySQL.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%ifarch alpha
# this is strange: mysqld functions for UDF modules are not explicitly defined,
# so -rdynamic is used; in such case gcc3+ld on alpha doesn't like C++ vtables
# in objects compiled without -fPIC
%patch7 -p1
%endif
%patch8 -p1

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-exceptions %{!?debug:-fomit-frame-pointer}"
CFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"
%configure \
	PS='/bin/ps' \
	FIND_PROC='/bin/ps p $$PID' \
	KILL='/bin/kill' \
	CHECK_PID='/bin/kill -0 $$PID' \
	-C \
	--with-pthread \
	--with-raid \
	--with-unix-socket-path=/var/lib/mysql/mysql.sock \
	--with-mysqld-user=mysql \
	--with-libwrap \
	--with%{!?debug:out}-debug \
	%{?_with_bdb:--with-berkeley-db} \
	--with-embedded-server \
	--with-vio \
	--with-openssl \
	--with-extra-charsets=all \
	--enable-shared \
	--enable-static \
	--with-named-curses-libs="-lncurses" \
	--enable-assembler \
	--without-readline \
	--without-docs \
	--with-low-memory  \
	--with-comment="PLD Linux Distribution MySQL RPM" \
	--enable-thread-safe-client
#	--with-mysqlfs

echo -e "all:\ninstall:\nclean:\nlink_sources:\n" > libmysqld/examples/Makefile

%{__make} benchdir=$RPM_BUILD_ROOT%{_datadir}/sql-bench
%{__make} -C Docs mysql.info

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,rc.d/init.d,sysconfig} \
	   $RPM_BUILD_ROOT/var/{log/{archiv,}/mysql,lib/mysql/db} \
	   $RPM_BUILD_ROOT%{_infodir} \
	   $RPM_BUILD_ROOT%{_mysqlhome}

install -d $RPM_BUILD_ROOT/var/lib/mysql/innodb/{data,log}
%if %{?_with_bdb:1}%{!?_with_bdb:0}
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
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/mysqld.conf
touch $RPM_BUILD_ROOT/var/log/mysql/{err,log,update,isamlog.log}

# remove mysqld's *.po files
find . $RPM_BUILD_ROOT%{_datadir}/%{name} -name \*.txt | xargs -n 100 rm -f
mv -f $RPM_BUILD_ROOT%{_libdir}/mysql/lib* $RPM_BUILD_ROOT%{_libdir}
%{__perl} -pi -e 's,%{_libdir}/mysql,%{_libdir},;' $RPM_BUILD_ROOT%{_libdir}/libmysqlclient.la

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`getgid mysql`" ]; then
	if [ "`getgid mysql`" != "89" ]; then
		echo "Error: group mysql doesn't have gid=89. Correct this before installing mysql." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 89 -r -f mysql
fi
if [ -n "`id -u mysql 2>/dev/null`" ]; then
	if [ "`id -u mysql`" != "89" ]; then
		echo "Error: user mysql doesn't have uid=89. Correct this before installing mysql." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -M -o -r -u 89 \
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
	/usr/sbin/userdel mysql
	/usr/sbin/groupdel mysql
fi

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/logrotate.d/mysql
%attr(754,root,root) /etc/rc.d/init.d/mysql
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/mysql
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mysqld.conf
%attr(755,root,root) %{_bindir}/isamchk
%attr(755,root,root) %{_bindir}/isamlog
%attr(755,root,root) %{_bindir}/myisamchk
%attr(755,root,root) %{_bindir}/myisamlog
%attr(755,root,root) %{_bindir}/myisampack
%attr(755,root,root) %{_bindir}/pack_isam
%attr(755,root,root) %{_sbindir}/mysqld
%{_mandir}/man1/isamchk.1*
%{_mandir}/man1/isamlog.1*
%{_mandir}/man1/mysqld.1*

%attr(700,mysql,mysql) %{_mysqlhome}
%attr(751,mysql,mysql) /var/lib/mysql
%attr(750,mysql,mysql) %dir /var/log/mysql
%attr(750,mysql,mysql) %dir /var/log/archiv/mysql
%attr(640,mysql,mysql) %config(noreplace) %verify(not md5 size mtime) /var/log/mysql/*

%{_infodir}/mysql.info*
%dir %{_datadir}/mysql
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
%lang(nn) %{_datadir}/mysql/norwegian-ny
%lang(no) %{_datadir}/mysql/norwegian
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
%attr(755,root,root) %{_bindir}/mysql_config
%attr(755,root,root) %{_bindir}/mysql_fix_privilege_tables
%attr(755,root,root) %{_bindir}/perror
%attr(755,root,root) %{_bindir}/my_print_defaults
%attr(755,root,root) %{_bindir}/replace
%attr(755,root,root) %{_bindir}/resolveip
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
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/lib*.la
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*[^tr].a
%{_includedir}/mysql

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*[tr].a

%files bench
%defattr(644,root,root,755)
%dir %{_datadir}/sql-bench
%{_datadir}/sql-bench/[CDRl]*
%attr(755,root,root) %{_datadir}/sql-bench/[bcgrst]*
