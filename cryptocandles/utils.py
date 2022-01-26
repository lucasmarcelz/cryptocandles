from typing import List

import pydantic


class Arguments(pydantic.BaseModel):
    tickers: List[str] = pydantic.Field(..., description="List of tickers to be observed")
