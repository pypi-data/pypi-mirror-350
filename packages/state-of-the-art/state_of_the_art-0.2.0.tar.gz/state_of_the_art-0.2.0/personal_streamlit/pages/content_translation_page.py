import streamlit as st
from state_of_the_art.streamlit_app.utils.sidebar_utils import initialize_page
from state_of_the_art.tables.key_value_table import KeyValueTable
initialize_page()

from state_of_the_art.article_translation.article_translation_utils import cleanup_content, extract_article_content
from state_of_the_art.article_translation.article_translation_utils import translate_article
from state_of_the_art.article_translation.article_translation_utils import SiteSpecificConfig
from state_of_the_art.register_papers.website_content_extractor import WebsiteContentExtractor
from state_of_the_art.tables.article_translation_table import ArticleTranslationTable



content_name = st.text_input("Content name", value=st.query_params.get("content_name", "")) 
content = st.text_area("Content")

c1, c2 = st.columns([1,1])
with c1:
    translate_clicked = st.button("Translate")
with c2:
    regenerate = st.checkbox("Regenerate", value=st.query_params.get("regenerate", False))



article_translation_table = ArticleTranslationTable()
# check if url is already in table
if  translate_clicked:

    st.query_params["content_name"] = content_name


    # load existing translation
    translation = article_translation_table.get_translation_by_id(content_name)
    if translation and not regenerate:
        st.info("Article already translated")
        st.markdown(translation.merged_content)
        st.stop()

    with st.spinner("Translating..."):
        st.write("Getting content...")
        original_text = content

        text = ""
        for text_block in translate_article(original_text):
            text += text_block
            st.markdown(text_block)
        

        article_translation_table.add_article(url=content_name, original_content=original_text, merged_content=text)
