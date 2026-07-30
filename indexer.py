import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocessing import preprocess_text

DOCUMENTS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "documents.json")

class DocumentIndexError(Exception):
    """Raised when the document corpus cannot be loaded or indexed."""
    pass

def load_documents(path=DOCUMENTS_PATH):
    """Load and validate the document corpus from a JSON file."""
    if not os.path.exists(path):
        raise DocumentIndexError(f"Document dataset not found at '{path}'. Run crawler.py first to generate it.")
    
    with open(path, "r", encoding="utf-8") as f:
        try:
            documents = json.load(f)
        except json.JSONDecodeError as err:
            raise DocumentIndexError(f"Document dataset at '{path}' is not valid JSON.") from err

    if not isinstance(documents, list) or len(documents) == 0:
        raise DocumentIndexError(f"Document dataset at '{path}' is empty.")
    
    return documents

def build_searchable_text(doc):
    """Combine a document's fields into one string for indexing."""
    title = doc.get("title", "")
    heading = doc.get("heading", "")
    content = doc.get("content", "")
    
    combined = f"{title} {title} {heading} {content}"
    return preprocess_text(combined)

def build_index(path=DOCUMENTS_PATH):
    """
    Builds TF-IDF index matrices across all loaded documents.
    Creates the searchable representation of all documents using Term Frequency - Inverse Document Frequency.
    """
    documents = load_documents(path)
    corpus = [build_searchable_text(doc) for doc in documents]
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    return documents, vectorizer, tfidf_matrix