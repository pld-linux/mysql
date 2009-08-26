#!/bin/sh
# updates percona patches

ver=5.0.84-b18
patches=http://www.percona.com/mysql/$ver/patches
series=$patches/series
branch=MYSQL_5_0

filter() {
	grep -v 'mysqld_safe_syslog.patch'
}

> percona.spec
i=100
for patch in $(wget -q -O - $series | filter); do
	file=mysql-$patch
	wget -nv $patches/$patch -O $file

	if [ -z "$(awk -vfile=$file -F/ '$2 == file{print}' CVS/Entries)" ]; then
		cvs add $file
		${branch:+cvs up -r $branch $file}
	fi

	printf "Source%d:\t%s\n" $i $file >> percona.spec
	i=$((i+1))
done
