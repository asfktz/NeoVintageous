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

# A port of https://github.com/tpope/vim-abolish.

import re

from sublime_plugin import TextCommand

from NeoVintageous.nv.plugin import register
from NeoVintageous.nv.vi.cmd_base import RequiresOneCharMixinDef
from NeoVintageous.nv.vi.cmd_base import ViOperatorDef
from NeoVintageous.nv.vim import NORMAL


__all__ = [
    '_nv_abolish_command'
]


def _coerce_to_mixedcase(string):
    return _coerce_to_spacecase(string).title().replace(' ', '')


def _coerce_to_camelcase(string):
    string = _coerce_to_spacecase(string).title().replace(' ', '')
    if len(string) > 1:
        return string[0].lower() + string[1:]
    return string.lower()


def _coerce_to_snakecase(string):
    # https://stackoverflow.com/a/1176023
    # https://github.com/jpvanhal/inflection
    string = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', string)
    string = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', string)
    string = string.replace("-", "_")
    return string.lower()


def _coerce_to_uppercase(string):
    return _coerce_to_snakecase(string).upper()


def _coerce_to_dashcase(string):
    return _coerce_to_snakecase(string).replace('_', '-')


def _coerce_to_spacecase(string):
    return _coerce_to_snakecase(string).replace('_', ' ')


def _coerce_to_dotcase(string):
    return _coerce_to_snakecase(string).replace('_', '.')


def _coerce_to_titlecase(string):
    return _coerce_to_spacecase(string).title()


_COERCIONS = {
    'mixedcase': _coerce_to_mixedcase,
    'camelcase': _coerce_to_camelcase,
    'snakecase': _coerce_to_snakecase,
    'uppercase': _coerce_to_uppercase,
    'dashcase': _coerce_to_dashcase,
    'spacecase': _coerce_to_spacecase,
    'dotcase': _coerce_to_dotcase,
    'titlecase': _coerce_to_titlecase
}


_ALIASES = {
    'm': 'mixedcase',
    'c': 'camelcase',
    '_': 'snakecase',
    's': 'snakecase',
    'u': 'uppercase',
    'U': 'uppercase',
    '-': 'dashcase',
    'k': 'dashcase',
    ' ': 'spacecase',
    '<space>': 'spacecase',
    '.': 'dotcase',
    't': 'titlecase'
}


@register(seq='cr', modes=(NORMAL,))
class _AbolishCoercions(RequiresOneCharMixinDef, ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'action': '_nv_abolish',
            'action_args': {
                'to': self.inp
            }
        }


class _nv_abolish_command(TextCommand):
    def run(self, edit, to=None, mode=None):

        if to in _ALIASES:
            to = _ALIASES[to]

        if to in _COERCIONS:
            coerce_func = _COERCIONS[to]
        else:
            raise ValueError('unknown coercion')

        new_sels = []
        for sel in self.view.sel():
            if sel.empty():
                sel = self.view.word(sel)

            new_sels.append(sel.begin())

            self.view.replace(edit, sel, coerce_func(self.view.substr(sel)))

        if new_sels:
            self.view.sel().clear()
            self.view.sel().add_all(new_sels)
