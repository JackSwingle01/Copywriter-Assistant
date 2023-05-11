import streamlit as st
from custom_chains import make_parseOutline_chain, make_pageContent_chain
from vector_db import VectorDB
from web_search import web_search
# title:
st.title("Copywriter Assistant")
# get user input
institution_name = st.text_input("Enter institution name")
outline = st.text_area("Enter outline")
submit = st.button("Generate")

# instantiate chains
parse_outline = make_parseOutline_chain()  # llm chain to
generate_content = make_pageContent_chain()
pages = dict()  # store pages

db = VectorDB() # instantiate db

if outline and institution_name and submit:

    # run title chain:
    st.write("Ok, so first, lets get the page titles from the outline.")
    titles = parse_outline({"outline": outline})["page_titles"]

    # titles is a str: '[title1, title2, title3, ...]', so parse it
    titles = list(titles.strip("[]").split(","))
    st.write(f"Here they are: {[title for title in titles]}")
    st.write("Now, lets get the content for each page.")

    st.write("So for each page title, we'll get the relevant info from the docs and web, and then pass it to the content chain to generate the page content.")
    for title in titles:
        st.header(title)
        # get relevant info from docs:
        st.write(f"Getting relevant info from docs about {title} at {institution_name}...")
        docs_info = db.ask_db(f"{title} at {institution_name}")
        st.write(f"Here's the info we got:")
        st.code(docs_info)
        st.write("Now we'll get relevant info from the web.")
        # get relevant info from web:
        web_info = web_search(f"What is {title} at {institution_name}")
        st.write(f"Here's the info we got:")
        st.code(web_info)
        # combine info
        info = docs_info + web_info
        # pass info to content chain:
        st.write("Now we'll pass that info to the content chain to generate the page content.")
        content = generate_content.run(
            {"page_title": title, "relevant_info": info, "institution_name": institution_name})
        st.write(f"Here's the content we got:")
        st.code(content)
        # store page content
        pages[title] = content

    # display pages
    st.header("Here is the final result:")
    st.write("Pages:")
    for title, content in pages.items():
        st.header(title)
        st.write(content)

elif submit:
    st.write("Enter institution name and outline to generate pages.")

elif outline and institution_name:
    st.write("Click submit to generate pages.")
