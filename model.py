import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def highlight_keywords(text, keywords):
    for kw in keywords:
        pattern = re.compile(rf'({re.escape(kw)})', re.IGNORECASE)
        text = pattern.sub(r'<mark>\1</mark>', text)
    return text

def get_best_policies(user_input, data, top_n=3, suggestion_n=2, threshold=0.2):
    if not user_input.strip():
        return {"best_matches": [], "suggestions": [], "no_matches": True}

    # Extract keywords from user input
    keywords = [word.strip().lower() for word in re.findall(r'\w+', user_input)]
    
    # Lowercased descriptions for processing
    descriptions = [policy["description"].lower() for policy in data]
    documents = descriptions + [' '.join(keywords)]

    # TF-IDF + Cosine Similarity
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]

    # Score based on keyword match
    keyword_match_scores = []
    for desc in descriptions:
        matches = sum(1 for kw in keywords if kw in desc)
        keyword_match_scores.append(matches / len(keywords) if keywords else 0)

    # Combine scores
    combined_scores = [
        (0.7 * cosine_sim[i] + 0.3 * keyword_match_scores[i])
        for i in range(len(data))
    ]

    # Sort by score
    sorted_indices = sorted(range(len(combined_scores)), key=lambda i: combined_scores[i], reverse=True)

    # Get best matches and suggestions
    best_matches = [data[i] for i in sorted_indices[:top_n] if combined_scores[i] > threshold]
    suggestions = [data[i] for i in sorted_indices[top_n:top_n + suggestion_n] if combined_scores[i] > 0.1]
    no_matches = len(best_matches) == 0

    # Highlight keywords in descriptions
    for policy in best_matches + suggestions:
        policy["highlighted_description"] = highlight_keywords(policy["description"], keywords)

    return {
        "best_matches": best_matches,
        "suggestions": suggestions,
        "no_matches": no_matches
    }
