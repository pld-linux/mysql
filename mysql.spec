%define mysql-version		3.22.14b-gamma
%define shared_lib_version		5:2:0
%define Release			2col


Name 		: MySQL
Version 		: %{mysql-version}
Release 		: %{Release}

Distribution    	: OpenLinux 1.3 contrib
Packager        	: Stephan Seyboth <sseyboth@linuxland.de>
Vendor		: LinuxLand International


Source0		: http://www.tcx.se/Downloads/MySQL-3.22/mysql-%{mysql-version}.tar.gz

BuildRoot 	: /tmp/%{Name}-%{Version}-root
 
Provides		: msqlormysql MySQL-server


Copyright 	: MySQL FREE PUBLIC LICENSE (See the file PUBLIC)
Icon 		: mysql.gif
URL 		: http://www.tcx.se/

Group 		: Applications/Databases
Summary 		: MySQL: a very fast and reliable SQL database engine
%Description
MySQL is a true multi-user, multi-threaded SQL (Structured Query Language) database
server. SQL is the most popular database language in the world. MySQL is a client/server
implementation that consists of a server daemon mysqld and many different client
programs/libraries. The main goals of MySQL are speed, robustness and easy to use. 
The base upon which MySQL is built is a set of routines that have been used in a highly
demanding production environment for many years. While MySQL is still in development,
it already offers a rich and highly useful function set. See the documentation for more
information


%Package client
Requires 		: %{Name} = %{Version}-%{Release}

Group		: Applications/Databases
Summary		: MySQL client programs and libs
%Description client
This package contains the client part of the MySQL database. It includes utilities
and libraries to access and manipulate data on a MySQL database Server


%Package devel
Requires 		: %{Name} = %{Version}-%{Release}  %{Name}-client = %{Version}-%{Release}

Group		: Applications/Databases
Summary		: MySQL development header files and libraries
%Description devel
This package contains the header files and libraries (shared and static) for
developing applications that use the MySQL database.


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
 


%Prep

%setup -n mysql-%{mysql-version}


%Build

sh -c  'PATH=/bin:/usr/bin \
	CC=gcc \
	CFLAGS="$RPM_OPT_FLAGS" \
	CXX=gcc \
	CXXFLAGS="$RPM_OPT_FLAGS" \
	./configure \
		--enable-shared \
		--enable-static \
		--enable-assembler \
		--with-mysqld-user=mysql \
		--with-unix-socket-path=/var/lib/mysql/mysql.sock \
		--prefix=/ \
		--exec-prefix=/usr \
		--libexecdir=/usr/sbin \
		--sysconfdir=/etc \
		--datadir=/usr/share \
		--localstatedir=/var/lib/mysql \
		--infodir=/usr/info \
		--includedir=/usr/include \
		--mandir=/usr/man'

# benchdir does not fit in above model. Fix when we make a separate package
make benchdir=$RPM_BUILD_ROOT/usr/share/sql-bench


%Install

%{mkDESTDIR}

# Ensure that needed directories exists
install -d $DESTDIR/var/lib/mysql/mysql
install -d $DESTDIR/usr/share/sql-bench
install -d $DESTDIR/usr/{sbin,share,man,include}
install -d $DESTDIR/usr/doc/MySQL-%{mysql-version}

# Make install
make install-strip DESTDIR=$DESTDIR benchdir=/usr/share/sql-bench

# fixme: can´t this be done via configure?
mv $DESTDIR/usr/lib/mysql/*.so* $DESTDIR/usr/lib

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
 $DESTDIR/usr/info/mysql.info
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


%PreUn
if test -x /etc/rc.d/init.d/mysql
then
  /etc/rc.d/init.d/mysql stop > /dev/null
fi
# Remove autostart of mysql
lisa --SysV-init remove mysql $1

%PostUn
/sbin/ldconfig

# We do not remove the mysql user since it may still own a lot of
# database files.

%Files
%attr(-, root, root) %doc /usr/doc/MySQL-%{mysql-version}/

%attr(755, root, root) /usr/bin/isamchk
%attr(755, root, root) /usr/bin/isamlog
%attr(755, root, root) /usr/bin/mysql_fix_privilege_tables
%attr(755, root, root) /usr/bin/mysql_install_db
%attr(755, root, root) /usr/bin/mysql_setpermission
%attr(755, root, root) /usr/bin/mysql_zap
%attr(755, root, root) /usr/bin/mysqlbug
%attr(755, root, root) /usr/bin/perror
%attr(755, root, root) /usr/bin/replace
%attr(755, root, root) /usr/bin/resolveip
%attr(755, root, root) /usr/bin/safe_mysqld

%attr(644, root, root) /usr/info/mysql.info

%attr(755, root, root) /usr/sbin/mysqld

%attr(644, root, root) /etc/logrotate.d/mysql
%attr(755, root, root) /etc/rc.d/init.d/mysql
%attr(644, root, root) %config /etc/sysconfig/daemons/mysql


%attr(755, root, root) /usr/share/mysql/


%Post client
/sbin/ldconfig

%Files client
%attr(644, root, root) /usr/lib/libmysqlclient.so.5 
%attr(755, root, root) /usr/lib/libmysqlclient.so.5.0.2

%attr(755, root, root) /usr/bin/msql2mysql
%attr(755, root, root) /usr/bin/mysql
%attr(755, root, root) /usr/bin/mysqlaccess
%attr(755, root, root) /usr/bin/mysqladmin
%attr(755, root, root) /usr/bin/mysqlbug
%attr(755, root, root) /usr/bin/mysqldump
%attr(755, root, root) /usr/bin/mysqlimport
%attr(755, root, root) /usr/bin/mysqlshow

%attr(644, root, man) %doc /usr/man/man1/mysql.1


%Files devel
%dir /usr/include/mysql
%dir /usr/lib/mysql
%attr(644, root, root) /usr/include/mysql/*
%attr(644, root, root) /usr/lib/mysql/*
%attr(644, root, root) /usr/lib/libmysqlclient.so
%attr(755, root, root) /usr/bin/comp_err
