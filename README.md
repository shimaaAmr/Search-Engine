![image](https://github.com/hagerkha/search-engine-/assets/131220220/d1e4eaa1-ed87-4fd3-bc29-5c84535c7644)
![image](https://github.com/hagerkha/search-engine-/assets/131220220/589cc6f7-e0c9-4572-82a1-ccfcc218f507)


Project Description: Implementing a Search Engine with Web Crawling, Indexing, Searching, and Ranking
This project aims to develop a robust search engine by implementing web crawling, indexing, searching, and ranking functionalities using the MapReduce algorithm. The following sections describe each task in detail:

1. Web Crawler
The first task involves developing a web crawler to collect approximately 100,000 news pages, starting with a seed list of 20 news websites. The crawler will:

Initialize with a Seed List: Begin crawling from the initial list of 20 seed news pages.
Extract Hyperlinks: Automatically extract all hyperlinks from each crawled page using HTML parsing libraries such as BeautifulSoup and urllib, without utilizing Scrapy or similar packages.
Recursive Crawling: Continue crawling by following the extracted hyperlinks to discover and download additional news pages.
2. Inverted Index Construction Using MapReduce
Next, we will construct an inverted index for the collected data using the MapReduce framework:

Tokenization: Tokenize the text content of each webpage to extract unique terms (tokens).
Mapping Phase: In the map phase, emit each token along with the document ID in which it appears.
Shuffling and Sorting: Group the tokens by their values, effectively collating all occurrences of each token.
Reducing Phase: In the reduce phase, aggregate the document IDs for each token to produce a list of indices (document IDs) where the token appears.
Output: Generate an inverted index where every unique token maps to a list of document indices.
3. Single Word Search Using MapReduce
Implement a search functionality to find documents containing a single word using the inverted index with MapReduce:

Mapping Phase: Emit the search term and scan the inverted index to retrieve the corresponding list of document IDs.
Shuffling and Sorting: Ensure the results are grouped by the search term.
Reducing Phase: Collect and output the list of document IDs where the search term appears.
4. Ranking Results Using TF-IDF with MapReduce
To rank the search results, we will implement the TF-IDF (Term Frequency-Inverse Document Frequency) scheme using MapReduce:

Term Frequency Calculation (TF): Use MapReduce to count the frequency of the search term in each document.
Document Frequency Calculation (DF): Use MapReduce to count the number of documents containing the search term.
TF-IDF Computation: Combine the TF and DF values to compute the TF-IDF score for each document. This involves:
Mapping Phase: Emit intermediate values for TF and DF calculations.
Reducing Phase: Aggregate the values to produce the final TF-IDF scores for ranking.
5. Ranking Results Using PageRank with MapReduce
Finally, we will implement the PageRank algorithm to further rank the search results using MapReduce:

Initialize PageRank Values: Assign an initial PageRank value to each document.
Mapping Phase: Distribute the PageRank value of each document to its outbound links.
Shuffling and Sorting: Group the contributions to each document's PageRank.
Reducing Phase: Sum the contributions to compute the updated PageRank for each document.
Iterative Computation: Repeat the MapReduce process iteratively to refine the PageRank values until convergence.
Final Ranking: Combine the TF-IDF scores and PageRank values to produce a final ranked list of search results.
