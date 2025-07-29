from imdb import IMDb
import requests

# === IMDb Section ===

imdb_scraper = IMDb()

def get_movie_or_series_metadata(query):
    try:
        print(f"[IMDB SEARCH] {query}")
        results = imdb_scraper.search_movie(query)
        if not results:
            print(f"[IMDB] No results for: {query}")
            return None

        movie = results[0]
        imdb_scraper.update(movie)

        kind = movie.get('kind', 'movie')
        title = movie.get('title')
        year = movie.get('year')

        if not title:
            return None

        category = "series" if kind in ("tv series", "tv mini series") else "movies"
        formatted_name = f"{title} ({year})" if year else title

        print(f"[IMDB RESULT] {formatted_name} as {category}")
        return {"name": formatted_name, "category": category}
    except Exception as e:
        print(f"[IMDB ERROR] {e}")
        return None

# === Google Books Section ===

def get_book_metadata(query):
    try:
        print(f"[BOOK SEARCH] {query}")
        url = "https://www.googleapis.com/books/v1/volumes"
        params = {
            "q": query,
            "maxResults": 1,
            "printType": "books",
            "projection": "lite"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if "items" not in data:
            print(f"[BOOK] No results for: {query}")
            return None

        item = data["items"][0]["volumeInfo"]
        title = item.get("title")
        year = item.get("publishedDate", "")[:4]

        if not title:
            return None

        formatted_name = f"{title} ({year})" if year.isdigit() else title
        print(f"[BOOK RESULT] {formatted_name}")
        return {"name": formatted_name, "category": "books"}
    except Exception as e:
        print(f"[BOOK ERROR] {e}")
        return None
