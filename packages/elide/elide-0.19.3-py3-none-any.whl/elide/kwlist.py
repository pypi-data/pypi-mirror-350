# This file is part of Elide, frontend to Lisien, a framework for life simulation games.
# Copyright (c) Zachary Spector, public@zacharyspector.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from kivy.properties import ListProperty
from kivy.uix.modalview import ModalView

from .util import load_string_once


class KeywordListModal(ModalView):
	data = ListProperty([])


Builder.load_string("""
<KeywordListModal>:
	size_hint_x: 0.6
	BoxLayout:
		orientation: 'vertical'
		StatListView:
			data: root.data
		BoxLayout:
			Button:
				text: 'Cancel'
			Button:
				text: 'Done'
""")
