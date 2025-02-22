# Copyright (C) 2018 The NeoVintageous Team (NeoVintageous).
#
# This file is part of NeoVintageous.
#
# NeoVintageous is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeoVintageous is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NeoVintageous.  If not, see <https://www.gnu.org/licenses/>.

from NeoVintageous.tests import unittest


class Test_ctrl_g(unittest.FunctionalTestCase):

    def onRunFeedCommand(self, command, args):
        args.clear()

    @unittest.mock_status_message()
    def test_n(self):
        self.eq('a|bc', 'n_<C-g>', 'a|bc')
        self.assertStatusMessage('"[No Name]" [Modified] -- no lines in the buffer --')

    @unittest.mock_status_message()
    def test_n_with_lines(self):
        self.eq('1\n|2\n3', 'n_<C-g>', '1\n|2\n3')
        self.assertStatusMessage('"[No Name]" [Modified] 3 lines --66%--')
