# Advising NLP Microservice 🎓

خدمة مصغرة معتمدة على FastAPI و RAG لمساعدة المرشدين الأكاديميين واقتراح ردود دقيقة بناءً على اللوائح الأكاديمية.

## 🚀 التشغيل المباشر

```powershell
# 1. تفعيل البيئة
.\venv\Scripts\Activate.ps1

# 2. تشغيل السيرفر
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload