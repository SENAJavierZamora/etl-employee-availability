import os
import io
import logging
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


def extract_data(output_file, scopes, file_id, service_account_file):
    try:
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=scopes)
        service = build('drive', 'v3', credentials=credentials)
    except Exception as e:
        logger.error(f"An error occurred: {e} while authenticating the service account.")
        raise

    if os.path.exists(output_file):
        logger.info(f"File {output_file} already exists. Deleting the file.")
        os.remove(output_file)
        logger.info(f"File {output_file} deleted successfully.")

    try:
        file_metadata = service.files().get(fileId=file_id, fields="id, name, mimeType, size").execute()
        mime_type = file_metadata['mimeType']
        if mime_type.startswith('application/vnd.google-apps.'):
            request = service.files().export_media(fileId=file_id,
                                                   mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        else:
            request = service.files().get_media(fileId=file_id)
    except Exception as e:
        logger.error(f"An error occurred: {e} while getting file metadata.")
        raise

    try:
        logger.info(f"Downloading file {output_file}...")
        fh = io.FileIO(output_file, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            logger.info(f"Download {int(status.progress() * 100)}% complete.")
        fh.close()
        logger.info(f"File {output_file} downloaded successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
                logger.info(f"File {output_file} deleted successfully.")
            except Exception as delete_error:
                logger.error(f"An error occurred while deleting the file: {delete_error}")
        raise
