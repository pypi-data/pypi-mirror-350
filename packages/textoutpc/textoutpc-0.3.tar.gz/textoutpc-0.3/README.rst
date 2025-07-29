``textoutpc`` -- Planète Casio's textout() BBcode markup language translator
============================================================================

This module defines BBcode parsers, including HTML rendering, for
`Planète Casio`_.

For example, as described in `Rendering BBCode as HTML`_, in order to
render BBCode into HTML, you can use the following snippet:

.. code-block:: python

    from __future__ import annotations

    from textoutpc import render_as_html

    text = """\
    [img=center]https://www.planet-casio.com/assets/img/logo.png[/img]

    Hello [color=R10]world[/color]!
    [list]
    [li]This module is made by [url=https://thomas.touhey.fr/]me[/url]!
    [li]Use `render_as_html()` to translate magically to HTML!
    [/]
    """

    print(render_as_html(text), end="")

The project is present at the following locations:

* `Official website and documentation at textoutpc.touhey.pro <Website_>`_;
* `thomas.touhey/textoutpc repository on Gitlab <Gitlab repository_>`_;
* `textoutpc project on PyPI <PyPI project_>`_.

.. _Planète Casio: https://www.planet-casio.com/
.. _Website: https://textoutpc.touhey.pro/
.. _Gitlab repository: https://gitlab.com/thomas.touhey/textoutpc
.. _PyPI project: https://pypi.org/project/textoutpc/
.. _Rendering BBCode as HTML:
    https://textoutpc.touhey.pro/user-guides/render-as-html.html
