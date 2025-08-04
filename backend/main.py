from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from .routes import router

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="Reca11 Memory API",
    description="A lightweight open-source memory architecture for LLMs. Manage chat memory, summaries, and memory strands via simple endpoints.",
    version="1.0.0",
    contact={
        "name": "Reca11",
        "url": "https://github.com/shashvcode/reca11-memory",
        "email": "shashi.shekhar.s.verma@vanderbilt.edu",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

