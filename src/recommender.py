from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":            int(row["id"]),
                "title":         row["title"],
                "artist":        row["artist"],
                "genre":         row["genre"],
                "mood":          row["mood"],
                "energy":        float(row["energy"]),
                "tempo_bpm":     float(row["tempo_bpm"]),
                "valence":       float(row["valence"]),
                "danceability":  float(row["danceability"]),
                "acousticness":  float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against a user preference dictionary.

    Returns a tuple of:
      - total score (float, max 5.0)
      - list of human-readable reason strings explaining each point awarded
    """
    score = 0.0
    reasons = []

    # Genre match: +2.0
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 2.0
        reasons.append(f"genre match: {song['genre']} (+2.0)")

    # Mood match: +1.5
    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.5
        reasons.append(f"mood match: {song['mood']} (+1.5)")

    # Energy similarity: +0.0 to +1.0
    energy_points = round(1.0 - abs(user_prefs["target_energy"] - song["energy"]), 2)
    score += energy_points
    reasons.append(f"energy similarity: {song['energy']} vs target {user_prefs['target_energy']} (+{energy_points})")

    # Acoustic bonus: +0.5
    if user_prefs.get("likes_acoustic") and song["acousticness"] > 0.65:
        score += 0.5
        reasons.append(f"acoustic match: acousticness {song['acousticness']} (+0.5)")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Scores every song using score_song(), sorts by score descending,
    and returns the top k results as (song_dict, score, explanation) tuples.
    """
    # Score every song in one pass using a list comprehension.
    # score_song returns (score, reasons), so we unpack with * to get
    # a flat (song, score, reasons) tuple for each entry.
    scored = [(song, *score_song(user_prefs, song)) for song in songs]

    # sorted() returns a new list — the original catalog is not modified.
    # key=lambda x: x[1] ranks by score (index 1).
    # reverse=True puts the highest score first.
    top_k = sorted(scored, key=lambda x: x[1], reverse=True)[:k]

    # Convert the reasons list into a single readable explanation string.
    return [(song, score, " | ".join(reasons)) for song, score, reasons in top_k]
