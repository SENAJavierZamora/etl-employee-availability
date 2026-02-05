import re
import pandas as pd
from pydantic import ValidationError
import logging
from services.dto import (ApiPayloadDTO)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

time_pattern = re.compile(r"(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})")


def normalize_time(t: str) -> str:
    try:
        h, m = t.split(":")
        return f"{int(h):02d}:{int(m):02d}"
    except Exception as e:
        logger.error(f"Error normalizing time '{t}': {e}")
        return "00:00"


def parse_ranges(value):
    try:
        if pd.isna(value):
            return []
        return [
            (normalize_time(start), normalize_time(end))
            for start, end in time_pattern.findall(str(value))
        ]
    except Exception as e:
        logger.error(f"Error parsing ranges from value '{value}': {e}")
        return []


def transform_data(data_file_path: str, columns: dict):
    try:
        payload = []
        df = pd.read_excel(data_file_path)

        day_cols = [c for c in df.columns if c in columns.keys()]

        for _, row in df.iterrows():
            id_empleado = str(row["id_empleado"])

            for day in day_cols:
                day_index = int(columns.get(day))
                ranges = parse_ranges(row[day])

                for start, end in ranges:
                    try:
                        dto = ApiPayloadDTO(
                            id_week_day=int(day_index),
                            id_empleado=id_empleado,
                            start_time=start,
                            end_time=end,
                            estado=1
                        )
                        payload.append(dto.model_dump())

                    except ValidationError as e:
                        logger.error(f"Validation error for row {row} day {day} with start {start} and end {end}: {e}")
        return payload
    except Exception as e:
        logger.error(f"Error parsing availability regs: {e}")
        raise
