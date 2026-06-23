from fastapi import FastAPI
from app.route.issues import router as issues_router
from app.middleware.timer import timing_middleware

app = FastAPI()

app.middleware("http")(timing_middleware)

app.include_router(issues_router)



    