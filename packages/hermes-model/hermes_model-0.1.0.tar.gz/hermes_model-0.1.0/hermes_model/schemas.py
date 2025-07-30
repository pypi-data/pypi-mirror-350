from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ModelInput(BaseModel):
    forecast_start: datetime
    forecast_end: datetime

    injection_observation: list[dict | None] | None = None
    injection_plan: list[dict] | None = None

    seismicity_observation: str | None = None

    bounding_polygon: str | None = None
    depth_min: float | None = None
    depth_max: float | None = None

    model_parameters: dict = {}

    model_settings: dict = {}

    model_config = ConfigDict(
        protected_namespaces=(),
        extra='forbid',
    )
