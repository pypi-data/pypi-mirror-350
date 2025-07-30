from dataclasses import dataclass
from datetime import datetime
from typing import Union


@dataclass
class Context:
    start_time: Union[
        str, datetime
    ] = "${qwak_ingestion_start_timestamp}"  # todo mlops-2312 - rename?
    end_time: Union[
        str, datetime
    ] = "${qwak_ingestion_end_timestamp}"  # todo mlops-2312 - rename?
