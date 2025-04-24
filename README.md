# tarriflookup

Install ollama and add models 'nomic-embed-text' and 'llama3.2'

Create python venv (``pythom -m venv venv`` + ``source venv/bin/activate``)

Install dependencies (``pip install -r requirements.txt``)

Create the embedding file:

``python tariff.py --embed``

Query with:

``python tariff.py "Lego Star Wars figurines"``

result should be:

```
[LOG] Top 50 matches retrieved. Calling find_best...
Here is the list of tariff codes that match "Lego Star Wars figurines":

1. 95030000 - Toys, including riding toys o/than bicycles, puzzles, reduced scale models
2. 95051040 - Arts. for Christmas festivities (o/than ornaments & nativity scenes) nesoi, of plastics
3. 95082400 - Amusement park rides, motion simulators and moving theaters; parts and accessories thereof
4. 95051010 - Arts. for Christmas festivities, ornaments of glass
5. 71162035 - Semiprecious stone (except rock crystal) figurines
```
