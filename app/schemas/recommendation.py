from pydantic import BaseModel, Field
from typing import List, Optional


class RecommendationRequest(BaseModel):
    student_message: str = Field(..., min_length=3, description="رسالة الطالب أو الاستفسار الأكاديمي")
    top_k: Optional[int] = Field(default=3, ge=1, le=5, description="عدد التوصيات المطلوبة")


class RecommendationItem(BaseModel):
    id: str
    title: str
    category: str
    recommended_reply: str
    similarity_score: float


class RecommendationResponse(BaseModel):
    student_message: str
    recommendations: List[RecommendationItem]