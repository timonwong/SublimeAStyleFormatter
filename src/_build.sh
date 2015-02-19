#!/bin/bash

# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "${SCRIPT}")

# Parsing arguments
is_user_build=1
while [[ -n "$1" ]]; do
	case "$1" in
		--python=*)
       		python_bin="${1#*=}"
			;;
		--dist)
			is_user_build=
			;;
	esac
	shift
done

if [[ -z "${python_bin}" ]]; then
	echo "Usage: $0 --python=/path/to/python"
	exit 1
fi

python_ver=$(${python_bin} -c 'import sys; print(sys.version[0])')

reset() {
	pushd "${SCRIPTPATH}" > /dev/null
	rm -rf pyastyle/build
	popd > /dev/null
}

reset

if [[ "${OSTYPE}" = "linux-gnu" ]]; then
	echo "Linux build!"

	if [[ $(uname -m) == 'x86_64' ]]; then
		pkg_folder="_linux_x86_64"

		CXXFLAGS="-fPIC ${CXXFLAGS}"
		CFLAGS="-fPIC ${CFLAGS}"
	else
		pkg_folder="_linux_x86"

		CXXFLAGS="${CFLAGS}"
		CFLAGS="${CFLAGS}"
	fi

	# In Linux, Sublime Text's Python is compiled with UCS4:
	if [[ "${python_ver}" == "2" ]]; then
		CFLAGS="-DPy_UNICODE_SIZE=4 ${CFLAGS}"
		CXXFLAGS="-DPy_UNICODE_SIZE=4 ${CXXFLAGS}"
	fi
elif [[ "${OSTYPE:0:6}" == "darwin" ]]; then
	echo "Mac OS X build!"

	if [[ "${python_ver}" == "2" ]]; then
		pkg_folder="_macosx_universal"
		arch_flags="-arch i386 -arch x86_64"
		osxver_flags="-stdlib=libstdc++ -mmacosx-version-min=10.6"
	else
		pkg_folder="_macosx_universal"
		arch_flags="-arch x86_64"
		osxver_flags="-stdlib=libstdc++ -mmacosx-version-min=10.7"
	fi

	ARCHFLAGS="${arch_flags} ${ARCHFLAGS}"
	CXXFLAGS="${arch_flags} ${osxver_flags} ${CXXFLAGS}"
	CFLAGS="${arch_flags} ${osxver_flags} ${CFLAGS}"
	LDFLAGS="${arch_flags} ${osxver_flags} ${LDFLAGS}"
else
	echo "Unknown system!"
	exit 1
fi

export CXXFLAGS
export CFLAGS
export CXXFLAGS
export LDFLAGS

# Is user build?
if [[ -n "${is_user_build}" ]]; then
	pkg_folder="_local_arch"
fi

target_folder="../pyastyle/python${python_ver}/${pkg_folder}"

(echo "Building pyastyle..." && \
	cd "${SCRIPTPATH}/pyastyle" && \
	${python_bin} setup.py build && \
	cd "${SCRIPTPATH}"
) && \
mkdir -p "${target_folder}" && \
echo "Copying binary to ${target_folder}..." && \
find "${SCRIPTPATH}/pyastyle/build" -type f '(' -name "pyastyle.so" -o -name "pyastyle.*.so" ')' -exec cp {} "${target_folder}" \; && \

reset && \
echo "Done!" || \
echo "Build Failed!${ERR}"

strip "${target_folder}"/*.so > /dev/null 2>&1
