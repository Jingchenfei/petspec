from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
def root():
    return {"message": "Hello World"}

@app.get('/health')
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    print("Starting minimal FastAPI server...")
    uvicorn.run(
        "test_fastapi:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )