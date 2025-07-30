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


''' Factories and registries. '''
# TODO? Registry for deferred decoration.


from . import __
from . import xtnsapi as _xtnsapi


# _package_location = __.Path( __file__ ).parent
def notify( level: _xtnsapi.NotificationLevels, message: str ) -> None:
    # TODO: Python 3.12: Use 'skip_file_prefixes' option.
    ''' Issues warning message. '''
    __.warnings.warn( message, category = RuntimeWarning, stacklevel = 2 )
        # skip_file_prefixes = ( str( _package_location ), ) )


def rectify_fragment(
    fragment: str, source: _xtnsapi.FragmentSources
) -> str:
    ''' Cleans and normalizes fragment according to source. '''
    match source:
        case _xtnsapi.FragmentSources.Annotation: return fragment.strip( )
        case _xtnsapi.FragmentSources.Renderer: return fragment.strip( )
        case _: return __.inspect.cleandoc( fragment ).rstrip( )


def produce_context( # noqa: PLR0913
    invoker_globals: _xtnsapi.InvokerGlobalsArgument = None,
    resolver_globals: _xtnsapi.ResolverGlobalsArgument = None,
    resolver_locals: _xtnsapi.ResolverLocalsArgument = None,
    notifier: _xtnsapi.NotifierArgument = notify,
    fragment_rectifier: _xtnsapi.FragmentRectifierArgument = (
        rectify_fragment ),
    visibility_decider: _xtnsapi.VisibilityDeciderArgument = (
        _xtnsapi.is_attribute_visible ),
    fragments_name: _xtnsapi.FragmentsNameArgument = (
        _xtnsapi.fragments_name_default ),
    introspection_limit_name: _xtnsapi.IntrospectionLimitNameArgument = (
        _xtnsapi.introspection_limit_name_default ),
) -> _xtnsapi.Context:
    ''' Produces context data transfer object.

        Reasonable defaults are used for arguments that are not supplied.
    '''
    return _xtnsapi.Context(
        notifier = notifier,
        fragment_rectifier = fragment_rectifier,
        visibility_decider = visibility_decider,
        invoker_globals = invoker_globals,
        resolver_globals = resolver_globals,
        resolver_locals = resolver_locals )
