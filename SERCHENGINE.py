from flask import Flask, render_template, request
import pandas as pd
import re
from collections import Counter, defaultdict
import numpy as np

app = Flask(__name__)

# Read data files
PR = pd.read_csv("output pr", sep="\t", header=None)
with open("inverted index out", "r", encoding="utf-8") as f:
    inverted_index = f.read()
with open("input pr.txt", "r", encoding="utf-8") as f2:
    links = f2.readlines()

# Read documents for TF-IDF
documents = [line.strip() for line in links]


# Calculate term frequency (TF)
def calculate_tf(documents):
    tf = []
    for doc in documents:
        tokens = doc.split()
        tf_dict = Counter(tokens)
        doc_len = len(tokens)
        for term in tf_dict:
            tf_dict[term] /= doc_len
        tf.append(tf_dict)
    return tf


# Calculate inverse document frequency (IDF)
def calculate_idf(documents):
    idf = defaultdict(float)
    total_docs = len(documents)
    for doc in documents:
        tokens = set(doc.split())
        for term in tokens:
            idf[term] += 1
    for term in idf:
        idf[term] = np.log(total_docs / (idf[term] + 1))
    return idf


# Calculate TF-IDF
def calculate_tfidf(documents):
    tf = calculate_tf(documents)
    idf = calculate_idf(documents)
    tfidf = []
    for doc_tf in tf:
        doc_tfidf = {}
        for term, tf_val in doc_tf.items():
            doc_tfidf[term] = tf_val * idf[term]
        tfidf.append(doc_tfidf)
    return tfidf


tfidf_documents = calculate_tfidf(documents)


# Function to perform search using inverted index
def search_inverted_index(s_word, i_index_f, links_f):
    urls = []
    flag = 1

    start = i_index_f.find(s_word)
    if start == -1:
        flag = 0
    else:
        end = start + i_index_f[start:].find("\n")
        line = i_index_f[start:end]
        content = line.split()
        num = [m.end() for m in re.finditer("file", content[1])]
        page_num = []
        for n in num:
            page_num.append(content[1][n : n + content[1][n:].find(":")])

        link_counter = Counter()
        for z in page_num:
            s_link = links_f[int(z) + 1].find(" ") + 1
            e_link = links_f[int(z) + 1].find("\n")
            link = links_f[int(z) + 1][s_link:e_link]
            link_counter[link] += links_f[int(z) + 1].count(s_word)

        sorted_links = sorted(link_counter.items(), key=lambda x: x[1], reverse=True)
        urls = [link[0] for link in sorted_links]

    return urls, flag


def search_tfidf(s_word, i_index_f, links_f, tfidf_documents):
    urls = []
    tfidf_scores = []
    flag = 1

    start = i_index_f.find(s_word)
    if start == -1:
        flag = 0
    else:
        end = start + i_index_f[start:].find("\n")
        line = i_index_f[start:end]
        content = line.split()
        num = [m.end() for m in re.finditer("file", content[1])]
        page_num = []
        for n in num:
            page_num.append(content[1][n : n + content[1][n:].find(":")])

        for z in page_num:
            s_link = links_f[int(z) + 1].find(" ") + 1
            e_link = links_f[int(z) + 1].find("\n")
            url = links_f[int(z) + 1][s_link:e_link]
            urls.append(url)  # Append URL

            # Calculate TF-IDF score for the word in the document
            tfidf_score = tfidf_documents[int(z)].get(s_word, 0)
            tfidf_scores.append(tfidf_score)

        # Sort URLs by TF-IDF scores
        combined_scores = [(url, tfidf) for url, tfidf in zip(urls, tfidf_scores)]
        combined_scores_sorted = sorted(
            combined_scores, key=lambda x: x[1], reverse=True
        )
        urls = [score[0] for score in combined_scores_sorted]

    return urls, tfidf_scores, flag


def search_page_rank(s_word, PR_f, i_index_f, links_f):
    urls = []
    page_ranks = []
    flag = 1

    start = i_index_f.find(s_word)
    if start == -1:
        flag = 0
    else:
        end = start + i_index_f[start:].find("\n")
        line = i_index_f[start:end]
        content = line.split()
        num = [m.end() for m in re.finditer("file", content[1])]
        page_num = []
        for n in num:
            page_num.append(content[1][n : n + content[1][n:].find(":")])

        page_weight = {}
        for x in page_num:
            page_weight[x] = float(PR_f[PR_f[0] == int(x)][1])

        page_weight_sorted = sorted(
            page_weight.items(), key=lambda x: x[1], reverse=True
        )
        the_pages = dict(page_weight_sorted)

        for z in the_pages.keys():
            s_link = links_f[int(z) + 1].find(" ") + 1
            e_link = links_f[int(z) + 1].find("\n")
            url = links_f[int(z) + 1][s_link:e_link]
            page_ranks.append(the_pages[z])  # Append page rank score
            urls.append(url)  # Append URL

    return urls, page_ranks, flag


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/search", methods=["POST", "GET"])
def take_input():
    is_get_request = False

    if request.method == "POST":
        input_text = request.form["query"]
    elif request.method == "GET":
        is_get_request = True
        input_text = request.args.get("query")

    input_words = input_text.split()

    inverted_index_results = []
    page_rank_results = []
    tfidf_results = []
    all_flags = []

    for word in input_words:
        result, flag = search_inverted_index(word, inverted_index, links)
        inverted_index_results.extend(result)
        all_flags.append(flag)

    for word in input_words:
        result, _, flag = search_page_rank(word, PR, inverted_index, links)
        page_rank_results.extend(result)
        all_flags.append(flag)

    for word in input_words:
        result, _, flag = search_tfidf(word, inverted_index, links, tfidf_documents)
        tfidf_results.extend(result)
        all_flags.append(flag)

    if 0 in all_flags:
        return render_template(
            "search_results.html", 
            page_rank_results=None, 
            inverted_index_results=None,
            tfidf_results=None
        )
    else:
        # Display results
        return render_template(
            "search_results.html",
            inverted_index_results=inverted_index_results,
            page_rank_results=page_rank_results,
            tfidf_results=tfidf_results,
        )


if __name__ == "__main__":
    app.run(debug=True)

