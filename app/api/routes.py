from fastapi import APIRouter, HTTPException, status
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse, RecommendationItem
from app.services.vector_store import vector_store

router = APIRouter(tags=["Academic Advising Recommendations"])


@router.post("/recommend-reply", response_model=RecommendationResponse)
def recommend_reply(payload: RecommendationRequest):
    # التحقق من أن النص ليس مسافات فارغة فقط
    clean_message = payload.student_message.strip()
    if not clean_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student message cannot be empty or blank space."
        )

    try:
        results = vector_store.search_similar_regulations(
            query=clean_message,
            top_k=payload.top_k
        )

        recommendations = []
        if results and results.get("ids") and len(results["ids"][0]) > 0:
            ids = results["ids"][0]
            metadatas = results["metadatas"][0]
            distances = results["distances"][0] if "distances" in results and results["distances"] else [0.0] * len(ids)

            for i in range(len(ids)):
                # تحويل المسافة (Distance) إلى نسبة تشابه (Similarity Score)
                distance = distances[i]
                similarity_score = round(max(0.0, 1.0 - (distance / 2.0)), 4)

                meta = metadatas[i]
                recommendations.append(
                    RecommendationItem(
                        id=ids[i],
                        title=meta.get("title", ""),
                        category=meta.get("category", ""),
                        recommended_reply=meta.get("recommended_reply", ""),
                        similarity_score=similarity_score
                    )
                )

        return RecommendationResponse(
            student_message=clean_message,
            recommendations=recommendations
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing recommendation: {str(e)}"
        )