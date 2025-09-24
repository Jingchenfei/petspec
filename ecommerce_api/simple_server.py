#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uvicorn
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import time
import traceback

# Configure logging
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger("simple_server")

logger = setup_logging()

# Initialize FastAPI app
app = FastAPI()

# Mock product description generator
class ProductInfo(BaseModel):
    product_name = None
    product_category = None
    key_features = []
    target_audience = None
    style = "professional"
    language = "zh"
    version_count = 1

# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "version": "1.0",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

# Root endpoint
@app.get("/")
def root():
    return {"message": "API is running"}

# Mock generate description endpoint
@app.post("/generate-description")
def generate_description(request):
    try:
        logger.info("Received request for: %s" % request.product_name)
        # Simple mock response without model loading
        descriptions = ["This is a sample description for %s. It has features: %s. Targeting: %s. Style: %s." % (request.product_name, ', '.join(request.key_features), request.target_audience, request.style)]
        return {
            "request_id": "mock_req_123",
            "descriptions": descriptions,
            "generation_time": 0.5
        }
    except Exception as e:
        logger.error("Error: %s" % str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    try:
        # Get environment variables with defaults
        host = os.getenv('APP_HOST', '0.0.0.0')
        port = int(os.getenv('APP_PORT', '9000'))
        
        logger.info("Starting server on %s:%s" % (host, port))
        # Start uvicorn server
        uvicorn.run(
            "simple_server:app",
            host=host,
            port=port,
            reload=False,
            log_level="info"
        )
    except Exception as e:
        logger.critical("Server failed to start: %s" % str(e))
        traceback.print_exc()