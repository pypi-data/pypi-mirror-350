import mimetypes
import os
import tempfile
from dotenv import load_dotenv
from botrun_hatch.models.hatch import Hatch
from botrun_hatch_client.hatch_client import HatchClient
from botrun_hatch_client.storage_client import StorageClient
from botrun_hatch.models.upload_file import UploadFile

from botrun_ask_folder.util.file_handler import (
    FailedToExtractContentException,
    HandlePowerpointError,
    UnsupportedFileException,
    handle_file_upload,
)

load_dotenv()


async def read_notice_prompt_and_model_from_hatch(hatch_id):
    print(f"read_notice_prompt_and_collection_from_hatch: {hatch_id}")
    hatch = await HatchClient().get_hatch(hatch_id)
    if hatch is None:
        raise Exception(f"Hatch {hatch_id} not found")
    system_prompt = hatch.prompt_template
    if len(hatch.files) > 0:
        embed_content = await process_all_files(hatch.user_id, hatch)
        system_prompt += embed_content

    return system_prompt, None, hatch.model_name


async def process_file(user_id: str, file: UploadFile):
    storage_client = StorageClient()
    temp_path = None
    try:
        # Get file content from storage
        file_data = await storage_client.get_file(user_id, file.id)
        if file_data:
            # Create temporary file with original filename
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, file.name)

            # Write content to temp file
            with open(temp_path, "wb") as temp_file:
                temp_file.write(file_data.getvalue())

            try:
                # Extract text content
                err, content = await get_doc_content(temp_path)
                if not err:
                    return f"檔名：\n{file.name}\n檔案內容：\n{content}\n\n"
                else:
                    print(f"Error extracting content from {file.name}: {err}")
            finally:
                # Clean up temporary file
                if temp_path and os.path.exists(temp_path):
                    os.unlink(temp_path)
        else:
            print(f"Could not retrieve file {file.id} for user {user_id}")
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"Error processing file {file.name}: {str(e)}")
        # Make sure to clean up temp file even if an error occurs
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
    return f"檔名：\n{file.name}\n"


async def get_doc_content(file_path: str) -> tuple[str, str]:
    """獲取文件內容，並確保正確處理 MIME 類型"""
    file_name = os.path.basename(file_path)

    # 1. 先嘗試使用 mimetypes
    file_mime = mimetypes.guess_type(file_path)[0]

    # 2. 如果 mimetypes 返回 None，使用擴展名映射
    if file_mime is None:
        ext = os.path.splitext(file_path)[1].lower()
        mime_map = {
            ".txt": "text/plain",
            ".pdf": "application/pdf",
            ".doc": "application/msword",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".xls": "application/vnd.ms-excel",
            ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".ppt": "application/vnd.ms-powerpoint",
            ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            ".csv": "text/csv",
            ".json": "application/json",
            ".xml": "application/xml",
            ".html": "text/html",
            ".htm": "text/html",
        }
        file_mime = mime_map.get(ext)

    try:
        content = await handle_file_upload(file_name, file_path, file_mime)
        return "", content
    except UnsupportedFileException as e:
        return f"目前不支援這個檔案類型: {file_mime}", ""
    except FailedToExtractContentException as e:
        return f"無法從檔案 {file_name} 取得內容", ""
    except HandlePowerpointError as e:
        return f"無法處理 PowerPoint 文件: {str(e)}", ""


# Process all files concurrently
async def process_all_files(user_id: str, hatch: Hatch):
    results = []
    for file in hatch.files:
        result = await process_file(user_id, file)
        results.append(result)
    return "".join(results)
