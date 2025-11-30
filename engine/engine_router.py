class EngineRouter:
    def __init__(self, loader):
        self.loader = loader

    def triggered_plays(self, kpi_name: str, condition: str):
        plays = self.loader.plays["plays"]
        return [
            (play_id, cfg)
            for play_id, cfg in plays.items()
            if cfg["trigger"]["kpi"] == kpi_name
            and cfg["trigger"]["condition"] == condition
        ]
