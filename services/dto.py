from pydantic import BaseModel


class ApiPayloadDTO(BaseModel):
    id_week_day: int
    id_empleado: str
    start_time: str
    end_time: str
    estado: int
