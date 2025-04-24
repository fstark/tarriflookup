import csv
import requests
import json
import sys
import math

def get_embedding(text):
    url = "http://localhost:11434/api/embeddings"
    payload = {
        "model": "nomic-embed-text",  # or your preferred embedding model
        "prompt": text
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["embedding"]

def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

def embed_all():
    data = []
    with open('tariff_database_2025.csv', newline='', encoding='latin1') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for idx, row in enumerate(reader, start=2):
            text = row[1]
            embedding = get_embedding(text)
            data.append([row[0], row[1], embedding])
    with open('tariff.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

def get_top_matches(query, data):
    query_embedding = get_embedding(query)
    scored = []
    for code, desc, embedding in data:
        score = cosine_similarity(query_embedding, embedding)
        scored.append((score, code, desc))
    top_matches = sorted(scored, reverse=True)[:50]
    return [(code, desc) for score, code, desc in top_matches]

def find_best(query, codes):
    url = "http://localhost:11434/api/generate"
    prompt = (
        f"You are a tariff code expert. You need to find the best matches for a product named \"{query}\". "
        "The list of possible tariffs is:\n" + '\n'.join([f"{code} {desc}" for code, desc in codes]) +
        "\ndo not print extra information, just print the ordered list of top matching items."
    )
    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()["response"]
    print(result)
    return result

def exec_query(query):
    debug = '--debug' in sys.argv
    with open('tariff.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    top_matches = get_top_matches(query, data)
    if debug:
        for code, desc in top_matches:
            print(f"{code} {desc}")
    print("[LOG] Top 50 matches retrieved. Calling find_best...")
    find_best(query, top_matches)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--embed":
        embed_all()
    else:
        query = sys.argv[1] if len(sys.argv) > 1 else ''
        exec_query(query)

if __name__ == "__main__":
    main()
