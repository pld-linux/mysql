#!/bin/sh
# updates percona patches
# http://www.percona.com/docs/wiki/release:start

ver=5.0.84-b18
patches=http://www.percona.com/mysql/$ver/patches
series=$patches/series
branch=MYSQL_5_0

filter_names() {
	grep -v 'mysqld_safe_syslog.patch'
}

filter_files() {
	filterdiff -x '*/configure'
}

> percona.spec
> patch.spec
i=100
for patch in $(wget -q -O - $series | filter_names); do
	file=mysql-$patch
	wget -nv $patches/$patch -O - | filter_files > $file

	if [ -z "$(awk -vfile=$file -F/ '$2 == file{print}' CVS/Entries)" ]; then
		cvs add $file
		${branch:+cvs up -r $branch $file}
	fi

	printf "Patch%d:\t%s\n" $i %{name}-$patch >> percona.spec
	printf "%%patch%d -p1\n" $i >> patch.spec
	i=$((i+1))
done

# update PatchX section
sed -i -e '
/^# <percona patches/,/^# <\/percona>/ {
	/^ <\/percona>/b
	/^# <percona patches/ {
		p # print header
		r percona.spec
		a# </percona>
	}
	d
}
' mysql.spec

# update %patchX section
sed -i -e '
/^# <percona %patches/,/^# <\/percona>/ {
	/^ <\/percona>/b
	/^# <percona %patches/ {
		p # print header
		r patch.spec
		a# </percona>
	}
	d
}
' mysql.spec
