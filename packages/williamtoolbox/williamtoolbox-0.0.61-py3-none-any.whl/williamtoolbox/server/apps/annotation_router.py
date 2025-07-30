from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import uuid
import traceback
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List
from williamtoolbox.storage.json_file import load_file_resources, save_file_resources
from williamtoolbox.annotation import extract_text_from_docx, extract_annotations_from_docx, auto_generate_annotations
from datetime import datetime
from pydantic import BaseModel
import json
import aiofiles

router = APIRouter()


# 线程池用于处理阻塞操作
executor = ThreadPoolExecutor(max_workers=4)

# 确保上传目录存在
UPLOAD_DIR = Path("./data/upload")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

async def save_uploaded_file(file: UploadFile) -> str:
    """保存上传的文件并返回生成的UUID"""
    file_uuid = str(uuid.uuid4())
    file_path = UPLOAD_DIR / file_uuid
    
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        return file_uuid
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

@router.post("/api/annotations/upload")
async def upload_file(file: UploadFile, username: str):
    """上传文档接口"""
    file_uuid = await save_uploaded_file(file)
    
    # 保存文件资源信息
    file_resources = await load_file_resources()
    file_resources[file_uuid] = {
        "uuid": file_uuid,
        "path": str(UPLOAD_DIR / file_uuid),
        "username": username,
        "original_name": file.filename,
        "upload_time": str(datetime.now())
    }
    await save_file_resources(file_resources)
    
    return JSONResponse({
        "uuid": file_uuid,
        "message": "File uploaded successfully"
    })

@router.get("/api/annotations/document/{file_uuid}")
async def get_document_content(file_uuid: str):
    """获取文档内容和注释"""
    file_resources = await load_file_resources()
    if file_uuid not in file_resources:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path = file_resources[file_uuid]["path"]
    
    # 使用线程池处理阻塞操作
    loop = asyncio.get_event_loop()
    try:
        full_text = await loop.run_in_executor(
            executor, extract_text_from_docx, file_path
        )
        comments = await loop.run_in_executor(
            executor, extract_annotations_from_docx, file_path
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")
    
    return JSONResponse({
        "full_text": full_text,
        "comments": comments
    })

@router.get("/api/annotations/document/{file_uuid}/info")
async def get_document_info(file_uuid: str):
    """获取文档元信息"""
    file_resources = await load_file_resources()
    if file_uuid not in file_resources:
        raise HTTPException(status_code=404, detail="File not found")
    
    return JSONResponse(file_resources[file_uuid])

@router.post("/api/annotations/save_all")
async def save_all_annotations(file_uuid: str, annotations: List[Dict[str, Any]]):
    """保存文档的所有批注"""
    try:
        # 检查文件是否存在
        file_resources = await load_file_resources()
        if file_uuid not in file_resources:
            raise HTTPException(status_code=404, detail="File not found")
        
        file_path = file_resources[file_uuid]["path"]
        
        # 读取文档内容
        loop = asyncio.get_event_loop()
        doc_text = await loop.run_in_executor(
            executor, extract_text_from_docx, file_path
        )
        
        # 确保保存目录存在
        save_dir = Path("./data/annotations")
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # 构建保存数据
        save_data = {
            "doc_text": doc_text,
            "annotations": annotations
        }
        
        # 保存到文件
        save_path = save_dir / f"{file_uuid}.json"
        async with aiofiles.open(save_path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(save_data, ensure_ascii=False, indent=2))
            
        return JSONResponse({"message": "Annotations saved successfully"})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save annotations: {str(e)}")

from pydantic import BaseModel

class AutoGenerateAnnotationRequest(BaseModel):
    file_uuid: str
    rag_name: str
    model_name: str

@router.post("/api/annotations/auto_generate")
async def auto_generate_annotation(request: AutoGenerateAnnotationRequest):
    """自动生成文档批注"""
    file_resources = await load_file_resources()
    if request.file_uuid not in file_resources:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path = file_resources[request.file_uuid]["path"]
    
    try:
        # 读取文档内容
        loop = asyncio.get_event_loop()
        doc_text = await loop.run_in_executor(
            executor, extract_text_from_docx, file_path
        )
        
        # 调用自动生成批注
        result = await auto_generate_annotations(request.rag_name, doc_text, request.model_name)
        
        return JSONResponse({
            "doc_text": result.doc_text,
            "annotations": [
                {
                    "text": annotation.text,
                    "comment": annotation.comment,
                    "timestamp": annotation.timestamp if hasattr(annotation, "timestamp") else None
                }
                for annotation in result.annotations
            ]
        })
    except Exception as e:        
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to generate annotations: {str(e)}")