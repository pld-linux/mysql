Name:		MySQL
Summary:	MySQL: a very fast and reliable SQL database engine
Summary(pl):	MySQL: bardzo szybki i niezawodna baza danych (SQL)
Group:		Applications/Databases
Group(pl):	Aplikacje/Bazy danych
Summary(pt_BR): MySQL: Um servidor SQL r�pido e confi�vel.
Group(pt_BR):	Aplica��es/Banco_de_Dados
Version:	3.22.22
Release:	1
Copyright:	MySQL FREE PUBLIC LICENSE (See the file PUBLIC)
Source:		http://www.mysql.com/Downloads/MySQL-3.22/mysql-%{version}.tar.gz
Patch:		mysql-optimization.patch
Icon:		mysql.gif
URL:		http://www.mysql.com/
Provides:	msqlormysql MySQL-server
Obsoletes:	mysql
BuildRoot:	/tmp/%{name}-%{version}

%description
MySQL is a true multi-user, multi-threaded SQL (Structured Query
Language) database server. SQL is the most popular database language
in the world. MySQL is a client/server implementation that consists of
a server daemon mysqld and many different client programs/libraries.

The main goals of MySQL are speed, robustness and easy to use.  MySQL
was originally developed because we at Tcx needed a SQL server that
could handle very big databases with magnitude higher speed than what
any database vendor could offer to us. We have now been using MySQL
since 1996 in a environment with more than 40 databases, 10,000
tables, of which more than 500 have more than 7 million rows. This is
about 50G of mission critical data.

The base upon which MySQL is built is a set of routines that have been
used in a highly demanding production environment for many
years. While MySQL is still in development, it already offers a rich
and highly useful function set.

%description -l pl
MySQL to wielow�tkowy serwer baz danych SQL.

G��wne zalety MySQL to szybko��, pot�ga i �atwo�� u�ytkowania. MySQL
jes wykorzystywany m.in. do obs�ugi 40 baz danych, 10 000 tabeli,
gdzie ka�da tabela zawiera 7 milion�w pozycji. To ok 50GB danych.

%description -l pt_BR
O MySQL � um servidor de banco de dados SQL realmente multiusu�rio e\
multi-tarefa. A linguagem SQL � a mais popular linguagem para banco de\
dados no mundo. O MySQL � uma implementa��o cliente/servidor que\
consiste de um servidor chamado mysqld e diversos\
programas/bibliotecas clientes. Os principais objetivos do MySQL s�o:\
velocidade, robustez e facilidade de uso.  O MySQL foi originalmente\
desenvolvido porque n�s na Tcx precis�vamos de um servidor SQL que\
pudesse lidar com grandes bases de dados e com uma velocidade muito\
maior do que a que qualquer vendedor podia nos oferecer. Estamos\
usando\
o MySQL desde 1996 em um ambiente com mais de 40 bases de dados com 10.000\
tabelas, das quais mais de 500 t�m mais de 7 milh�es de linhas. Isto � o\
equivalente a aproximadamente 50G de dados cr�ticos. A base da constru��o do\
MySQL � uma s�rie de rotinas que foram usadas em um ambiente de produ��o com\
alta demanda por muitos anos. Mesmo o MySQL estando ainda em desenvolvimento,\
ele j� oferece um conjunto de fun��es muito ricas e �teis. Veja a documenta��o\
para maiores informa��es.

%package client
Requires:	%{name} = %{version}-%{release}
Summary:	MySQL - Client
Summary(pl):	MySQL - Klient
Group:		Applications/Databases
Group(pl):	Aplikacje/Bazy danych
Summary(pt_BR):	MySQL - Cliente
Group(pt_BR):	Aplica��es/Banco_de_Dados
Obsoletes:	mysql-client

%description client
This package contains the standard MySQL clients. 

%description client -l pl
Standardowe programy klienckie MySQL.

%description client -l pt_BR
Este pacote cont�m os clientes padr�o para o MySQL.

%package bench
Requires:	MySQL-client
Requires:	MySQL-DBI-perl-bin
Requires:	perl
Summary:	MySQL - Benchmarks
Summary:	mySQL - Programy testuj�ce szybko�� dzia�ania bazy
Group:		Applications/Databases
Group(pl):	Aplikacje/Bazy danych
Summary(pt_BR):	MySQL - Medi��es de desempenho
Group(pt_BR):	Aplica��es/Banco_de_Dados
Obsoletes:	mysql-bench

%description bench
This package contains MySQL benchmark scripts and data.

%description -l pl
Programy testuj�ce szybko�� serwera MySQL.

%description bench -l pt_BR
Este pacote cont�m medi��es de desempenho de scripts e dados do MySQL.

%package devel
Requires:	%{name} = %{version}-%{release}
Requires:	MySQL-client
Summary:	MySQL - Development header files and libraries
Summary(pl):	MySQL - Pliki nag��wkowe i biblioteki dla developer�w
Group:		Applications/Databases
Group(pl):	Aplikacje/Bazy danych
Summary(pt_BR):	MySQL - Medi��es de desempenho
Group(pt_BR):	Aplica��es/Banco_de_Dados
Obsoletes:	mysql-devel

%description devel
This package contains the development header files and libraries
necessary to develop MySQL client applications.

%description -l pl
Pliki nag��wkowe i biblioteki konieczne do rozwijania aplikacji
klienckich MySQL.

%description devel -l pt_BR
Este pacote cont�m os arquivos de cabe�alho (header files) e bibliotecas 
necess�rias para desenvolver aplica��es clientes do MySQL. 

%prep
%setup -q -n mysql-%{version}
%patch -p1

%build
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure \
	    --without-debug \
            --enable-shared \
	    --enable-static \
	    --with-pthread \
	    --enable-thread-safe-client \
	    --enable-assembler \
	    --with-charset=latin2 \
            --with-mysqld-user=mysql \
            --with-unix-socket-path=/var/state/mysql/mysql.sock \
            --prefix=/ \
            --exec-prefix=%{_exec_prefix} \
            --libexecdir=%{_sbindir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --localstatedir=/var/state/mysql \
            --infodir=%{_infodir} \
            --includedir=%{_includedir} \
            --mandir=%{_mandir} \
	    --with-comment='Polish Linux Distribution MySQL RPM' \
	    --without-readline \
	    --with-low-memory
# If you have much RAM you can remove --with-low-memory

make benchdir=$RPM_BUILD_ROOT%{_datadir}/sql-bench


%install
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{logrotate.d,rc.d/init.d}
install -d $RPM_BUILD_ROOT/var/state/mysql/{mysql,test}
install -d $RPM_BUILD_ROOT%{_datadir}/sql-bench
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT%{_mandir}
install -d $RPM_BUILD_ROOT%{_includedir}

# Make install
make install-strip DESTDIR=$RPM_BUILD_ROOT benchdir=%{_datadir}/sql-bench

# Install logrotate and autostart
install -m644 support-files/mysql-log-rotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/mysql
install -m755 support-files/mysql.server     $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/mysql

find Docs -type f ! -name *.gif ! -name *.html -exec rm {} \;
find . -name ./CVS -exec rm -rf {} \;

mv $RPM_BUILD_ROOT%{_libdir}/mysql/*.so* $RPM_BUILD_ROOT%{_libdir}

strip $RPM_BUILD_ROOT%{_bindir}/*  || true
strip $RPM_BUILD_ROOT%{_sbindir}/* || true
strip $RPM_BUILD_ROOT%{_libdir}/*.so* || true

%pre
echo "Creating system group mysql with GID 83"
%{_sbindir}/groupadd -f -g 83 mysql
echo "Creating system user mysql with UID 83"
%{_sbindir}/useradd -u 83 -g mysql -d /var/state/mysql -s /bin/sh mysql 2> /dev/null

%post
/sbin/chkconfig --add mysql
mysql_install_db -IN-RPM
chown -R mysql /var/state/mysql

%postun
# We do not remove the mysql user since it may still own a lot of
# database files.

%files
%defattr(644,root,root,755)
%doc Docs
%attr(755,root,root) %{_bindir}/isamchk
%attr(755,root,root) %{_bindir}/isamlog
%attr(755,root,root) %{_bindir}/mysql_fix_privilege_tables
%attr(755,root,root) %{_bindir}/mysql_install_db
%attr(755,root,root) %{_bindir}/mysql_setpermission
%attr(755,root,root) %{_bindir}/mysql_zap
%attr(755,root,root) %{_bindir}/mysqlbug
%attr(755,root,root) %{_bindir}/perror
%attr(755,root,root) %{_bindir}/replace
%attr(755,root,root) %{_bindir}/resolveip
%attr(755,root,root) %{_bindir}/safe_mysqld
%attr(644,root,root) %{_infodir}/mysql.info
%attr(755,root,root) %{_sbindir}/mysqld
%attr(644,root,root) %{_sysconfdir}/logrotate.d/mysql
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/mysql
%attr(755,root,root) %{_libdir}/mysql/

%files client
%attr(755,root,root) %{_bindir}/msql2mysql
%attr(755,root,root) %{_bindir}/mysql
%attr(755,root,root) %{_bindir}/mysqlaccess
%attr(755,root,root) %{_bindir}/mysqladmin
%attr(755,root,root) %{_bindir}/mysqlbug
%attr(755,root,root) %{_bindir}/mysqldump
%attr(755,root,root) %{_bindir}/mysqlimport
%attr(755,root,root) %{_bindir}/mysqlshow
%attr(755,root,root) %{_libdir}/*.so*
%attr(644,root,root) %{_mandir}/man1/mysql.1

%post client
/sbin/ldconfig

%postun client
/sbin/ldconfig

%files devel
%attr(755,root,root) %{_bindir}/comp_err
%attr(755,root,root) %{_includedir}/mysql/
%attr(755,root,root) %{_libdir}/mysql/

%files bench
%attr(-,root,root) %{_datadir}/sql-bench

%changelog
* Mon May 31 1999 Arkadiusz Mi�kiewicz <misiek@pld.org.pl>
- PLDized (spec rewrited)

* Mon Feb 22 1999 David Axmark <david@detron.se>
- Removed unportable cc switches from the spec file. The defaults can
  now be overridden with environment variables. This feature is used
  to compile the official RPM with optimal (but compiler version
  specific) switches.
- Removed the repetitive description parts for the sub rpms. Maybe add
  again if RPM gets a multiline macro capability.
- Added support for a pt_BR translation. Translation contributed by
  Jorge Godoy <jorge@bestway.com.br>.

* Wed Nov 4 1998 David Axmark <david@detron.se>
- A lot of changes in all the rpm and install scripts. This may even
  be a working RPM :-)

* Sun Aug 16 1998 David Axmark <david@detron.se>
- A developers changelog for MySQL is available in the source RPM. And
  there is a history of major user visible changed in the Reference
  Manual.  Only RPM specific changes will be documented here.
