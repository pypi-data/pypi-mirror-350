import os
from state_of_the_art.image_processing.images_extractor import ImagesExtractor
from state_of_the_art.image_processing.image_inference import ImageInference
from state_of_the_art.paper.papers_data_loader import PapersLoader
from state_of_the_art.streamlit_app.utils.paginator import paginator
from state_of_the_art.streamlit_app.utils.sidebar_utils import initialize_page
from state_of_the_art.image_processing.image_feeddback_table import ImageFeedbackTable
initialize_page()
from datetime import datetime, timedelta
from state_of_the_art.config import config

import streamlit as st

st.title("Image Evaluator")

NUMBER_OF_DAYS_TO_LOOK_BACK = 14
MAX_PAPERS_TO_RENDER = 10
MAX_WIDTH = 1000

date_from = st.date_input("Date from", value=datetime.now() - timedelta(days=NUMBER_OF_DAYS_TO_LOOK_BACK))
date_to = st.date_input("Date to", value=datetime.now())
# add a toggle for the sort order
best_first = True
best_first = st.toggle("Best / Worst First", value=best_first)


@st.cache_data
def load_data(input_parameters: dict):
    papers_df = PapersLoader().load_between_dates(input_parameters['date_from'], input_parameters['date_to'])
    st.write('Found {} papers'.format(len(papers_df)))
    all_papers = PapersLoader().df_to_papers(papers_df)
    all_papers = all_papers[:MAX_PAPERS_TO_RENDER]

    images_with_paper = {}
    image_extractor = ImagesExtractor()
    image_inference = ImageInference()
    for paper in all_papers:
        with st.spinner('Extracting images for {}'.format(paper.arxiv_id)):
            images = image_extractor.extract_images_from_paper(paper=paper, skip_if_folder_exists=True)
            images_and_paper = {image: {'paper': paper, 'predicted_score': image_inference.predict_image(image)} for image in images}

            images_with_paper.update(images_and_paper)

    # sort image by predicted score
    reverse = input_parameters['best_first']
    images_with_paper = sorted(images_with_paper.items(), key=lambda x: x[1]['predicted_score'], reverse=reverse)
    return images_with_paper


images_with_paper = load_data({
    'date_from': date_from,
    'date_to': date_to,
    'best_first': best_first
})
for k, v in paginator(label="Papers pages", items=images_with_paper):
    image, paper_data = v
    paper = paper_data['paper']
    predicted_score = paper_data['predicted_score']

    # image path fooo/1.png
    # image_number = 1
    image_number = image.split('/')[-1].split('.')[0]

    # link to the arxiv paper
    arxiv_paper_link = f'https://arxiv.org/abs/{paper.arxiv_id}'
    image_key = f"{paper.arxiv_id}_{image}"
    st.write(f'[{image_number} {paper.title}]({arxiv_paper_link})')
    st.image(os.path.join(config.IMAGES_FOLDER, paper.arxiv_id, image), width=MAX_WIDTH)
    default_score = ImageFeedbackTable().get_image_score(paper_id=paper.arxiv_id, image_position=image_number)
    score = st.feedback('stars', key=f"feedback_{image_key}")
    st.write(f'Existing Value: {default_score}')
    st.write('Predicted Value: {}'.format(predicted_score))
    if score != None:
        ImageFeedbackTable().add_feedback(paper_id=paper.arxiv_id, image_position=image_number, score=score)
        st.success(f'Feedback added for {image}')
    
