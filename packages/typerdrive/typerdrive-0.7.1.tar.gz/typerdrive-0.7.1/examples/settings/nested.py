from typing import Annotated

import typer
from pydantic import AfterValidator, BaseModel
from snick import unwrap
from typerdrive import add_settings_subcommand, attach_settings, set_typerdrive_config
from typerdrive.logging.commands import add_logs_subcommand


def valid_alignment(value: str) -> str:
    if value not in ["good", "neutral", "evil"]:
        raise ValueError(f"{value} is an invalid alignment")
    return value


class Coloration(BaseModel):
    eyes: str
    hair: str


class Planet(BaseModel):
    name: str
    climate: str


class SettingsModel(BaseModel):
    name: str
    planet: Planet
    coloration: Coloration
    is_humanoid: bool = True
    alignment: Annotated[str, AfterValidator(valid_alignment)] = "neutral"


cli = typer.Typer()
add_settings_subcommand(cli, SettingsModel)
add_logs_subcommand(cli)
set_typerdrive_config(app_name="settings-nested-example")


@cli.command()
@attach_settings(SettingsModel)
def report(ctx: typer.Context, cfg: SettingsModel):
    print(
        unwrap(
            f"""
            Look at this {cfg.alignment} {cfg.name}
            from the {cfg.planet.climate} planet {cfg.planet.name}
            with {cfg.coloration.eyes} eyes and {cfg.coloration.hair} hair
            {"walking" if cfg.is_humanoid else "slithering"} by.
            """
        )
    )


if __name__ == "__main__":
    cli()
