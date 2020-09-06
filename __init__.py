# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "wiredworks_winches",
    "author" : "Martin Burger",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Node"
}

from . import auto_load

from . preferences import getBlenderVersion
if getBlenderVersion() < (2, 80, 0):
    message = ("\n\n"
        "The wiredworks addon requires at least Blender 2.83.\n"
        "Your are using an older version.\n"
        "Please download the latest official release.")
    raise Exception(message)

auto_load.init()

def register():
    auto_load.register()
    print("Registered wiredworks winches")

def unregister():
    auto_load.unregister()
    print("Unregistered wiredworks winches")