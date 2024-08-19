from pydantic import BaseModel
from typing import List, Dict

class BerryStatsResponseModel(BaseModel):
    berries_names: List[str]
    min_growth_time: int
    median_growth_time: float
    max_growth_time: int
    variance_growth_time: float
    mean_growth_time: float
    frequency_growth_time: Dict[int, int]

    class Config:
        schema_extra = {
            "example": {
                "berries_names": ["cheri", "pecha"],
                "min_growth_time": 2,
                "median_growth_time": 4.5,
                "max_growth_time": 8,
                "variance_growth_time": 1.3,
                "mean_growth_time": 5.2,
                "frequency_growth_time": {2: 3, 4: 5, 8: 2}
            }
        }