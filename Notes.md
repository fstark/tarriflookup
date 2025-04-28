Create a python command line tariff.py that reads the tariff_database_2025.csv csv file and prints the first two column (starting line 2)

print the line number too

527 04061018 Fresh (unripened/uncured) blue-mold cheese, cheese/subs for cheese cont or proc fr blue-mold cheese, not subj to Ch4 US note 17 or GN15
Traceback (most recent call last):
File "/home/fred/Development/tarriflookup/tariff.py", line 11, in <module>
main()
File "/home/fred/Development/tarriflookup/tariff.py", line 7, in main
for idx, row in enumerate(reader, start=2):
File "<frozen codecs>", line 322, in decode
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa2 in position 2925: invalid start byte


make the change

using locally running ollama via REST API, embed the second column and print the resulting vector

instead of printing them, store them in an array of array of 3 columns (first is the first column, second is the second column, third is the embedding). Save this array in json in the file tariff.json

Do this operation if the first parameter of the script is "--embed".
If the first parameter is not embed, call it "query" and print it.

put embeed in its own function. put the printing of query in its own function too.

in the print query, do the following:

embed the query
open and read the "tariff.json" file
compute the cosine of the embeddings and print the top 10 matching items in order (codes + description)

print the top 50, not the top 10


split the query in two functions. One retreives the 50 best matches (code identical to the one we have). the second is called with the query and the array of codes and is called find_best. For now, it return ""

Implement find best by calling a local ollama model via the REST API. The model is "llama3.2". The prompt is: "You are a tariff code expert. You need to find the best matches for a product named "QUERY". The list of possible tariffs is:". Append a list with the code and the names. Replace QUERY by the user query. Print the response. Use stream=False in the ollama call.

rename "print_query" into "exec_query". After getting the matches, call find_best. Add a log after the top matches.

Remove the printing of the top 50 unless there is a "--debug" flag passed to the script









