# MovieFlix — Movie Recommendation System

A beginner-friendly Python/Kivy starter project for a genre-based movie recommendation app.

## Features
- Choose a genre and number of recommendations.
- Uses TF-IDF and cosine similarity when scikit-learn is installed.
- Includes a small built-in movie dataset that you can expand.
- Simple Kivy interface suitable as a starting point for an Android APK.

## Run on a computer
1. Install Python 3.10 or 3.11.
2. Open a terminal in this folder.
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python main.py`

If scikit-learn is unavailable, the app falls back to simple genre matching.

## Android APK note
This ZIP is the project source, not a prebuilt APK. Building an APK usually requires Linux and Buildozer:
1. Use a Linux machine or cloud Linux environment.
2. Install Buildozer and its Android build dependencies.
3. In this folder, run `buildozer init`, then configure the spec to include `main.py`, `movies.csv`, and Python packages.
4. Build with `buildozer -v android debug`.

APK builds can require additional setup and may not work directly inside Google Colab. Do not claim an APK exists until the build completes successfully.

## Background video/audio
The starter app does not bundle copyrighted video or music. You can add media you own or have permission to use; implement video/audio playback separately and test on Android.
