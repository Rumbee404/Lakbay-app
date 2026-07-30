import time
from flask import Flask, render_template, request
from indexer import build_index
from search_engine import search
from database import initialize_database, log_search, get_analytics_summary

# Main Flask application.
# Central coordinator of the entire project.
app = Flask(__name__)

# Initialize DB and index on startup
initialize_database()
documents, vectorizer, tfidf_matrix = build_index()

@app.route("/")
def index():
    """Home search page."""
    return render_template("index.html")

@app.route("/search")
def search_route():
    """
    Search route handling sequence:
    User enters query --> app.py receives --> search_engine.py processes it
    --> results are returned --> webpage displays results
    """
    start_time = time.time()
    query = request.args.get("q", "")
    category = request.args.get("category")
    source = request.args.get("source")
    
    results = search(query, documents, vectorizer, tfidf_matrix, category=category, source=source)
    
    execution_time_ms = (time.time() - start_time) * 1000
    top_result = results[0]["title"] if results else None
    
    if query.strip():
        log_search(query, len(results), top_result, execution_time_ms)
        
    # Extract unique categories/sources for filter dropdowns
    categories = sorted(list({doc.get("category") for doc in documents if doc.get("category")}))
    sources = sorted(list({doc.get("source") for doc in documents if doc.get("source")}))
    
    return render_template(
        "results.html",
        query=query,
        results=results,
        categories=categories,
        sources=sources,
        selected_category=category,
        selected_source=source,
        execution_time=round(execution_time_ms, 2)
    )

@app.route("/analytics")
def analytics():
    """Displays search analytics dashboard."""
    data = get_analytics_summary()
    return render_template("analytics.html", analytics=data)

if __name__ == "__main__":
    app.run(debug=True)