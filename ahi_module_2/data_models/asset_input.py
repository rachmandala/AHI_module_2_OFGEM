"""Asset input data model."""

from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

from ahi_module_2.utils.enums import AssetClass


class AssetInput(BaseModel):
    """Primary input data for an industrial asset."""

    asset_id: str = Field(..., description="Unique asset identifier")
    asset_name: str = Field(..., description="Human-readable asset name")
    asset_class: AssetClass = Field(..., description="Asset class/type")
    design_life: float = Field(..., gt=0, description="Design life in years")
    current_age: float = Field(..., ge=0, description="Current age in years")
    max_load: float = Field(..., gt=0, description="Maximum permissible load (MW or engineering unit)")
    normal_load: float = Field(..., gt=0, description="Normal operating load")

    # Environmental factors (each in range [0.5, 2.0] is typical; must be > 0)
    distance_to_coast_factor: float = Field(..., gt=0, description="Distance-to-coast environmental factor")
    altitude_factor: float = Field(..., gt=0, description="Altitude environmental factor")
    temperature_factor: float = Field(..., gt=0, description="Temperature environmental factor")
    corrosive_factor: float = Field(..., gt=0, description="Corrosive environment factor")
    dust_factor: float = Field(..., gt=0, description="Dust/particulate environmental factor")

    @model_validator(mode="after")
    def normal_load_le_max_load(self) -> "AssetInput":
        if self.normal_load > self.max_load:
            raise ValueError("normal_load must not exceed max_load")
        return self
