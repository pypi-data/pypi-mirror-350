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


''' Docstring fragments. '''


from . import imports as __


_FragmentsTable: __.typx.TypeAlias = __.cabc.Mapping[ str, str ]
fragments: _FragmentsTable = __.types.MappingProxyType( {

    'context':
    ''' Data transfer object for various behaviors.

        Controls how annotations are resolved and how fragments are
        processed and rendered.
    ''',

    'fragment rectifier':
    ''' Cleans and normalizes documentation fragment. ''',

    'fragments name':
    ''' Name of class attribute which stores documentation fragments. ''',

    'introspection':
    ''' Controls on introspection behavior.

        Is introspection enabled?
        Which kinds of objects to recursively document?
        Etc...
    ''',

    'introspection limit name':
    ''' Name of class attribute which stores introspection limit. ''',

    'invoker globals':
    ''' Dictionary of globals from the frame of a caller.

        Used by renderers for determing whether to fully-qualify a name.
    ''',

    'notifier': ''' Notifies of warnings and errors. ''',

    'renderer':
    ''' Produces docstring fragment from object and information about it. ''',

    'resolver globals':
    ''' Dictionary of globals for annotation resolution.

        Used for resolving string annotations.
    ''',

    'resolver locals':
    ''' Dictionary of locals for annotation resolution.

        Used for resolving string annotations.
    ''',

    'visibility decider':
    ''' Decides if attribute should have visible documentation. ''',

} )
