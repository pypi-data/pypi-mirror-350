import streamlit as st
from state_of_the_art.streamlit_app.utils.sidebar_utils import initialize_page
from state_of_the_art.tables.key_value_table import KeyValueTable
initialize_page()

from state_of_the_art.article_translation.article_translation_utils import cleanup_content, extract_article_content
from state_of_the_art.article_translation.article_translation_utils import translate_article
from state_of_the_art.article_translation.article_translation_utils import SiteSpecificConfig
from state_of_the_art.register_papers.website_content_extractor import WebsiteContentExtractor
from state_of_the_art.tables.article_translation_table import ArticleTranslationTable

@st.dialog("Set cookie")
def set_cookie():
    st.markdown("""
                [Get your cookie here](https://www.spiegel.de/fuermich/)
    """)
    key_value_table = KeyValueTable()

    current_value = key_value_table.get_value("der_spiegel_cookie")
    if not current_value:
        current_value = ""

    new_value = st.text_area("Cookie", value=current_value)

    with st.expander("See new value"):
        st.write("new_value: '", new_value, "'")


    if st.button("Save"):
        key_value_table.update_or_create("der_spiegel_cookie", new_value)
        st.success("Cookie saved")


translation_url = st.text_input("Translate url", value=st.query_params.get("translation_url", ""))

c1, c2, c3, c4 = st.columns([1,1 ,1, 1])
with c1:
    translate_clicked = st.button("Translate")
with c2:
    regenerate = st.checkbox("Regenerate", value=st.query_params.get("regenerate", False))
with c3:
    load_content = st.button("Load website content")
with c4:
    if st.button("Set cookie"):
        set_cookie()

key_value_table = KeyValueTable()
cookie = key_value_table.get_value("der_spiegel_cookie")

if load_content:
    text, title = WebsiteContentExtractor().get_website_content(translation_url, cookie)
    text = cleanup_content(text)
    st.write(text)
    st.stop()


article_translation_table = ArticleTranslationTable()
# check if url is already in table
if  translate_clicked or st.query_params.get("translation_url", None):

    st.query_params["translation_url"] = translation_url


    # load existing translation
    translation = article_translation_table.get_translation_by_id(translation_url)
    if translation and not regenerate:
        st.info("Article already translated")
        st.markdown(translation.merged_content)
        st.stop()

    with st.spinner("Translating..."):
        st.write("Getting content...")
        original_text = extract_article_content(translation_url)

        text = ""
        for text_block in translate_article(original_text):
            text += text_block
            st.markdown(text_block)
        

        article_translation_table.add_article(url=translation_url, original_content=original_text, merged_content=text)
