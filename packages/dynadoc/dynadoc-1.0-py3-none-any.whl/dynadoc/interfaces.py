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


''' Rich annotations, public interfaces for cutomization functions, etc....

    .. note::

       By default, this module exports ``typing_extensions.Doc``, which is
       based on the withdrawn :pep:`727`. A ``typing_extensions`` maintainer,
       who was also the sponsor of this PEP, has indicated `in the PEP 727
       Discourse thread
       <https://discuss.python.org/t/pep-727-documentation-metadata-in-typing/32566/183>`_
       that ``typing_extensions`` will support ``Doc`` indefinitely. However,
       if it should disappear from ``typing_extensions``, we provide a
       compatible fallback. Unless you are using ``typing_extensions.Doc`` for
       other purposes, it is recommended that you import it from this package
       instead, to ensure future availability.
'''


from . import __
from . import nomina as _nomina


try: from typing_extensions import Doc # pyright: ignore[reportAssignmentType]
except ImportError: # pragma: no cover

    @__.dcls.dataclass( frozen = True, slots = True )
    class Doc:
        ''' Description of argument or attribute.

            Compatible with :pep:`727` ``Doc`` objects.
        '''

        documentation: str


Fragment: __.typx.TypeAlias = str | Doc
Fragments: __.typx.TypeAlias = __.cabc.Sequence[ Fragment ]


@__.dcls.dataclass( frozen = True, slots = True )
class Fname:
    ''' Name of documentation fragment in table. '''

    name: __.typx.Annotated[
        str, Doc( ''' Index to look up content in fragments table. ''' ) ]


@__.dcls.dataclass( frozen = True, slots = True )
class Raises:
    ''' Class and description of exception which can be raised.

        Should appear in the return annotations for a function.
    '''

    classes: __.typx.Annotated[
        type[ BaseException ] | __.cabc.Sequence[ type[ BaseException ] ],
        Doc( ''' Exception class or classes which can be raised. ''' ),
    ]
    description: __.typx.Annotated[
        __.typx.Optional[ str ],
        Doc( ''' When and why the exception is raised. ''' ),
    ] = None


AnnotationsArgument: __.typx.TypeAlias = __.typx.Annotated[
    _nomina.Annotations,
    Doc( ''' Annotations mapping for documentable object. ''' ),
]
FragmentsTableArgument: __.typx.TypeAlias = __.typx.Annotated[
    _nomina.FragmentsTable,
    Doc( ''' Table from which to copy docstring fragments. ''' ),
]
GlobalsLevelArgument: __.typx.TypeAlias = __.typx.Annotated[
    int,
    Doc(
        ''' Stack frame level from which to obtain globals.

            Default is 2, which is the caller of the caller.
        ''' ),
]
NotifierLevelArgument: __.typx.TypeAlias = __.typx.Annotated[
    _nomina.NotificationLevels,
    Doc( ''' Severity level of the notification. ''' ),
]
NotifierMessageArgument: __.typx.TypeAlias = __.typx.Annotated[
    str,
    Doc( ''' Message content to notify about. ''' ),
]
PossessorArgument: __.typx.TypeAlias = __.typx.Annotated[
    _nomina.Documentable,
    Doc(
        ''' Object being documented.

            May be a module, class, or function.
        ''' ),
]
PossessorClassArgument: __.typx.TypeAlias = __.typx.Annotated[
    type, Doc( ''' Class being documented. ''' ) ]
PossessorFunctionArgument: __.typx.TypeAlias = __.typx.Annotated[
    __.cabc.Callable[ ..., __.typx.Any ],
    Doc( ''' Function being documented. ''' ),
]
PossessorModuleArgument: __.typx.TypeAlias = __.typx.Annotated[
    __.types.ModuleType, Doc( ''' Module being documented. ''' ) ]
VisibilityAnnotationArgument: __.typx.TypeAlias = __.typx.Annotated[
    __.typx.Any, Doc( ''' Type annotation of the attribute. ''' ) ]
VisibilityDescriptionArgument: __.typx.TypeAlias = __.typx.Annotated[
    __.typx.Optional[ str ],
    Doc( ''' Optional description text for the attribute. ''' ),
]
VisibilityNameArgument: __.typx.TypeAlias = __.typx.Annotated[
    str, Doc( ''' Name of the attribute being evaluated. ''' ) ]


class Sentinels( __.enum.Enum ):
    ''' Sentinel values used in various parts of the package. '''

    Absent      = __.enum.auto( )
    Incomplete  = __.enum.auto( )


absent: __.typx.Annotated[
    Sentinels, Doc( ''' Indicates annotation or other data is missing. ''' )
] = Sentinels.Absent
incomplete: __.typx.Annotated[
    Sentinels, Doc( ''' Indicates annotation reduction is incomplete. ''' ),
] = Sentinels.Incomplete


@__.dcls.dataclass( frozen = True, kw_only = True, slots = True )
class AdjunctsData:
    ''' Data about type-adjacent entities. '''

    extras: __.typx.Annotated[
        __.cabc.MutableSequence[ __.typx.Any ],
        Doc( ''' Additional annotations. ''' ),
    ] = __.dcls.field( default_factory = list[ __.typx.Any ] )
    traits: __.typx.Annotated[
        __.cabc.MutableSet[ str ],
        Doc( ''' Trait names collected during annotation processing. ''' ),
    ] = __.dcls.field( default_factory = set[ str ] )

    def copy( self ) -> __.typx.Self:
        ''' Creates a shallow copy of the adjuncts data. '''
        return type( self )(
            extras = list( self.extras ),
            traits = set( self.traits ) )


@__.dcls.dataclass( frozen = True, kw_only = True, slots = True )
class AnnotationsCache:
    ''' Lookup table for reduced annotations from original annotations.

        Has special values for absent and incomplete entries.
    '''

    entries: __.typx.Annotated[
        dict[ __.typx.Any, __.typx.Any ],
        Doc( ''' Mapping from original annotations to reduced forms. ''' ),
    ] = __.dcls.field( default_factory = dict[ __.typx.Any, __.typx.Any ] )

    def access(
        self, original: __.typx.Annotated[
            __.typx.Any,
            Doc( ''' Original annotation to look up in cache. ''' ),
        ]
    ) -> __.typx.Annotated[
        __.typx.Any,
        Doc(
            ''' Reduced annotation from cache.

                Absence sentinel if not found.
            ''' ),
    ]:
        ''' Accesses entry value, if it exists. '''
        try: return self.entries.get( original, absent )
        except TypeError: return self.entries.get( id( original ), absent )

    def enter(
        self,
        original: __.typx.Annotated[
            __.typx.Any,
            Doc( ''' Original annotation to use as cache key. ''' ),
        ],
        reduction: __.typx.Annotated[
            __.typx.Any,
            Doc( ''' Reduced form of annotation to store as value. ''' ),
        ] = incomplete,
    ) -> __.typx.Any:
        ''' Adds reduced annotation to cache, returning it.

            Cache key is original annotation.
            If reduction is not specified, then an incompletion sentinel is
            added as the value for the entry.
        '''
        try: self.entries[ original ] = reduction
        except TypeError: self.entries[ id( original ) ] = reduction
        return reduction


class AttributeAssociations( __.enum.Enum ):
    ''' Association level of an attribute with its containing entity. '''

    Module      = __.enum.auto( )
    Class       = __.enum.auto( )
    Instance    = __.enum.auto( )


class ValuationModes( __.enum.Enum ):
    ''' Annotation for how default value is determined.

        Accept means to use assigned value.
        Suppress means to use no value.
        Surrogate means to use surrogate value.
    '''

    Accept      = __.enum.auto( )
    Suppress    = __.enum.auto( )
    Surrogate   = __.enum.auto( )


@__.dcls.dataclass( frozen = True, kw_only = True, slots = True )
class Default:
    ''' How to process default value. '''

    mode: __.typx.Annotated[
        ValuationModes,
        Doc( ''' Method for handling default value processing. ''' ),
    ] = ValuationModes.Accept
    surrogate: __.typx.Annotated[
        __.typx.Any,
        Doc(
            ''' Alternative value to use when surrogate mode.

                Usually a description string.
            ''' ),
    ] = absent


class FragmentSources( __.enum.Enum ):
    ''' Possible sources for documentation fragments. '''

    Annotation  = __.enum.auto( )
    Argument    = __.enum.auto( ) # *fragments
    Attribute   = __.enum.auto( ) # _dynadoc_fragments_
    Docstring   = __.enum.auto( )
    Renderer    = __.enum.auto( )


class FragmentRectifier( __.typx.Protocol ):
    ''' Cleans and normalizes documentation fragment. '''

    @staticmethod
    def __call__(
        fragment: __.typx.Annotated[
            str,
            Doc( ''' Raw fragment text to be cleaned and normalized. ''' ),
        ],
        source: __.typx.Annotated[
            FragmentSources,
            Doc(
                ''' Source type of fragment for context-aware processing.
                ''' ),
        ],
    ) -> str:
        ''' (Signature for fragment rectifier.) '''
        raise NotImplementedError # pragma: no cover


@__.dcls.dataclass( frozen = True, kw_only = True, slots = True )
class InformationBase:
    ''' Base for information on various kinds of entities. '''

    annotation: __.typx.Annotated[
        __.typx.Any,
        Doc( ''' Type annotation associated with this entity. ''' ),
    ]
    description: __.typx.Annotated[
        __.typx.Optional[ str ],
        Doc( ''' Human-readable description of the entity. ''' ),
    ]


@__.dcls.dataclass( frozen = True, kw_only = True, slots = True )
class ArgumentInformation( InformationBase ):
    ''' Information about a function argument. '''

    name: __.typx.Annotated[
        str,
        Doc( ''' Name of the function parameter. ''' ),
    ]
    paramspec: __.typx.Annotated[
        __.inspect.Parameter,
        Doc( ''' Inspection parameter object with various details. ''' ),
    ]
    default: __.typx.Annotated[
        Default,
        Doc( ''' Configuration for how to handle default value. ''' ),
    ]


@__.dcls.dataclass( frozen = True, kw_only = True, slots = True )
class AttributeInformation( InformationBase ):
    ''' Information about a class or module attribute. '''

    name: __.typx.Annotated[
        str,
        Doc( ''' Name of the attribute. ''' ),
    ]
    association: __.typx.Annotated[
        AttributeAssociations,
        Doc( ''' Attribute associated with module, class, or instance? ''' ),
    ]
    default: __.typx.Annotated[
        Default, Doc( ''' How to handle default value. ''' ) ]


@__.dcls.dataclass( frozen = True, kw_only = True, slots = True )
class ExceptionInformation( InformationBase ):
    ''' Information about an exception that can be raised. '''
    pass


@__.dcls.dataclass( frozen = True, kw_only = True, slots = True )
class ReturnInformation( InformationBase ):
    ''' Information about a function's return value. '''
    pass


Informations: __.typx.TypeAlias = __.cabc.Sequence[ InformationBase ]


class Notifier( __.typx.Protocol ):
    ''' Notifies of warnings and errors. '''

    @staticmethod
    def __call__(
        level: NotifierLevelArgument,
        message: NotifierMessageArgument,
    ) -> None:
        ''' (Signature for notifier callback.) '''
        raise NotImplementedError # pragma: no cover


class Visibilities( __.enum.Enum ):
    ''' Annotation to determine visibility of attribute.

        Default means to defer to visibility predicate in use.
        Conceal means to hide regardless of visibility predicate.
        Reveal means to show regardless of visibility predicate.
    '''

    Default     = __.enum.auto( )
    Conceal     = __.enum.auto( )
    Reveal      = __.enum.auto( )


class VisibilityDecider( __.typx.Protocol ):
    ''' Decides if attribute should have visible documentation. '''

    @staticmethod
    def __call__(
        possessor: PossessorArgument,
        name: VisibilityNameArgument,
        annotation: VisibilityAnnotationArgument,
        description: VisibilityDescriptionArgument,
    ) -> bool:
        ''' (Signature for visibility decider.) '''
        raise NotImplementedError # pragma: no cover


AnnotationsCacheArgument: __.typx.TypeAlias = __.typx.Annotated[
    AnnotationsCache,
    Doc(
        ''' Cache for storing reduced annotation forms.

            Also used for cycle detection.
        ''' ),
]
