# app_config.py

"""Core configuration module for Terminaide.

This module contains shared configuration classes and utilities used by different parts of the Terminaide library. It serves as a central point of configuration to avoid circular dependencies.
"""

import sys
import os
import shutil
import logging
import hashlib
from pathlib import Path
from dataclasses import dataclass, field
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, WebSocket
from typing import Optional, Dict, Union, Tuple, List, Callable, Any

from .proxy import ProxyManager
from .ttyd_manager import TTYDManager
from .exceptions import TemplateError
from .data_models import TTYDConfig, ThemeConfig, TTYDOptions, create_script_configs

logger = logging.getLogger("terminaide")


def smart_resolve_path(path: Union[str, Path, Callable]) -> Union[Path, Callable]:
    """Resolves a path using a predictable strategy:
    1. If it's a callable function, return it as-is
    2. First try the path as-is (absolute or relative to CWD)
    3. Then try relative to the main script being run (sys.argv[0])

    This approach is both flexible and predictable.
    """
    # If path is a callable function, return it directly
    if callable(path):
        return path

    original_path = Path(path)

    # Strategy 1: Use the path as-is (absolute or relative to CWD)
    if original_path.is_absolute() or original_path.exists():
        return original_path.absolute()

    # Strategy 2: Try relative to the main script being run
    try:
        main_script = Path(sys.argv[0]).absolute()
        main_script_dir = main_script.parent
        script_relative_path = main_script_dir / original_path
        if script_relative_path.exists():
            logger.debug(
                f"Found script at {script_relative_path} (relative to main script)"
            )
            return script_relative_path.absolute()
    except Exception as e:
        logger.debug(f"Error resolving path relative to main script: {e}")

    # Return the original if nothing was found
    return original_path


def copy_preview_image_to_static(preview_image: Path) -> str:
    """
    Copy a preview image to the static directory with a unique name based on its content.
    Returns the filename of the copied image in the static directory.
    """
    logger.debug(f"copy_preview_image_to_static called with: {preview_image}")

    if not preview_image or not preview_image.exists():
        logger.debug(f"Preview image doesn't exist, using default: {preview_image}")
        return "preview.png"  # Use default

    # Get the static directory
    static_dir = Path(__file__).parent.parent / "static"
    static_dir.mkdir(exist_ok=True)

    # Generate a unique filename based on the image content hash
    try:
        # Generate a hash of the file content to create a unique name
        file_hash = hashlib.md5(preview_image.read_bytes()).hexdigest()[:12]
        extension = preview_image.suffix.lower()

        # Only allow common image extensions
        if extension not in (".png", ".jpg", ".jpeg", ".gif", ".svg"):
            logger.warning(
                f"Unsupported image extension: {extension}. Using default preview."
            )
            return "preview.png"

        new_filename = f"preview_{file_hash}{extension}"
        new_path = static_dir / new_filename

        # Copy the file
        shutil.copy2(preview_image, new_path)
        logger.debug(f"Copied preview image from {preview_image} to {new_path}")

        return new_filename
    except Exception as e:
        logger.warning(f"Failed to copy preview image: {e}. Using default preview.")
        return "preview.png"


@dataclass
class TerminaideConfig:
    """Unified configuration for all Terminaide serving modes."""

    # Common configuration options
    port: int = 8000
    title: str = "Terminal"
    theme: Dict[str, Any] = field(
        default_factory=lambda: {"background": "black", "foreground": "white"}
    )
    debug: bool = True
    reload: bool = False
    desktop: bool = False
    desktop_width: int = 1200
    desktop_height: int = 800
    forward_env: Union[bool, List[str], Dict[str, Optional[str]]] = True

    # Advanced configuration
    ttyd_options: Dict[str, Any] = field(default_factory=dict)
    template_override: Optional[Path] = None
    trust_proxy_headers: bool = True
    mount_path: str = "/"

    # Preview image configuration
    preview_image: Optional[Path] = None

    # Proxy settings
    ttyd_port: int = 7681  # Base port for ttyd processes

    # Internal fields (not exposed directly)
    _target: Optional[Union[Callable, Path, Dict[str, Any]]] = None
    _app: Optional[FastAPI] = None
    _mode: str = "function"  # "function", "script", "apps", or "meta"


def build_config(
    config: Optional[TerminaideConfig], overrides: Dict[str, Any]
) -> TerminaideConfig:
    """Build a config object from the provided config and overrides."""
    if config is None:
        config = TerminaideConfig()

    # Apply overrides
    for key, value in overrides.items():
        if hasattr(config, key):
            setattr(config, key, value)

    return config


def setup_templates(config: TerminaideConfig) -> Tuple[Jinja2Templates, str]:
    """Set up the Jinja2 templates for the HTML interface."""
    if config.template_override:
        template_dir = config.template_override.parent
        template_file = config.template_override.name
    else:
        template_dir = Path(__file__).parent.parent / "templates"
        template_file = "terminal.html"

    if not template_dir.exists():
        raise TemplateError(str(template_dir), "Template directory not found")

    templates = Jinja2Templates(directory=str(template_dir))

    if not (template_dir / template_file).exists():
        raise TemplateError(template_file, "Template file not found")

    return templates, template_file


def configure_routes(
    app: FastAPI,
    config: TTYDConfig,
    ttyd_manager: TTYDManager,
    proxy_manager: ProxyManager,
    templates: Jinja2Templates,
    template_file: str,
) -> None:
    """Define routes for TTYD: health, interface, websocket, and proxy."""

    @app.get(f"{config.mount_path}/health")
    async def health_check():
        return {
            "ttyd": ttyd_manager.check_health(),
            "proxy": proxy_manager.get_routes_info(),
        }

    for script_config in config.script_configs:
        route_path = script_config.route_path
        terminal_path = config.get_terminal_path_for_route(route_path)
        title = script_config.title or config.title

        # Debug logging for preview image config
        logger.debug(f"Script config preview_image: {script_config.preview_image}")
        logger.debug(f"Config preview_image: {config.preview_image}")

        # Get preview image path - prefer script_config's image, fall back to config's, then default
        preview_image = "preview.png"  # Default fallback

        # Try script config preview first
        if script_config.preview_image and script_config.preview_image.exists():
            logger.debug(
                f"Using script config preview image: {script_config.preview_image}"
            )
            preview_image = copy_preview_image_to_static(script_config.preview_image)
        elif script_config.preview_image:
            logger.warning(
                f"Script preview image doesn't exist: {script_config.preview_image}"
            )

        # If no script preview or it failed, try global config
        elif config.preview_image:
            logger.debug(f"Using global config preview image: {config.preview_image}")
            if config.preview_image.exists():
                preview_image = copy_preview_image_to_static(config.preview_image)
            else:
                logger.warning(
                    f"Global preview image doesn't exist: {config.preview_image}"
                )
        else:
            logger.debug("No custom preview images configured, using default")

        logger.debug(f"Final preview image for route {route_path}: {preview_image}")

        @app.get(route_path, response_class=HTMLResponse)
        async def terminal_interface(
            request: Request,
            route_path=route_path,
            terminal_path=terminal_path,
            title=title,
            preview_image=preview_image,
        ):
            try:
                logger.debug(f"Rendering template with preview_image={preview_image}")
                return templates.TemplateResponse(
                    template_file,
                    {
                        "request": request,
                        "mount_path": terminal_path,
                        "theme": config.theme.model_dump(),
                        "title": title,
                        "preview_image": preview_image,
                    },
                )
            except Exception as e:
                logger.error(f"Template rendering error for route {route_path}: {e}")
                raise TemplateError(template_file, str(e))

        @app.websocket(f"{terminal_path}/ws")
        async def terminal_ws(websocket: WebSocket, route_path=route_path):
            await proxy_manager.proxy_websocket(websocket, route_path=route_path)

        @app.api_route(
            f"{terminal_path}/{{path:path}}",
            methods=[
                "GET",
                "POST",
                "PUT",
                "DELETE",
                "OPTIONS",
                "HEAD",
                "PATCH",
                "TRACE",
            ],
        )
        async def proxy_terminal_request(
            request: Request, path: str, route_path=route_path
        ):
            return await proxy_manager.proxy_http(request)


def configure_app(app: FastAPI, config: TTYDConfig):
    """Configure the FastAPI app with the TTYDManager, ProxyManager, and routes."""
    mode = "apps-server" if config.is_multi_script else "solo-server"
    entry_mode = getattr(config, "_mode", "script")

    # Update log message to include meta mode
    if entry_mode == "meta":
        logger.info(
            f"Configuring ttyd service with {config.mount_path} mounting (meta-server mode)"
        )
    else:
        logger.info(
            f"Configuring ttyd service with {config.mount_path} mounting ({entry_mode} API, {mode} mode)"
        )

    ttyd_manager = TTYDManager(config)
    proxy_manager = ProxyManager(config)

    package_dir = Path(__file__).parent.parent
    static_dir = package_dir / "static"
    static_dir.mkdir(exist_ok=True)

    terminaide_static_path = "/terminaide-static"  # one-place constant
    app.mount(
        terminaide_static_path,
        StaticFiles(directory=str(static_dir)),
        name="terminaide_static",  # unique route-name
    )

    # config.static_path = terminaide_static_path

    templates, template_file = setup_templates(config)
    app.state.terminaide_templates = templates
    app.state.terminaide_template_file = template_file
    app.state.terminaide_config = config

    configure_routes(app, config, ttyd_manager, proxy_manager, templates, template_file)

    return ttyd_manager, proxy_manager


@asynccontextmanager
async def terminaide_lifespan(app: FastAPI, config: TTYDConfig):
    """Lifespan context manager for the TTYDManager and ProxyManager."""
    ttyd_manager, proxy_manager = configure_app(app, config)

    mode = "apps-server" if config.is_multi_script else "solo-server"
    entry_mode = getattr(config, "_mode", "script")

    # Update startup log message to include meta mode
    if entry_mode == "meta":
        logger.info(f"Starting ttyd service in meta-server mode")
    else:
        logger.info(
            f"Starting ttyd service (mounting: "
            f"{'root' if config.is_root_mounted else 'non-root'}, mode: {mode}, API: {entry_mode})"
        )

    ttyd_manager.start()
    try:
        yield
    finally:
        logger.info("Cleaning up ttyd service...")
        ttyd_manager.stop()
        await proxy_manager.cleanup()


def convert_terminaide_config_to_ttyd_config(
    config: TerminaideConfig, script_path: Path = None
) -> TTYDConfig:
    """Convert a TerminaideConfig to a TTYDConfig."""
    if (
        script_path is None
        and config._target is not None
        and isinstance(config._target, Path)
    ):
        script_path = config._target

    terminal_routes = {}
    if config._mode == "apps" and isinstance(config._target, dict):
        terminal_routes = config._target
    elif script_path is not None:
        terminal_routes = {"/": script_path}
    elif callable(config._target):
        # Handle function target for serve_function mode
        terminal_routes = {"/": config._target}

    script_configs = create_script_configs(terminal_routes)

    # If we have script configs and a custom title is set, apply it to the first script config
    if script_configs and config.title != "Terminal":
        script_configs[0].title = config.title

    # Debug log for preview_image
    if hasattr(config, "preview_image") and config.preview_image:
        logger.debug(
            f"Converting preview_image from TerminaideConfig: {config.preview_image}"
        )

    # Convert theme dict to ThemeConfig
    theme_config = ThemeConfig(**(config.theme or {}))

    # Convert ttyd_options dict to TTYDOptions
    ttyd_options_config = TTYDOptions(**(config.ttyd_options or {}))

    ttyd_config = TTYDConfig(
        client_script=(
            script_configs[0].client_script
            if script_configs and not script_configs[0].is_function_based
            else None
        ),
        mount_path=config.mount_path,
        port=config.ttyd_port,
        theme=theme_config,
        ttyd_options=ttyd_options_config,
        template_override=config.template_override,
        preview_image=config.preview_image,  # Pass the preview_image to TTYDConfig
        title=config.title,  # Keep the original title
        debug=config.debug,
        script_configs=script_configs,
        forward_env=config.forward_env,
    )

    # Propagate the entry mode to TTYDConfig - include meta mode
    ttyd_config._mode = config._mode

    # Debug log for meta mode
    if config._mode == "meta":
        logger.debug(f"Converting meta-server config to TTYDConfig")
        # Copy any special meta-specific attributes
        if hasattr(config, "_app_dir"):
            ttyd_config._app_dir = config._app_dir

    return ttyd_config
