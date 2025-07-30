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


''' Docstring assembly and decoration. '''
# TODO? with_docstring_defer
#       Registers with_docstring partial function in registry.
#       Registry can be executed after modules are loaded and all string
#       annotations should be resolvable.


from . import __
from . import factories as _factories
from . import renderers as _renderers
from . import xtnsapi as _xtnsapi


_visitees: __.weakref.WeakSet[ _xtnsapi.Documentable ] = __.weakref.WeakSet( )


context_default: __.typx.Annotated[
    _xtnsapi.Context,
    _xtnsapi.Doc(
        ''' Default context for introspection and rendering. ''' ),
    _xtnsapi.Fname( 'context' ),
    _xtnsapi.Default( mode = _xtnsapi.ValuationModes.Suppress ),
] = _factories.produce_context( )
introspection_default: __.typx.Annotated[
    _xtnsapi.IntrospectionControl,
    _xtnsapi.Doc( ''' Default introspection control. ''' ),
    _xtnsapi.Fname( 'introspection' ),
    _xtnsapi.Default( mode = _xtnsapi.ValuationModes.Suppress ),
] = _xtnsapi.IntrospectionControl( )
renderer_default: __.typx.Annotated[
    _xtnsapi.Renderer,
    _xtnsapi.Doc( ''' Default renderer for docstring fragments. ''' ),
    _xtnsapi.Fname( 'renderer' ),
    _xtnsapi.Default( mode = _xtnsapi.ValuationModes.Suppress ),
] = _renderers.sphinxad.produce_fragment


def assign_module_docstring( # noqa: PLR0913
    module: _xtnsapi.Module, /,
    *fragments: _xtnsapi.FragmentsArgumentMultivalent,
    context: _xtnsapi.ContextArgument = context_default,
    introspection: _xtnsapi.IntrospectionArgument = introspection_default,
    preserve: _xtnsapi.PreserveArgument = True,
    renderer: _xtnsapi.RendererArgument = renderer_default,
    table: _xtnsapi.FragmentsTableArgument = __.dictproxy_empty,
) -> None:
    ''' Assembles docstring from fragments and assigns it to module. '''
    if isinstance( module, str ):
        module = __.sys.modules[ module ]
    _decorate(
        module,
        context = context,
        introspection = introspection,
        preserve = preserve,
        renderer = renderer,
        fragments = fragments,
        table = table )


def with_docstring(
    *fragments: _xtnsapi.FragmentsArgumentMultivalent,
    context: _xtnsapi.ContextArgument = context_default,
    introspection: _xtnsapi.IntrospectionArgument = introspection_default,
    preserve: _xtnsapi.PreserveArgument = True,
    renderer: _xtnsapi.RendererArgument = renderer_default,
    table: _xtnsapi.FragmentsTableArgument = __.dictproxy_empty,
) -> _xtnsapi.Decorator[ _xtnsapi.D ]:
    ''' Assembles docstring from fragments and decorates object with it. '''
    def decorate( objct: _xtnsapi.D ) -> _xtnsapi.D:
        _decorate(
            objct,
            context = context,
            introspection = introspection,
            preserve = preserve,
            renderer = renderer,
            fragments = fragments,
            table = table )
        return objct

    return decorate


def _check_module_recursion(
    objct: object, /,
    introspection: _xtnsapi.IntrospectionControl,
    mname: str
) -> __.typx.TypeIs[ __.types.ModuleType ]:
    ''' Checks if a module should be recursively documented.

        Returns True if the object is a module that should be recursively
        documented based on the introspection control and module name prefix.
    '''
    if (    introspection.targets & _xtnsapi.IntrospectionTargets.Module
        and __.inspect.ismodule( objct )
    ): return objct.__name__.startswith( f"{mname}." )
    return False


def _collect_fragments(
    objct: _xtnsapi.Documentable, /, context: _xtnsapi.Context, fqname: str
) -> _xtnsapi.Fragments:
    ''' Collects docstring fragments from an object.

        Retrieves the sequence of fragments stored on the object using the
        fragments_name from the context. Validates that the fragments are
        of the expected types.
    '''
    fragments: _xtnsapi.Fragments = (
        getattr( objct, context.fragments_name, ( ) ) )
    if (    isinstance( fragments, ( bytes, str ) )
        or not isinstance( fragments, __.cabc.Sequence )
    ):
        emessage = f"Invalid fragments sequence on {fqname}: {fragments!r}"
        context.notifier( 'error', emessage )
        fragments = ( )
    for fragment in fragments:
        if not isinstance( fragment, ( str, _xtnsapi.Doc ) ):
            emessage = f"Invalid fragment on {fqname}: {fragment!r}"
            context.notifier( 'error', emessage )
    return fragments


def _consider_class_attribute( # noqa: C901,PLR0913
    attribute: object, /,
    context: _xtnsapi.Context,
    introspection: _xtnsapi.IntrospectionControl,
    pmname: str, pqname: str, aname: str,
) -> tuple[ __.typx.Optional[ _xtnsapi.Documentable ], bool ]:
    ''' Considers whether a class attribute should be documented.

        Examines a class attribute to determine if it should be included
        in the documentation process based on introspection targets and
        class ownership. Returns the documentable attribute and a flag
        indicating whether the surface attribute needs updating.
    '''
    if _check_module_recursion( attribute, introspection, pmname ):
        return attribute, False
    attribute_ = None
    update_surface = False
    if (    not attribute_
        and introspection.targets & _xtnsapi.IntrospectionTargets.Class
        and __.inspect.isclass( attribute )
    ): attribute_ = attribute
    if (    not attribute_
        and introspection.targets & _xtnsapi.IntrospectionTargets.Descriptor
    ):
        if isinstance( attribute, property ) and attribute.fget:
            # Examine docstring and signature of getter method on property.
            attribute_ = attribute.fget
            update_surface = True
        # TODO: Apply custom processors from context.
        elif __.inspect.isdatadescriptor( attribute ):
            # Ignore descriptors which we do not know how to handle.
            return None, False
    if (    not attribute_
        and introspection.targets & _xtnsapi.IntrospectionTargets.Function
    ):
        if __.inspect.ismethod( attribute ):
            # Methods proxy docstrings from their core functions.
            attribute_ = attribute.__func__
        elif __.inspect.isfunction( attribute ) and aname != '<lambda>':
            attribute_ = attribute
    if attribute_:
        mname = getattr( attribute_, '__module__', None )
        if not mname or mname != pmname:
            attribute_ = None
    if attribute_:
        qname = getattr( attribute_, '__qualname__', None )
        if not qname or not qname.startswith( f"{pqname}." ):
            attribute_ = None
    return attribute_, update_surface


def _consider_module_attribute(
    attribute: object, /,
    context: _xtnsapi.Context,
    introspection: _xtnsapi.IntrospectionControl,
    pmname: str, aname: str,
) -> tuple[ __.typx.Optional[ _xtnsapi.Documentable ], bool ]:
    ''' Considers whether a module attribute should be documented.

        Examines a module attribute to determine if it should be included
        in the documentation process based on introspection targets and
        module ownership. Returns the documentable attribute and a flag
        indicating whether the surface attribute needs updating.
    '''
    if _check_module_recursion( attribute, introspection, pmname ):
        return attribute, False
    attribute_ = None
    update_surface = False
    if (    not attribute_
        and introspection.targets & _xtnsapi.IntrospectionTargets.Class
        and __.inspect.isclass( attribute )
    ): attribute_ = attribute
    if (    not attribute_
        and introspection.targets & _xtnsapi.IntrospectionTargets.Function
        and __.inspect.isfunction( attribute ) and aname != '<lambda>'
    ): attribute_ = attribute
    if attribute_:
        mname = getattr( attribute_, '__module__', None )
        if not mname or mname != pmname:
            attribute_ = None
    return attribute_, update_surface


def _decorate( # noqa: PLR0913
    objct: _xtnsapi.Documentable, /,
    context: _xtnsapi.Context,
    introspection: _xtnsapi.IntrospectionControl,
    preserve: bool,
    renderer: _xtnsapi.Renderer,
    fragments: _xtnsapi.Fragments,
    table: _xtnsapi.FragmentsTable,
) -> None:
    ''' Decorates an object with assembled docstring.

        Handles core docstring decoration and potentially recursive decoration
        of the object's attributes based on introspection control settings.
        Prevents multiple decoration of the same object.
    '''
    if objct in _visitees: return # Prevent multiple decoration.
    _visitees.add( objct )
    if introspection.targets:
        if __.inspect.isclass( objct ):
            _decorate_class_attributes(
                objct,
                context = context,
                introspection = introspection,
                preserve = preserve,
                renderer = renderer,
                table = table )
        elif __.inspect.ismodule( objct ):
            _decorate_module_attributes(
                objct,
                context = context,
                introspection = introspection,
                preserve = preserve,
                renderer = renderer,
                table = table )
    if __.inspect.ismodule( objct ): fqname = objct.__name__
    else: fqname = f"{objct.__module__}.{objct.__qualname__}"
    fragments_ = _collect_fragments( objct, context, fqname )
    if not fragments_: fragments_ = fragments
    _decorate_core(
        objct,
        context = context,
        introspection = introspection,
        preserve = preserve,
        renderer = renderer,
        fragments = fragments_,
        table = table )


def _decorate_core( # noqa: PLR0913
    objct: _xtnsapi.Documentable, /,
    context: _xtnsapi.Context,
    introspection: _xtnsapi.IntrospectionControl,
    preserve: bool,
    renderer: _xtnsapi.Renderer,
    fragments: _xtnsapi.Fragments,
    table: _xtnsapi.FragmentsTable,
) -> None:
    ''' Core implementation of docstring decoration.

        Assembles a docstring from fragments, existing docstring (if
        preserved), and introspection results. Assigns the assembled docstring
        to the object.
    '''
    fragments_: list[ str ] = [ ]
    if preserve and ( fragment := getattr( objct, '__doc__', None ) ):
        fragments_.append( context.fragment_rectifier(
            fragment, source = _xtnsapi.FragmentSources.Docstring ) )
    fragments_.extend(
        _process_fragments_argument( context, fragments, table ) )
    if introspection.enable:
        cache = _xtnsapi.AnnotationsCache( )
        informations = (
            _xtnsapi.introspect(
                objct,
                context = context, introspection = introspection,
                cache = cache, table = table ) )
        fragments_.append( context.fragment_rectifier(
            renderer( objct, informations, context = context ),
            source = _xtnsapi.FragmentSources.Renderer ) )
    docstring = '\n\n'.join(
        fragment for fragment in filter( None, fragments_ ) ).rstrip( )
    objct.__doc__ = docstring if docstring else None


def _decorate_class_attributes( # noqa: PLR0913
    objct: type, /,
    context: _xtnsapi.Context,
    introspection: _xtnsapi.IntrospectionControl,
    preserve: bool,
    renderer: _xtnsapi.Renderer,
    table: _xtnsapi.FragmentsTable,
) -> None:
    ''' Decorates attributes of a class with assembled docstrings.

        Iterates through relevant class attributes, collects fragments,
        and applies appropriate docstring decoration to each attribute.
    '''
    pmname = objct.__module__
    pqname = objct.__qualname__
    for aname, attribute, surface_attribute in (
        _survey_class_attributes( objct, context, introspection )
    ):
        fqname = f"{pmname}.{pqname}.{aname}"
        introspection_ = _limit_introspection(
            attribute, context, introspection, fqname )
        introspection_ = introspection_.evaluate_limits_for( attribute )
        _decorate(
            attribute,
            context = context,
            introspection = introspection_,
            preserve = preserve,
            renderer = renderer,
            fragments = ( ),
            table = table )
        if attribute is not surface_attribute:
            surface_attribute.__doc__ = attribute.__doc__


def _decorate_module_attributes( # noqa: PLR0913
    module: __.types.ModuleType, /,
    context: _xtnsapi.Context,
    introspection: _xtnsapi.IntrospectionControl,
    preserve: bool,
    renderer: _xtnsapi.Renderer,
    table: _xtnsapi.FragmentsTable,
) -> None:
    ''' Decorates attributes of a module with assembled docstrings.

        Iterates through relevant module attributes, collects fragments,
        and applies appropriate docstring decoration to each attribute.
    '''
    pmname = module.__name__
    for aname, attribute, surface_attribute in (
        _survey_module_attributes( module, context, introspection )
    ):
        fqname = f"{pmname}.{aname}"
        introspection_ = _limit_introspection(
            attribute, context, introspection, fqname )
        introspection_ = introspection_.evaluate_limits_for( attribute )
        _decorate(
            attribute,
            context = context,
            introspection = introspection_,
            preserve = preserve,
            renderer = renderer,
            fragments = ( ),
            table = table )
        if attribute is not surface_attribute: # pragma: no cover
            surface_attribute.__doc__ = attribute.__doc__


def _limit_introspection(
    objct: _xtnsapi.Documentable, /,
    context: _xtnsapi.Context,
    introspection: _xtnsapi.IntrospectionControl,
    fqname: str,
) -> _xtnsapi.IntrospectionControl:
    ''' Limits introspection based on object-specific constraints.

        Returns a new IntrospectionControl that respects the limits
        specified by the object being documented. This allows objects
        to control how deeply they are introspected.
    '''
    limit: _xtnsapi.IntrospectionLimit = (
        getattr(
            objct,
            context.introspection_limit_name,
            _xtnsapi.IntrospectionLimit( ) ) )
    if not isinstance( limit, _xtnsapi.IntrospectionLimit ):
        emessage = f"Invalid introspection limit on {fqname}: {limit!r}"
        context.notifier( 'error', emessage )
        return introspection
    return introspection.with_limit( limit )


def _process_fragments_argument(
    context: _xtnsapi.Context,
    fragments: _xtnsapi.Fragments,
    table: _xtnsapi.FragmentsTable,
) -> __.cabc.Sequence[ str ]:
    ''' Processes fragments argument into a sequence of string fragments.

        Converts Doc objects to their documentation strings and resolves
        string references to the fragments table. Returns a sequence of
        rectified fragment strings.
    '''
    fragments_: list[ str ] = [ ]
    for fragment in fragments:
        if isinstance( fragment, _xtnsapi.Doc ):
            fragment_r = fragment.documentation
        elif isinstance( fragment, str ):
            if fragment not in table:
                emessage = f"Fragment '{fragment}' not in provided table."
                context.notifier( 'error', emessage )
                continue
            fragment_r = table[ fragment ]
        else:
            emessage = f"Fragment {fragment!r} is invalid. Must be Doc or str."
            context.notifier( 'error', emessage )
            continue
        fragments_.append( context.fragment_rectifier(
            fragment_r, source = _xtnsapi.FragmentSources.Argument ) )
    return fragments_


def _survey_class_attributes(
    possessor: type, /,
    context: _xtnsapi.Context,
    introspection: _xtnsapi.IntrospectionControl,
) -> __.cabc.Iterator[ tuple[ str, _xtnsapi.Documentable, object ] ]:
    ''' Surveys attributes of a class for documentation.

        Yields a sequence of (name, attribute, surface_attribute) tuples
        representing documentable attributes of the class. The surface
        attribute may differ from attribute in cases like properties where the
        attribute's getter method holds the documentation.
    '''
    pmname = possessor.__module__
    pqname = possessor.__qualname__
    for aname, attribute in __.inspect.getmembers( possessor ):
        attribute_, update_surface = (
            _consider_class_attribute(
                attribute, context, introspection, pmname, pqname, aname ) )
        if attribute_ is None: continue
        if update_surface:
            yield aname, attribute_, attribute
            continue
        yield aname, attribute_, attribute_


def _survey_module_attributes(
    possessor: __.types.ModuleType, /,
    context: _xtnsapi.Context,
    introspection: _xtnsapi.IntrospectionControl,
) -> __.cabc.Iterator[ tuple[ str, _xtnsapi.Documentable, object ] ]:
    ''' Surveys attributes of a module for documentation.

        Yields a sequence of (name, attribute, surface_attribute) tuples
        representing documentable attributes of the module. The surface
        attribute may differ from attribute in cases where the actual
        documented object is not directly accessible.
    '''
    pmname = possessor.__name__
    for aname, attribute in __.inspect.getmembers( possessor ):
        attribute_, update_surface = (
            _consider_module_attribute(
                attribute, context, introspection, pmname, aname ) )
        if attribute_ is None: continue
        if update_surface: # pragma: no cover
            yield aname, attribute_, attribute
            continue
        yield aname, attribute_, attribute_
