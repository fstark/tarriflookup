import csv
import requests
import json
import sys
import math

verbose = False
tariffs_db = []

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
    global verbose
    print("[LOG] Performing RAG...")
    query_embedding = get_embedding(query, embedding_model)
    scored = []
    for code, desc, embedding in data:
        score = cosine_similarity(query_embedding, embedding)
        scored.append((score, code, desc))
    top_matches = sorted(scored, reverse=True)[:rag_count]
    if verbose:
        print(f"    [LOG] Top matches:")
        for idx, (score, code, desc) in enumerate(top_matches, 1):
            print(f"    [LOG] {score:.4f} {idx}: {code} {desc}")
    return [(code, desc) for score, code, desc in top_matches]

# This finds the best matches, but returns the result as a free text
def find_best(query, codes, llm_model="llama3.2"):
    global verbose
    print(f"[LOG] Calling LLM {llm_model} for tariffs matches...")
    url = "http://localhost:11434/api/generate"
    prompt = (
        f"You are a tariff code expert. You need to find the best matches for a product named \"{query}\". "
        "The list of possible tariffs is:\n" + '\n'.join([f"{code} {desc}" for code, desc in codes]) +
        # "\nUsing this list of possible tariff codes, find the best matches and return the answer as a JSON array of codes."
        "\nUsing this list of possible tariff codes, find the best matches."
    )
    if verbose:
        print(f"    [LOG] Using prompt:\n\n\n{prompt}\n\n\n" )
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
    if verbose:
        print(f"    [LOG] LLM response:\n\n\n{result}\n\n\n")
    return result

# This takes a a free-form response and format it
def format_response(query, text_response, llm_model="llama3.2"):
    global verbose
    print(f"[LOG] Calling LLM {llm_model} for formatting...")
    url = "http://localhost:11434/api/generate"
    prompt = (
        f"parse the text between '------' and '------'. " +
        f"In it there is a list of tariffs code that are good matches for {query}. " +
        f"Prints them as a JSON array, containing only the codes. Output only the json nothing else. If there are no suitable codes, return an empty array." +
        f"\n------\n{text_response}\n------\n"
    )
    if verbose:
        print(f"    [LOG] Using prompt:\n\n\n{prompt}\n\n\n" )
    format_schema = {
        "type": "array",
        "items": { "type": "string" }
    }
    payload = {
        "model": llm_model,
        "prompt": prompt,
        "stream": False,
        "format": format_schema
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()["response"]
    if verbose:
        print(f"    [LOG] LLM response:\n\n\n{result}\n\n\n")
    # Parse the result as JSON and return the object
    return json.loads(result)

def load_tariffs_db():
    global verbose
    global tariffs_db
    print("[LOG] Loading embedding database...")
    with open('tariff.json', 'r', encoding='utf-8') as f:
        tariffs_db = json.load(f)
    if verbose:
        print(f"    [LOG] Loaded {len(tariffs_db)} tariff codes")

def exec_query(query, embedding_model, rag_count=50, llm_model="llama3.2", llm_model_format="llama3.2"):
    global verbose
    global tariffs_db
    top_matches = get_top_matches(query, tariffs_db, embedding_model, rag_count)
    text_response = find_best(query, top_matches, llm_model)
    codes = format_response(query, text_response, llm_model_format)
    # Build array of {"code": code, "description": description} for codes found in tariffs_db
    print("[LOG] Completing answer...")
    code_to_desc = {row[0]: row[1] for row in tariffs_db}
    result = []
    for code in codes:
        if code in code_to_desc:
            result.append({"code": code, "description": code_to_desc[code]})
        else:
            if verbose:
                print(f"    [LOG] Unknow code '{code}'")
    print(f"[LOG] Matched {len(result)} codes:")
    for idx, item in enumerate(result, 1):
        print(f"[LOG] {idx}: {item['code']} {item['description']}")
    return result

def print_help():
    print("""
Usage: python tariff.py [OPTIONS] [QUERY]

Options:
  --help                 Show this help message and exit
  --embed                Generate embeddings from the tariff CSV file
  --tariffs <file>       Specify the source CSV file for tariff codes (default: tariff_database_2025.csv)
  --embedding-model <m>  Specify the embedding model to use (default: nomic-embed-text)
  --llm-model <m>        Specify the LLM model for final selection (default: llama3.2)
  --llm-model-format <m> Specify the LLM model for formatting output (default: llama3.2)
  --rag-count <n>        Number of top matches to retrieve using cosine similarity (default: 50)
  --verbose              Print the top matches before calling the LLM

Examples:
  python tariff.py --embed --tariffs mytariffs.csv --embedding-model my-embed-model
  python tariff.py "Pillow" --llm-model llama3.2 --llm-model-format llama3.2 --rag-count 20 --verbose
""")

def main():
    global verbose
    global tariffs_db
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
    llm_model_format = "llama3.2"
    if '--llm-model-format' in sys.argv:
        idx = sys.argv.index('--llm-model-format')
        if idx + 1 < len(sys.argv):
            llm_model_format = sys.argv[idx + 1]
    if '--verbose' in sys.argv:
        verbose = True
    if len(sys.argv) > 1 and sys.argv[1] == "--embed":
        embed_all(tariff_file=tariffs_file, embedding_model=embedding_model)
    else:
        load_tariffs_db()
        query = sys.argv[1] if len(sys.argv) > 1 else ''
        result = exec_query(query, embedding_model, rag_count, llm_model, llm_model_format)
        print( result )

if __name__ == "__main__":
    main()
