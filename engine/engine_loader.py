from pathlib import Path
import yaml


class EngineLoader:
    def __init__(self, root: str | Path | None = None):
        self.root = Path(root) if root else Path(__file__).resolve().parent
        self.prompt = None
        self.agents = None
        self.kpis = None
        self.plays = None
        self.manifest = None

    def _load_yaml(self, filename: str):
        path = self.root / filename
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def load(self):
        self.prompt = self._load_yaml("engine_prompt.yml")
        self.agents = self._load_yaml("agents.yml")
        self.kpis = self._load_yaml("kpis.yml")
        self.plays = self._load_yaml("plays.yml")
        self.manifest = self._load_yaml("engine_manifest.yml")
        return self

    def summary(self) -> dict:
        return {
            "engine": self.prompt["engine"]["name"],
            "version": self.prompt["engine"]["version"],
            "agents": list(self.agents["agents"].keys()),
            "kpis": list(self.kpis["kpis"].keys()),
            "plays": list(self.plays["plays"].keys()),
        }


if __name__ == "__main__":
    loader = EngineLoader().load()
    print(loader.summary())
