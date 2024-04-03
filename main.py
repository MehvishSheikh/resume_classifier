import streamlit as st
import pickle
import re
import PyPDF2
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the TF-IDF vectorizer
with open('tfidf.pkl', 'rb') as f:
    loaded_tfidf = pickle.load(f)

# Load the classifier
with open('clf.pkl', 'rb') as f:
    loaded_clf = pickle.load(f)

# Define function to clean resume text
def clean_text(text):
    # Remove extra spaces
    cleaned_text = re.sub(r'\s+', ' ', text)
    return cleaned_text

# Define the main function to classify the resume
def classify_resume(resume_file):
    # Initialize text variable
    text = ""

    # Check file type and read content
    if resume_file.type == 'application/pdf':
        # Read PDF file
        pdf_reader = PyPDF2.PdfFileReader(resume_file)
        for page_num in range(pdf_reader.numPages):
            text += pdf_reader.getPage(page_num).extractText()
    elif resume_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        # Read DOCX file
        doc = Document(resume_file)
        for para in doc.paragraphs:
            text += para.text + '\n'

    # Clean the text
    cleaned_text = clean_text(text)

    # Transform the cleaned text using the loaded TF-IDF vectorizer
    resume_tfidf = loaded_tfidf.transform([cleaned_text])

    # Predict the category of the resume using the loaded classifier
    predicted_category = loaded_clf.predict(resume_tfidf)[0]

    return predicted_category

# Streamlit UI
def main():
    st.title("Resume Classifier")

    # File uploader widget
    uploaded_file = st.file_uploader("Upload a resume (PDF or Word)", type=['pdf', 'docx'])

    if uploaded_file is not None:
        # Display the uploaded file
        st.write("Uploaded resume:")
        st.write(uploaded_file)

        # Classify the resume
        classification_result = classify_resume(uploaded_file)

        # Display the classification result
        st.write("Classification result:")
        st.write("Predicted Category:", classification_result)

if __name__ == "__main__":
    main()
