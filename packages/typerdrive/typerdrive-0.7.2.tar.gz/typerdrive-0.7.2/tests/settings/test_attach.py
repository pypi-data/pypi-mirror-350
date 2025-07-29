import json
from pathlib import Path
from typing import cast

import pytest
import typer
from pydantic import BaseModel
from typer.testing import CliRunner
from typerdrive.constants import Validation
from typerdrive.settings.attach import attach_settings, get_settings, get_settings_manager
from typerdrive.settings.exceptions import SettingsError
from typerdrive.settings.manager import SettingsManager

from tests.helpers import match_help, match_output
from tests.settings.models import DefaultSettingsModel, RequiredFieldsModel


class TestAttachSettings:
    def test_attach_settings__adds_settings_to_context(self, runner: CliRunner):
        cli: typer.Typer = typer.Typer()

        @cli.command()
        @attach_settings(DefaultSettingsModel)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            settings = get_settings(ctx, DefaultSettingsModel)
            assert settings.name == "jawa"
            assert settings.planet == "tatooine"
            assert settings.is_humanoid
            assert settings.alignment == "neutral"

        result = runner.invoke(cli, [], prog_name="test")
        assert result.exit_code == 0

    def test_attach_settings__fails_on_invalid_settings_by_default(self, runner: CliRunner):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(RequiredFieldsModel)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction, reportUnusedParameter]
            pass

        result = runner.invoke(cli, [], prog_name="test")
        assert result.exit_code == 1

    def test_attach_settings__does_not_fail_on_invalid_settings_with_no_validation(self, runner: CliRunner):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(RequiredFieldsModel, validation=Validation.NEVER)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            settings = get_settings(ctx, RequiredFieldsModel)
            assert not hasattr(settings, "name")
            assert not hasattr(settings, "planet")
            assert settings.is_humanoid
            assert settings.alignment == "neutral"

        result = runner.invoke(cli, [], prog_name="test")
        assert result.exit_code == 0

    def test_attach_settings__fails_before_with_before_validation(self):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(RequiredFieldsModel, validation=Validation.BEFORE)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction, reportUnusedParameter]
            print("in function body")

        expected_pattern = [
            "in function body",
        ]
        match_output(
            cli,
            exit_code=1,
            unwanted_pattern=expected_pattern,
            exception_type=SettingsError,
            exception_pattern="Initial settings are invalid",
            prog_name="test",
        )

    def test_attach_settings__fails_after_with_after_validation(self):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(RequiredFieldsModel, validation=Validation.AFTER)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction, reportUnusedParameter]
            print("in function body")

        expected_pattern = [
            "in function body",
        ]
        match_output(
            cli,
            exit_code=1,
            expected_pattern=expected_pattern,
            exception_type=SettingsError,
            exception_pattern="Final settings are invalid",
            prog_name="test",
        )

    @pytest.mark.parametrize(
        "model,exception_pattern",
        [
            (RequiredFieldsModel, "Initial settings are invalid"),
            (DefaultSettingsModel, "Final settings are invalid"),
        ],
    )
    def test_attach_settings__fails_before_and_after_with_both_validation(
        self,
        model: type[BaseModel],
        exception_pattern: str,
    ):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(model, validation=Validation.BOTH)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            print("in function body")
            settings = get_settings(ctx, model)
            setattr(settings, "alignment", "invalid-alignment")

        match_output(
            cli,
            exit_code=1,
            exception_type=SettingsError,
            exception_pattern=exception_pattern,
            prog_name="test",
        )

    def test_attach_settings__persist(self, fake_settings_path: Path, runner: CliRunner):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(DefaultSettingsModel, persist=True)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            settings = get_settings(ctx, DefaultSettingsModel)
            settings.name = "hutt"
            settings.planet = "nal hutta"
            settings.is_humanoid = False
            settings.alignment = "evil"

        result = runner.invoke(cli, [], prog_name="test")
        assert result.exit_code == 0

        assert fake_settings_path.exists()
        data = json.loads(fake_settings_path.read_text())
        assert data == dict(
            name="hutt",
            planet="nal hutta",
            is_humanoid=False,
            alignment="evil",
        )

    def test_attach_settings__loads_settings_from_disk_if_file_exists(
        self,
        fake_settings_path: Path,
        runner: CliRunner,
    ):
        fake_settings_path.write_text(
            json.dumps(
                dict(
                    name="jawa",
                    planet="tatooine",
                    is_humanoid=True,
                    alignment="neutral",
                )
            )
        )
        cli = typer.Typer()

        @cli.command()
        @attach_settings(RequiredFieldsModel)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            settings = get_settings(ctx, RequiredFieldsModel)
            assert settings.name == "jawa"
            assert settings.planet == "tatooine"
            assert settings.is_humanoid
            assert settings.alignment == "neutral"

        result = runner.invoke(cli, [], prog_name="test")
        assert result.exit_code == 0

    def test_attach_settings__show_no_footer(self):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(DefaultSettingsModel, show=True)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction, reportUnusedParameter]
            pass

        expected_pattern = [
            "name.*jawa",
            "planet.*tatooine",
            "is-humanoid.*True",
            "alignment.*neutral",
        ]
        match_output(
            cli,
            expected_pattern=expected_pattern,
            prog_name="test",
        )

    def test_attach_settings__adds_footer_if_persisted(self, fake_settings_path: Path):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(DefaultSettingsModel, persist=True, show=True)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction, reportUnusedParameter]
            pass

        expected_pattern = [
            "name.*jawa",
            "planet.*tatooine",
            "is-humanoid.*True",
            "alignment.*neutral",
            f"saved to {str(fake_settings_path)[:40]}",
        ]
        match_output(
            cli,
            expected_pattern=expected_pattern,
            prog_name="test",
        )


class TestWithParameters:
    def test_attach_settings__with_settings_parameter(self):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(DefaultSettingsModel, show=True)
        def noop(ctx: typer.Context, stuff: DefaultSettingsModel):  # pyright: ignore[reportUnusedFunction]
            assert stuff.name == "jawa"
            assert stuff.planet == "tatooine"
            assert stuff.is_humanoid
            assert stuff.alignment == "neutral"
            ctx_settings = get_settings(ctx, DefaultSettingsModel)
            assert ctx_settings is stuff

        expected_pattern = [
            "name.*jawa",
            "planet.*tatooine",
            "is-humanoid.*True",
            "alignment.*neutral",
        ]
        match_output(
            cli,
            expected_pattern=expected_pattern,
            prog_name="test",
        )

        match_help(cli, unwanted_pattern="stuff")

    def test_attach_settings__with_manager_parameter(self):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(DefaultSettingsModel, show=True)
        def noop(ctx: typer.Context, mgr: SettingsManager):  # pyright: ignore[reportUnusedFunction]
            settings: DefaultSettingsModel = cast(DefaultSettingsModel, mgr.settings_instance)
            assert settings.name == "jawa"
            assert settings.planet == "tatooine"
            assert settings.is_humanoid
            assert settings.alignment == "neutral"
            ctx_settings = get_settings(ctx, DefaultSettingsModel)
            assert ctx_settings is settings

        expected_pattern = [
            "name.*jawa",
            "planet.*tatooine",
            "is-humanoid.*True",
            "alignment.*neutral",
        ]
        match_output(
            cli,
            expected_pattern=expected_pattern,
            prog_name="test",
        )

        match_help(cli, unwanted_pattern="mgr")


class TestGetSettings:
    def test_get_settings__extracts_settings_from_context(self, runner: CliRunner):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(DefaultSettingsModel)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            settings = get_settings(ctx, DefaultSettingsModel)
            assert isinstance(settings, DefaultSettingsModel)
            assert settings.name == "jawa"
            assert settings.planet == "tatooine"
            assert settings.is_humanoid
            assert settings.alignment == "neutral"

        result = runner.invoke(cli, [], prog_name="test")
        assert result.exit_code == 0

    def test_get_settings__raises_error_with_no_attached_settings(self):
        cli = typer.Typer()

        @cli.command()
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            get_settings(ctx, DefaultSettingsModel)

        match_output(
            cli,
            exception_type=SettingsError,
            exception_pattern="Settings are not bound to the context",
            exit_code=1,
            prog_name="test",
        )

    def test_get_settings__raises_error_with_wrong_settings_type(self):
        class NoMatchSettings(BaseModel):
            name: str = "jawa"
            planet: str = "tatooine"
            is_humanoid: bool = True
            alignment: str = "neutral"

        cli = typer.Typer()

        @cli.command()
        @attach_settings(DefaultSettingsModel)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            get_settings(ctx, NoMatchSettings)

        match_output(
            cli,
            exception_type=SettingsError,
            exception_pattern="instance doesn't match expected",
            exit_code=1,
            prog_name="test",
        )


class TestGetManager:
    def test_get_settings_manager__extracts_settings_manager_from_context(self, fake_settings_path: Path):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(DefaultSettingsModel)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            manager = get_settings_manager(ctx)
            assert isinstance(manager, SettingsManager)
            assert manager.settings_model == DefaultSettingsModel
            assert manager.settings_path == fake_settings_path
            assert manager.invalid_warnings == {}
            assert isinstance(manager.settings_instance, DefaultSettingsModel)
            print("Passed!")

        match_output(
            cli,
            expected_pattern=["Passed"],
            exit_code=0,
            prog_name="test",
        )

    def test_get_settings_manager__raises_exception_if_context_has_no_manager(self):
        cli = typer.Typer()

        @cli.command()
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            get_settings_manager(ctx)
            print("Passed!")

        match_output(
            cli,
            exception_type=SettingsError,
            exception_pattern="Settings are not bound to the context",
            exit_code=1,
            prog_name="test",
        )

    def test_get_settings_manager__raises_exception_if_non_manager_retrieved(self):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(DefaultSettingsModel)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            ctx.obj.settings_manager = "Not a manager!"
            get_settings_manager(ctx)
            print("Passed!")

        match_output(
            cli,
            exception_type=SettingsError,
            exception_pattern="Item in user context at `settings_manager` was not a SettingsManager",
            exit_code=1,
            prog_name="test",
        )
