#!/bin/bash

PYTHON=python

reset() {
	rm -rf pyastyle/build
}

reset

CURRENT_PATH=`pwd`

if [ $OSTYPE = "linux-gnu" ]; then
	# In Linux, Sublime Text's Python is compiled with UCS4:
	echo "Linux build!"
	if [ `uname -m` == 'x86_64' ]; then
		export CXXFLAGS="-fPIC -DPy_UNICODE_SIZE=4 $CFLAGS"
		export CFLAGS="-fPIC -DPy_UNICODE_SIZE=4 $CFLAGS"
	else
		export CXXFLAGS="-DPy_UNICODE_SIZE=4 -I $CFLAGS"
		export CFLAGS="-DPy_UNICODE_SIZE=4 -I $CFLAGS"
	fi
elif [ ${OSTYPE:0:6} = "darwin" ]; then
	echo "Mac OS X build!"
	export ARCHFLAGS="-arch i386 -arch x86_64 $ARCHFLAGS"
	export CXXFLAGS="-arch i386 -arch x86_64 -I /tmp/pcre-8.21 $CFLAGS"
	export CFLAGS="-arch i386 -arch x86_64 -I /tmp/pcre-8.21 $CFLAGS"
	export LDFLAGS="-arch i386 -arch x86_64 $LDFLAGS"
fi

(echo "Building pyastyle..." && \
	cd pyastyle && \
	$PYTHON setup.py build && \
	cd "$CURRENT_PATH"
) && \

find . -type f -name "pyastyle.so" -exec cp {} ../_local_arch \; && \

reset && \
echo "Done!" || \
echo "Build Failed!$ERR"

strip ../_local_arch/*.so > /dev/null 2>&1
