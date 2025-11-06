# Scripture Search

Semantic search engine for the Book of Mormon and King James Bible. Search 37,000+ verses using AI embeddings.

## Features

- Semantic search across both texts simultaneously
- One-click copy verses to clipboard
- Shareable URLs for searches
- Fast search with optimized embeddings
- Search statistics and similarity scores

## Setup

```bash
# Install dependencies
uv sync

# Add your API key
echo "OPENROUTER_API_KEY=your_key" > .env

# Run the app
uv run python main.py
```

Visit `http://localhost:5001`

## Tech Stack

- **FastHTML** - Web framework
- **OpenRouter** - Embeddings API
- **NumPy** - Fast vector operations
