from dotenv import load_dotenv
load_dotenv()
from config.server.conn import fastapi_instance as app
from config.socket.main import sio_app

app.mount("/", app=sio_app)


@app.get("/")
def read_root():
    return {"message": "FastAPI Audio Stream Server is Running!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=5000,
        log_level="info",
        reload=True
    )
