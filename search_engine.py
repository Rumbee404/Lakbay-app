from sklearn.metrics.pairwise import cosine_similarity
from preprocessing import preprocess_text

DEFAULT_TOP_N = 10
SNIPPET_TARGET_LENGTH = 200
SNIPPET_HALF_WINDOW = 100

def generate_snippet(content, query, window=SNIPPET_HALF_WINDOW):
    """Generates a contextual snippet around the first matching query word."""
    if not content:
        return ""
    
    words = preprocess_text(query).split()
    content_lower = content.lower()
    
    match_pos = -1
    for w in words:
        pos = content_lower.find(w)
        if pos != -1:
            match_pos = pos
            break
            
    if match_pos == -1:
        return content[:SNIPPET_TARGET_LENGTH] + ("..." if len(content) > SNIPPET_TARGET_LENGTH else "")
    
    start = max(0, match_pos - window)
    end = min(len(content), match_pos + window)
    snippet = content[start:end]
    
    if start > 0:
        snippet = "..." + snippet
    if end < len(content):
        snippet = snippet + "..."
        
    return snippet

def search(query, documents, vectorizer, tfidf_matrix, top_n=DEFAULT_TOP_N, category=None, source=None):
    """
    Runs actual searches here against the TF-IDF index using Cosine Similarity ranking.
    """
    if not query or not query.strip():
        return []
    
    processed_query = preprocess_text(query)
    if not processed_query:
        return []
        
    query_vector = vectorizer.transform([processed_query])
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
    
    results = []
    for idx, score in enumerate(similarity_scores):
        if score > 0:
            doc = documents[idx]
            
            # Apply optional filters
            if category and doc.get("category", "").lower() != category.lower():
                continue
            if source and doc.get("source", "").lower() != source.lower():
                continue
                
            relevance_percent = round(score * 100, 1)
            snippet = generate_snippet(doc.get("content", ""), query)
            
            results.append({
                "title": doc.get("title", ""),
                "category": doc.get("category", ""),
                "source": doc.get("source", ""),
                "url": doc.get("url", "#"),
                "snippet": snippet,
                "relevance_percent": relevance_percent,
                "score": score
            })
            
    # Rank by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]