import asyncio
from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import AsyncGenerator, Optional

import uvicorn
import uvloop
from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.datastructures import State

from vajra.config import ModelConfig
from vajra.engine.inference_engine import InferenceEngine
from vajra.entrypoints.openai.api_server_engine import ApiServerEngine
from vajra.entrypoints.openai.config import OpenAIServerConfig
from vajra.entrypoints.openai.protocol import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    CompletionRequest,
    ErrorResponse,
)
from vajra.entrypoints.openai.serving_chat import OpenAIServingChat
from vajra.entrypoints.openai.serving_completion import OpenAIServingCompletion
from vajra.logger import init_logger

TIMEOUT_KEEP_ALIVE = 5  # seconds

logger = init_logger(__name__)

shutdown_event = asyncio.Event()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Entering lifespan context manager")
    try:
        yield
    finally:
        # Signal shutdown to all components
        shutdown_event.set()
        # Wait a moment for cleanup
        await asyncio.sleep(0.1)
        # Ensure app state including engine ref is gc'd
        if hasattr(app, "state"):
            del app.state
        logger.info("Exiting lifespan context manager")


router = APIRouter()


def chat(request: Request) -> Optional[OpenAIServingChat]:
    return request.app.state.openai_serving_chat


def completion(request: Request) -> Optional[OpenAIServingCompletion]:
    return request.app.state.openai_serving_completion


def engine(request: Request) -> Optional[ApiServerEngine]:
    return request.app.state.engine


@router.get("/v1/models")
async def show_available_models(raw_request: Request):
    logger.info("Received request to show available models")
    handler = chat(raw_request)
    assert handler is not None

    models_ = await handler.show_available_models()
    return JSONResponse(content=models_.model_dump())


@router.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest, raw_request: Request):
    logger.info("Received request to create chat completion")
    handler = chat(raw_request)
    assert handler is not None

    generator = await handler.create_chat_completion(request, raw_request)
    if isinstance(generator, ErrorResponse):
        return JSONResponse(content=generator.model_dump(), status_code=generator.code)
    if request.stream:
        assert isinstance(generator, AsyncGenerator)
        return StreamingResponse(content=generator, media_type="text/event-stream")
    else:
        assert isinstance(generator, ChatCompletionResponse)
        return JSONResponse(content=generator.model_dump())


@router.post("/v1/completions")
async def create_completion(request: CompletionRequest, raw_request: Request):
    logger.info("Received request to create completion")
    handler = completion(raw_request)
    assert handler is not None

    generator = await handler.create_completion(request, raw_request)
    if isinstance(generator, ErrorResponse):
        return JSONResponse(content=generator.model_dump(), status_code=generator.code)
    if request.stream:
        assert isinstance(generator, AsyncGenerator)
        return StreamingResponse(content=generator, media_type="text/event-stream")
    else:
        assert isinstance(generator, ChatCompletionResponse)
        return JSONResponse(content=generator.model_dump())


def build_app(config: OpenAIServerConfig) -> FastAPI:
    logger.info("Building FastAPI app")
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_, exc):
        err = ErrorResponse(
            message=str(exc), type="BadRequestError", code=HTTPStatus.BAD_REQUEST
        )
        return JSONResponse(err.model_dump(), status_code=HTTPStatus.BAD_REQUEST)

    if not config.api_key:
        logger.warning("API key is not set. API server will be open to all requests")
        return app

    @app.middleware("http")
    async def authentication(request: Request, call_next):
        root_path = "" if config.server_root_path is None else config.server_root_path
        if request.method == "OPTIONS":
            return await call_next(request)
        if not request.url.path.startswith(f"{root_path}/v1"):
            return await call_next(request)

        api_key = config.api_key or ""  # Convert None to empty string if needed
        if request.headers.get("Authorization") != f"Bearer {api_key}":
            return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
        return await call_next(request)

    return app


async def init_app_state(
    engine: ApiServerEngine,
    model_config: ModelConfig,
    state: State,
    config: OpenAIServerConfig,
) -> None:
    logger.info("Initializing app state")
    served_model_names = [model_config.model]

    state.engine = engine

    state.openai_serving_chat = OpenAIServingChat(
        engine,
        model_config,
        served_model_names,
        config.response_role,
        config.chat_template,
    )
    state.openai_serving_completion = OpenAIServingCompletion(
        engine, model_config, served_model_names
    )
    logger.info("Created OpenAIServingChat and OpenAIServingCompletion")


async def run_app(config: OpenAIServerConfig, **uvicorn_kwargs) -> None:
    logger.info("Launching OpenAI compatible server with config: %s", config)

    engine = InferenceEngine(config.inference_engine_config)
    server_engine = ApiServerEngine(engine)
    app = build_app(config)
    # TODO(Amey): Need to handle the case where we have multiple models
    model_config = engine.get_model_config()
    await init_app_state(server_engine, model_config, app.state, config)

    uv_config = uvicorn.Config(
        app,
        host=config.host,
        port=config.port,
        log_level=config.log_level,
        ssl_keyfile=config.ssl_keyfile,
        ssl_certfile=config.ssl_certfile,
        ssl_ca_certs=config.ssl_ca_certs,
        ssl_cert_reqs=config.ssl_cert_reqs,
        timeout_keep_alive=TIMEOUT_KEEP_ALIVE,
    )
    server = uvicorn.Server(uv_config)
    await server.serve()


if __name__ == "__main__":
    config: OpenAIServerConfig = OpenAIServerConfig.create_from_cli_args()
    logger.info("Starting server with configuration: %s", config)
    uvloop.install()
    asyncio.run(run_app(config))
