# -*- coding: utf-8 -*-
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Optional

class BerryStatsResponseModel(BaseModel):
    """
    Data model for representing statistics of berry growth times.

    Attributes:
        berries_names (List[str]): A list of berry names.
        min_growth_time (Optional[int]): The minimum growth time among the berries.
        median_growth_time (Optional[float]): The median growth time.
        max_growth_time (Optional[int]): The maximum growth time.
        variance_growth_time (Optional[float]): The variance of the growth times.
        mean_growth_time (Optional[float]): The mean of the growth times.
        frequency_growth_time (Dict[int, int]): A dictionary mapping growth times to the frequency 
            of berries having that growth time.
    """
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