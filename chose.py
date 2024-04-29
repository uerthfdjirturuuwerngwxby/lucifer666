import streamlit as st
from PyPDF2 import PdfReader
import spacy

# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

def read_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def answer_question(text, question):
    # Process the text and question using spaCy
    doc = nlp(text)
    question_doc = nlp(question)

    # Find the most relevant sentence in the text to the question
    sentences = [sent for sent in doc.sents]
    max_similarity = -1
    best_sentence = None
    for sent in sentences:
        similarity = sent.similarity(question_doc)
        if similarity > max_similarity:
            max_similarity = similarity
            best_sentence = sent

    # Return the best sentence as the answer
    return best_sentence.text if best_sentence else "Sorry, I couldn't find an answer to your question."

def main():
    st.title("Ask Questions about the Uploaded PDF")

    # File upload
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file is not None:
        # Read the contents of the uploaded PDF
        text = read_pdf(uploaded_file)
        
        st.write("File content:")
        st.write(text)

        # Ask the user for a question
        question = st.text_input("Ask a question about the PDF:")

        if st.button("Ask"):
            if question:
                # Answer the question based on the content of the PDF
                answer = answer_question(text, question)
                st.write("AI's Answer:")
                st.write(answer)
            else:
                st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
