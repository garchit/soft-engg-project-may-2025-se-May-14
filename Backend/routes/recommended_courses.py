from sentence_transformers import SentenceTransformer, util
import torch

# Initialize model (efficient and accurate)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Example course data (course_id: description or tags)
# all_courses = {
#     "intro_finance": "Learn the basics of finance and money management.",
#     "budgeting_101": "Understand how to create and manage a budget effectively.",
#     "stock_basics": "Introduction to investing in the stock market and equities.",
#     "crypto_intro": "Fundamentals of cryptocurrencies like Bitcoin and Ethereum.",
#     "retirement_planning": "Plan for a financially secure retirement.",
#     "tax_planning": "Strategies to optimize your income tax and deductions.",
#     "real_estate_investing": "Beginner’s guide to investing in real estate.",
#     "advanced_investing": "Deep dive into investment vehicles and portfolio theory.",
# }

# Example user history
# completed_courses = ["intro_finance", "stock_basics"]

# === Recommender Function ===
def recommend_courses_semantic(completed_courses, all_courses, top_n=5):
    course_ids = list(all_courses.keys())
    course_texts = list(all_courses.values())

    # Generate embeddings for all course descriptions
    course_embeddings = model.encode(course_texts, convert_to_tensor=True)

    # Find indices of completed courses
    completed_indices = [course_ids.index(cid) for cid in completed_courses if cid in course_ids]
    if not completed_indices:
        return []

    # Compute average embedding of completed courses
    user_embedding = course_embeddings[completed_indices].mean(dim=0, keepdim=True)

    # Compute cosine similarities between user and all courses
    similarities = util.pytorch_cos_sim(user_embedding, course_embeddings)[0]

    # Filter and rank unseen courses
    results = [
        (cid, float(similarities[i]))
        for i, cid in enumerate(course_ids)
        if cid not in completed_courses
    ]
    results.sort(key=lambda x: -x[1])

    return [cid for cid, _ in results[:top_n]]

# === Usage ===
# recommended = recommend_courses_semantic(completed_courses, all_courses)
# print("Recommended Courses:", recommended)
