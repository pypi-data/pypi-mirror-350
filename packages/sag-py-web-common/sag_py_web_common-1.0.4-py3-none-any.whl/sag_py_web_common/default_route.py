from fastapi import APIRouter
from fastapi.responses import RedirectResponse


def build_default_route(default_redirect_path: str = "/swagger", ingress_base_path: str = "") -> APIRouter:
    """Builds an api router for the default route / It can be used to redirect to a specific path.

    Args:
        default_redirect_path (str): The path (starting with /) where you want to redirect to if / is called.
        ingress_base_path (str): The ingress base path starting with / or empty

    Returns:
        APIRouter: A fastapi api router
    """
    default_route = APIRouter()
    default_route.add_route(
        "/",
        methods=["GET"],
        name="default",
        include_in_schema=False,
        endpoint=lambda _: RedirectResponse(url=f"{ingress_base_path}{default_redirect_path}"),
    )
    return default_route
