import PyPDF2
from sklearn.feature_extraction.text import CountVectorizer
import logging



# Check if the content is relevant to the subject
def is_content_relevant(text, keywords):
    vectorizer = CountVectorizer(vocabulary=keywords)
    vector = vectorizer.transform([text])
    return vector.nnz > 0

subject_keywords = {
    "Physics": ["force", "energy", "momentum", "quantum", "electromagnetic", "thermodynamics"],
    "Chemistry": ["atom", "molecule", "reaction", "compound", "chemical", "organic"],
    "Biology": ["cell", "organism", "ecosystem", "genetics", "evolution", "anatomy"]
}

