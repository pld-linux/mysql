%include	/usr/lib/rpm/macros.perl
%define		__find_requires	%{_builddir}/mysql-%{version}/find-perl-requires
Summary:	MySQL: a very fast and reliable SQL database engine
Summary(fr):	MySQL: un serveur SQL rapide et fiable
Summary(pl):	MySQL: bardzo szybka i niezawodna baza danych (SQL)
Summary(pt_BR): MySQL: Um servidor SQL rápido e confiável.
Name:           mysql
Group:		Applications/Databases
Group(pl):	Aplikacje/Bazy Danych
Group(pt_BR):	Aplicações/Banco_de_Dados
Version:	3.22.30
Release:	2
License:	MySQL FREE PUBLIC LICENSE (See the file PUBLIC)
Source0:	http://www.mysql.com/Downloads/MySQL-3.22/%{name}-%{version}.tar.gz
Source1:	mysql.init
Source2:	mysql.sysconfig
Source3:	mysql.logrotate
Patch0:		mysql-info.patch
Patch1:		mysql-no_libbind.patch
Patch2:		mysql-perldep.patch
Icon:		mysql.gif
URL:		http://www.mysql.com/
Requires:	%{name}-libs = %{version}
BuildRequires:	libstdc++-devel
BuildRequires:	zlib-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	texinfo
BuildRequires:	rpm-perlprov
Prereq:		shadow
Provides:	msqlormysql MySQL-server
Obsoletes:	MySQL
BuildRoot:	/tmp/%{name}-%{version}

%define		_libexecdir	%{_prefix}/sbin
%define		_sysconfdir	/etc
%define		_localstatedir	/var/state/mysql

%description
MySQL is a true multi-user, multi-threaded SQL (Structured Query Language)
database server. SQL is the most popular database language in the world.
MySQL is a client/server implementation that consists of a server daemon
mysqld and many different client programs/libraries.

The main goals of MySQL are speed, robustness and easy to use. MySQL was
originally developed because we at Tcx needed a SQL server that could handle
very big databases with magnitude higher speed than what any database vendor
could offer to us. We have now been using MySQL since 1996 in a environment
with more than 40 databases, 10,000 tables, of which more than 500 have more
than 7 million rows. This is about 50G of mission critical data.

The base upon which MySQL is built is a set of routines that have been used
in a highly demanding production environment for many years. While MySQL is
still in development, it already offers a rich and highly useful function
set.

%description -l fr
MySQL est un serveur de bases de donnees SQL vraiment multi-usagers et
multi-taches. Le langage SQL est le langage de bases de donnees le plus
populaire au monde. MySQL est une implementation client/serveur qui consiste
en un serveur (mysqld) et differents programmes/bibliotheques clientes.

Les objectifs principaux de MySQL sont: vitesse, robustesse et facilite
d'utilisation. MySQL fut originalement developpe parce que nous, chez Tcx,
avions besoin d'un serveur SQL qui pouvait gerer de tres grandes bases de
donnees avec une vitesse d'un ordre de magnitude superieur a ce que
n'importe quel vendeur pouvait nous offrir. Nous utilisons MySQL depuis 1996
dans un environnement avec plus de 40 bases de donnees, 10000 tables,
desquelles plus de 500 ont plus de 7 millions de lignes. Ceci represente
environ 50G de donnees critiques.

A la base de la conception de MySQL, on retrouve une serie de routines qui
ont ete utilisees dans un environnement de production pendant plusieurs
annees. Meme si MySQL est encore en developpement, il offre deja une riche
et utile serie de fonctions.

%description -l pl
MySQL to wielow±tkowy serwer baz danych SQL.

G³ówne zalety MySQL to szybko¶æ, potêga i ³atwo¶æ u¿ytkowania. MySQL jes
wykorzystywany m.in. do obs³ugi 40 baz danych, 10 000 tabeli, gdzie ka¿da
tabela zawiera 7 milionów pozycji. To ok 50GB danych.

%description -l pt_BR
O MySQL é um servidor de banco de dados SQL realmente multiusuário e
multi-tarefa. A linguagem SQL é a mais popular linguagem para banco de dados
no mundo. O MySQL é uma implementação cliente/servidor que consiste de um
servidor chamado mysqld e diversos programas/bibliotecas clientes. Os
principais objetivos do MySQL são: velocidade, robustez e facilidade de uso. 
O MySQL foi originalmente desenvolvido porque nós na Tcx precisávamos de um
servidor SQL que pudesse lidar com grandes bases de dados e com uma
velocidade muito maior do que a que qualquer vendedor podia nos oferecer.
Estamos usando o MySQL desde 1996 em um ambiente com mais de 40 bases de
dados com 10.000 tabelas, das quais mais de 500 têm mais de 7 milhões de
linhas. Isto é o equivalente a aproximadamente 50G de dados críticos. A base
da construção do MySQL é uma série de rotinas que foram usadas em um
ambiente de produção com alta demanda por muitos anos. Mesmo o MySQL estando
ainda em desenvolvimento, ele já oferece um conjunto de funções muito ricas
e úteis. Veja a documentação para maiores informações.

%package client
Summary:	MySQL - Client
Summary(pl):	MySQL - Klient
Summary(pt_BR):	MySQL - Cliente
Group:		Applications/Databases
Group(pl):	Aplikacje/Bazy Danych
Group(pt_BR):	Aplicações/Banco_de_Dados
Requires:	%{name}-libs = %{version}
Obsoletes:	MySQL-client

%description client
This package contains the standard MySQL clients. 

%description -l fr client
Ce package contient les clients MySQL standards.

%description -l pl client
Standardowe programy klienckie MySQL.

%description -l pt_BR client
Este pacote contém os clientes padrão para o MySQL.

%package libs
Summary:	Shared libraries for MySQL
Group:		Applications/Databases

%description libs
Shared libraries for MySQL.

%package devel
Summary:	MySQL - Development header files and libraries
Summary(pl):	MySQL - Pliki nag³ówkowe i biblioteki dla developerów
Summary(pt_BR):	MySQL - Medições de desempenho
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-libs = %{version}
Obsoletes:	MySQL-devel

%description devel
This package contains the development header files and libraries
necessary to develop MySQL client applications.

%description -l pl devel
Pliki nag³ówkowe i biblioteki konieczne do rozwijania aplikacji
klienckich MySQL.

%description devel -l pt_BR
Este pacote contém os arquivos de cabeçalho (header files) e bibliotecas 
necessárias para desenvolver aplicações clientes do MySQL. 

%description -l fr devel
Ce package contient les fichiers entetes et les librairies de developpement
necessaires pour developper des applications clientes MySQL.

%package static
Summary:	MySQL staic libraris
Summary(pl):	Biblioteki statyczne MySQL
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}
Obsoletes:	MySQL-static

%description static
MySQL staic libraris.

%description -l pl static
Biblioteki statyczne MySQL.

%package bench
Summary:	MySQL - Benchmarks
Summary(pl):	mySQL - Programy testuj±ce szybko¶æ dzia³ania bazy
Summary(pt_BR):	MySQL - Medições de desempenho
Group:		Applications/Databases
Group(pl):	Aplikacje/Bazy Danych
Group(pt_BR):	Aplicações/Banco_de_Dados
Requires:	%{name} = %{version}
Requires:	%{name}-client
Obsoletes:	MySQL-bench

%description bench
This package contains MySQL benchmark scripts and data.

%description -l pl bench
Programy testuj±ce szybko¶æ serwera MySQL.

%description -l pt_BR bench
Este pacote contém medições de desempenho de scripts e dados do MySQL.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

chmod +x find-perl-requires

%build
automake
aclocal
autoconf
LDFLAGS="-s"
CXXFLAGS="$RPM_OPT_FLAGS -fno-rtti -fno-exceptions"
export LDFLAGS CXXFLAGS
%configure \
	--without-debug \
	--enable-shared \
	--enable-static \
	--with-pthread \
	--with-named-curses-libs="-lncurses" \
	--enable-assembler \
	--with-charset=latin2 \
	--with-mysqld-user=mysql \
	--with-unix-socket-path=/var/state/mysql/mysql.sock \
	--with-comment='Polish Linux Distribution MySQL RPM' \
	--with-readline \
	--with-low-memory
	
# If you have much RAM you can remove --with-low-memory

make benchdir=$RPM_BUILD_ROOT%{_datadir}/sql-bench
(cd Docs; make info manual.texi)

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{logrotate.d,rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT/var/{log,state/mysql}

# Make install
make install DESTDIR=$RPM_BUILD_ROOT benchdir=%{_datadir}/sql-bench

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mysql
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/mysql
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/mysql
touch $RPM_BUILD_ROOT/var/log/mysqld.log

find Docs -type f ! -name *.gif ! -name *.html -exec rm {} \;
find . -name ./CVS -exec rm -rf {} \;

mv $RPM_BUILD_ROOT%{_libdir}/mysql/lib* $RPM_BUILD_ROOT%{_libdir}

strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/lib*.so*.*

gzip -9nf $RPM_BUILD_ROOT{%{_mandir}/man1/*,%{_infodir}/mysql.info*}

%pre
grep -l mysql /etc/group &>/dev/null || (
    echo "Creating system group mysql with GID 89"
    /usr/sbin/groupadd -f -g 89 mysql
)
grep -l mysql /etc/passwd &>/dev/null || (
    echo "Creating system user mysql with UID 89"
    /usr/sbin/useradd -u 89 -g mysql -d /var/state/mysql -s /bin/sh mysql > /dev/null
)

%post
/usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/sbin/chkconfig --add mysql

%preun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/mysql ]; then
	/etc/rc.d/init.d/mysql stop
    fi
    /sbin/chkconfig --del mysql
fi

%postun
/usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/isamchk
%attr(755,root,root) %{_bindir}/isamlog
%attr(755,root,root) %{_bindir}/mysql_fix_privilege_tables
%attr(755,root,root) %{_bindir}/mysql_install_db
%attr(755,root,root) %{_bindir}/mysql_setpermission
%attr(755,root,root) %{_bindir}/mysql_zap
%attr(755,root,root) %{_bindir}/mysqladmin
%attr(755,root,root) %{_bindir}/mysqlbug
%attr(755,root,root) %{_bindir}/perror
%attr(755,root,root) %{_bindir}/replace
%attr(755,root,root) %{_bindir}/resolveip
%attr(755,root,root) %{_bindir}/safe_mysqld
%attr(755,root,root) %{_sbindir}/mysqld
%attr(640,root,root) /etc/logrotate.d/mysql
%attr(754,root,root) /etc/rc.d/init.d/mysql
%attr(640,root,root) %config(noreplace) /etc/sysconfig/mysql
%{_infodir}/mysql.info*
%dir %{_datadir}/mysql

%attr(751,mysql,mysql) %dir /var/state/mysql
%attr(640,mysql,mysql) %config(noreplace) %verify(not md5 size mtime) /var/log/*

%{_datadir}/mysql/english
%lang(cs) %{_datadir}/mysql/czech
%lang(da) %{_datadir}/mysql/danish
%lang(nl) %{_datadir}/mysql/dutch
%lang(et) %{_datadir}/mysql/estonia
%lang(fr) %{_datadir}/mysql/french
%lang(de) %{_datadir}/mysql/german
%lang(el) %{_datadir}/mysql/greek
%lang(hu) %{_datadir}/mysql/hungarian
%lang(it) %{_datadir}/mysql/italian
%lang(ja) %{_datadir}/mysql/japanese
%lang(ko) %{_datadir}/mysql/korean
%lang(no) %{_datadir}/mysql/norwegian
%lang(no@nynorsk) %{_datadir}/mysql/norwegian-ny
%lang(pl) %{_datadir}/mysql/polish
%lang(pt) %{_datadir}/mysql/portuguese
%lang(ru) %{_datadir}/mysql/russian
%lang(sk) %{_datadir}/mysql/slovak
%lang(es) %{_datadir}/mysql/spanish
%lang(sv) %{_datadir}/mysql/swedish

%files client
%attr(755,root,root) %{_bindir}/msql2mysql
%attr(755,root,root) %{_bindir}/mysql
%attr(755,root,root) %{_bindir}/mysql_find_rows
%attr(755,root,root) %{_bindir}/mysqlaccess
%attr(755,root,root) %{_bindir}/mysqlbug
%attr(755,root,root) %{_bindir}/mysqldump
%attr(755,root,root) %{_bindir}/mysqlimport
%attr(755,root,root) %{_bindir}/mysqlshow
%attr(644,root,root) %{_mandir}/man1/mysql.1*

%files libs
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.la
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_bindir}/comp_err
%{_includedir}/mysql

%files static
%attr(644,root,root) %{_libdir}/lib*.a

%files bench
%attr(-,root,root) %{_datadir}/sql-bench
