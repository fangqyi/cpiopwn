# This file is part of GNU cpio
# Copyright (C) 2016 Free Software Foundation
#
# GNU cpio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU cpio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU cpio.  If not, see <http://www.gnu.org/licenses/>.

# CPIO_DEFAULT_QUOTING_STYLE(style) - set default style for the gnulib
# quotearg module.
m4_define([QUOTING_STYLES],dnl
          [literal|shell|shell-always|c|escape|locale|clocale])
AC_DEFUN([CPIO_DEFAULT_QUOTING_STYLE],[
  DEFAULT_QUOTING_STYLE="$1"
  AC_ARG_VAR([DEFAULT_QUOTING_STYLE],
           [Set the default quoting style. Allowed values are: ] m4_bpatsubst(QU
OTING_STYLES,[|], [[, ]]) [. Default is "escape".])
  case $DEFAULT_QUOTING_STYLE in
QUOTING_STYLES) ;;
*)  AC_MSG_ERROR(Invalid quoting style);;
esac
  DEFAULT_QUOTING_STYLE=`echo ${DEFAULT_QUOTING_STYLE}|sed 's/-/_/g'`_quoting_style
  AC_DEFINE_UNQUOTED(DEFAULT_QUOTING_STYLE, $DEFAULT_QUOTING_STYLE,
     [Define to a default quoting style (see lib/quoteargs.c for the list)])])
