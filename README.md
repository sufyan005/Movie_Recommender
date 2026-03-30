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
- 🛠️ Version-agnostic storage — no Pickle deserialization errors across environments
- 📱 Responsive grid layout with Streamlit

---

## 🛠️ Tech Stack
| Layer | Tools |
|-------|-------|
| Language | Python 3.11+ |
| Data Processing | Pandas, NumPy, SciPy |
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
| Storage | Reason |
|---|---|
| `movies.parquet` | Version-agnostic, columnar, faster I/O via PyArrow |
| `tfidf_matrix.npz` | Scipy sparse format — no scikit-learn version dependency |
| `indices.csv` | Plain text, zero deserialization overhead |

Pickle is sensitive to both Python and library versions. Deploying to Streamlit Cloud with a different runtime than your local environment can cause silent failures or crashes. Parquet and NPZ eliminate that risk entirely.

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
Pull requests are welcome! If you find a bug or want to improve the recommendation logic, feel free to open an issue or submit a PR.
