# Search-Engine
Implementation of some parts of a search engine using Python programming language, Information Retrieval final course project, Spring 2019
## Part 1
At this stage of the project, you must fetch any news from the collection of input documents and take the necessary steps to create a reverse index. You must implement two cases with the following steps to index the collection of documents and build a dictionary:
- First case
1. Fetch news
2. Replace meaningless items such as numbers, html tags and punctuation marks such as question marks, exclamation marks, commas, etc. with a space.
3. Token extraction
4. Delete Stop words
5. Create reverse index
- Second case
1. Fetch news
2. Normalization
3. Token extraction
4. Stemming
5. Delete Stop words
6. Create reverse index ِ<br/>
<br/>
Examine the Zipf and Heaps rules on input documents, and compare the results of the two cases. <br/>
Consider the axes of the Zipf rule diagram log^rank, log^cf, and the axes of the Heaps rule diagram, log^T log^M. <br/>
## Part 2 <br/>
- At this phase, the data retrieval model should be able to rank search results based on relevance. The data retrieval model does this by modeling documents in the vector space. In this way, a numerical vector is extracted for each document, which is the representation of that document in the vector space. Then, having a query from the user, first take it to the vector space and then, using an appropriate similarity criterion, calculate the numerical vector distance of the query with all documents in the vector space, and finally sort the output results based on similarity. <br/>
- To represent documents in vector space, a numerical vector for each document will be calculated using the tf-idf method, and finally each document will be represented as a vector containing the weights of all the words in that document. <br/>
- Use the Index Elimination technique to represent documents in vector space to prevent overuse of space.<br/>
- Extract the query vector with the user query. Then try to find the documents that have the most similarity (least distance) to the input query using the similarity criterion. Then display them in similar order. Different distance criteria can be considered for this purpose, the simplest of which is the cosine similarity between the vectors that calculates the angle between them.

