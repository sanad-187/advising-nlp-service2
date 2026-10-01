from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="Advising NLP Service",
    description="API for Academic Advising RAG Recommendation System",
    version="1.0.0"
)

# تفعيل CORS للربط مع واجهة المستخدم Frontend (Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تضمين مسارات النظام
app.include_router(router)


@app.get("/", tags=["General"])
def root(request: Request):
    return {
        "message": "Welcome to Academic Advising NLP Service",
        "docs_url": f"{request.base_url}docs"
    }


@app.get("/health", tags=["General"])
def health_check():
    return {"status": "healthy", "service": "advising-nlp-service"}