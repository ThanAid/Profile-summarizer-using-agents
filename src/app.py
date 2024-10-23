import streamlit as st
from dotenv import load_dotenv
from profile_summarizer import summarize_with

load_dotenv()


def sidebar():
    """Sidebar"""
    with st.sidebar:
        st.image("src/static/ai_search.png", width=300)
        st.title("Profile Summarizer")
        st.write(
            """
        This project leverages advanced language models to generate concise summaries and interesting facts about individuals based on their LinkedIn profiles. 
        """
        )


def search_person():
    st.title("Search Person")
    name = st.text_input("Enter the name of the person you would like to search")
    if st.button("Search"):
        placeholder = st.empty()
        placeholder.write(f"Searching for {name}...")
        # Call the summarizer function here
        summary, profile_pic_url = summarize_with(name)
        placeholder.empty()

        # display the image
        st.image(profile_pic_url, width=300)
        st.subheader("Summary")
        st.write(summary.to_dict()["summary"])
        st.subheader("Interesting Facts")
        for fact in summary.to_dict()["facts"]:
            st.markdown(f"- {fact}")


def main():
    search_person()


if __name__ == "__main__":
    sidebar()
    main()
