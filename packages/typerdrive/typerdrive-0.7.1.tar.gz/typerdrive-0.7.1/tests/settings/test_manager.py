import json
from collections.abc import Generator
from pathlib import Path
from typing import Annotated

import pytest
from rich.console import Console
import snick
from pydantic import AfterValidator, BaseModel, ValidationError
from pytest_mock import MockerFixture
from typerdrive.config import get_typerdrive_config
from typerdrive.env import tweak_env
from typerdrive.settings.exceptions import SettingsInitError, SettingsSaveError, SettingsUpdateError
from typerdrive.settings.manager import SettingsManager


def valid_alignment(value: str) -> str:
    if value not in ["good", "neutral", "evil"]:
        raise ValueError(f"{value} is an invalid alignment")
    return value


class DefaultSettingsModel(BaseModel):
    name: str = "jawa"
    planet: str = "tatooine"
    is_humanoid: bool = True
    alignment: Annotated[str, AfterValidator(valid_alignment)] = "neutral"


class RequiredFieldsModel(BaseModel):
    name: str
    planet: str
    is_humanoid: bool = True
    alignment: Annotated[str, AfterValidator(valid_alignment)] = "neutral"


@pytest.fixture
def fake_settings_path(tmp_path: Path) -> Generator[Path, None, None]:
    fake_settings_dir = tmp_path / ".local/share/test"
    fake_settings_dir.mkdir(parents=True)
    settings_path = fake_settings_dir / "settings.json"

    with tweak_env(HOME=str(tmp_path)):
        yield settings_path


class TestSettingsManager:
    def test_init__loads_default_model(self):
        manager = SettingsManager(DefaultSettingsModel)
        assert manager.settings_model == DefaultSettingsModel
        assert manager.settings_path == get_typerdrive_config().settings_path
        assert manager.invalid_warnings == {}

        assert isinstance(manager.settings_instance, DefaultSettingsModel)
        assert manager.settings_instance.name == "jawa"
        assert manager.settings_instance.planet == "tatooine"
        assert manager.settings_instance.is_humanoid
        assert manager.settings_instance.alignment == "neutral"

    def test_init__loads_default_model_from_disk(self, fake_settings_path: Path):
        settings_path = fake_settings_path
        settings_path.write_text(
            json.dumps(
                dict(name="hutt", planet="nal hutta", is_humanoid=False, alignment="evil"),
            )
        )

        manager = SettingsManager(DefaultSettingsModel)

        assert manager.settings_model == DefaultSettingsModel
        assert manager.settings_path == settings_path
        assert manager.invalid_warnings == {}

        assert isinstance(manager.settings_instance, DefaultSettingsModel)
        assert manager.settings_instance.name == "hutt"
        assert manager.settings_instance.planet == "nal hutta"
        assert not manager.settings_instance.is_humanoid
        assert manager.settings_instance.alignment == "evil"

    def test_init__loads_invalid_model_with_warnings(self):
        manager = SettingsManager(RequiredFieldsModel)
        assert manager.settings_model == RequiredFieldsModel
        assert manager.settings_path == get_typerdrive_config().settings_path
        assert manager.invalid_warnings == dict(
            name="Field required",
            planet="Field required",
        )

        assert isinstance(manager.settings_instance, RequiredFieldsModel)
        assert not hasattr(manager.settings_instance, "name")
        assert not hasattr(manager.settings_instance, "planet")
        assert manager.settings_instance.is_humanoid
        assert manager.settings_instance.alignment == "neutral"

    def test_init__loads_invalid_model_from_disk(self, fake_settings_path: Path):
        settings_path = fake_settings_path
        settings_path.write_text(json.dumps(dict(name="hutt")))

        manager = SettingsManager(RequiredFieldsModel)

        assert manager.settings_model == RequiredFieldsModel
        assert manager.settings_path == settings_path
        assert manager.invalid_warnings == dict(
            planet="Field required",
        )

        assert isinstance(manager.settings_instance, RequiredFieldsModel)
        assert manager.settings_instance.name == "hutt"
        assert not hasattr(manager.settings_instance, "planet")
        assert manager.settings_instance.is_humanoid
        assert manager.settings_instance.alignment == "neutral"

    def test_init__raises_error_on_failure(self, mocker: MockerFixture):
        mocker.patch.object(DefaultSettingsModel, "__init__", side_effect=RuntimeError("BOOM"))
        with pytest.raises(SettingsInitError, match="Failed to initialize settings"):
            SettingsManager(DefaultSettingsModel)

    def test_set_warnings__unpacks_validation_error(self):
        manager = SettingsManager(DefaultSettingsModel)
        err = ValidationError.from_exception_data(
            "BOOM",
            [
                {
                    "type": "missing",
                    "loc": ("name",),
                    "input": dict(),
                },
                {
                    "type": "missing",
                    "loc": ("planet",),
                    "input": dict(),
                },
            ],
        )
        manager.set_warnings(err)

        assert manager.invalid_warnings == dict(
            name="Field required",
            planet="Field required",
        )

    def test_update__updates_valid_to_valid_settings(self):
        manager = SettingsManager(DefaultSettingsModel)
        manager.update(planet="nevarro", alignment="good")
        assert isinstance(manager.settings_instance, DefaultSettingsModel)
        assert manager.settings_instance.name == "jawa"
        assert manager.settings_instance.planet == "nevarro"
        assert manager.settings_instance.alignment == "good"
        assert manager.settings_instance.is_humanoid
        assert manager.invalid_warnings == {}

    def test_update__updates_invalid_to_valid_settings(self):
        manager = SettingsManager(RequiredFieldsModel)
        assert len(manager.invalid_warnings) > 0
        manager.update(name="pyke", planet="oba diah")
        assert isinstance(manager.settings_instance, RequiredFieldsModel)
        assert manager.settings_instance.name == "pyke"
        assert manager.settings_instance.planet == "oba diah"
        assert manager.settings_instance.is_humanoid
        assert manager.settings_instance.alignment == "neutral"
        assert manager.invalid_warnings == {}

    def test_update__updates_valid_to_invalid_settings(self):
        manager = SettingsManager(DefaultSettingsModel)
        manager.update(planet="nevarro", alignment="negative")
        assert isinstance(manager.settings_instance, DefaultSettingsModel)
        assert manager.settings_instance.name == "jawa"
        assert manager.settings_instance.planet == "nevarro"
        assert manager.settings_instance.is_humanoid
        assert manager.settings_instance.alignment == "negative"
        assert manager.invalid_warnings == dict(
            alignment="Value error, negative is an invalid alignment",
        )

    def test_update__raises_error_on_failure(self, mocker: MockerFixture):
        manager = SettingsManager(DefaultSettingsModel)
        mocker.patch.object(manager.settings_model, "__init__", side_effect=RuntimeError("BOOM"))
        with pytest.raises(SettingsUpdateError, match="Failed to update settings"):
            manager.update()

    def test_unset__resets_field_to_default(self):
        manager = SettingsManager(DefaultSettingsModel)
        manager.update(name="pyke", planet="oba diah", alignment="evil")
        assert isinstance(manager.settings_instance, DefaultSettingsModel)
        assert manager.settings_instance.name == "pyke"
        assert manager.settings_instance.planet == "oba diah"
        assert manager.settings_instance.is_humanoid
        assert manager.settings_instance.alignment == "evil"
        assert manager.invalid_warnings == {}
        manager.unset("name", "alignment")
        assert manager.settings_instance.name == "jawa"
        assert manager.settings_instance.planet == "oba diah"
        assert manager.settings_instance.alignment == "neutral"

    def test_unset__adds_warnings_if_field_has_no_default(self):
        manager = SettingsManager(RequiredFieldsModel)
        assert isinstance(manager.settings_instance, RequiredFieldsModel)
        manager.update(name="jawa", planet="tatooine", alignment="neutral")
        assert manager.invalid_warnings == {}
        manager.unset("planet")
        assert manager.settings_instance.name == "jawa"
        assert not hasattr(manager.settings_instance, "planet")
        assert manager.settings_instance.is_humanoid
        assert manager.settings_instance.alignment == "neutral"
        assert manager.invalid_warnings == dict(
            planet="Field required",
        )

    def test_reset__returns_all_fields_to_default(self):
        manager = SettingsManager(DefaultSettingsModel)
        manager.update(name="hutt", planet="nal hutta", is_humanoid=False, alignment="evil")
        assert isinstance(manager.settings_instance, DefaultSettingsModel)
        assert manager.settings_instance.name == "hutt"
        assert manager.settings_instance.planet == "nal hutta"
        assert not manager.settings_instance.is_humanoid
        assert manager.settings_instance.alignment == "evil"
        assert manager.invalid_warnings == {}
        manager.reset()
        assert manager.settings_instance.name == "jawa"
        assert manager.settings_instance.planet == "tatooine"
        assert manager.settings_instance.is_humanoid
        assert manager.settings_instance.alignment == "neutral"

    def test_reset__adds_warnings_for_fields_with_no_defaults(self):
        manager = SettingsManager(RequiredFieldsModel)
        manager.update(name="hutt", planet="nal hutta", is_humanoid=False, alignment="evil")
        assert isinstance(manager.settings_instance, RequiredFieldsModel)
        assert manager.settings_instance.name == "hutt"
        assert manager.settings_instance.planet == "nal hutta"
        assert not manager.settings_instance.is_humanoid
        assert manager.settings_instance.alignment == "evil"
        assert manager.invalid_warnings == {}
        manager.reset()
        assert not hasattr(manager.settings_instance, "name")
        assert not hasattr(manager.settings_instance, "planet")
        assert manager.settings_instance.is_humanoid
        assert manager.settings_instance.alignment == "neutral"
        assert manager.invalid_warnings == dict(
            name="Field required",
            planet="Field required",
        )

    def test_pretty__provides_string_reflecting_settings_instance(self):
        manager = SettingsManager(RequiredFieldsModel)
        manager.update(name="pyke", alignment="negative")
        console = Console()
        with console.capture() as snag:
            console.print(manager.pretty())
        computed = snick.strip_trailing_whitespace(snag.get())
        expected = snick.dedent(
            """
            Settings Values

                    name  str   ->  pyke
                  planet  str   ->  <UNSET>
             is-humanoid  bool  ->  True
               alignment  str   ->  negative


            Invalid Values

                planet  ->  Field required
             alignment  ->  Value error, negative is an invalid alignment
            """
        ).strip()
        assert expected == computed


    def test_pretty__does_not_error_with_no_default_fields(self):

        class NoDefaultsModel(BaseModel):
            name: str
            planet: str
            is_humanoid: bool
            alignment: Annotated[str, AfterValidator(valid_alignment)]

        manager = SettingsManager(NoDefaultsModel)
        console = Console()
        with console.capture() as snag:
            console.print(manager.pretty())
        computed = snick.strip_trailing_whitespace(snag.get())
        expected = snick.dedent(
            """
            Settings Values

                    name  str   ->  <UNSET>
                  planet  str   ->  <UNSET>
             is-humanoid  bool  ->  <UNSET>
               alignment  str   ->  <UNSET>


            Invalid Values

                    name  ->  Field required
                  planet  ->  Field required
             is-humanoid  ->  Field required
               alignment  ->  Field required
            """
        ).strip()
        assert expected == computed, f"Values didn't match\n\ncomputed:\n{computed}\n\nexpected:\n{expected}"

    def test_save__writes_settings_to_disk(self, fake_settings_path: Path):
        manager = SettingsManager(DefaultSettingsModel)
        manager.save()

        assert json.loads(fake_settings_path.read_text()) == dict(
            name="jawa", planet="tatooine", is_humanoid=True, alignment="neutral"
        )

    def test_save__raises_error_on_failure(self, mocker: MockerFixture):
        manager = SettingsManager(DefaultSettingsModel)
        mocker.patch.object(manager, "settings_path").write_text.side_effect = RuntimeError("BOOM")
        with pytest.raises(SettingsSaveError, match="Failed to save settings"):
            manager.save()
