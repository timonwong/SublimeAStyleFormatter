#!/bin/bash

if [[ -z "${PYTHON}" ]]; then
	PYTHON=python3.3
fi

reset() {
	rm -rf pyastyle/build
}

reset

CURRENT_PATH=$(pwd)

if [[ "${OSTYPE}" = "linux-gnu" ]]; then
	# In Linux, Sublime Text's Python is compiled with UCS4:
	echo "Linux build!"
	if [[ $(uname -m) == 'x86_64' ]]; then
		pkg_folder="_linux_x86_64"

		export CXXFLAGS="-fPIC ${CXXFLAGS}"
		export CFLAGS="-fPIC ${CFLAGS}"
	else
		pkg_folder="_linux_x86"

		export CXXFLAGS="${CFLAGS}"
		export CFLAGS="${CFLAGS}"
	fi
elif [[ "${OSTYPE:0:6}" = "darwin" ]]; then
	echo "Mac OS X build!"
	pkg_folder="_macosx_universal"
	arch_flags="-arch x86_64"
	osxver_flags="-stdlib=libstdc++ -mmacosx-version-min=10.7"

	export ARCHFLAGS="${arch_flags} ${ARCHFLAGS}"
	export CXXFLAGS="${arch_flags} ${osxver_flags} ${CXXFLAGS}"
	export CFLAGS="${arch_flags} ${osxver_flags} ${CFLAGS}"
	export LDFLAGS="${arch_flags} ${osxver_flags} ${LDFLAGS}"
else
	echo "Unknown system!"
	exit 1
fi

target_folder="../pyastyle/python3/${pkg_folder}"

(echo "Building pyastyle..." && \
	cd pyastyle && \
	${PYTHON} setup.py build && \
	cd "${CURRENT_PATH}"
) && \
mkdir -p "${target_folder}" && \
find . -type f -name "pyastyle.so" -exec cp {} "${target_folder}" \; && \

reset && \
echo "Done!" || \
echo "Build Failed!${ERR}"

strip "${target_folder}/*.so" > /dev/null 2>&1
