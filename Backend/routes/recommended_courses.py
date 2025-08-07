# app/recommender.py
from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer('all-MiniLM-L6-v2')

def recommend_courses_semantic(completed_titles, all_courses, top_n=5):
    try:
        if not all_courses:
            return []

        course_titles = list(all_courses.keys())
        course_texts = list(all_courses.values())

        # Encode all course descriptions
        course_embeddings = model.encode(course_texts, convert_to_tensor=True)

        if completed_titles:
            completed_indices = [
                course_titles.index(title) for title in completed_titles if title in course_titles
            ]
            if completed_indices:
                user_embedding = course_embeddings[completed_indices].mean(dim=0, keepdim=True)
                similarities = util.pytorch_cos_sim(user_embedding, course_embeddings)[0]
            else:
                similarities = util.pytorch_cos_sim(course_embeddings.mean(dim=0, keepdim=True), course_embeddings)[0]
        else:
            user_embedding = course_embeddings.mean(dim=0, keepdim=True)
            similarities = util.pytorch_cos_sim(user_embedding, course_embeddings)[0]

        # Filter and rank
        ranked = [
            (course_titles[i], float(similarities[i]))
            for i in range(len(course_titles))
            if course_titles[i] not in completed_titles
        ]
        ranked.sort(key=lambda x: -x[1])
        return [title for title, _ in ranked[:top_n]]

    except Exception as e:
        print(f"Error in recommendation logic: {str(e)}")
        return []
