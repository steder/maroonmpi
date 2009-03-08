#
#  subunit.sh: shell functions to report test status via the subunit protocol.
#  Copyright (C) 2006  Robert Collins <robertc@robertcollins.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

subunit_start_test () {
  # emit the current protocol start-marker for test $1
  echo "test: $1"
}


subunit_pass_test () {
  # emit the current protocol test passed marker for test $1
  echo "success: $1"
}


subunit_fail_test () {
  # emit the current protocol fail-marker for test $1, and emit stdin as
  # the error text.
  # we use stdin because the failure message can be arbitrarily long, and this
  # makes it convenient to write in scripts (using <<END syntax.
  echo "failure: $1 ["
  cat -
  echo "]"
}


subunit_error_test () {
  # emit the current protocol error-marker for test $1, and emit stdin as
  # the error text.
  # we use stdin because the failure message can be arbitrarily long, and this
  # makes it convenient to write in scripts (using <<END syntax.
  echo "error: $1 ["
  cat -
  echo "]"
}
