from fasthtml.common import *
from src.search import ScriptureSearchEngine

# Initialize the search engine (this will load once at startup)
print("Loading search engine...")
search_engine = ScriptureSearchEngine()
print("Search engine ready!")

app, rt = fast_app(
    hdrs=(
        Script("""
            let lastSearchTime = 0;
            function canSearch() {
                const now = Date.now();
                if (now - lastSearchTime < 1000) {
                    return false;
                }
                lastSearchTime = now;
                return true;
            }

            function copyVerse(reference, text) {
                const content = reference + '\\n' + text;
                navigator.clipboard.writeText(content).then(() => {
                    // Show a brief notification
                    const btn = event.target.closest('.copy-btn');
                    const original = btn.innerHTML;
                    btn.innerHTML = '✓ Copied!';
                    btn.style.color = '#27ae60';
                    setTimeout(() => {
                        btn.innerHTML = original;
                        btn.style.color = '';
                    }, 2000);
                });
            }

            function exampleSearch(query) {
                if (!canSearch()) return;
                document.querySelector('input[name="query"]').value = query;
                document.querySelector('form').requestSubmit();
            }

            // Load search from URL on page load
            window.addEventListener('DOMContentLoaded', () => {
                const params = new URLSearchParams(window.location.search);
                const query = params.get('q');
                if (query) {
                    document.querySelector('input[name="query"]').value = query;
                    // Auto-search if there's a query in URL
                    setTimeout(() => {
                        document.querySelector('form').requestSubmit();
                    }, 100);
                }
            });

            // Update URL when search completes
            document.body.addEventListener('htmx:afterRequest', (event) => {
                if (event.detail.pathInfo.requestPath === '/search') {
                    const query = new FormData(event.detail.elt).get('query');
                    const url = new URL(window.location);
                    url.searchParams.set('q', query);
                    window.history.pushState({}, '', url);
                }
            });
        """),
        Style("""
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                max-width: 1600px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2c3e50;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            .subtitle {
                color: #7f8c8d;
                margin-bottom: 30px;
                font-size: 1.1em;
            }
            .search-form {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
                align-items: stretch;
            }
            .search-box {
                flex: 1;
                min-width: 0;
                padding: 15px;
                font-size: 16px;
                border: 2px solid #ddd;
                border-radius: 8px;
                box-sizing: border-box;
            }
            .search-box:focus {
                outline: none;
                border-color: #3498db;
            }
            .search-btn {
                background: #3498db;
                color: white;
                border: none;
                padding: 15px 20px;
                font-size: 16px;
                border-radius: 8px;
                cursor: pointer;
                transition: background 0.3s;
                white-space: nowrap;
                flex-shrink: 0;
                width: 100px;
                max-width: 100px;
            }
            .search-btn:hover {
                background: #2980b9;
            }
            .result-card {
                background: #f8f9fa;
                padding: 20px;
                margin-bottom: 15px;
                border-radius: 8px;
                border-left: 4px solid #3498db;
                cursor: pointer;
                transition: all 0.2s;
            }
            .result-card:hover {
                background: #e9ecef;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .result-card.bom {
                border-left-color: #e74c3c;
            }
            .result-card.kjb {
                border-left-color: #9b59b6;
            }
            .result-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }
            .reference {
                font-weight: bold;
                color: #2c3e50;
                font-size: 1.1em;
            }
            .source {
                color: #7f8c8d;
                font-size: 0.9em;
            }
            .similarity {
                background: #3498db;
                color: white;
                padding: 4px 10px;
                border-radius: 12px;
                font-size: 0.85em;
            }
            .result-text {
                color: #34495e;
                line-height: 1.6;
                font-size: 1.05em;
            }
            .context-section {
                margin-top: 15px;
                padding-top: 15px;
                border-top: 2px dashed #dee2e6;
            }
            .context-label {
                font-weight: bold;
                color: #7f8c8d;
                font-size: 0.9em;
                margin-bottom: 8px;
            }
            .context-text {
                color: #5a6c7d;
                line-height: 1.6;
                font-size: 0.95em;
                font-style: italic;
            }
            .no-results {
                text-align: center;
                padding: 40px;
                color: #7f8c8d;
            }
            .loading {
                text-align: center;
                padding: 20px;
                color: #3498db;
                font-weight: bold;
                font-size: 1.1em;
                background: #e3f2fd;
                border-radius: 8px;
                margin: 10px 0;
            }
            .loading.htmx-request {
                display: block !important;
            }
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            .loading.htmx-request {
                animation: pulse 1.5s ease-in-out infinite;
            }
            .highlight-verse {
                background-color: #fff3cd;
                padding: 2px 4px;
                border-radius: 3px;
                font-weight: 500;
            }
            .examples {
                margin-bottom: 20px;
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                align-items: center;
            }
            .examples-label {
                color: #7f8c8d;
                font-size: 0.9em;
                font-weight: 500;
            }
            .example-query {
                background: #ecf0f1;
                color: #2c3e50;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 0.9em;
                cursor: pointer;
                transition: all 0.2s;
                border: 1px solid #bdc3c7;
            }
            .example-query:hover {
                background: #3498db;
                color: white;
                border-color: #3498db;
            }
            .copy-btn {
                background: transparent;
                border: none;
                color: #7f8c8d;
                cursor: pointer;
                padding: 4px 8px;
                font-size: 0.9em;
                transition: color 0.2s;
                margin-left: 8px;
            }
            .copy-btn:hover {
                color: #3498db;
            }
            .stats {
                text-align: center;
                color: #7f8c8d;
                font-size: 0.9em;
                margin-top: 15px;
                padding: 10px;
                background: #f8f9fa;
                border-radius: 6px;
            }
            .stats strong {
                color: #2c3e50;
            }
            .results-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-top: 20px;
            }
            .column {
                min-height: 200px;
            }
            .column-header {
                font-size: 1.5em;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 3px solid;
            }
            .column-header.kjb {
                border-bottom-color: #9b59b6;
                color: #9b59b6;
            }
            .column-header.bom {
                border-bottom-color: #e74c3c;
                color: #e74c3c;
            }
            .no-results-column {
                text-align: center;
                padding: 20px;
                color: #bdc3c7;
                font-style: italic;
            }
            @media (max-width: 768px) {
                .results-container {
                    grid-template-columns: 1fr;
                }
            }
        """),
    )
)


def SearchForm():
    return Div(
        Form(
            Div(
                Input(
                    type="text",
                    name="query",
                    placeholder="Search for verses... (e.g., 'faith and prayer', 'creation of the world')",
                    cls="search-box",
                    required=True,
                    autofocus=True
                ),
                Button("Search", cls="search-btn", type="submit"),
                cls="search-form"
            ),
            method="post",
            action="/search",
            hx_post="/search",
            hx_target="#results",
            hx_indicator="#loading",
            onsubmit="return canSearch();"
        ),
        Div(
            Span("Try: ", cls="examples-label"),
            Span("faith and prayer", cls="example-query", onclick="exampleSearch('faith and prayer')"),
            Span("love thy neighbor", cls="example-query", onclick="exampleSearch('love thy neighbor')"),
            Span("the creation", cls="example-query", onclick="exampleSearch('the creation')"),
            Span("repentance and forgiveness", cls="example-query", onclick="exampleSearch('repentance and forgiveness')"),
            Span("miracles of Jesus", cls="example-query", onclick="exampleSearch('miracles of Jesus')"),
            cls="examples"
        )
    )


def highlight_verse_in_context(verse_text: str, context_text: str) -> str:
    """Highlight the verse text within the context text."""
    # Find the verse in the context
    verse_clean = verse_text.strip()
    if verse_clean in context_text:
        # Replace with highlighted version
        highlighted = context_text.replace(
            verse_clean,
            f'<span class="highlight-verse">{verse_clean}</span>'
        )
        return NotStr(highlighted)  # NotStr tells FastHTML not to escape HTML
    return context_text


def ResultCard(result):
    source_class = "bom" if result["source"] == "Book of Mormon" else "kjb"
    similarity_pct = f"{result['similarity'] * 100:.1f}%"
    card_id = f"card-{result['source']}-{result['verse_idx']}"

    # Highlight the verse within the context
    highlighted_context = highlight_verse_in_context(result["text"], result["embedding_text"])

    # Escape quotes for JavaScript
    reference_escaped = result["reference"].replace("'", "\\'")
    text_escaped = result["text"].replace("'", "\\'").replace("\n", "\\n")

    return Div(
        Div(
            Div(
                Span(result["reference"], cls="reference"),
                Button(
                    "📋 Copy",
                    cls="copy-btn",
                    onclick=f"event.stopPropagation(); copyVerse('{reference_escaped}', '{text_escaped}');"
                )
            ),
            Div(similarity_pct, cls="similarity"),
            cls="result-header"
        ),
        Div(result["text"], cls="result-text"),
        Div(
            Div("Full Context:", cls="context-label"),
            Div(highlighted_context, cls="context-text"),
            cls="context-section",
            id=f"context-{card_id}",
            style="display: none;"
        ),
        cls=f"result-card {source_class}",
        onclick=f"document.getElementById('context-{card_id}').style.display = document.getElementById('context-{card_id}').style.display === 'none' ? 'block' : 'none';"
    )


@rt("/")
def get():
    return Titled(
        "Scripture Search",
        Div(
            Div("Semantic search across the Book of Mormon and King James Bible", cls="subtitle"),
            SearchForm(),
            Div("Searching...", id="loading", cls="loading", style="display:none;"),
            Div(id="results"),
            cls="container"
        )
    )


@rt("/search")
def post(query: str):
    if not query.strip():
        return Div("Please enter a search query", cls="no-results")

    try:
        import time
        start_time = time.time()

        # Search returns dict with 'kjb' and 'bom' keys, each with 30 results
        results = search_engine.search(query, top_k_per_source=30)

        search_time = time.time() - start_time

        kjb_results = results["kjb"]
        bom_results = results["bom"]

        # Calculate total verses searched
        total_verses = len(search_engine.bom_metadata) + len(search_engine.kjb_metadata)

        # Create statistics display
        stats = Div(
            f"Searched ",
            Strong(f"{total_verses:,} verses"),
            f" in ",
            Strong(f"{search_time:.2f}s"),
            f" • Found ",
            Strong(f"{len(kjb_results)} KJB"),
            f" and ",
            Strong(f"{len(bom_results)} BOM"),
            f" results",
            cls="stats"
        )

        # Create two columns
        kjb_column = Div(
            Div("King James Bible", cls="column-header kjb"),
            *[ResultCard(result) for result in kjb_results] if kjb_results else [Div("No results", cls="no-results-column")],
            cls="column"
        )

        bom_column = Div(
            Div("Book of Mormon", cls="column-header bom"),
            *[ResultCard(result) for result in bom_results] if bom_results else [Div("No results", cls="no-results-column")],
            cls="column"
        )

        return Div(
            stats,
            Div(
                kjb_column,
                bom_column,
                cls="results-container"
            )
        )
    except Exception as e:
        return Div(
            f"Error during search: {str(e)}",
            cls="no-results",
            style="color: #e74c3c;"
        )


if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 5001))
    serve(host="0.0.0.0", port=port)
