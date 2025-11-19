"""
FastAPI application entry point for Y2K Shopping Website
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Import routers
from app.routes import products, artists, analytics, exports
# from app.routes import auth, cart, orders  # Uncomment as you create them

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=False,  # Must be False when using wildcard origins
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Welcome to Y2K Shopping API",
        "status": "online",
        "docs": f"{settings.API_V1_STR}/docs"
    }


@app.get(f"{settings.API_V1_STR}/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}


# Include routers
app.include_router(products.router, prefix=f"{settings.API_V1_STR}/products", tags=["products"])
app.include_router(artists.router, prefix=f"{settings.API_V1_STR}/artists", tags=["artists"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])
app.include_router(exports.router, prefix=f"{settings.API_V1_STR}/exports", tags=["exports"])
# app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
# app.include_router(cart.router, prefix=f"{settings.API_V1_STR}/cart", tags=["cart"])
# app.include_router(orders.router, prefix=f"{settings.API_V1_STR}/orders", tags=["orders"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (development only)
    )
