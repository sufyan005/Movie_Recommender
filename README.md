# 🎬 Movie Recommender

A Streamlit-based movie recommendation system using TF-IDF vectorization and cosine similarity.

## Installation

### Local Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd Movie

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your TMDB API key
echo TMDB_API_KEY=your_api_key_here > .env
```

### Run Locally

```bash
streamlit run app.py
```

## Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io)
3. Click "New app" and connect your GitHub repo
4. Select your main app file: `app.py`
5. Click "Deploy"
6. After deployment, go to Settings → Secrets and add:
   ```
   TMDB_API_KEY = your_actual_tmdb_api_key
   ```
## Project Structure

```
.
├── app.py                 # Main Streamlit app
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── movies.pkl            # Movie data cache
├── indices.pkl           # Movie index mapping
├── tfidf_matrix.pkl      # TF-IDF matrix for similarity
└── README.md             # This file
```

## Dependencies

- streamlit
- pandas
- scikit-learn
- requests
- python-dotenv

## Environment Variables

- `TMDB_API_KEY`: Your TMDB API key for fetching movie posters

## Features

- Movie recommendations based on similarity
- Poster fetching from TMDB
- Fast caching for performance
- Responsive UI design
