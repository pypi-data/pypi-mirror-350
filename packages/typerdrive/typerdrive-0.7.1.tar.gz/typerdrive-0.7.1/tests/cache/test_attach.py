from pathlib import Path

import typer
from typerdrive.cache.attach import attach_cache, get_cache_manager
from typerdrive.cache.exceptions import CacheError
from typerdrive.cache.manager import CacheManager

from tests.helpers import check_output, match_output


class TestAttachCache:
    def test_attach_cache__adds_cache_manager_to_context(self):
        cli: typer.Typer = typer.Typer()

        @cli.command()
        @attach_cache()
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            manager = ctx.obj.cache_manager
            assert isinstance(manager, CacheManager)

        check_output(cli, prog_name="test")

    def test_attach_cache__show(self, fake_cache_path: Path):
        cli = typer.Typer()

        @cli.command()
        @attach_cache(show=True)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            manager = get_cache_manager(ctx)
            manager.store_bytes(b"jawa", "jawa")
            manager.store_bytes(b"ewok", "ewok")
            manager.store_bytes(b"hutt & pyke", "hutt/pyke")

        expected_pattern = f"""
            📂 {fake_cache_path}
            ├── 📂 hutt
            │   └── 📄pyke (11 Bytes)
            ├── 📄ewok (4 Bytes)
            └── 📄jawa (4 Bytes)
        """
        match_output(
            cli,
            expected_pattern=expected_pattern,
            escape_parens=True,
            prog_name="test",
        )


class TestWithParameters:
    def test_attach_cache__with_manager_parameter(self, fake_cache_path: Path):
        cli = typer.Typer()

        @cli.command()
        @attach_cache(show=True)
        def noop(ctx: typer.Context, mgr: CacheManager):  # pyright: ignore[reportUnusedFunction, reportUnusedParameter]
            mgr.store_bytes(b"jawa", "jawa")
            mgr.store_bytes(b"ewok", "ewok")
            mgr.store_bytes(b"hutt & pyke", "hutt/pyke")

        expected_pattern = f"""
            📂 {fake_cache_path}
            ├── 📂 hutt
            │   └── 📄pyke (11 Bytes)
            ├── 📄ewok (4 Bytes)
            └── 📄jawa (4 Bytes)
        """
        match_output(
            cli,
            expected_pattern=expected_pattern,
            escape_parens=True,
            prog_name="test",
        )


class TestGetManager:
    def test_get_cache_manager__extracts_cache_manager_from_context(self, fake_cache_path: Path):
        cli = typer.Typer()

        @cli.command()
        @attach_cache()
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            manager = get_cache_manager(ctx)
            assert isinstance(manager, CacheManager)
            assert manager.cache_dir == fake_cache_path
            print("Passed!")

        match_output(
            cli,
            expected_pattern=["Passed"],
            exit_code=0,
            prog_name="test",
        )

    def test_get_cache_manager__raises_exception_if_context_has_no_manager(self):
        cli = typer.Typer()

        @cli.command()
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            get_cache_manager(ctx)
            print("Passed!")

        match_output(
            cli,
            exception_type=CacheError,
            exception_pattern="Cache is not bound to the context",
            exit_code=1,
            prog_name="test",
        )

    def test_get_cache_manager__raises_exception_if_non_manager_retrieved(self):
        cli = typer.Typer()

        @cli.command()
        @attach_cache()
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            ctx.obj.cache_manager = "Not a manager!"
            get_cache_manager(ctx)
            print("Passed!")

        match_output(
            cli,
            exception_type=CacheError,
            exception_pattern="Item in user context at `cache_manager` was not a CacheManager",
            exit_code=1,
            prog_name="test",
        )
