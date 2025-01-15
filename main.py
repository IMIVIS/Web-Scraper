import streamlit as st
from scrape import (scrape_website, clean_body_content, extract_body_content, split_dom_content)
from parse import parse_with_ollama

st.title("AI Web Scraper")
url = st.text_input("Enter the URL of the website to scrape:")

if st.button("Scrape"):
    st.write("Scraping the website...")
    result = scrape_website(url)
    body_content = extract_body_content(result)
    clean_content = clean_body_content(body_content)

    st.session_state.dom_content = clean_content

    with st.expander("View Dom Content"):
        st.text_area("Dom Content", clean_content, height = 300)

if "dom_content" in st.session_state:
    parse_description = st.text_area("Decribe what you want to parse:")

    if st.button("Parse Content"):
        st.write("Parsing Content...")

        dom_chunks = split_dom_content(st.session_state.dom_content)
        result = parse_with_ollama(dom_chunks, parse_description)
        st.write(result)
