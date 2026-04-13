"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = {
        "favorite_genre": "lofi",
        "favorite_mood":  "chill",
        "target_energy":  0.40,
        "likes_acoustic": True,
    }

    recommendations = recommend_songs(user_prefs, songs, k=3)

    # ── Header ────────────────────────────────────────────────────────────────
    print("\n" + "=" * 52)
    print("  Music Recommender — Top Picks")
    print("=" * 52)
    print(f"  Genre : {user_prefs['favorite_genre']}")
    print(f"  Mood  : {user_prefs['favorite_mood']}")
    print(f"  Energy: {user_prefs['target_energy']}  |  Acoustic: {user_prefs['likes_acoustic']}")
    print("=" * 52)

    # ── Results ───────────────────────────────────────────────────────────────
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"       Score: {score:.2f} / 5.00")
        print("       Why:")
        for reason in explanation.split(" | "):
            print(f"         • {reason}")

    print("\n" + "=" * 52 + "\n")


if __name__ == "__main__":
    main()
