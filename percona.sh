#!/bin/sh
# updates percona patches
# http://www.percona.com/docs/wiki/repositories:start
# http://bazaar.launchpad.net/~percona-dev/percona-server/5.5.8/files
# https://launchpad.net/percona-server/5.5
# bzr branch lp:percona-server/5.5

version=5.1
bzr_branch=lp:percona-server/$version
#version=5.5.9
#bzr_branch=lp:percona-dev/percona-server/$version
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

set -e

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
[ -d "$version/patches" ] && dir=$version/patches || dir=$version
for patch in $(cat $dir/series | filter_names); do
	# if patch already existed, use mysql- prefix
	if [ -f mysql-$patch ]; then
		file=mysql-$patch
	else
		file=$patch
	fi
	cat $dir/$patch | filter_files > $file

	if [ -z "$(awk -vfile=$file -F/ '$2 == file{print}' CVS/Entries)" ]; then
		cvs add ${branch:+-r $branch} $file
		${branch:+cvs up -r $branch $file}
	fi

	if [ "$patch" != "$file" ]; then
		echo >&2 "Adding: $file ($patch)"
	else
		echo >&2 "Adding: $file"
	fi
	printf "Patch%d:\t%s\n" $i $(echo "$file" | sed -e 's,^mysql-,%{name}-,') >> .percona.spec
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
