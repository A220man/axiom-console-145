from fastapi import APIRouter

# Import controllers from the correct location
from api.controllers.health_controller import router as health_router
from api.controllers.models_controller import router as models_router
from api.controllers.keys_controller import router as keys_router

# Create main V1 router
router = APIRouter()

# Include all sub-routers
router.include_router(health_router, prefix="/health")
router.include_router(models_router, prefix="/models")
router.include_router(keys_router, prefix="/keys")

