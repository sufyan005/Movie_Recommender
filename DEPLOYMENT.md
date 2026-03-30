# Streamlit Cloud Deployment Instructions

# ===========================================

#

# For Streamlit Cloud (https://streamlit.io/cloud), you have two options:

#

# OPTION 1: Store secrets in Streamlit Cloud dashboard

# ======================================================

# 1. Push your code to GitHub

# 2. Go to https://share.streamlit.io and sign in

# 3. Click "New app" and select your repo, branch, and app.py

# 4. Once deployed, go to Settings → Secrets and add:

# TMDB_API_KEY = your_actual_api_key_here

#

# OPTION 2: Local development with .env file

# =============================================

# 1. Create a .env file in the project root (already in .gitignore):

# TMDB_API_KEY=your_actual_api_key_here

# 2. The app will automatically load it via python-dotenv

# 3. Never commit .env to Git!

#

# For Streamlit Cloud, you must use OPTION 1 (dashboard secrets)

# because .env files won't be deployed.
