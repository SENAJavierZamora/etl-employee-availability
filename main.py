import logging
import os
from dotenv import load_dotenv
from services.extract import extract_data
from services.transform import transform_data
from services.load import load_data

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)

SCOPES = [s.strip() for s in os.getenv('SCOPES').split(',')]
FILENAME = os.getenv("FILENAME")
FILEID = os.getenv("FILEID")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")

WEEK_DAYS = {
    'LUNES': 1,
    'MARTES': 2,
    'MIERCOLES': 3,
    'JUEVES': 4,
    'VIERNES': 5,
    'SABADO': 6,
    'DOMINGO': 7
}


def main():
    try:
        logger.info("Extracting data...")
        extract_data(output_file='data.xlsx',
                     scopes=SCOPES,
                     file_id=FILEID,
                     service_account_file=SERVICE_ACCOUNT_FILE)

        logger.info("Transforming data...")

        transformed_data = transform_data(data_file_path='data.xlsx', columns=WEEK_DAYS)

        logger.info(f"Transform Process completed successfully. {transformed_data}")

        load_data(data=transformed_data)

    except Exception as e:
        logger.error("Error en el proceso principal: %s", e)


if __name__ == "__main__":
    main()
