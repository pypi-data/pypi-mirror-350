"""matplatex: export matplotlib figures as pdf and text separately for
use in LaTeX.

Copyright (C) 2024 2025 Johannes Sørby Heines

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

fontsize_map = {
    # Values indicate largest point size for each LaTeX size.
    # These probably need tweaking
    r'\tiny': 4,
    r'\scriptsize': 6,
    r'\footnotesize': 7,
    r'\small': 9,
    r'\normalsize': 11,
    r'\large': 13,
    r'\Large': 15,
    r'\LARGE': 18,
    r'\huge': 25
    }
