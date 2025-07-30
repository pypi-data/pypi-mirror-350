import io
import os

import chardet
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.auth.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


load_dotenv()


def authenticate_google_services(service_account_file: str):
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=[
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/documents",
            "https://www.googleapis.com/auth/spreadsheets",
        ],
    )
    drive_service = build("drive", "v3", credentials=credentials)
    docs_service = build("docs", "v1", credentials=credentials)
    return drive_service, docs_service


def service_account_authentication(service_name, version, scopes):
    service_account_file: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "./keys/google_service_account_key.json")
    credentials: Credentials = service_account.Credentials.from_service_account_file(service_account_file,
                                                                                     scopes=scopes)
    return build(service_name, version, credentials=credentials)


def get_google_doc_content(file_id: str, mime_type):
    scopes = ['https://www.googleapis.com/auth/drive']
    service = service_account_authentication(service_name="drive", version="v3", scopes=scopes)

    return get_google_doc_content_with_service(file_id, mime_type, service)


def get_google_doc_content_with_service(file_id: str, mime_type, service, with_decode=True):
    request = None
    if mime_type == 'application/vnd.google-apps.document':
        request = service.files().export_media(fileId=file_id, mimeType='text/plain')
    elif mime_type == 'application/octet-stream':
        request = service.files().get_media(fileId=file_id)
    elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        request = service.files().get_media(fileId=file_id)
    else:
        request = service.files().get_media(fileId=file_id)

    if request is None:
        return None

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.seek(0)

    if with_decode:
        raw_content = fh.getvalue()
        detected_encoding = chardet.detect(raw_content)
        content = raw_content.decode(detected_encoding['encoding'])
        if content.startswith('\ufeff'):
            content = content[1:]
        return content

    return fh.getvalue()


def get_google_doc_mime_type(file_id: str) -> str:
    """
    取得指定 Google 文件的 MIME 類型
    
    Args:
        file_id (str): Google 文件的 ID
        
    Returns:
        str: 文件的 MIME 類型，例如 'application/vnd.google-apps.document'
        
    Raises:
        HttpError: 當無法取得檔案資訊時拋出
    """
    scopes = ['https://www.googleapis.com/auth/drive']
    try:
        service = service_account_authentication(
            service_name="drive", 
            version="v3", 
            scopes=scopes
        )
        
        # 取得檔案的中繼資料
        file_metadata = service.files().get(
            fileId=file_id,
            fields='mimeType'
        ).execute()
        
        return file_metadata.get('mimeType', '')
    except HttpError as error:
        print(f'An error occurred: {error}')
        raise
