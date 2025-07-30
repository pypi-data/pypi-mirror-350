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


''' Interface for extension development. '''

# ruff: noqa: F403,F405


from . import __

from .context import *
from .interfaces import *
from .introspection import *
from .nomina import *


FragmentRectifierArgument: __.typx.TypeAlias = __.typx.Annotated[
    FragmentRectifier, Fname( 'fragment rectifier' ) ]
FragmentsArgumentMultivalent: __.typx.TypeAlias = __.typx.Annotated[
    Fragment,
    Doc(
        ''' Fragments from which to produce a docstring.

            If fragment is a string, then it will be used as an index
            into a table of docstring fragments.
            If fragment is a :pep:`727` ``Doc`` object, then the value of its
            ``documentation`` attribute will be incorporated.
        ''' ),
]
FragmentsNameArgument: __.typx.TypeAlias = __.typx.Annotated[
    str, Fname( 'fragments name' ) ]
InformationsArgument: __.typx.TypeAlias = __.typx.Annotated[
    Informations,
    Doc( ''' Information extracted from object introspection. ''' ),
]
IntrospectionLimitNameArgument: __.typx.TypeAlias = __.typx.Annotated[
    str, Fname( 'introspection limit name' ) ]
InvokerGlobalsArgument: __.typx.TypeAlias = __.typx.Annotated[
    __.typx.Optional[ Variables ], Fname( 'invoker globals' ) ]
NotifierArgument: __.typx.TypeAlias = __.typx.Annotated[
    Notifier, Fname( 'notifier' ) ]
PreserveArgument: __.typx.TypeAlias = __.typx.Annotated[
    bool, Doc( ''' Preserve extant docstring? ''' ) ]
ResolverGlobalsArgument: __.typx.TypeAlias = __.typx.Annotated[
    __.typx.Optional[ Variables ], Fname( 'resolver globals' ) ]
ResolverLocalsArgument: __.typx.TypeAlias = __.typx.Annotated[
    __.typx.Optional[ Variables ], Fname( 'resolver locals' ) ]
VisibilityDeciderArgument: __.typx.TypeAlias = __.typx.Annotated[
    VisibilityDecider, Fname( 'visibility decider' ) ]


RendererReturnValue: __.typx.TypeAlias = __.typx.Annotated[
    str, Doc( ''' Rendered docstring fragment. ''' ) ]

class Renderer( __.typx.Protocol ):
    ''' Produces docstring fragment from object and information about it. '''

    @staticmethod
    def __call__(
        possessor: PossessorArgument,
        informations: InformationsArgument,
        context: ContextArgument,
    ) -> RendererReturnValue:
        ''' (Signature for fragment renderer.) '''
        raise NotImplementedError # pragma: no cover

RendererArgument: __.typx.TypeAlias = __.typx.Annotated[
    Renderer, Fname( 'renderer' ) ]
