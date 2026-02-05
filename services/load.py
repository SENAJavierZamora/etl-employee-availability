import requests
import json
import os
from dotenv import load_dotenv
import logging
from .dto import ApiPayloadDTO

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
BATCH_SIZE = 1000


def load_data(data: list[ApiPayloadDTO]):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {API_KEY}"
    }

    try:
        if not data:
            logger.info("No hay datos para subir.")
            return

        batch_size = int(BATCH_SIZE)

        for i in range(0, len(data), batch_size):
            logger.info("Subiendo lote %d a %d", i, min(i + batch_size, len(data)))
            batch = data[i:i + batch_size]
            logger.info(f"Subiendo lote {batch}")
            json_data = json.dumps(batch)
            logger.info(f"Subiendo lote {json_data}")

            response = requests.post(API_URL, headers=headers, data=json.dumps(batch))
            if response.ok:
                logger.info("Lote subido correctamente (%s)", response.status_code)
            else:
                logger.error(
                    "Error al subir lote: %s - %s",
                    response.status_code,
                    response.text,
                )
    except Exception as e:
        logger.error(f"Error al subir datos: {e}")
