# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

#============================================================================#
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License");           #
#  you may not use this file except in compliance with the License.          #
#  You may obtain a copy of the License at                                   #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  Unless required by applicable law or agreed to in writing, software       #
#  distributed under the License is distributed on an "AS IS" BASIS,         #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#  See the License for the specific language governing permissions and       #
#  limitations under the License.                                            #
#                                                                            #
#============================================================================#


''' Docstring generation from annotations with configurable output formats. '''


from . import __
from . import assembly
from . import context
from . import factories
from . import interfaces
from . import introspection
from . import nomina
from . import renderers
from . import xtnsapi
# --- BEGIN: Injected by Copier ---
# --- END: Injected by Copier ---

from .userapi import *


__version__: __.typx.Annotated[ str, Visibilities.Reveal ]
__version__ = '1.0rc0'


def _notify( level: NotificationLevels, message: str ) -> None:
    ''' Issues warning message. (Internal use within this package itself.) '''
    __.warnings.warn( # pyright: ignore[reportCallIssue]
        message, category = RuntimeWarning, stacklevel = 2 )


_context = produce_context( notifier = _notify )
_introspection_cc = ClassIntrospectionControl(
    inheritance = True,
    introspectors = ( introspection.introspect_special_classes, ) )
_introspection = IntrospectionControl(
    class_control = _introspection_cc, targets = IntrospectionTargetsOmni )
assign_module_docstring(
    __.package_name,
    context = _context,
    introspection = _introspection,
    table = __.fragments )
# TODO: Reclassify package modules as immutable and concealed.
