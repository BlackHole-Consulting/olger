#!/bin/bash
# TARGETS   linux-glibc, linux-glibc-legacy, solaris, freebsd, openbsd, netbsd,
#   cygwin, haiku, aix51, aix52, aix72-gcc, osx, generic, custom


git clone http://git.haproxy.org/git/haproxy-2.1.git/

cd haproxy-2.1

make TARGET=linux-glibc


sudo make install
