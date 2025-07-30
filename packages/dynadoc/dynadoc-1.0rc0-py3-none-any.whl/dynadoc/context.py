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


''' Data transfer objects for execution context. '''


from . import __
from . import interfaces as _interfaces
from . import nomina as _nomina


fragments_name_default = '_dynadoc_fragments_'
introspection_limit_name_default = '_dynadoc_introspection_limit_'


@__.dcls.dataclass( frozen = True, kw_only = True, slots = True )
class Context:

    _dynadoc_fragments_: __.typx.ClassVar[
        _interfaces.Fragments ] = ( 'context', )

    notifier: __.typx.Annotated[
        _interfaces.Notifier,
        _interfaces.Fname( 'notifier' ),
    ]
    fragment_rectifier: __.typx.Annotated[
        _interfaces.FragmentRectifier,
        _interfaces.Fname( 'fragment rectifier' ),
    ]
    visibility_decider: __.typx.Annotated[
        _interfaces.VisibilityDecider,
        _interfaces.Fname( 'visibility decider' ),
    ]
    fragments_name: __.typx.Annotated[
        str,
        _interfaces.Fname( 'fragments name' ),
    ] = fragments_name_default
    introspection_limit_name: __.typx.Annotated[
        str,
        _interfaces.Fname( 'introspection limit name' ),
    ] = introspection_limit_name_default
    invoker_globals: __.typx.Annotated[
        __.typx.Optional[ _nomina.Variables ],
        _interfaces.Fname( 'invoker globals' ),
    ] = None
    resolver_globals: __.typx.Annotated[
        __.typx.Optional[ _nomina.Variables ],
        _interfaces.Fname( 'resolver globals' ),
    ] = None
    resolver_locals: __.typx.Annotated[
        __.typx.Optional[ _nomina.Variables ],
        _interfaces.Fname( 'resolver locals' ),
    ] = None

    def with_invoker_globals(
        self,
        level: _interfaces.GlobalsLevelArgument = 2
    ) -> __.typx.Self:
        ''' Returns new context with invoker globals from stack frame. '''
        iglobals = __.inspect.stack( )[ level ].frame.f_globals
        return type( self )(
            notifier = self.notifier,
            fragment_rectifier = self.fragment_rectifier,
            visibility_decider = self.visibility_decider,
            fragments_name = self.fragments_name,
            introspection_limit_name = self.introspection_limit_name,
            invoker_globals = iglobals,
            resolver_globals = self.resolver_globals,
            resolver_locals = self.resolver_locals )


ContextArgument: __.typx.TypeAlias = __.typx.Annotated[
    Context, _interfaces.Fname( 'context' ) ]
IntrospectionArgumentFref: __.typx.TypeAlias = __.typx.Annotated[
    'IntrospectionControl', _interfaces.Fname( 'introspection' ) ]


class ClassIntrospector( __.typx.Protocol ):
    ''' Custom introspector for class annotations and attributes. '''

    @staticmethod
    def __call__( # noqa: PLR0913
        possessor: _interfaces.PossessorClassArgument, /,
        context: ContextArgument,
        introspection: IntrospectionArgumentFref,
        annotations: _interfaces.AnnotationsArgument,
        cache: _interfaces.AnnotationsCacheArgument,
        table: _interfaces.FragmentsTableArgument,
    ) -> __.typx.Optional[ _interfaces.Informations ]:
        ''' Introspects class and returns information about its members. '''
        raise NotImplementedError # pragma: no cover

ClassIntrospectors: __.typx.TypeAlias = __.cabc.Sequence[ ClassIntrospector ]


@__.dcls.dataclass( frozen = True, kw_only = True, slots = True )
class ClassIntrospectionLimit:
    ''' Limits on class introspection behavior. '''

    avoid_inheritance: __.typx.Annotated[
        bool,
        _interfaces.Doc( ''' Avoid introspecting inherited members? ''' ),
    ] = False
    ignore_attributes: __.typx.Annotated[
        bool,
        _interfaces.Doc(
            ''' Ignore attributes not covered by annotations? ''' ),
    ] = False


@__.dcls.dataclass( frozen = True, kw_only = True, slots = True )
class ClassIntrospectionControl:
    ''' Controls on class introspection behavior. '''

    inheritance: __.typx.Annotated[
        bool, _interfaces.Doc( ''' Inherit annotations? ''' )
    ] = False
    introspectors: __.typx.Annotated[
        ClassIntrospectors,
        _interfaces.Doc( ''' Custom introspectors to apply. ''' ),
    ] = ( )
    scan_attributes: __.typx.Annotated[
        bool,
        _interfaces.Doc( ''' Scan attributes not covered by annotations? ''' ),
    ] = False

    def with_limit(
        self,
        limit: __.typx.Annotated[
            ClassIntrospectionLimit,
            _interfaces.Doc(
                ''' Limits to apply to this introspection control. ''' ),
        ]
    ) -> __.typx.Self:
        ''' Returns new control with applied limits. '''
        inheritance = self.inheritance and not limit.avoid_inheritance
        scan_attributes = self.scan_attributes and not limit.ignore_attributes
        return type( self )(
            inheritance = inheritance,
            introspectors = self.introspectors,
            scan_attributes = scan_attributes )


@__.dcls.dataclass( frozen = True, kw_only = True, slots = True )
class ModuleIntrospectionLimit:
    ''' Limits on module introspection behavior. '''

    ignore_attributes: __.typx.Annotated[
        bool,
        _interfaces.Doc(
            ''' Ignore attributes not covered by annotations? ''' ),
    ] = False


@__.dcls.dataclass( frozen = True, kw_only = True, slots = True )
class ModuleIntrospectionControl:
    ''' Controls on module introspection behavior. '''

    scan_attributes: __.typx.Annotated[
        bool,
        _interfaces.Doc( ''' Scan attributes not covered by annotations? ''' ),
    ] = False

    def with_limit(
        self,
        limit: __.typx.Annotated[
            ModuleIntrospectionLimit,
            _interfaces.Doc(
                ''' Limits to apply to this introspection control. ''' ),
        ]
    ) -> __.typx.Self:
        ''' Returns new control with applied limits. '''
        scan_attributes = self.scan_attributes and not limit.ignore_attributes
        return type( self )( scan_attributes = scan_attributes )


class IntrospectionLimiter( __.typx.Protocol ):
    ''' Can return modified introspection control for attribute. '''

    @staticmethod
    def __call__(
        objct: __.typx.Annotated[
            object,
            _interfaces.Doc(
                ''' Object being evaluated for introspection limits. ''' ),
        ],
        introspection: IntrospectionArgumentFref,
    ) -> 'IntrospectionControl':
        ''' Returns modified introspection control with limits applied. '''
        raise NotImplementedError # pragma: no cover

IntrospectionLimiters: __.typx.TypeAlias = __.typx.Annotated[
    __.cabc.Sequence[ IntrospectionLimiter ],
    _interfaces.Doc(
        ''' Functions which can apply limits to introspection control. ''' ),
]


class IntrospectionTargets( __.enum.IntFlag ):
    ''' Kinds of objects to recursively document. '''

    Null        = 0
    Class       = __.enum.auto( )
    Descriptor  = __.enum.auto( )
    Function    = __.enum.auto( )
    Module      = __.enum.auto( )


IntrospectionTargetsSansModule: __.typx.Annotated[
    IntrospectionTargets,
    _interfaces.Doc( ''' All introspection targets except modules. ''' ),
] = (   IntrospectionTargets.Class
    |   IntrospectionTargets.Descriptor
    |   IntrospectionTargets.Function )
IntrospectionTargetsOmni: __.typx.Annotated[
    IntrospectionTargets,
    _interfaces.Doc(
        ''' All available introspection targets including modules. ''' ),
] = IntrospectionTargetsSansModule | IntrospectionTargets.Module


@__.dcls.dataclass( frozen = True, kw_only = True, slots = True )
class IntrospectionLimit:
    ''' Limits on introspection behavior. '''

    class_limit: __.typx.Annotated[
        ClassIntrospectionLimit,
        _interfaces.Doc( ''' Limits specific to class introspection. ''' ),
    ] = ClassIntrospectionLimit( )
    module_limit: __.typx.Annotated[
        ModuleIntrospectionLimit,
        _interfaces.Doc( ''' Limits specific to module introspection. ''' ),
    ] = ModuleIntrospectionLimit( )
    targets_exclusions: __.typx.Annotated[
        IntrospectionTargets,
        _interfaces.Doc( ''' Target types to exclude from introspection. ''' ),
    ] = IntrospectionTargets.Null


@__.dcls.dataclass( frozen = True, kw_only = True, slots = True )
class IntrospectionControl:

    _dynadoc_fragments_ = ( 'introspection', )

    enable: __.typx.Annotated[
        bool,
        _interfaces.Doc( ''' Whether introspection is enabled at all. ''' ),
    ] = True
    class_control: __.typx.Annotated[
        ClassIntrospectionControl,
        _interfaces.Doc( ''' Controls specific to class introspection. ''' ),
    ] = ClassIntrospectionControl( )
    module_control: __.typx.Annotated[
        ModuleIntrospectionControl,
        _interfaces.Doc( ''' Controls specific to module introspection. ''' ),
    ] = ModuleIntrospectionControl( )
    limiters: __.typx.Annotated[
        IntrospectionLimiters,
        _interfaces.Doc(
            ''' Functions that can apply limits to introspection. ''' ),
    ] = ( )
    targets: __.typx.Annotated[
        IntrospectionTargets,
        _interfaces.Doc(
            ''' Which types of objects to recursively document. ''' ),
    ] = IntrospectionTargets.Null
    # TODO? Maximum depth.
    #       (Suggested by multiple LLMs; not convinced that it is needed.)

    def evaluate_limits_for(
        self,
        objct: __.typx.Annotated[
            object,
            _interfaces.Doc( ''' Object to evaluate limits for. ''' ),
        ]
    ) -> 'IntrospectionControl':
        ''' Determine which introspection limits apply to object. '''
        introspection_ = self
        for limiter in self.limiters:
            introspection_ = limiter( objct, introspection_ )
        return introspection_

    def with_limit(
        self,
        limit: __.typx.Annotated[
            IntrospectionLimit,
            _interfaces.Doc(
                ''' Limits to apply to this introspection control. ''' ),
        ]
    ) -> __.typx.Self:
        ''' Returns new control with applied limits. '''
        class_control = self.class_control.with_limit( limit.class_limit )
        module_control = self.module_control.with_limit( limit.module_limit )
        targets = self.targets & ~limit.targets_exclusions
        return type( self )(
            enable = self.enable,
            class_control = class_control,
            module_control = module_control,
            limiters = self.limiters,
            targets = targets )


IntrospectionArgument: __.typx.TypeAlias = __.typx.Annotated[
    IntrospectionControl, _interfaces.Fname( 'introspection' ) ]


# def avoid_enum_inheritance(
#     objct: object, recursion: RecursionControl
# ) -> RecursionControl:
#     ''' Enums inherit copious amounts of documentation. Avoids this. '''
#     if isinstance( objct, __.enum.EnumMeta ):
#         return recursion.with_limit(
#             RecursionLimit( avoid_inheritance = True ) )
#     return recursion
