from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_best_matching_column(question, columns):
    columns = [str(col) for col in columns]

    corpus = [question] + columns

    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(corpus)

    question_vector = tfidf_matrix[0:1]
    column_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(
        question_vector,
        column_vectors
    )[0]

    best_index = similarities.argmax()
    best_score = similarities[best_index]

    return columns[best_index], round(float(best_score), 2)