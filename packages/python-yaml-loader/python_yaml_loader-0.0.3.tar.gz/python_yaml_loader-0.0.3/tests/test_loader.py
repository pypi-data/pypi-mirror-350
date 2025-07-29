import os
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch
from config_loader.loader import YamlConfigLoader


BASE = Path.cwd() / "tests" / "resources"


@patch("pathlib.Path.cwd", return_value=Path.cwd() / "tests")
class TestYamlConfigLoader:
    def test_basic_loading(self, mock_cwd):
        loader = YamlConfigLoader(BASE / "base.yml")
        assert loader.get("app.name") == "test-app"
        assert loader.get("app.debug") is False

    def test_nested_key_access(self, mock_cwd):
        loader = YamlConfigLoader(BASE / "with_profiles.yml", profile="dev")
        assert loader.get("database.connection.host") == "localhost"
        assert loader.get("database.connection.port") == 5432

    def test_profile_override(self, mock_cwd):
        loader = YamlConfigLoader(BASE / "with_profiles.yml", profile="prod")
        assert loader.get("app.debug") is False
        assert loader.get("database.connection.host") == "prod.db.internal"

    def test_missing_key_returns_default(self, mock_cwd):
        loader = YamlConfigLoader(BASE / "base.yml")
        assert loader.get("nonexistent.key", default="fallback") == "fallback"

    def test_missing_file_returns_empty_config(self, mock_cwd, capfd):
        loader = YamlConfigLoader(config_file="nonexistent.yml")
        assert loader.get("anything") is None

        out, err = capfd.readouterr()
        assert "Config file not found" in out

    def test_invalid_yaml_raises(self, mock_cwd):
        with pytest.raises(Exception):
            YamlConfigLoader(BASE / "invalid.yml")

    def test_profile_root_level_override(self, mock_cwd):
        loader = YamlConfigLoader(BASE / "root_profiles.yml", profile="prod")
        assert loader.get("app.name") == "my-prod-app"
        assert loader.get("app.debug") is False
        assert loader.get("feature.enabled") is True

    def test_profile_separate_file(self, mock_cwd):
        loader = YamlConfigLoader(BASE / "multi_file_base.yml", profile="test")
        assert loader.get("service.name") == "test-service"
        assert loader.get("service.debug") is True

    def test_deep_merge_override_nested_values(self, mock_cwd):
        loader = YamlConfigLoader(BASE / "merge_base.yml", profile="custom")
        assert loader.get("nested.level1.level2") == "override"
        assert loader.get("nested.level1.keep") == "original"

    def test_deep_merge_non_dict_override(self, mock_cwd):
        loader = YamlConfigLoader(BASE / "merge_base.yml", profile="scalar_override")
        assert loader.get("scalar") == "replaced"

    def test_unknown_profile_falls_back_to_base(self, mock_cwd):
        loader = YamlConfigLoader(BASE / "base.yml", profile="nonexistent")
        assert loader.get("app.name") == "test-app"
        assert loader.get("app.debug") is False

    def test_get_fails_on_non_dict_intermediate(self, mock_cwd):
        loader = YamlConfigLoader(BASE / "base.yml")
        # app.name == "test-app", tehát string -> nem tudunk továbblépni mélyebbre
        assert loader.get("app.name.subkey", default="fail-safe") == "fail-safe"

    def test_default_application_yml_loaded_from_project_resources(self, mock_cwd, monkeypatch):
        mock_cwd.stop()

        # Szimulálunk egy "ProjectDir/resources/application.yml" struktúrát
        with tempfile.TemporaryDirectory() as tmpdirname:
            project_dir = Path(tmpdirname) / "myproject"
            resources = project_dir / "resources"
            resources.mkdir(parents=True)
            (resources / "application.yml").write_text("app:\n  name: default-app\n")

            monkeypatch.setattr(Path, "cwd", lambda: project_dir)
            loader = YamlConfigLoader(project_root=project_dir)
            assert loader.get("app.name") == "default-app"

    def test_module_resources_override(self, mock_cwd, monkeypatch):
        mock_cwd.stop()
        # root/
        # ├── mainproject/resources/application.yml                 (app.name = "main")
        # └── mainproject/submodule/resources/application.yml       (app.name = "sub")

        with tempfile.TemporaryDirectory() as tmpdirname:
            root = Path(tmpdirname)
            main = root / "mainproject" / "resources"
            sub = root / "mainproject" / "submodule" / "resources"
            main.mkdir(parents=True)
            sub.mkdir(parents=True)
            (main / "application.yml").write_text("app:\n  name: main\n  debug: false\n")
            (sub / "application.yml").write_text("app:\n  name: sub\n")

            # Emuláljuk, hogy a mainproject a "settings" root
            monkeypatch.setattr(Path, "cwd", lambda: main.parent)

            loader = YamlConfigLoader(project_root=main.parent)
            assert loader.get("app.name") == "sub"  # override-olja a modulbeli érték
            assert loader.get("app.debug") is False  # de a base érték megmarad

    def test_module_profile_merging(self, mock_cwd, monkeypatch):
        mock_cwd.stop()
        with tempfile.TemporaryDirectory() as tmpdirname:
            root = Path(tmpdirname)
            project_res = root / "project" / "resources"
            module_res = root / "module" / "resources"
            profile_file = module_res / "application-prod.yml"

            project_res.mkdir(parents=True)
            module_res.mkdir(parents=True)

            (project_res / "application.yml").write_text("app:\n  debug: false\n")
            (profile_file).write_text("app:\n  debug: true\n")

            monkeypatch.setattr(Path, "cwd", lambda: project_res.parent)

            loader = YamlConfigLoader(profile="prod", settings_root=project_res.parent)
            assert loader.get("app.debug") is True
