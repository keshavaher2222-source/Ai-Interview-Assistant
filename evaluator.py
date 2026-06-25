from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def evaluate_answer(candidate_answer, ideal_answer):

    documents = [candidate_answer, ideal_answer]

    tfidf = TfidfVectorizer()
    matrix = tfidf.fit_transform(documents)

    similarity = cosine_similarity(matrix[0], matrix[1])[0][0]

    score = round(similarity * 10, 2)

    return score