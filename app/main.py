from api import router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Incoming request: {request.method} {request.url}")
    logger.debug(f"Request headers: {dict(request.headers)}")

    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"Completed request: {request.method} {request.url} "
            f"status_code={response.status_code} process_time={process_time:.3f}s"
        )
        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error"}
        )
        
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("FastAPIApp")
app.mount("/static", StaticFiles(directory="./static"), name="static")
app.include_router(router)