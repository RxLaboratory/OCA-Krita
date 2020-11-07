# DuExportAnim - Duduf Export Animation for Krita
# Copyright (c) 2020 - Nicolas Dufresne, Rainbox Laboratory
# This script is licensed under the GNU General Public License v3
# https://rainboxlab.org
# 
# DuExportAnim was made using "Export Layers" for Krita, which is licensed CC 0 1.0  - public domain
#
# This file is part of DuExportAnim.
#   DuExportAnim is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    DuExportAnim is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with DuExportAnim. If not, see <http://www.gnu.org/licenses/>.

import krita # pylint: disable=import-error
from .oca import OCAExport

Scripter.addExtension(OCAExport(krita.Krita.instance())) # pylint: disable=undefined-variable
