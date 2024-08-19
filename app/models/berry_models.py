from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Optional

class BerryStatsResponseModel(BaseModel):
    berries_names: List[str] = []
    min_growth_time: Optional[int] = None
    median_growth_time: Optional[float] = None
    max_growth_time: Optional[int] = None
    variance_growth_time: Optional[float] = None
    mean_growth_time: Optional[float] = None
    frequency_growth_time: Dict[int, int] = {}
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "berries_names": ["cheri", "pecha"],
                "min_growth_time": 2,
                "median_growth_time": 4.5,
                "max_growth_time": 8,
                "variance_growth_time": 1.3,
                "mean_growth_time": 5.2,
                "frequency_growth_time": {"2": 3, "4": 5, "8": 2}
            }
        }
    )