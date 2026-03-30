# 🎬 Movie Recommender
A content-based movie recommendation engine that suggests similar films based on genre, cast, crew, keywords, and plot — powered by TF-IDF vectorization and cosine similarity, wrapped in a clean Streamlit interface with live TMDB poster fetching.

🔗 **Live Demo:** [movie-recommender-for-all.streamlit.app](https://movie-recommender-for-all.streamlit.app)

---

## 📸 Preview
> Pick any movie → Get a visual grid of similar titles with posters instantly.

---

## ✨ Features
- 🔍 Search from 5,000+ movies via a dropdown
- 🎯 Content-based filtering using TF-IDF + Cosine Similarity
- 🖼️ Live movie posters fetched in parallel from the TMDB API
- 🎚️ Adjustable recommendations (5, 10, 15, or 20 results)
- ⚡ Fast poster loading via `ThreadPoolExecutor` for parallel API calls
- 🚀 ~5x faster load times using Parquet + NPZ over legacy Pickle
- 🛠️ Version-agnostic storage — no deserialization errors across environments
- 📱 Responsive grid layout with Streamlit

---

## 🛠️ Tech Stack
| Layer | Tools |
|-------|-------|
| Language | Python 3.11+ |
| Data Processing | Pandas, NumPy, SciPy |
| NLP | NLTK (Stopwords, WordNetLemmatizer) |
| ML / Similarity | Scikit-learn (TF-IDF, Cosine Similarity) |
| Data Storage | Apache Parquet, Scipy NPZ, CSV |
| Frontend | Streamlit (v1.55+) |
| Poster API | TMDB (The Movie Database) |
| Concurrency | `concurrent.futures.ThreadPoolExecutor` |

---

## 🧠 How It Works
```
User selects a movie
        ↓
Look up its index in the precomputed TF-IDF matrix
        ↓
Compute cosine similarity against all other movies
        ↓
Return top-N most similar titles
        ↓
Fetch posters in parallel from TMDB API
        ↓
Render visual grid in Streamlit
```

The model combines the following features for each movie into a single text "soup":
- **Genres**
- **Top 3 cast members**
- **Director**
- **Plot keywords**
- **Movie overview**

This combined text is vectorized using **TF-IDF** (5000 features, unigrams + bigrams), and similarity is measured via **Cosine Similarity** — movies with closer vectors are considered more similar.

---

## 🧹 Data Pipeline & Feature Engineering

### 1. Data Ingestion & Merging
Two TMDB datasets — `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` — are merged on `title` and reduced to seven columns relevant to content-based filtering: `title`, `cast`, `genres`, `movie_id`, `crew`, `keywords`, and `overview`.

### 2. Data Cleaning
Null rows are dropped via `dropna()`. Duplicate entries are removed by `title` after tag construction, followed by a full index reset to ensure positional lookups remain consistent.

### 3. Feature Extraction
All metadata columns are stored as raw JSON strings in the dataset. Each is parsed using `ast.literal_eval` and converted into structured Python lists:

| Column | Extraction Logic |
|---|---|
| `genres` | All genre names |
| `keywords` | All keyword names |
| `cast` | Top 3 billed actors |
| `crew` | Director only, filtered by `job == 'director'` |
| `overview` | Tokenized into individual words |

Multi-word names such as *Sam Mendes* are collapsed into single tokens (`SamMendes`) to prevent the vectorizer from treating first and last names as independent terms — preserving named-entity integrity during vectorization.

### 4. Metadata Soup Construction
All five features are concatenated per movie into a single `tags` field:
```
tags = overview + genres + keywords + cast + crew
```
This unified representation allows the vectorizer to treat a movie's entire content profile as one document.

### 5. Text Preprocessing
Each `tags` string is normalized through a sequential NLP pipeline built with NLTK:
- **Lowercasing** — ensures case-insensitive token matching
- **Punctuation removal** — via regex pattern `[^a-zA-Z\s]`
- **Stopword removal** — NLTK English stopword corpus
- **Lemmatization** — WordNetLemmatizer reduces inflected forms to their base (e.g. *directed* → *direct*, *running* → *run*), improving token consolidation across documents

### 6. TF-IDF Vectorization
```python
TfidfVectorizer(max_features=5000, ngram_range=(1,2), stop_words='english')
```
- **`max_features=5000`** — constrains the vocabulary to the 5000 highest-scoring terms, keeping the sparse matrix computationally efficient
- **`ngram_range=(1,2)`** — captures both unigrams and bigrams, enabling the model to recognize multi-word concepts such as *"space exploration"* or *"serial killer"* that single tokens would fragment
- **`stop_words='english'`** — applies a second stopword filter at the vectorizer level for additional noise reduction

### 7. Similarity Computation
Cosine similarity is computed **at query time** between the selected movie's TF-IDF vector and the full matrix — no pairwise similarity matrix is precomputed or stored. This keeps memory overhead constant regardless of dataset size and avoids stale similarity scores if the corpus is updated.

---

## ⚙️ Production Storage Design
| Storage | Reason |
|---|---|
| `movies.parquet` | Version-agnostic, columnar, faster I/O via PyArrow |
| `tfidf_matrix.npz` | Scipy sparse format — no scikit-learn version dependency |
| `indices.csv` | Plain text, zero deserialization overhead |

Pickle is sensitive to both Python and library versions. Deploying across environments with mismatched runtimes can cause silent failures or crashes. Parquet and NPZ eliminate that risk entirely while delivering measurably faster load times.

---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/your-username/movie-recommender-for-all.git
cd movie-recommender-for-all
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your TMDB API key
Create a `.env` file in the root directory:
```
TMDB_API_KEY=your_api_key_here
```
Or export it directly:
```bash
export TMDB_API_KEY=your_api_key_here
```
> Get a free API key at [themoviedb.org](https://www.themoviedb.org/settings/api)

### 4. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure
```
movie-recommender-for-all/
│
├── app.py                    # Main Streamlit application
├── requirements.txt          # Optimized dependencies (no version conflicts)
├── .env                      # API key (not committed)
├── .gitignore
│
├── movies.parquet            # Compressed movie metadata (stable across versions)
├── indices.csv               # Title-to-index mapping (human-readable)
├── tfidf_matrix.npz          # Sparse TF-IDF matrix (memory-efficient)
```

---

## 📦 Requirements
```
streamlit
pandas
scikit-learn
scipy
pyarrow
requests
nltk
python-dotenv
```

---

## ⚙️ Deployment (Streamlit Community Cloud)
1. Push your repo to GitHub (ensure `.parquet`, `.npz`, and `.csv` files are included)
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Under **Settings → Secrets**, add:
```toml
TMDB_API_KEY = "your_api_key_here"
```
4. Deploy — your app will be live at `your-app-name.streamlit.app`

---

## 🤝 Contributing
Pull requests are welcome. If you find a bug or want to improve the recommendation logic, feel free to open an issue or submit a PR.
