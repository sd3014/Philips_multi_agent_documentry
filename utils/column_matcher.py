from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def normalize(text):
    return re.sub(r"[^a-zA-Z0-9 ]", " ", text.lower())


def get_best_matching_column(question, columns):
    columns = [str(col) for col in columns]

    q_clean = normalize(question)
    cols_clean = [normalize(col) for col in columns]

    # ---------- TF-IDF score ----------
    corpus = [q_clean] + cols_clean
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf = vectorizer.fit_transform(corpus)

    sim_scores = cosine_similarity(tfidf[0:1], tfidf[1:])[0]

    # ---------- keyword overlap boost ----------
    q_words = set(q_clean.split())

    final_scores = []

    for idx, col in enumerate(cols_clean):
        col_words = set(col.split())

        overlap = len(q_words.intersection(col_words))

        # boost important location words
        location_boost = 0
        if any(w in q_words for w in ["where", "place", "location", "occur"]):
            if any(w in col_words for w in ["where", "place", "location", "surface"]):
                location_boost = 1.5

        final_score = sim_scores[idx] + overlap * 0.3 + location_boost
        final_scores.append(final_score)

    best_index = final_scores.index(max(final_scores))

    return columns[best_index], round(final_scores[best_index], 2)