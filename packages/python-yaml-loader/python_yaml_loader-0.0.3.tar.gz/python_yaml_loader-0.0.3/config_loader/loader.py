import yaml
from pathlib import Path
from copy import deepcopy


class YamlConfigLoader:
    DEFAULT_FILE_NAME = "application.yml"

    def __init__(
        self,
        config_file: str | Path | None = None,
        profile: str | None = None,
        settings_root: Path | None = None,
        project_root: Path | None = None
    ):
        cwd = Path.cwd()
        self.profile = profile
        self.settings_root = settings_root.resolve() if settings_root else cwd
        self.project_root = project_root.resolve() if project_root else cwd.parent
        self.config_file = Path(config_file).resolve() if config_file else self.settings_root / "resources" / "application.yml"
        self._explicit_config_file = Path(config_file) if config_file else None
        self._config = self._load()

    def _load(self):
        final_config = {}

        if not self.config_file.exists() and not self._explicit_config_file.exists():
            print(
                f"[YamlConfigLoader] ⚠️ Config file not found:"
                f" {self.config_file} (using empty config)"
            )
            return final_config

        # 1. Project root szintű betöltés
        final_config = self._merge_config_layers(final_config, self.project_root / "resources")

        # 2. Settings root (felülírhatja a project root-ot)
        final_config = self._merge_config_layers(final_config, self.settings_root / "resources")

        # 3. Modulok bejárása (project_root közvetlen gyerekei, kivéve settings_root)
        for child in self.project_root.iterdir():
            if child.is_dir() and child.resolve() != self.settings_root:
                final_config = self._merge_config_layers(final_config, child / "resources")

        return final_config

    def _merge_config_layers(self, base_config: dict, resource_dir: Path) -> dict:
        if not resource_dir.exists():
            return base_config

        merged = deepcopy(base_config)

        # Ha a config_file explicit meg volt adva, ne keresgéljünk automatikusan
        base_file =(
            resource_dir / (
            self._explicit_config_file.name if self._explicit_config_file else YamlConfigLoader.DEFAULT_FILE_NAME
            )
        )

        merged = self._deep_merge(merged, self._load_from_path(base_file))
        profile_file = self._get_profile_filename_from_base(resource_dir)

        if self.profile and "profiles" in merged:
            profile_data = merged["profiles"].get(self.profile)
            if profile_data:
                merged = self._deep_merge(merged, profile_data)

        if self.profile and self.profile in merged:
            default_data = merged.get("default", {})
            profile_data = merged.get(self.profile, {})
            return self._deep_merge(default_data, profile_data)

        if self.profile and profile_file and profile_file.exists():
            merged = self._deep_merge(merged, self._load_from_path(profile_file))

        return merged

    @staticmethod
    def _load_from_path(path: Path):
        if not path.exists():
            return {}
        with open(path) as f:
            return yaml.safe_load(f) or {}

    def _deep_merge(self, base: dict, override: dict) -> dict:
        result = deepcopy(base)
        for k, v in override.items():
            if (
                k in result and isinstance(result[k], dict)
                and isinstance(v, dict)
            ):
                result[k] = self._deep_merge(result[k], v)
            else:
                result[k] = deepcopy(v)
        return result

    def _get_profile_filename_from_base(self, resource_dir: Path):
        if self.profile:
            base_name = (
                self._explicit_config_file.stem
                if self._explicit_config_file
                else YamlConfigLoader.DEFAULT_FILE_NAME.removesuffix(".yml")
            )
            return resource_dir / f"{base_name}-{self.profile}.yml"
        return None

    def get(self, key, default=None):
        keys = key.split(".")
        value = self._config
        for k in keys:
            if not isinstance(value, dict):
                return default
            value = value.get(k)
            if value is None:
                return default
        return value
