from typing import cast

from starlette.routing import Route

from sag_py_web_common.default_route import build_default_route


def test_build_default_route() -> None:
    # Act
    actual = build_default_route()

    # Assert
    assert len(actual.routes) == 1
    actual_route = cast(Route, actual.routes[0])
    assert actual_route.name == "default"
    assert actual_route.path == "/"
