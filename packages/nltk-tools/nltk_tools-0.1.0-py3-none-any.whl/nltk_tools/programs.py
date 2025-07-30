import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import pandas as pd
import numpy as np
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from sklearn.feature_extraction.text import TfidfVectorizer

def p1():
    """Tokenization, stopwords removal, stemming and lemmatization"""
    print("=== Program 1 ===")
    print("Performing tokenization, stopwords removal, stemming and lemmatization\n")
    
    # Download required NLTK data
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    
    text = """Natural language processing (NLP) is a field of computer science, artificial intelligence 
    and computational linguistics concerned with the interactions between computers and human (natural) 
    languages, and, in particular, concerned with programming computers to fruitfully process large 
    natural language corpora. Challenges in natural language processing frequently involve natural 
    language understanding, natural language generation (frequently from formal, machine- 
    readable logical forms), connecting language and machine perception, managing human-computer dialog 
    systems, or some combination thereof."""
    
    # Tokenization
    word_tokens = word_tokenize(text)
    print("Word tokens:", word_tokens)
    
    # Stopwords removal
    stop_words = set(stopwords.words('english'))
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    print("\nAfter stopwords removal:", filtered_sentence)
    
    # Stemming
    ps = PorterStemmer()
    print("\nStemming results:")
    for w in word_tokens[:10]:  # Showing first 10 for brevity
        print(w, " : ", ps.stem(w))
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    print("\nLemmatization results:")
    print("rocks :", lemmatizer.lemmatize("rocks"))
    print("corpora :", lemmatizer.lemmatize("corpora"))
    print("better :", lemmatizer.lemmatize("better", pos="a"))

def p2():
    """Parts of Speech tagging and Named entity recognition"""
    print("\n=== Program 2 ===")
    print("Performing POS tagging and Named Entity Recognition\n")
    
    # Download required NLTK data
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
    nltk.download('averaged_perceptron_tagger')
    
    sentence = "Apple is looking at buying U.K. startup for $1 billion."
    
    # POS Tagging
    tokens = word_tokenize(sentence)
    pos_tags = pos_tag(tokens)
    print("POS Tags:", pos_tags)
    
    # NER
    chunked = ne_chunk(pos_tags)
    print("\nNamed Entity Recognition:", chunked)

def p3():
    """Term Frequency and Inverse Document Frequency (TF-IDF)"""
    print("\n=== Program 3 ===")
    print("Calculating TF-IDF\n")
    
    corpus = [
        'data science is one of the most important fields of science',
        'this is one of the best data science courses',
        'data scientists analyze data'
    ]
    
    # Using sklearn's TfidfVectorizer
    print("Using sklearn's TfidfVectorizer:")
    tf_idf_model = TfidfVectorizer()
    tf_idf_vector = tf_idf_model.fit_transform(corpus)
    words_set = tf_idf_model.get_feature_names_out()
    df_tf_idf = pd.DataFrame(tf_idf_vector.toarray(), columns=words_set)
    print(df_tf_idf)
    
    # Manual calculation
    print("\nManual calculation:")
    words_set = set()
    for doc in corpus:
        words = doc.split(' ')
        words_set = words_set.union(set(words))
    
    n_docs = len(corpus)
    n_words_set = len(words_set)
    
    # Term Frequency
    df_tf = pd.DataFrame(np.zeros((n_docs, n_words_set)), columns=list(words_set))
    for i in range(n_docs):
        words = corpus[i].split(' ')
        for w in words:
            df_tf[w][i] = df_tf[w][i] + (1 / len(words))
    
    # IDF
    idf = {}
    for w in words_set:
        k = 0
        for i in range(n_docs):
            if w in corpus[i].split():
                k += 1
        idf[w] = np.log10(n_docs / k)
    
    # TF-IDF
    df_tf_idf_manual = df_tf.copy()
    for w in words_set:
        for i in range(n_docs):
            df_tf_idf_manual[w][i] = df_tf[w][i] * idf[w]
    
    print(df_tf_idf_manual)