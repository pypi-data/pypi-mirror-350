from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, Any, List
from .request_types import *
from ..storage.json_file import load_models_from_json, save_models_to_json
from loguru import logger
from .auth import verify_token, JWT_SECRET, JWT_ALGORITHM
from fastapi import Depends
from ..storage.json_file import *
import asyncio
import subprocess
import traceback
from autocoder import models as autocoder_models

router = APIRouter()

# Load supported models from JSON file
supported_models = b_load_models_from_json()

# If the JSON file is empty or doesn't exist, use the default models
if not supported_models:
    supported_models = {}
    b_save_models_to_json(supported_models)


def deploy_command_to_string(cmd: DeployCommand) -> str:
    base_cmd = f"byzerllm deploy --pretrained_model_type {cmd.pretrained_model_type} "
    base_cmd += f"--cpus_per_worker {cmd.cpus_per_worker} --gpus_per_worker {cmd.gpus_per_worker} "
    base_cmd += f"--num_workers {cmd.num_workers} "

    if cmd.worker_concurrency:
        base_cmd += f"--worker_concurrency {cmd.worker_concurrency} "

    if cmd.infer_params:
        base_cmd += "--infer_params "
        for key, value in cmd.infer_params.items():
            base_cmd += f"""{key}="{value}" """

    base_cmd += f"--model {cmd.model}"

    if cmd.model_path:
        base_cmd += f" --model_path {cmd.model_path}"

    if cmd.infer_backend:
        base_cmd += f" --infer_backend {cmd.infer_backend}"

    return base_cmd


@router.get("/models", response_model=List[ModelInfo])
async def list_models():
    """List all supported models and their current status."""
    models = await load_models_from_json() or supported_models
    return [
        ModelInfo(
            name=name, 
            status=info["status"],
            product_type=info.get("product_type", ProductType.pro)
        )
        for name, info in models.items()
    ]


@router.delete("/models/{model_name}")
async def delete_model(model_name: str):
    """Delete a model from the supported models list."""
    models = await load_models_from_json() or supported_models
    if model_name not in models:
        raise HTTPException(
            status_code=404, detail=f"Model {model_name} not found")

    # 获取模型信息
    model_info = models[model_name]
    product_type = model_info.get("product_type", ProductType.pro)
    
    # 如果是 pro 模式，检查模型是否在运行
    if product_type == ProductType.pro and model_info["status"] == "running":
        raise HTTPException(
            status_code=400, detail="Cannot delete a running model")
    
    # 如果是 lite 模式，尝试从 autocoder 中删除
    if product_type == ProductType.lite:
        try:
            autocoder_models.delete_model(model_name)
        except Exception as e:
            logger.error(f"Failed to delete model from autocoder: {str(e)}")
            # 继续删除本地记录，即使 autocoder 删除失败

    # 删除模型记录
    del models[model_name]
    await save_models_to_json(models)
    return {"message": f"Model {model_name} deleted successfully"}


@router.post("/models/add")
async def add_model(model: AddModelRequest):
    """Add a new model to the supported models list."""
    if model.product_type == ProductType.lite:
        # Lite mode: use auto-coder's model management        
        try:
            autocoder_models.add_and_activate_models([{
                "name": model.name,
                "description": f"Auto created by William Toolbox",
                "model_name": model.infer_params.get("saas.model", ""),
                "model_type": model.pretrained_model_type,
                "base_url": model.infer_params.get("saas.base_url", ""),
                "api_key": model.infer_params.get("saas.api_key", ""),
                "is_reasoning": model.is_reasoning or False,
                "input_price": model.input_price or 0.0,
                "output_price": model.output_price or 0.0,
                "average_speed": 0.0
            }])
            
            # 创建一个与 pro 模式结构一致的模型记录，标记为 lite 模式
            models = await load_models_from_json() or supported_models
            models[model.name] = {
                "status": "running",  # lite 模式下默认为运行状态
                "product_type": ProductType.lite,
                "is_reasoning": model.is_reasoning or False,
                "input_price": model.input_price or 0.0,
                "output_price": model.output_price or 0.0,
                "deploy_command": DeployCommand(
                    pretrained_model_type=model.pretrained_model_type,
                    cpus_per_worker=model.cpus_per_worker,
                    gpus_per_worker=model.gpus_per_worker,
                    num_workers=model.num_workers,
                    worker_concurrency=model.worker_concurrency,
                    infer_params=model.infer_params,
                    model=model.name,
                    model_path=model.model_path,
                    infer_backend=model.infer_backend,
                ).model_dump(),
                "undeploy_command": f"byzerllm undeploy --model {model.name} --force",
            }
            await save_models_to_json(models)
            
            return {"message": f"Model {model.name} added successfully in Lite mode"}
        except Exception as e:
            logger.error(f"Failed to add model in Lite mode: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to add model in Lite mode: {str(e)}")
    else:
        # Pro mode: original logic
        models = await load_models_from_json() or supported_models
        if model.name in models:
            raise HTTPException(
                status_code=400, detail=f"Model {model.name} already exists"
            )

        if model.infer_backend == "saas":
            model.infer_backend = None

        new_model = {
            "status": "stopped",
            "product_type": "pro",
            "is_reasoning": model.is_reasoning or False,
            "input_price": model.input_price or 0.0,
            "output_price": model.output_price or 0.0,
            "deploy_command": DeployCommand(
                pretrained_model_type=model.pretrained_model_type,
                cpus_per_worker=model.cpus_per_worker,
                gpus_per_worker=model.gpus_per_worker,
                num_workers=model.num_workers,
                worker_concurrency=model.worker_concurrency,
                infer_params=model.infer_params,
                model=model.name,
                model_path=model.model_path,
                infer_backend=model.infer_backend,
            ).model_dump(),
            "undeploy_command": f"byzerllm undeploy --model {model.name} --force",
        }

        models[model.name] = new_model
        await save_models_to_json(models)
        return {"message": f"Model {model.name} added successfully in Pro mode"}


@router.get("/models/{model_name}")
async def get_model(model_name: str):
    """Get detailed information for a specific model."""
    models = await load_models_from_json()

    if model_name not in models:
        raise HTTPException(
            status_code=404, detail=f"Model {model_name} not found")

    return models[model_name]


@router.put("/models/{model_name}")
async def update_model(model_name: str, request: AddModelRequest):
    """Update an existing model."""
    models = await load_models_from_json()

    if model_name not in models:
        raise HTTPException(
            status_code=404, detail=f"Model {model_name} not found")

    model_info = models[model_name]
    if request.product_type == ProductType.pro and model_info['status'] == 'running':
        raise HTTPException(
            status_code=400,
            detail="Cannot update a running model in pro mode. Please stop it first."
        )

    if request.product_type == ProductType.lite:
        # Lite mode: use auto-coder's model management
        try:
            autocoder_models.update_model(model_name, {
                "name": model_name,
                "description": f"Updated by William Toolbox",
                "model_name": request.infer_params.get("saas.model", ""),
                "model_type": request.pretrained_model_type,
                "base_url": request.infer_params.get("saas.base_url", ""),
                "api_key": request.infer_params.get("saas.api_key", ""),
                "is_reasoning": request.is_reasoning or False,
                "input_price": request.input_price or 0.0,
                "output_price": request.output_price or 0.0
            })

            models = await load_models_from_json() or supported_models
            models[model_name] = {
                "status": "running",  # lite 模式下默认为运行状态
                "product_type": ProductType.lite,
                "is_reasoning": request.is_reasoning or False,
                "input_price": request.input_price or 0.0,
                "output_price": request.output_price or 0.0,
                "deploy_command": DeployCommand(
                    pretrained_model_type=request.pretrained_model_type,
                    cpus_per_worker=request.cpus_per_worker,
                    gpus_per_worker=request.gpus_per_worker,
                    num_workers=request.num_workers,
                    worker_concurrency=request.worker_concurrency,
                    infer_params=request.infer_params,
                    model=request.name,
                    model_path=request.model_path,
                    infer_backend=request.infer_backend,
                ).model_dump(),
                "undeploy_command": f"byzerllm undeploy --model {request.name} --force",
            }                                                
            await save_models_to_json(models)
            
            return {"message": f"Model {model_name} updated successfully in Lite mode"}
        except Exception as e:
            logger.error(f"Failed to update model in Lite mode: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to update model in Lite mode: {str(e)}")
    else:
        # Pro mode: original logic
        # Update the model's deploy command
        model_info['deploy_command'] = DeployCommand(
            pretrained_model_type=request.pretrained_model_type,
            cpus_per_worker=request.cpus_per_worker,
            gpus_per_worker=request.gpus_per_worker,
            num_workers=request.num_workers,
            worker_concurrency=request.worker_concurrency,
            infer_params=request.infer_params,
            model=model_name,
            model_path=request.model_path,
            infer_backend=request.infer_backend,
        ).model_dump()
        
        # Update product_type in model_info
        model_info['product_type'] = ProductType.pro
        model_info['is_reasoning'] = request.is_reasoning
        model_info['input_price'] = request.input_price
        model_info['output_price'] = request.output_price

        models[model_name] = model_info
        await save_models_to_json(models)

        return {"message": f"Model {model_name} updated successfully in Pro mode"}


@router.post("/models/{model_name}/{action}")
async def manage_model(model_name: str, action: str):
    """Start or stop a specified model."""
    models = await load_models_from_json() or supported_models
    if model_name not in models:
        raise HTTPException(
            status_code=404, detail=f"Model {model_name} not found")

    if action not in ["start", "stop"]:
        raise HTTPException(
            status_code=400, detail="Invalid action. Use 'start' or 'stop'"
        )
        
    # 检查是否是 lite 模式，lite 模式下不允许启动/停止
    model_info = models[model_name]
    if model_info.get("product_type") == ProductType.lite:
        raise HTTPException(
            status_code=400, 
            detail="Lite mode models cannot be started or stopped manually"
        )

    model_info = models[model_name]
    command = (
        deploy_command_to_string(DeployCommand(**model_info["deploy_command"]))
        if action == "start"
        else model_info["undeploy_command"]
    )

    try:
        # Execute the command asynchronously
        logger.info(f"manage model {model_name} with command: {command}")
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        # Check if the command was successful
        if process.returncode == 0:
            # Update model status only if the command was successful
            model_info["status"] = "running" if action == "start" else "stopped"
            models[model_name] = model_info

            # Save updated models to JSON file
            await save_models_to_json(models)

            return {
                "message": f"Model {model_name} {action}ed successfully",
                "output": stdout.decode(),
            }
        else:
            # If the command failed, raise an exception
            logger.error(
                f"Failed to {action} model: {stderr.decode() or stdout.decode()}")
            traceback.print_exc()
            raise subprocess.CalledProcessError(
                process.returncode, command, stdout.decode(), stderr.decode()
            )
    except subprocess.CalledProcessError as e:
        # If an exception occurred, don't update the model status
        error_message = f"Failed to {action} model: {e.stderr or e.stdout}"
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=error_message)


@router.get("/models/{model_name}/status")
async def get_model_status(model_name: str):
    """Get the status of a specified model."""
    models = await load_models_from_json() or supported_models
    if model_name not in models:
        raise HTTPException(
            status_code=404, detail=f"Model {model_name} not found")

    try:
        # Execute the byzerllm stat command
        command = (
            models[model_name]["status_command"]
            if model_name in models
            and "status_command" in models[model_name]
            else f"byzerllm stat --model {model_name}"
        )
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        # Check the result status
        if process.returncode == 0:
            status_output = stdout.decode().strip()
            models[model_name]["status"] = "running"
            await save_models_to_json(models)
            return {"model": model_name, "status": status_output, "success": True}
        else:
            error_message = f"Command failed with return code {process.returncode}: {stderr.decode().strip()}"
            models[model_name]["status"] = "stopped"
            await save_models_to_json(models)
            return {
                "model": model_name,
                "status": "error",
                "error": error_message,
                "success": False,
            }
    except Exception as e:
        error_message = f"Failed to get status for model {model_name}: {str(e)}"
        return {
            "model": model_name,
            "status": "error",
            "error": error_message,
            "success": False,
        }
