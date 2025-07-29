"""
Provide commands that can be added to a `typer` app to manage settings.
"""

from typing import Any

import typer
from pydantic import BaseModel
from pydantic_core import PydanticUndefined
from typer_repyt.build_command import DecDef, OptDef, build_command
from typer_repyt.constants import Sentinel

from typerdrive.constants import Validation
from typerdrive.handle_errors import handle_errors
from typerdrive.model_parser import make_parser
from typerdrive.settings.attach import attach_settings, get_settings_manager
from typerdrive.settings.exceptions import SettingsError
from typerdrive.format import pretty_model
from typerdrive.settings.manager import SettingsManager


def bind(ctx: typer.Context):
    """
    Bind all settings for the app.
    """
    __manager: SettingsManager = get_settings_manager(ctx)
    excluded_locals = ["__manager", "ctx"]
    settings_values = {k: v for (k, v) in locals().items() if k not in excluded_locals}
    __manager.update(**settings_values)


def add_bind(cli: typer.Typer, settings_model: type[BaseModel]):
    """
    Add the `bind` command to the given `typer` app.
    """
    opt_defs: list[OptDef] = []
    for name, field_info in settings_model.model_fields.items():
        default = field_info.default if field_info.default is not PydanticUndefined else Sentinel.NOT_GIVEN
        param_type: type[Any] = SettingsError.enforce_defined(
            field_info.annotation, "Option type may not be `None`"
        )  # TODO: Figure out if this can even be triggered
        opt_kwargs: dict[str, Any] = dict(
            name=name,
            param_type=param_type,
            default=default,
            help=field_info.description,
            show_default=True,
        )
        if issubclass(param_type, BaseModel):
            model_type = param_type
            opt_kwargs["parser"] = make_parser(model_type)
            opt_kwargs["metavar"] = pretty_model(model_type)

        opt_defs.append(
            OptDef(**opt_kwargs)
        )
    build_command(
        cli,
        bind,
        *opt_defs,
        decorators=[
            DecDef(
                dec_func=handle_errors,
                dec_args=["Failed to bind settings"],
                dec_kwargs=dict(
                    handle_exc_class=SettingsError,
                    unwrap_message=False,
                    debug=True,
                ),
                is_simple=False,
            ),
            DecDef(
                dec_func=attach_settings,
                dec_args=[settings_model],
                dec_kwargs=dict(validation=Validation.AFTER, persist=True, show=True),
                is_simple=False,
            ),
        ],
        include_context=True,
    )


def update(ctx: typer.Context):
    """
    Update some settings for the app.
    """
    __manager: SettingsManager = get_settings_manager(ctx)
    excluded_locals = ["__manager", "ctx"]
    settings_values = {k: v for (k, v) in locals().items() if k not in excluded_locals and v is not None}
    __manager.update(**settings_values)


def add_update(cli: typer.Typer, settings_model: type[BaseModel]):
    """
    Add the `update` command to the given `typer` app.
    """
    opt_defs: list[OptDef] = []
    for name, field_info in settings_model.model_fields.items():
        param_type: type[Any] = SettingsError.enforce_defined(field_info.annotation, "Option type may not be `None`")
        default: None | bool = None
        opt_kwargs: dict[str, Any] = dict(
            name=name,
            param_type=param_type | None,
            default=default,
            help=field_info.description,
            show_default=True,
        )
        if param_type is bool:
            default = field_info.default
        elif issubclass(param_type, BaseModel):
            model_type = param_type
            opt_kwargs["parser"] = make_parser(model_type)
            opt_kwargs["metavar"] = pretty_model(model_type)

        opt_defs.append(OptDef(**opt_kwargs))
    build_command(
        cli,
        update,
        *opt_defs,
        decorators=[
            DecDef(
                dec_func=handle_errors,
                dec_args=["Failed to update settings"],
                dec_kwargs=dict(
                    handle_exc_class=SettingsError,
                    unwrap_message=False,
                    debug=True,
                ),
                is_simple=False,
            ),
            DecDef(
                dec_func=attach_settings,
                dec_args=[settings_model],
                dec_kwargs=dict(validation=Validation.NEVER, persist=True, show=True),
                is_simple=False,
            ),
        ],
        include_context=True,
    )


def unset(ctx: typer.Context):
    """
    Remove some settings from the app.
    """
    __manager: SettingsManager = get_settings_manager(ctx)
    excluded_locals = ["__manager", "ctx"]
    settings_values = {k: v for (k, v) in locals().items() if k not in excluded_locals and v}
    __manager.unset(*settings_values.keys())


def add_unset(cli: typer.Typer, settings_model: type[BaseModel]):
    """
    Add the `unset` command to the given `typer` app.
    """
    opt_defs: list[OptDef] = []
    for name, field_info in settings_model.model_fields.items():
        opt_defs.append(
            OptDef(
                name=name,
                param_type=bool,
                default=False,
                help=field_info.description,
                show_default=True,
                override_name=name,
            )
        )
    build_command(
        cli,
        unset,
        *opt_defs,
        decorators=[
            DecDef(
                dec_func=handle_errors,
                dec_args=["Failed to unset settings"],
                dec_kwargs=dict(
                    handle_exc_class=SettingsError,
                    unwrap_message=False,
                    debug=True,
                ),
                is_simple=False,
            ),
            DecDef(
                dec_func=attach_settings,
                dec_args=[settings_model],
                dec_kwargs=dict(validation=Validation.NEVER, persist=True, show=True),
                is_simple=False,
            ),
        ],
        include_context=True,
    )


def show(ctx: typer.Context):  # pyright: ignore[reportUnusedParameter]
    """
    Show the current app's settings.
    """


def add_show(cli: typer.Typer, settings_model: type[BaseModel]):
    """
    Add the `show` command to the given `typer` app.
    """
    build_command(
        cli,
        show,
        decorators=[
            DecDef(
                dec_func=handle_errors,
                dec_args=["Failed to show settings"],
                dec_kwargs=dict(
                    handle_exc_class=SettingsError,
                    unwrap_message=False,
                    debug=True,
                ),
                is_simple=False,
            ),
            DecDef(
                dec_func=attach_settings,
                dec_args=[settings_model],
                dec_kwargs=dict(validation=Validation.NEVER, persist=False, show=True),
                is_simple=False,
            ),
        ],
        include_context=True,
    )


def reset(ctx: typer.Context):
    """
    Remove all settings from the app.
    """
    typer.confirm("Are you sure you want to reset your settings?", abort=True)
    __manager: SettingsManager = get_settings_manager(ctx)
    __manager.reset()


def add_reset(cli: typer.Typer, settings_model: type[BaseModel]):
    """
    Add the `reset` command to the given `typer` app.
    """
    build_command(
        cli,
        reset,
        decorators=[
            DecDef(
                dec_func=handle_errors,
                dec_args=["Failed to reset settings"],
                dec_kwargs=dict(
                    handle_exc_class=SettingsError,
                    unwrap_message=False,
                    debug=True,
                ),
                is_simple=False,
            ),
            DecDef(
                dec_func=attach_settings,
                dec_args=[settings_model],
                dec_kwargs=dict(validation=Validation.NEVER, persist=True, show=True),
                is_simple=False,
            ),
        ],
        include_context=True,
    )


def add_settings_subcommand(cli: typer.Typer, settings_model: type[BaseModel]):
    """
    Add all `settings` commands to the given app.
    """
    settings_cli = typer.Typer(help="Manage settings for the app")

    for cmd in [add_bind, add_update, add_unset, add_reset, add_show]:
        cmd(settings_cli, settings_model)

    cli.add_typer(settings_cli, name="settings")
