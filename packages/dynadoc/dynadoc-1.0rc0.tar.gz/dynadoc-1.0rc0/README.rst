.. vim: set fileencoding=utf-8:
.. -*- coding: utf-8 -*-
.. +--------------------------------------------------------------------------+
   |                                                                          |
   | Licensed under the Apache License, Version 2.0 (the "License");          |
   | you may not use this file except in compliance with the License.         |
   | You may obtain a copy of the License at                                  |
   |                                                                          |
   |     http://www.apache.org/licenses/LICENSE-2.0                           |
   |                                                                          |
   | Unless required by applicable law or agreed to in writing, software      |
   | distributed under the License is distributed on an "AS IS" BASIS,        |
   | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. |
   | See the License for the specific language governing permissions and      |
   | limitations under the License.                                           |
   |                                                                          |
   +--------------------------------------------------------------------------+

*******************************************************************************
                                    dynadoc
*******************************************************************************

.. image:: https://img.shields.io/pypi/v/dynadoc
   :alt: Package Version
   :target: https://pypi.org/project/dynadoc/

.. image:: https://img.shields.io/pypi/status/dynadoc
   :alt: PyPI - Status
   :target: https://pypi.org/project/dynadoc/

.. image:: https://github.com/emcd/python-dynadoc/actions/workflows/tester.yaml/badge.svg?branch=master&event=push
   :alt: Tests Status
   :target: https://github.com/emcd/python-dynadoc/actions/workflows/tester.yaml

.. image:: https://emcd.github.io/python-dynadoc/coverage.svg
   :alt: Code Coverage Percentage
   :target: https://github.com/emcd/python-dynadoc/actions/workflows/tester.yaml

.. image:: https://img.shields.io/github/license/emcd/python-dynadoc
   :alt: Project License
   :target: https://github.com/emcd/python-dynadoc/blob/master/LICENSE.txt

.. image:: https://img.shields.io/pypi/pyversions/dynadoc
   :alt: Python Versions
   :target: https://pypi.org/project/dynadoc/


📝 A Python library package which bridges the gap between **rich annotations**
and **automatic documentation generation** with configurable renderers and
support for reusable fragments.

Key Features ⭐
===============================================================================

* 🔄 **Docstring Generation**: Generation of docstrings for modules, classes,
  functions, and methods via introspection with fine-grained control.
* 🧩 **Fragment System**: Reusable documentation snippets for consistent
  terminology across projects.
* 🏷️ **Annotation Metadata**: Extraction and inclusion of metadata from
  annotations into generated docstrings.
* 🔌 **Extensible Architecture**: Custom renderers, attribute visibility rules,
  and introspection limiters.
* 📖 **Sphinx-Compatible Output**: Render reStructuredText docstrings that work
  with Sphinx Autodoc out of the box.
* 🎨 **Configurable Renderers**: Ability to extend with other renderers as
  desired.

Installation 📦
===============================================================================

Via `uv <https://github.com/astral-sh/uv/blob/main/README.md>`_ ``pip``
command::

    uv pip install dynadoc

Or, via ``pip``::

    pip install dynadoc

Examples 💡
===============================================================================

Please see the `examples directory
<https://github.com/emcd/python-dynadoc/tree/master/documentation/examples>`_.

**Function Documentation**:

.. code-block:: python

    import dynadoc
    from typing import Annotated

    @dynadoc.with_docstring( )
    def process_api_data(
        endpoint: Annotated[ str, dynadoc.Doc( "API endpoint URL to query" ) ],
        timeout: Annotated[ float, dynadoc.Doc( "Request timeout in seconds" ) ] = 30.0,
    ) -> Annotated[ dict, dynadoc.Doc( "Processed API response data" ) ]:
        ''' Process data from API endpoint with configurable timeout. '''
        return { }

Which will be turned into the following docstring on the function by the
default renderer:

.. code-block:: text

    Process data from API endpoint with configurable timeout.

    :argument endpoint: API endpoint URL to query
    :type endpoint: str
    :argument timeout: Request timeout in seconds
    :type timeout: float
    :returns: Processed API response data
    :rtype: dict

**Module Documentation**:

Document all annotated attributes in current module:

.. code-block:: python

    import dynadoc

    dynadoc.assign_module_docstring( __name__ )

`More Flair <https://www.imdb.com/title/tt0151804/characters/nm0431918>`_
===============================================================================

.. image:: https://img.shields.io/github/last-commit/emcd/python-dynadoc
   :alt: GitHub last commit
   :target: https://github.com/emcd/python-dynadoc

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json
   :alt: Copier
   :target: https://github.com/copier-org/copier

.. image:: https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg
   :alt: Hatch
   :target: https://github.com/pypa/hatch

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit
   :alt: pre-commit
   :target: https://github.com/pre-commit/pre-commit

.. image:: https://microsoft.github.io/pyright/img/pyright_badge.svg
   :alt: Pyright
   :target: https://microsoft.github.io/pyright

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :alt: Ruff
   :target: https://github.com/astral-sh/ruff

.. image:: https://img.shields.io/pypi/implementation/dynadoc
   :alt: PyPI - Implementation
   :target: https://pypi.org/project/dynadoc/

.. image:: https://img.shields.io/pypi/wheel/dynadoc
   :alt: PyPI - Wheel
   :target: https://pypi.org/project/dynadoc/


Other Projects by This Author 🌟
===============================================================================


* `python-absence <https://github.com/emcd/python-absence>`_
    - PyPI: `absence <https://pypi.org/project/absence/>`_

    🕳️ A Python library package which provides a **sentinel for absent values** - a falsey, immutable singleton that represents the absence of a value in contexts where ``None`` or ``False`` may be valid values.
* `python-accretive <https://github.com/emcd/python-accretive>`_
    - PyPI: `accretive <https://pypi.org/project/accretive/>`_

    🌌 A Python library package which provides **accretive data structures** - collections which can grow but never shrink.
* `python-falsifier <https://github.com/emcd/python-falsifier>`_
    - PyPI: `falsifier <https://pypi.org/project/falsifier/>`_

    🎭 A very simple Python library package which provides a **base class for falsey objects** - objects that evaluate to ``False`` in boolean contexts.
* `python-frigid <https://github.com/emcd/python-frigid>`_
    - PyPI: `frigid <https://pypi.org/project/frigid/>`_

    🔒 A Python library package which provides **immutable data structures** - collections which cannot be modified after creation.
* `python-icecream-truck <https://github.com/emcd/python-icecream-truck>`_
    - PyPI: `icecream-truck <https://pypi.org/project/icecream-truck/>`_

    🍦 **Flavorful Debugging** - A Python library which enhances the powerful and well-known ``icecream`` package with flavored traces, configuration hierarchies, customized outputs, ready-made recipes, and more.
* `python-mimeogram <https://github.com/emcd/python-mimeogram>`_
    - PyPI: `mimeogram <https://pypi.org/project/mimeogram/>`_

    📨 A command-line tool for **exchanging collections of files with Large Language Models** - bundle multiple files into a single clipboard-ready document while preserving directory structure and metadata... good for code reviews, project sharing, and LLM interactions.
