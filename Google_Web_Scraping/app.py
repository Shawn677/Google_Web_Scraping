from flask import Flask, render_template, request, redirect, url_for, session
from scraper import (
    google_search,
    bing_search,
    duckduckgo_search,
    pubmed_search,
    google_scholar_search,
    arxiv_search,
    summarize_article,
)
from math import ceil

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management

@app.before_request
def initialize_session():
    """
    Initialize the session with empty lists if they don't exist.
    Clear search results if no query is provided.
    """
    if 'saved_results' not in session:
        session['saved_results'] = []
    if 'results' not in session:
        session['results'] = []

    # Clear search results if no query is provided
    if not request.args.get('query'):
        session['results'] = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        selected_engine = request.form.get('engine')
        results = perform_search(selected_engine, query)
        unique_results = remove_duplicates(results)
        sorted_results = sort_results(unique_results)
        session['results'] = sorted_results  # Store results in session
        return redirect(url_for('index', query=query, page=1))

    query = request.args.get('query')
    page = int(request.args.get('page', 1))
    per_page = 10
    results = session.get('results', [])
    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = results[start:end]
    total_pages = ceil(len(results) / per_page)
    return render_template('index.html', results=paginated_results, query=query, page=page, total_pages=total_pages)

@app.route('/save_result', methods=['POST'])
def save_result():
    result_title = request.form.get('result_title')
    result_link = request.form.get('result_link')
    result_source = request.form.get('result_source')
    result_type = request.form.get('result_type')

    if not all([result_title, result_link, result_source, result_type]):
        return "Invalid result data", 400

    # Ensure all fields are strings
    result_title = str(result_title)
    result_link = str(result_link)
    result_source = str(result_source)
    result_type = str(result_type)

    # Add the result to the saved results list
    session['saved_results'].append({
        "title": result_title,
        "link": result_link,
        "source": result_source,
        "type": result_type
    })
    session.modified = True  # Ensure the session is saved
    return redirect(url_for('index'))

@app.route('/delete_saved_result', methods=['POST'])
def delete_saved_result():
    """
    Delete a saved result based on its index.
    """
    try:
        index = int(request.form.get('index'))
        if 0 <= index < len(session['saved_results']):
            session['saved_results'].pop(index)
            session.modified = True
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error deleting saved result: {e}")
        return "Error deleting saved result", 400

@app.route('/clear_session')
def clear_session():
    """
    Clear the session (optional, for debugging).
    """
    session.clear()
    return redirect(url_for('index'))

def perform_search(engine, query):
    """
    Perform a search using the selected search engine.
    """
    if engine == 'google':
        return google_search(query)
    elif engine == 'bing':
        return bing_search(query)
    elif engine == 'duckduckgo':
        return duckduckgo_search(query)
    elif engine == 'pubmed':
        return pubmed_search(query)
    elif engine == 'scholar':
        return google_scholar_search(query)
    elif engine == 'arxiv':
        return arxiv_search(query)
    return []

def remove_duplicates(results):
    """
    Remove duplicate results based on the link.
    """
    unique_results = []
    seen_links = set()
    for result in results:
        if result["link"] not in seen_links:
            unique_results.append(result)
            seen_links.add(result["link"])
    return unique_results

def sort_results(results):
    """
    Sort results by source.
    """
    return sorted(results, key=lambda x: x["source"])

if __name__ == '__main__':
    app.run(debug=True)