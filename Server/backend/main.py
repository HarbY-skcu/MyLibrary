from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FastAPI Auth Boilerplate",
    description="Simple authentication API with hexagonal architecture",
    version="1.0.0",
)

# Configure CORS - Must be BEFORE including routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods including OPTIONS
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],
)

# register all routers from the service routes
# app.include_router(example_router)