from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, Any
import os
import json
import uuid
import asyncio
from datetime import datetime
from openai import AsyncOpenAI
from loguru import logger
from pydantic import BaseModel
from .request_types import *
from ..storage.json_file import *
import aiofiles
import traceback
from byzerllm.utils.client import code_utils
from autocoder.utils.stream_thinking import stream_with_thinking_async, separate_stream_thinking_async

router = APIRouter()

class AskRequest(BaseModel):
    message: str

@router.post("/chat/ask")
async def ask(request: AskRequest):
    try:
        # 加载配置
        config = await load_config()
        
        # 获取模型列表
        models = await load_models_from_json()
        if not models:
            raise HTTPException(status_code=404, detail="No models available")
            
        # 获取第一个运行中的模
        first_model = None
        for model in models.keys():
            if models[model]["status"] == "running":
                first_model = model
                break

        if not first_model:
            raise HTTPException(status_code=404, detail="No running models available")
            
        # 获取OpenAI服务配置
        openai_server = config.get("openaiServerList", [{}])[0]
        host = openai_server.get("host", "localhost")
        port = openai_server.get("port", 8000)
        if host == "0.0.0.0":
            host = "127.0.0.1"

        base_url = f"http://{host}:{port}/v1"
        client = AsyncOpenAI(base_url=base_url, api_key="xxxx")

        # 调用模型
        response = await client.chat.completions.create(
            model=first_model,
            messages=[{"role": "user", "content": request.message}],
            stream=False,
            max_tokens=4096
        )

        return {"response": response.choices[0].message.content}
        
    except Exception as e:
        logger.error(f"Error in ask endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/conversations")
async def get_conversation_list(username: str):
    chat_data = await load_chat_data(username)
    conversation_list = []
    
    for conv in chat_data["conversations"]:
        title = conv["title"]
        
        # If title is empty or default, use first user message as title
        if not title or title == "新的聊天":
            # Find the first user message
            for msg in conv["messages"]:
                if msg["role"] == "user" and msg["content"]:
                    # Truncate message if too long (30 characters max)
                    title = msg["content"][:30] + ("..." if len(msg["content"]) > 30 else "")
                    break
        
        conversation_list.append({
            "id": conv["id"],
            "title": title,
            "time": conv["updated_at"].split("T")[0],  # Format date to YYYY-MM-DD
            "messages": len(conv["messages"]),
            "created_at": conv["created_at"],
            "updated_at": conv["updated_at"],
        })
    
    # Sort conversations by updated_at in descending order (newest first)
    conversation_list.sort(key=lambda x: x["updated_at"], reverse=True)
    return conversation_list

@router.post("/chat/conversations", response_model=Conversation)
async def create_conversation(username: str, request: CreateConversationRequest):
    chat_data = await load_chat_data(username)
    new_conversation = Conversation(
        id=str(uuid.uuid4()),
        title=request.title,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
        messages=[],
    )
    chat_data["conversations"].append(new_conversation.model_dump())
    await save_chat_data(username, chat_data)
    return new_conversation

@router.get("/chat/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(username: str, conversation_id: str):
    chat_data = await load_chat_data(username)
    conversation = next(
        (conv for conv in chat_data["conversations"] if conv["id"] == conversation_id),
        None,
    )
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.post(
    "/chat/conversations/{conversation_id}/messages/stream",
    response_model=AddMessageResponse,
)
async def add_message_stream(username: str, conversation_id: str, request: AddMessageRequest):
    request_id = str(uuid.uuid4())

    chat_data = await load_chat_data(username)
    conversation = next(
        (conv for conv in chat_data["conversations"] if conv["id"] == conversation_id),
        None,
    )
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Replace the entire conversation messages with the full message history
    conversation["messages"] = [msg.model_dump() for msg in request.messages]
    await save_chat_data(username, chat_data)
    response_message_id = str(uuid.uuid4())

    asyncio.create_task(
        process_message_stream(
            username, request_id, request, conversation, response_message_id, chat_data=chat_data
        )
    )

    return AddMessageResponse(
        request_id=request_id, response_message_id=response_message_id
    )


@router.get(
    "/chat/conversations/events/{request_id}/{index}", response_model=EventResponse
)
async def get_message_events(request_id: str, index: int):
    file_path = await get_event_file_path(request_id)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404, detail=f"No events found for request_id: {request_id}"
        )

    events = []
    if not os.path.exists(file_path):
        return EventResponse(events=[])

    with open(file_path, "r") as f:
        for line in f:
            event = json.loads(line)
            if event["index"] >= index:
                events.append(event)

    return EventResponse(events=events)


async def process_message_stream(
    username: str,
    request_id: str,
    request: AddMessageRequest,
    conversation: Conversation,
    response_message_id: str,
    chat_data: ChatData,
):
    file_path = await get_event_file_path(request_id)
    idx = 0
    thoughts = []
    async with aiofiles.open(file_path, "w") as event_file:
        try:
            config = await load_config()
            if request.list_type == "models":
                model_name = request.selected_item
                models = await load_models_from_json()                
                # 获取模型信息
                model_info = models[model_name]
                product_type = model_info.get("product_type", "pro")

                if product_type == "pro":
                    openai_server = config.get("openaiServerList", [{}])[0]
                    
                    host = openai_server.get("host", "localhost")
                    port = openai_server.get("port", 8000)
                    if host == "0.0.0.0":
                        host = "127.0.0.1"

                    base_url = f"http://{host}:{port}/v1"
                    api_key = "xxxx"
                    real_model_name = model_name
                elif product_type == "lite":
                    base_url = model_info["deploy_command"]["infer_params"].get("saas.base_url", "")
                    api_key = model_info["deploy_command"]["infer_params"].get("saas.api_key", "")
                    real_model_name = model_info["deploy_command"]["infer_params"].get("saas.model", "")

                client = AsyncOpenAI(base_url=base_url, api_key=api_key)

                response = await client.chat.completions.create(
                    model=real_model_name,
                    messages=[
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in conversation["messages"]
                    ],
                    stream=True,
                    max_tokens=4096,
                    extra_body={"request_id":request_id},
                )
                
                thinking_gen,content_gen = await separate_stream_thinking_async(response)
                async for chunk in thinking_gen:
                    if chunk:
                        event = {
                            "index": idx,
                            "event": "stream_thought",
                            "content": chunk,
                            "timestamp": datetime.now().isoformat(),
                        }
                        await event_file.write(
                            json.dumps(event, ensure_ascii=False) + "\n"
                        )
                        await event_file.flush()
                        idx += 1

                async for chunk in content_gen:
                    if chunk:
                        event = {
                            "index": idx,
                            "event": "chunk",
                            "content": chunk,
                            "timestamp": datetime.now().isoformat(),
                        }
                        await event_file.write(
                            json.dumps(event, ensure_ascii=False) + "\n"
                        )
                        await event_file.flush()
                        idx += 1 

            elif request.list_type == "super-analysis":
                super_analyses = await load_super_analysis_from_json()
                analysis_info = super_analyses.get(request.selected_item, {})
                host = analysis_info.get("host", "localhost")
                port = analysis_info.get("port", 8000)
                if host == "0.0.0.0":
                    host = "127.0.0.1"

                base_url = f"http://{host}:{port}/v1"

                logger.info(f"Super Analysis {request.selected_item} is using {base_url}")
                
                client = AsyncOpenAI(base_url=base_url, api_key="xxxx")
                response = await client.chat.completions.create(
                    model=analysis_info.get("served_model_name", "default"),
                    messages=[
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in conversation["messages"]
                    ],
                    stream=True,
                    max_tokens=8096,
                    extra_body={"request_id":request_id},
                )
                thinking_gen,content_gen = await separate_stream_thinking_async(response)
                async for chunk in thinking_gen:
                    if chunk:
                        event = {
                            "index": idx,
                            "event": "stream_thought",
                            "content": chunk,
                            "timestamp": datetime.now().isoformat(),
                        }
                        await event_file.write(
                            json.dumps(event, ensure_ascii=False) + "\n"
                        )
                        await event_file.flush()
                        idx += 1

                async for chunk in content_gen:
                    if chunk:
                        event = {
                            "index": idx,
                            "event": "chunk",
                            "content": chunk,
                            "timestamp": datetime.now().isoformat(),
                        }
                        await event_file.write(
                            json.dumps(event, ensure_ascii=False) + "\n"
                        )
                        await event_file.flush()
                        idx += 1        

            elif request.list_type == "rags":
                rags = await load_rags_from_json()
                rag_info = rags.get(request.selected_item, {})
                host = rag_info.get("host", "localhost")
                port = rag_info.get("port", 8000)
                if host == "0.0.0.0":
                    host = "127.0.0.1"

                base_url = f"http://{host}:{port}/v1"

                logger.info(f"RAG {request.selected_item} is using {base_url}")
                inference_deep_thought = rag_info.get(
                    "inference_deep_thought", "False"
                ) in ["True", "true", True]

                client = AsyncOpenAI(base_url=base_url, api_key="xxxx")
                
                extra_body = {}
                if "only_contexts" in request.extra_metadata and request.extra_metadata["only_contexts"]:
                    extra_body = {
                        "extra_body": {
                            "only_contexts": True
                        }
                    }

                response = await client.chat.completions.create(
                    model=rag_info.get("model", "deepseek_chat"),
                    messages=[
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in conversation["messages"]
                    ],
                    stream=True,
                    max_tokens=8096,
                    extra_body={
                        **extra_body
                    },
                )
                if not inference_deep_thought:                    
                    thinking_gen,content_gen = await separate_stream_thinking_async(response)
                    async for chunk in thinking_gen:
                        if chunk:
                            event = {
                                "index": idx,
                                "event": "thought",
                                "content": chunk,
                                "timestamp": datetime.now().isoformat(),
                            }
                            await event_file.write(
                                json.dumps(event, ensure_ascii=False) + "\n"
                            )
                            await event_file.flush()

                            idx += 1
                    async for chunk in content_gen:
                        if chunk:
                            event = {
                                "index": idx,
                                "event": "chunk",                                
                                "content": chunk,
                                "timestamp": datetime.now().isoformat(),
                            }
                            await event_file.write(
                                json.dumps(event, ensure_ascii=False) + "\n"
                            )
                            await event_file.flush()

                            idx += 1
                else:                    
                    index = 0
                    is_in_thought = True
                    client = AsyncOpenAI(base_url=base_url, api_key="xxxx")
                    counter = 0
                    while is_in_thought and counter < 60:                        
                        round_response = await client.chat.completions.create(
                            model=rag_info.get("model", "deepseek_chat"),
                            messages=[
                                {
                                    "role": "user",
                                    "content": json.dumps(
                                        {"request_id": request_id, "index": index},
                                        ensure_ascii=False,
                                    ),
                                }
                            ],
                            stream=True,
                            max_tokens=8096                            
                        )
                        result = ""
                        async for chunk in round_response:
                            v = chunk.choices[0].delta.content
                            if v is not None:
                                result += v
                        logger.info(f"result: {result}")                                
                        evts = json.loads(result)
                        if not evts["events"]:
                            await asyncio.sleep(1)
                            counter += 1
                            continue
                        counter = 0
                        for evt in evts["events"]:                            
                            if evt["event_type"] == "thought":
                                thoughts.append(evt["content"])
                                event = {
                                    "index": idx,
                                    "event": "thought",
                                    "content": evt["content"],
                                    "timestamp": datetime.now().isoformat(),
                                }
                                await event_file.write(
                                    json.dumps(event, ensure_ascii=False) + "\n"
                                )
                                await event_file.flush()                            
                                idx += 1
                            if evt["event_type"] == "chunk" or evt["event_type"] == "done":
                                is_in_thought = False
                            index += 1  
                    asyncio.sleep(1)                                 

                    async for chunk in response:
                        if chunk.choices[0].delta.content:
                            event = {
                                "index": idx,
                                "event": "chunk",
                                "content": chunk.choices[0].delta.content,
                                "timestamp": datetime.now().isoformat(),
                            }
                            await event_file.write(
                                json.dumps(event, ensure_ascii=False) + "\n"
                            )
                            await event_file.flush()

                            idx += 1

        except Exception as e:
            # Add error event
            error_event = {
                "index": idx,
                "event": "error",
                "content": str(e),
                "timestamp": datetime.now().isoformat(),
            }
            await event_file.write(json.dumps(error_event, ensure_ascii=False) + "\n")
            await event_file.flush()
            logger.error(traceback.format_exc())

        await event_file.write(
            json.dumps(
                {
                    "index": idx,
                    "event": "done",
                    "content": "",
                    "timestamp": datetime.now().isoformat(),
                },
                ensure_ascii=False,
            )
            + "\n"
        )
        await event_file.flush()

    s = ""
    async with aiofiles.open(file_path, "r") as event_file:
        async for line in event_file:
            event = json.loads(line)
            if event["event"] == "chunk":
                s += event["content"]

    # Add the assistant's response to the messages list
    conversation["messages"] = [msg.model_dump() for msg in request.messages] + [
        {
            "id": response_message_id,
            "role": "assistant",
            "content": s,
            "timestamp": datetime.now().isoformat(),
            "thoughts": thoughts,
        }
    ]
    await save_chat_data(username, chat_data)


@router.put("/chat/conversations/{conversation_id}")
async def update_conversation(username: str, conversation_id: str, request: Conversation):
    """Update an existing conversation with new data."""
    chat_data = await load_chat_data(username)

    # Find and update the conversation
    for conv in chat_data["conversations"]:
        if conv["id"] == conversation_id:
            logger.info(f"Updating conversation {conversation_id}")
            conv.update(
                {
                    "title": request.title,
                    "messages": [msg.model_dump() for msg in request.messages],
                    "updated_at": datetime.now().isoformat(),
                }
            )
            await save_chat_data(username, chat_data)
            return conv

    raise HTTPException(status_code=404, detail="Conversation not found")


@router.put("/chat/conversations/{conversation_id}/title")
async def update_conversation_title(username: str, conversation_id: str, request: UpdateTitleRequest):
    """Update only the title of an existing conversation."""
    chat_data = await load_chat_data(username)

    # Find and update the conversation title
    for conv in chat_data["conversations"]:
        if conv["id"] == conversation_id:
            logger.info(f"Updating title for conversation {conversation_id}")
            conv["title"] = request.title
            conv["updated_at"] = datetime.now().isoformat()
            await save_chat_data(username, chat_data)
            return {"message": "Title updated successfully", "title": request.title}

    raise HTTPException(status_code=404, detail="Conversation not found")


class ExtractCSVRequest(BaseModel):
    content: str

@router.post("/chat/extract_csv")
async def extract_csv(request: ExtractCSVRequest):
    """Extract CSV content from markdown code block"""
    try:
        code_blocks = code_utils.extract_code(request.content)
        for code_block in code_blocks:
            if code_block[0] == "csv":
                return {"csv_content": code_block[1]}
        return {"csv_content": ""}
    except Exception as e:
        logger.error(f"Failed to extract CSV: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to extract CSV content")

@router.delete("/chat/conversations/{conversation_id}")
async def delete_conversation(username: str, conversation_id: str):
    chat_data = await load_chat_data(username)
    chat_data["conversations"] = [
        conv for conv in chat_data["conversations"] if conv["id"] != conversation_id
    ]
    await save_chat_data(username, chat_data)
    return {"message": "Conversation deleted successfully"}
