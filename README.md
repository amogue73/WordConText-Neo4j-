# 1. Introduction

When learning a language, perhaps the most important aspect is acquiring its vocabulary. Only when the lexicon of the new language is known can sentences be constructed to understand and communicate information. There are various tools that help learners acquire new vocabulary in another language. A very common one is translation software capable of translating words from or into the user's native language. Another useful tool for more advanced learners is a traditional dictionary.

These tools provide the exact meaning of a word. However, they are not sufficient on their own to ensure proper vocabulary acquisition. They must be accompanied by example sentences in which the words are used. These sentences provide contexts that learners need to understand in order to correctly place new vocabulary. The context of a word is its **semantic field**, and each language has its own semantic fields. In other words, each language has its own criteria for determining which words are related to one another and which have no elements in common. These relationships are largely shaped by cultural factors.

Thanks to the **Word2Vec** technique, it is possible to automatically determine the semantic similarity between words in a text or even across an entire language. The objective of this technique is to create an **embedding**, that is, a numerical vector for each word, such that words belonging to the same semantic field have vectors that, through a simple mathematical operation, are found to be similar.

On the other hand, **graph-oriented databases** allow relational searches to be performed much more efficiently than in traditional SQL-based systems. This efficiency comes from the way data is internally stored. These databases typically contain a large number of relationships, making it natural to interpret the entire database as a graph, where each vertex represents an element and edges represent relationships between them.

In this project, a prototype application has been developed that leverages a set of the **10,000 most frequent Spanish word forms**, together with their embeddings and approximately **17,000 sentences**, to create a graph database capable of performing fast semantic field searches. Words are connected to the sentences that contain them. These sentences provide examples of how words are used alongside other words within the same semantic field.

# 2. Methodology

This section describes how the prototype was developed, from the tools and datasets used as a starting point to the software implemented for data processing and database visualization.

## 2.1. Tools Used

This section presents the software tools employed in the project, as well as the datasets from which the words, embeddings, and sentences were obtained.

### Software Tools

**Neo4j**
A graph database management system. It includes its own query language, called **Cypher**, which belongs to the Graph Query Language (GQL) family.

**Neo4j Aura**
A cloud-based graph platform provided as a service. It includes several Neo4j tools and services. First, it provides a console for importing and interacting with data. Second, it offers a graphical interface with powerful visualization capabilities for explored graphs.

**Cypher**
Neo4j’s native database query language. Originally developed exclusively for Neo4j, it now aims to become a standard GQL language.

**Python**
Used to process datasets and transform them into CSV format so they could be imported into Neo4j Aura through Cypher.

**Google Drive**
Used as the source from which CSV files are imported into Neo4j Aura.

### Datasets

A total of three datasets were used, each serving a specific purpose.

**The list of the 10,000 most frequent Spanish word forms**, provided by the Royal Spanish Academy (RAE). This dataset contains the most frequent Spanish word forms together with their usage frequencies.

**A set of Spanish word embeddings.** This dataset was combined with the previous one so that only words appearing in both datasets were selected. The goal was for each word to include both its frequency information and its embedding. After the merge, a total of **9,999 words** were retained.

**A free sample of a Spanish-language corpus.** This corpus was used to extract a total of **17,102 sentences**.

Regarding the `embeddings.csv` dataset, it was created using the **Skip-Gram architecture** together with the **Negative Sampling** technique. The process can be broken down into the following steps:

### 1. Corpus Preprocessing

A Spanish corpus containing **120 million words** was used. These words were collected directly from Wikipedia articles and therefore contained many HTML-related elements that needed to be removed, such as tags.

The first step was therefore to eliminate these elements, which would otherwise interfere with training. Next, punctuation marks were converted into tokens so that they would function similarly to words. For example, `,` becomes `<COMMA>` and `.` becomes `<DOT>`.

After these steps, the resulting corpus contained **117.8 million words**, of which **279,000 were unique**. Each word was assigned its frequency of occurrence. This information was useful for removing some occurrences of very frequent words, making training more efficient and reducing execution time.

The probability used to discard occurrences of highly frequent words is defined as:

$$
P(w_i) = 1 - \sqrt{\frac{t}{f(w_i)}}
$$

where:

* (t) is a threshold parameter.
* (f(w_i)) is the frequency of the word (w_i) in the dataset.

### 2. Batch Preparation

Training batches were then prepared. For each batch, a random number (R) in the range ([1,5]) was selected. This value determines how many preceding and following words around the central word are included as context.

### 3. Model Definition

The Word2Vec model used for training was defined. In this project, the **Skip-Gram model with Negative Sampling** was employed to speed up the training process.

### 4. Validation

A similarity function was defined to verify that the embeddings were learning the semantic relationships between words. The similarity function is:

$$
\text{similarity} = \cos(\theta) = \frac{\vec{a} \cdot \vec{b}}{|\vec{a}|,|\vec{b}|}
$$

where:

* (\cdot) denotes the dot product of two vectors.
* The result lies within the interval ([-1,1]).

The closer the value is to **1**, the greater the semantic similarity between the words represented by embeddings (\vec{a}) and (\vec{b}).

### 5. Training

Finally, the model was trained. The training process was divided into **eight epochs**. During training, both the model loss and several examples of semantic fields were monitored. The latter was done by observing which words obtained the highest similarity values with respect to a set of predefined words.

## 2.2. Implemented Software

This section presents the software components developed for the project and their respective functions.

### `freq_txt_to_csv.py`

This program takes the files `10k_formas.txt`, `embeddings.csv`, and the auxiliary file `vocab_to_int.pickle`, and generates the file `emb_10k.csv`.

This output file contains the words that will be uploaded to the database. For each word, the file stores:

* Its normalized frequency value.
* Its embedding vector.

### `preprocessing.py`

This program processes the file `text.txt` and extracts the sentences contained within it.

Its operation is as follows:

1. The file is read character by character.
2. Whenever an uppercase letter is encountered, a new sentence is assumed to begin.
3. Subsequent characters are added to the current sentence until a period (`.`) is found.
4. At that point, the sentence is considered complete.
5. The extracted sentences are written to the file `frases.txt`.

### `frases_to_csv.py`

This program reads all sentences from the file `frases.txt`.

Only a subset of the sentences is retained according to the following criteria:

* Only one quarter of the total sentences is selected.
* Only sentences with a length between 40 and 150 characters are considered.

The selected sentences are written to the file `frases1.csv`, which is later used to create the **Sentence** nodes in the graph database.

### `cypher_queries.txt`

This file contains all Cypher queries used throughout the project, including:

* Data import queries.
* Graph visualization queries.
* Queries used to explore and interact with the database.

## 2.3. Development in Neo4j

Using the tools, datasets, and generated files described in the previous section, the work was implemented within the Neo4j Aura platform.

Neo4j Aura provides a free permanent database instance with the following limits:

* 200,000 nodes.
* 400,000 relationships.

These limits were sufficient for the prototype developed in this project.

### Data Import

Once the database instance is created, the data must be imported. In this project, the data files were imported from Google Drive. The following operations were performed through the Neo4j console:

#### 1. Creation of Word Nodes

The file containing the words was loaded, and nodes of type **Word** were created.

Each Word node stores:

* The word itself.
* Its frequency value.

In addition, a **Vector Index** was created using the word embeddings, allowing similarity searches to be performed efficiently.

#### 2. Creation of Sentence Nodes and Relationships

The file containing the sentences was loaded, and nodes of type **Sentence** were created.

Relationships of type **CONTAINS** were also generated.

A Sentence node is connected to a Word node whenever the exact word appears in that sentence.

#### 3. Querying the Database

At this stage, all desired queries can be executed on the database.

To make the system more accessible and eliminate the need for users to know Cypher, the **Explore** tool was used. Explore is a version of **Neo4j Bloom** that provides an expressive graphical interface for exploring and interacting with graph data.

### Parameterized Natural-Language Queries

Within the Explore tool, specifically in the **Perspective Designer**, Cypher queries can be stored and associated with natural-language expressions containing parameters.

For example, suppose we want a query that displays:

* The 10 words most similar to *tree*.
* The sentences containing at least two of those related words.

The corresponding Cypher query can be saved under the natural-language template:

```
$num related words to $word
```

where:

* `$num` is a numeric parameter.
* `$word` is the target word.

For the example above, the parameters would be:

```
$num = 10
$word = "tree"
```

This allows users to perform sophisticated graph queries through simple natural-language commands.

### Frequency-Based Node Coloring

Another feature provided by the Explore tool is the ability to modify node colors according to a numerical attribute.

This functionality was used to visually represent word frequency:

* More frequent words are displayed with darker shades.
* Less frequent words appear with lighter shades.

As a result, users can quickly identify the relative frequency of words directly from the graph visualization.
