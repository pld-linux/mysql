#!/bin/sh
# updates percona patches
# http://www.percona.com/docs/wiki/release:start
# https://launchpad.net/percona-server/release-5.0.91-22

version=release-5.0.91-22
bzr_branch=lp:percona-server/$version
branch=MYSQL_5_1

filter_names() {
	# mysql_dump_ignore_ct.patch is broken, therefore we skip
	grep -v 'mysql_dump_ignore_ct.patch' | \
	grep -v 'percona-support.patch' | \
	grep -v 'mysqld_safe_syslog.patch' | \
	grep -v 'mysql-test.diff'
}

filter_files() {
	filterdiff -x '*/configure'
}

if [ -d $version ]; then
	cd $version
	bzr pull
	cd ..
else
	bzr branch $bzr_branch $version
fi

> .percona.spec
> .patch.spec
i=100
for patch in $(cat $version/series | filter_names); do
	file=mysql-$patch
	cat $version/$patch | filter_files > $file

	if [ -z "$(awk -vfile=$file -F/ '$2 == file{print}' CVS/Entries)" ]; then
		cvs add $file
		${branch:+cvs up -r $branch $file}
	fi

	echo >&2 "Adding: $patch"
	printf "Patch%d:\t%s\n" $i %{name}-$patch >> .percona.spec
	printf "%%patch%d -p1\n" $i >> .patch.spec
	i=$((i+1))
done

# update PatchX section
sed -i -e '
/^# <percona patches/,/^# <\/percona>/ {
	/^ <\/percona>/b
	/^# <percona patches/ {
		p # print header
		r .percona.spec
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
		r .patch.spec
		a# </percona>
	}
	d
}
' mysql.spec
