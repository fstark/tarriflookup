import csv
import requests
import json
import sys
import math

verbose = False

def get_embedding(text, embedding_model):
    url = "http://localhost:11434/api/embeddings"
    payload = {
        "model": embedding_model,  # embedding model from argument
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

def embed_all(tariff_file, embedding_model):
    print( f"[LOG] Embedding all tariff codes from {tariff_file} using model '{embedding_model}'...")
    data = []
    with open( tariff_file, newline='', encoding='latin1') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        # Count the lines in the file
        count = sum(1 for _ in open(tariff_file, 'r', encoding='latin1'))-1

        for idx, row in enumerate(reader, start=2):
            print(f"\r[LOG] {idx-1}/{count} - {row[0]}", end="")
            text = row[1]
            embedding = get_embedding(text, embedding_model)
            data.append([row[0], row[1], embedding])
        
        print(f"\n[LOG] {len(data)} tariff codes embedded.\n")
    print(f"[LOG] Saving {len(data)} embeddings...")

    with open('tariff.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

    print(f"done\n")

def get_top_matches(query, data, embedding_model, rag_count=50):
    query_embedding = get_embedding(query, embedding_model)
    scored = []
    for code, desc, embedding in data:
        score = cosine_similarity(query_embedding, embedding)
        scored.append((score, code, desc))
    top_matches = sorted(scored, reverse=True)[:rag_count]
    return [(code, desc) for score, code, desc in top_matches]

def find_best(query, codes, llm_model="llama3.2"):
    global verbose
    url = "http://localhost:11434/api/generate"
    prompt = (
        f"You are a tariff code expert. You need to find the best matches for a product named \"{query}\". "
        "The list of possible tariffs is:\n" + '\n'.join([f"{code} {desc}" for code, desc in codes]) +
        # "\nUsing this list of possible tariff codes, find the best matches and return the answer as a JSON array of codes."
        "\nUsing this list of possible tariff codes, find the best matches."
    )
    if verbose:
        print("[VERBOSE] LLM prompt:\n" + prompt)
    # format_schema = {
    #     "type": "array",
    #     "items": {
    #         "type": "object",
    #         "properties": {
    #             "code": {"type": "string"},
    #             "description": {"type": "string"}
    #         },
    #         "required": ["code", "description"]
    #     }
    format_schema = {
        "type": "array",
    }
    payload = {
        "model": llm_model,
        "prompt": prompt,
        "stream": False,
        # "format": format_schema
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()["response"]
    print(result)
    return result

def exec_query(query, embedding_model, rag_count=50, llm_model="llama3.2"):
    global verbose
    with open('tariff.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    top_matches = get_top_matches(query, data, embedding_model, rag_count)
    if verbose:
        for idx, (code, desc) in enumerate(top_matches, 1):
            print(f"{idx}. {code} {desc}")
    print("[LOG] Top matches retrieved. Calling find_best...")
    find_best(query, top_matches, llm_model)

def print_help():
    print("""
Usage: python tariff.py [OPTIONS] [QUERY]

Options:
  --help                 Show this help message and exit
  --embed                Generate embeddings from the tariff CSV file
  --tariffs <file>       Specify the source CSV file for tariff codes (default: tariff_database_2025.csv)
  --embedding-model <m>  Specify the embedding model to use (default: nomic-embed-text)
  --llm-model <m>        Specify the LLM model for final selection (default: llama3.2)
  --rag-count <n>        Number of top matches to retrieve using cosine similarity (default: 50)
  --verbose              Print the top matches before calling the LLM

Examples:
  python tariff.py --embed --tariffs mytariffs.csv --embedding-model my-embed-model
  python tariff.py "Pillow" --llm-model llama3.2 --rag-count 20 --verbose
""")

def main():
    global verbose
    if '--help' in sys.argv:
        print_help()
        return
    # Parse --tariffs <file> argument
    tariffs_file = 'tariff_database_2025.csv'
    if '--tariffs' in sys.argv:
        idx = sys.argv.index('--tariffs')
        if idx + 1 < len(sys.argv):
            tariffs_file = sys.argv[idx + 1]
    # Parse --model <model> argument
    embedding_model = 'nomic-embed-text'
    if '--embedding-model' in sys.argv:
        idx = sys.argv.index('--embedding-model')
        if idx + 1 < len(sys.argv):
            embedding_model = sys.argv[idx + 1]
    rag_count = 50
    if '--rag-count' in sys.argv:
        idx = sys.argv.index('--rag-count')
        if idx + 1 < len(sys.argv):
            try:
                rag_count = int(sys.argv[idx + 1])
            except ValueError:
                pass
    llm_model = "llama3.2"
    if '--llm-model' in sys.argv:
        idx = sys.argv.index('--llm-model')
        if idx + 1 < len(sys.argv):
            llm_model = sys.argv[idx + 1]
    if '--verbose' in sys.argv:
        verbose = True
    if len(sys.argv) > 1 and sys.argv[1] == "--embed":
        embed_all(tariff_file=tariffs_file, embedding_model=embedding_model)
    else:
        query = sys.argv[1] if len(sys.argv) > 1 else ''
        exec_query(query, embedding_model, rag_count, llm_model)

if __name__ == "__main__":
    main()
