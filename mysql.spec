Summary:	MySQL: a very fast and reliable SQL database engine
Name:		MySQL
Version:	3.22.14b-gamma
Release:	3
Vendor:		LinuxLand International
Copyright:	MySQL FREE PUBLIC LICENSE (See the file PUBLIC)
Group:		Applications/Databases
Source0:	http://www.tcx.se/Downloads/MySQL-3.22/mysql-%{mysql-version}.tar.gz
Icon:		mysql.gif
URL:		http://www.tcx.se/
BuildRoot:	/tmp/%{Name}-%{Version}-root

%Description
MySQL is a true multi-user, multi-threaded SQL (Structured Query Language)
database server. SQL is the most popular database language in the world.
MySQL is a client/server implementation that consists of a server daemon
mysqld and many different client programs/libraries. The main goals of MySQL
are speed, robustness and easy to use.  The base upon which MySQL is built
is a set of routines that have been used in a highly demanding production
environment for many years. While MySQL is still in development, it already
offers a rich and highly useful function set. See the documentation for more
information

%Package client
Summary:	MySQL client programs and libs
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release}

%Description client
This package contains the client part of the MySQL database. It includes
utilities and libraries to access and manipulate data on a MySQL database
Server.

%Package devel
Summary:	MySQL development header files and libraries
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release}

%Description devel
This package contains the header files and libraries (shared and static) for
developing applications that use the MySQL database.

%prep
%setup -n

%build

CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" \
./configure %{_target} \
	--enable-shared \
	--enable-static \
	--enable-assembler \
	--with-mysqld-user=mysql \
	--with-unix-socket-path=/var/lib/mysql/mysql.sock \
	--prefix=/usr \
	--sysconfdir=/etc \
	--localstatedir=/var/lib/mysql

# benchdir does not fit in above model. Fix when we make a separate package
make benchdir=$RPM_BUILD_ROOT%{_datadir}/sql-bench

%install

%{mkDESTDIR}

# Ensure that needed directories exists
install -d $DESTDIR/var/lib/mysql/mysql
install -d $DESTDIR%{_datadir}/sql-bench
install -d $DESTDIR/usr/{sbin,share,man,include}
install -d $DESTDIR/usr/doc/MySQL-%{mysql-version}

# Make install
make install-strip DESTDIR=$DESTDIR benchdir=%{_datadir}/sql-bench

# fixme: can´t this be done via configure?
mv $DESTDIR%{_libdir}/mysql/*.so* $DESTDIR/usr/lib

# Install logrotate and autostart
MBD=$RPM_BUILD_DIR/mysql-%{mysql-version}
mkdir -p $DESTDIR/etc/logrotate.d
install -m644 $MBD/support-files/mysql-log-rotate $DESTDIR/etc/logrotate.d/mysql
mkdir -p $DESTDIR/etc/rc.d/init.d
install -m755 $MBD/support-files/mysql.server $DESTDIR/etc/rc.d/init.d/mysql

# daemon startup control
mkdir -p $DESTDIR/etc/sysconfig/daemons
cat <<EOF > $DESTDIR/etc/sysconfig/daemons/mysql
IDENT=mysql
DESCRIPTIVE="MySQL database server"
ONBOOT=no
EOF

# Install docs
install -m644 $RPM_BUILD_DIR/mysql-%{mysql-version}/Docs/mysql.info \
 $DESTDIR%{_infodir}/mysql.info
for file in README PUBLIC Docs/manual_toc.html Docs/manual.html \
    Docs/manual.txt Docs/manual.texi Docs/manual.ps
do
    b=`basename $file`
    install -m644 $MBD/$file $DESTDIR/usr/doc/MySQL-%{mysql-version}/$b
done


%Clean

%{rmDESTDIR}



%Pre
if test -x /etc/rc.d/init.d/mysql
then
  /etc/rc.d/init.d/mysql stop > /dev/null 2>&1
  echo "Giving mysqld a couple of seconds to exit nicely"
  sleep 5
fi

%Post
mysql_datadir=/var/lib/mysql

# Create data directory if needed
if test ! -d $mysql_datadir;		then mkdir $mysql_datadir; fi
if test ! -d $mysql_datadir/mysql;	then mkdir $mysql_datadir/mysql; fi
if test ! -d $mysql_datadir/test;	then mkdir $mysql_datadir/test; fi

# Make MySQL start/shutdown automatically when the machine does it.
lisa --SysV-init install  mysql S35 3:4:5 K65 0:1:2:6

# Create a MySQL user. Do not report any problems if it already
# exists.
echo "Creating system group mysql with GID 83"
#lisa --group create mysql :sys:
/usr/sbin/groupadd -g 83 mysql

echo "Creating system user mysql with UID 83"
#lisa --user create mysql :sys: mysql "MySQL Database" $mysql_datadir /bin/bash
/usr/sbin/useradd -u 83 -g mysql -d $mysql_datadir -s /bin/bash mysql

# Change permissions so that the user that will run the MySQL daemon
# owns all database files.
chown -R mysql.mysql $mysql_datadir

# Initiate databases
mysql_install_db -IN-RPM

# Change permissions again to fix any new files.
chown -R mysql.mysql $mysql_datadir

# Restart in the same way that mysqld will be started normally.
/etc/rc.d/init.d/mysql start

# Allow safe_mysqld to start mysqld and print a message before we exit
sleep 2


%preUn
if test -x /etc/rc.d/init.d/mysql
then
  /etc/rc.d/init.d/mysql stop > /dev/null
fi
# Remove autostart of mysql
lisa --SysV-init remove mysql $1

%postun -p /sbin/ldconfig

%post client -p /sbin/ldconfig

# We do not remove the mysql user since it may still own a lot of
# database files.

%Files
%defattr(644,root,root,755)
%doc /usr/doc/MySQL-%{mysql-version}/

%attr(755,root,root) /usr/bin/isamchk
%attr(755,root,root) /usr/bin/isamlog
%attr(755,root,root) /usr/bin/mysql_fix_privilege_tables
%attr(755,root,root) /usr/bin/mysql_install_db
%attr(755,root,root) /usr/bin/mysql_setpermission
%attr(755,root,root) /usr/bin/mysql_zap
%attr(755,root,root) /usr/bin/mysqlbug
%attr(755,root,root) /usr/bin/perror
%attr(755,root,root) /usr/bin/replace
%attr(755,root,root) /usr/bin/resolveip
%attr(755,root,root) /usr/bin/safe_mysqld

%attr(644,root,root) %{_infodir}/mysql.info

%attr(755,root,root) /usr/sbin/mysqld

%attr(644,root,root) /etc/logrotate.d/mysql
%attr(754,root,root) /etc/rc.d/init.d/mysql
%config /etc/sysconfig/daemons/mysql

%attr(755,root,root) %{_datadir}/mysql/

%Files client
%attr(755,root,root) %{_libdir}/libmysqlclient.so.*.*

%attr(755,root,root) /usr/bin/msql2mysql
%attr(755,root,root) /usr/bin/mysql
%attr(755,root,root) /usr/bin/mysqlaccess
%attr(755,root,root) /usr/bin/mysqladmin
%attr(755,root,root) /usr/bin/mysqlbug
%attr(755,root,root) /usr/bin/mysqldump
%attr(755,root,root) /usr/bin/mysqlimport
%attr(755,root,root) /usr/bin/mysqlshow

%{_mandir}/man1/mysql.1.*


%Files devel
%dir /usr/include/mysql
%dir %{_libdir}/mysql
%attr(644,root,root) /usr/include/mysql/*
%attr(644,root,root) %{_libdir}/mysql/*
%attr(644,root,root) %{_libdir}/libmysqlclient.so
%attr(755,root,root) /usr/bin/comp_err

%ChangeLog
* Thu Jan 25 1999 Stephan Seyboth <sseyboth@linuxland.de>
- user/group creation doesn´t work with lisa-3.2, use useradd/groupadd,
   hope nothing else uses uid/gid 83???

* Thu Jan 07 1999 Stephan Seyboth <sseyboth@linuxland.de>
- converted to COL style init
- updated to 3.22.14b-gamma

* Mon Dec 14 1998 Stephan Seyboth <sseyboth@linuxland.de>
- updated to mysql 3.22.12-beta

* Fri Dec 11 1998 Stephan Seyboth <sseyboth@linuxland.de>
- added mysql_fix_privilege_tables, needed by postin

* Thu Dec 10 1998 Stephan Seyboth <sseyboth@linuxland.de>
- don´t build mysqld with all-static (where´s libdl.a on COL?)

* Wed Dec 09 1998 Stephan Seyboth <sseyboth@linuxland.de>
- initial Version based on rpm by David Axmark <david@detron.se>
