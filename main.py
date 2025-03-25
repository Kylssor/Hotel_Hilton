from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from config.project_config import ProjectConfig
from domain.utils.seed import run_seed
from middlewares.exception_handler_middleware import ExceptionHandlerMiddleware
from domain.utils import singleton
from endpoints.routes import routers
from models.context.persistence_context import PersistenceContext

app = FastAPI()

@singleton
class AppCreator:
    def __init__(self):
        # set app default
        self.app = FastAPI(
            title=ProjectConfig.PROJECT_NAME(),
            version="0.0.1",
        )

        self.db_context = PersistenceContext(ProjectConfig().DATABASE_URI)
        run_seed(self.db_context)

        # set cors
        if ProjectConfig.BACKEND_CORS_ORIGINS():
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in ProjectConfig.BACKEND_CORS_ORIGINS()],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        #middlewares
        self.app.add_middleware(ExceptionHandlerMiddleware)

        # set routes
        @self.app.get("/")
        def root():
            return "service is working"

        self.app.include_router(
            routers,
            prefix=ProjectConfig.API_PREFIX()
        )


app_creator = AppCreator()
app = app_creator.app