import json
import os
import chromadb
from sentence_transformers import SentenceTransformer

# تحديد مسارات المشروع ديناميكياً
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

DATA_PATH = os.path.join(BASE_DIR, "data", "regulations.json")
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")


class VectorStoreManager:
    def __init__(self):
        # تحميل النموذج متعدد اللغات الداعم للغة العربية
        print("Loading Multilingual Sentence-Transformer model...")
        self.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        
        # تهيئة ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.collection = self.chroma_client.get_or_create_collection(name="regulations")
        
        # ملء قاعدة البيانات باللوائح إذا كانت فارغة
        if self.collection.count() == 0:
            self._initialize_database()

    def _initialize_database(self):
        """قراءة اللوائح وحفظ التضمينات الاتجاهية داخل ChromaDB"""
        print("Initializing Vector Database with regulations...")
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"Regulations file not found at: {DATA_PATH}")

        with open(DATA_PATH, "r", encoding="utf-8") as f:
            regulations = json.load(f)

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for reg in regulations:
            reg_id = str(reg["id"])
            combined_text = f"{reg.get('title', '')} - {reg.get('content_en', '')} - {reg.get('content_ar', '')}"
            vector = self.model.encode(combined_text).tolist()

            ids.append(reg_id)
            documents.append(combined_text)
            embeddings.append(vector)
            metadatas.append({
                "title": reg.get("title", ""),
                "category": reg.get("category", ""),
                "recommended_reply": reg.get("recommended_reply", "")
            })

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
        print(f"Successfully added {len(ids)} regulations to ChromaDB!")

    def search_similar_regulations(self, query: str, top_k: int = 3):
        """البحث عن أكثر اللوائح تشابهاً مع سؤال الطالب"""
        query_vector = self.model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=top_k
        )
        return results


# كائن منفرد للاستخدام في التطبيق
vector_store = VectorStoreManager()