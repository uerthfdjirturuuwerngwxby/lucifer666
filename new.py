import streamlit as st
from PyPDF2 import PdfReader
from io import BytesIO
import re

def main():
    st.sidebar.title("🙂💬 Text summarization")
    st.sidebar.markdown('''## About''')
    st.sidebar.markdown('''This app is an LLm chatbot ''')
    st.sidebar.markdown(''' --[about us](https://emojicopy.com/)''')
    st.sidebar.markdown('''--[contact us](https://emojicopy.com/) ''')

    st.sidebar.write('made by 🖕🫦')
    
    st.header("Chat with pdf 💬")
    file_type = st.selectbox("Select file type", ["Text", "PDF"])
    user_input = None
    
    if file_type == "Text":
        user_input = st.text_area("Enter your text here")
    elif file_type == "PDF":
        pdf_file = st.file_uploader("Upload PDF file", type=['pdf'])
        if pdf_file is not None:
            pdf_contents = pdf_file.read()
            user_input = extract_text_from_pdf(pdf_contents)

    num_lines = st.slider("Select number of lines for summary:", min_value=3, max_value=15, value=5, step=1)

    if st.button("Summarize"):
        if user_input:
            # Summarize text with user-selected number of lines
            summary = extractive_summarization(user_input, num_sentences=num_lines)
            
            st.write(f"Summary ({num_lines}-{num_lines+1} lines):")
            st.write(summary)
        else:
            st.warning("Please enter some text or upload a PDF file.")

    st.header("Ask Questions 🤔")
    question = st.text_input("Enter your question here:")
    if st.button("Get Answer"):
        if user_input:
            answer = find_answer(user_input, question)
            st.write("Answer:")
            st.write(answer)
        else:
            st.warning("Please enter some text or upload a PDF file.")

def extract_text_from_pdf(pdf_contents):
    pdf_file = BytesIO(pdf_contents)
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extractive_summarization(text, num_sentences=5):
    sentences = text.split(".")
    
    word_freq = {}
    for sentence in sentences:
        words = sentence.split()
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    sentence_scores = {}
    for sentence in sentences:
        score = sum([word_freq[word] for word in sentence.split()])
        sentence_scores[sentence] = score
    
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    
    summary = ". ".join(top_sentences)
    return summary

def find_answer(text, question):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    keywords = re.findall(r'\w+', question.lower())
    best_sentence = None
    max_matched_keywords = 0
    for sentence in sentences:
        matched_keywords = sum(keyword in sentence.lower() for keyword in keywords)
        if matched_keywords > max_matched_keywords:
            best_sentence = sentence
            max_matched_keywords = matched_keywords
    return best_sentence if best_sentence else "Sorry, I couldn't find an answer to your question."

if __name__=='__main__':
    main()
