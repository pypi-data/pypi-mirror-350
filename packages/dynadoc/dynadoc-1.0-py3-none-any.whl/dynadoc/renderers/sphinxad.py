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


''' Sphinx Autodoc reStructuredText renderers. '''


from . import __


class Style( __.enum.Enum ):
    ''' Style of formatter output. '''

    Legible     = __.enum.auto( )
    Pep8        = __.enum.auto( )


def produce_fragment(
    possessor: __.Documentable,
    informations: __.Informations,
    context: __.Context,
    style: Style = Style.Legible,
) -> str:
    ''' Produces a reStructuredText docstring fragment.

        Combines information from object introspection into a formatted
        docstring fragment suitable for Sphinx Autodoc.
    '''
    return '\n'.join(
        _produce_fragment_partial( possessor, information, context, style )
        for information in informations )


_qualident_regex = __.re.compile( r'''^([\w\.]+).*$''' )
def _extract_qualident( name: str, context: __.Context ) -> str:
    ''' Extracts a qualified identifier from a string representation.

        Used to extract the qualified name of an object from its string
        representation when direct name access is not available.
    '''
    extract = _qualident_regex.match( name )
    if extract is not None: return extract[ 1 ]
    return '<unknown>'


def _format_annotation(
    annotation: __.typx.Any, context: __.Context, style: Style
) -> str:
    ''' Formats a type annotation as a string for documentation.

        Handles various annotation types including unions, generics,
        and literals. Formats according to the selected style.
    '''
    if isinstance( annotation, list ):
        seqstr = ', '.join(
            _format_annotation( element, context, style )
            for element in annotation ) # pyright: ignore[reportUnknownVariableType]
        return _stylize_delimiter( style, '[]', seqstr )
    origin = __.typx.get_origin( annotation )
    if origin is None:
        return _qualify_object_name( annotation, context )
    arguments = __.typx.get_args( annotation )
    if origin in ( __.types.UnionType, __.typx.Union ):
        return ' | '.join(
            _format_annotation( argument, context, style )
            for argument in arguments )
    oname = _qualify_object_name( origin, context )
    if not arguments: return oname
    if origin is __.typx.Literal:
        argstr = ', '.join( repr( argument ) for argument in arguments )
    else:
        argstr = ', '.join(
            _format_annotation( argument, context, style )
            for argument in arguments )
    return _stylize_delimiter( style, '[]', argstr, oname )


def _produce_fragment_partial(
    possessor: __.Documentable,
    information: __.InformationBase,
    context: __.Context,
    style: Style,
) -> str:
    ''' Produces a docstring fragment for a single piece of information.

        Dispatches to appropriate producer based on the type of information.
    '''
    if isinstance( information, __.ArgumentInformation ):
        return (
            _produce_argument_text( possessor, information, context, style ) )
    if isinstance( information, __.AttributeInformation ):
        return (
            _produce_attribute_text( possessor, information, context, style ) )
    if isinstance( information, __.ExceptionInformation ):
        return (
            _produce_exception_text( possessor, information, context, style ) )
    if isinstance( information, __.ReturnInformation ):
        return (
            _produce_return_text( possessor, information, context, style ) )
    context.notifier(
        'admonition', f"Unrecognized information: {information!r}" )
    return ''


def _produce_argument_text(
    possessor: __.Documentable,
    information: __.ArgumentInformation,
    context: __.Context,
    style: Style,
) -> str:
    ''' Produces reStructuredText for argument information.

        Formats function arguments in Sphinx-compatible reST format,
        including parameter descriptions and types.
    '''
    annotation = information.annotation
    description = information.description
    name = information.name
    lines: list[ str ] = [ ]
    lines.append(
        f":argument {name}: {description}"
        if description else f":argument {name}:" )
    if annotation is not __.absent:
        typetext = _format_annotation( annotation, context, style )
        lines.append( f":type {information.name}: {typetext}" )
    return '\n'.join( lines )


def _produce_attribute_text(
    possessor: __.Documentable,
    information: __.AttributeInformation,
    context: __.Context,
    style: Style,
) -> str:
    ''' Produces reStructuredText for attribute information.

        Formats class and instance attributes in Sphinx-compatible reST format.
        Delegates to special handler for module attributes.
    '''
    annotation = information.annotation
    match information.association:
        case __.AttributeAssociations.Module:
            return _produce_module_attribute_text(
                possessor, information, context, style )
        case __.AttributeAssociations.Class: vlabel = 'cvar'
        case __.AttributeAssociations.Instance: vlabel = 'ivar'
    description = information.description
    name = information.name
    lines: list[ str ] = [ ]
    lines.append(
        f":{vlabel} {name}: {description}"
        if description else f":{vlabel} {name}:" )
    if annotation is not __.absent:
        typetext = _format_annotation( annotation, context, style )
        lines.append( f":vartype {name}: {typetext}" )
    return '\n'.join( lines )


def _produce_module_attribute_text(
    possessor: __.Documentable,
    information: __.AttributeInformation,
    context: __.Context,
    style: Style,
) -> str:
    ''' Produces reStructuredText for module attribute information.

        Formats module attributes in Sphinx-compatible reST format,
        with special handling for TypeAlias attributes.
    '''
    annotation = information.annotation
    description = information.description or ''
    name = information.name
    match information.default.mode:
        case __.ValuationModes.Accept:
            value = getattr( possessor, name, __.absent )
        case __.ValuationModes.Suppress:
            value = __.absent
        case __.ValuationModes.Surrogate: # pragma: no branch
            value = __.absent
    lines: list[ str ] = [ ]
    if annotation is __.typx.TypeAlias:
        lines.append( f".. py:type:: {name}" )
        if value is not __.absent: # pragma: no branch
            value_ar = __.reduce_annotation(
                value, context,
                __.AdjunctsData( ),
                __.AnnotationsCache( ) )
            value_s = _format_annotation( value_ar, context, style )
            lines.append( f"   :canonical: {value_s}" )
        if description: lines.extend( [ '', f"   {description}" ] )
    else:
        # Note: No way to inject data docstring as of 2025-05-11.
        #       Autodoc will read doc comments and pseudo-docstrings,
        #       but we have no means of supplying description via a field.
        lines.append( f".. py:data:: {name}" )
        if annotation is not __.absent:
            typetext = _format_annotation( annotation, context, style )
            lines.append( f"    :type: {typetext}" )
        if value is not __.absent:
            lines.append( f"    :value: {value!r}" )
    return '\n'.join( lines )


def _produce_exception_text(
    possessor: __.Documentable,
    information: __.ExceptionInformation,
    context: __.Context,
    style: Style,
) -> str:
    ''' Produces reStructuredText for exception information.

        Formats exception classes and descriptions in Sphinx-compatible
        reST format. Handles union types of exceptions appropriately.
    '''
    lines: list[ str ] = [ ]
    annotation = information.annotation
    description = information.description
    origin = __.typx.get_origin( annotation )
    if origin in ( __.types.UnionType, __.typx.Union ):
        annotations = __.typx.get_args( annotation )
    else: annotations = ( annotation, )
    for annotation_ in annotations:
        typetext = _format_annotation( annotation_, context, style )
        lines.append(
            f":raises {typetext}: {description}"
            if description else f":raises {typetext}:" )
    return '\n'.join( lines )


def _produce_return_text(
    possessor: __.Documentable,
    information: __.ReturnInformation,
    context: __.Context,
    style: Style,
) -> str:
    ''' Produces reStructuredText for function return information.

        Formats return type and description in Sphinx-compatible reST format.
        Returns empty string for None returns.
    '''
    if information.annotation in ( None, __.types.NoneType ): return ''
    description = information.description
    typetext = _format_annotation( information.annotation, context, style )
    lines: list[ str ] = [ ]
    if description:
        lines.append( f":returns: {description}" )
    lines.append( f":rtype: {typetext}" )
    return '\n'.join( lines )


def _qualify_object_name( # noqa: PLR0911
    objct: object, context: __.Context
) -> str:
    ''' Qualifies an object name for documentation.

        Determines the appropriate fully-qualified name for an object,
        considering builtin types, module namespaces, and qualname attributes.
    '''
    if objct is Ellipsis: return '...'
    if objct is __.types.NoneType: return 'None'
    if objct is __.types.ModuleType: return 'types.ModuleType'
    name = (
        getattr( objct, '__name__', None )
        or _extract_qualident( str( objct ), context ) )
    if name == '<unknown>': return name
    qname = getattr( objct, '__qualname__', None ) or name
    name0 = qname.split( '.', maxsplit = 1 )[ 0 ]
    if name0 in vars( __.builtins ): # int, etc...
        return qname
    if context.invoker_globals and name0 in context.invoker_globals:
        return qname
    mname = getattr( objct, '__module__', None )
    if mname: return f"{mname}.{qname}"
    return name # pragma: no cover


def _stylize_delimiter(
    style: Style,
    delimiters: str,
    content: str,
    prefix: str = '',
) -> str:
    ''' Stylizes delimiters according to the selected style.

        Formats delimiters around content based on the style setting,
        with options for more legible spacing or compact PEP 8 formatting.
    '''
    ld = delimiters[ 0 ]
    rd = delimiters[ 1 ]
    match style:
        case Style.Legible: return f"{prefix}{ld} {content} {rd}"
        case Style.Pep8: return f"{prefix}{ld}{content}{rd}"
