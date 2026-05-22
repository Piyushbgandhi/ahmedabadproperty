

from middleware.security_middleware import (
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
    SQLInjectionProtectionMiddleware,
    XSSProtectionMiddleware,
    AdminIPWhitelistMiddleware,
    CSRFProtectionMiddleware
)
from routes.admin_routes import router as admin_router

# Add middlewares
app.add_middleware(RateLimitMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(SQLInjectionProtectionMiddleware)
app.add_middleware(XSSProtectionMiddleware)
app.add_middleware(AdminIPWhitelistMiddleware)
app.add_middleware(CSRFProtectionMiddleware)

# Include admin routes
api_router.include_router(admin_router)
