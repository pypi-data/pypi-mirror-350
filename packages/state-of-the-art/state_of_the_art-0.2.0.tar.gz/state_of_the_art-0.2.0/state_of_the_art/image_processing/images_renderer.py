
import os
from typing import List

from state_of_the_art.config import config
from state_of_the_art.paper.arxiv_paper import ArxivPaper


class ImagesRenderer:
    def get_images_from_paper(self, paper: ArxivPaper) -> List[str]:
        # return the paths of existing images
        images_folder = config.IMAGES_FOLDER
        paper_subfolder = paper.arxiv_id
        images_folder = os.path.join(images_folder, paper_subfolder)

        # test if the folder exists
        if not os.path.exists(images_folder):
            return []

        image_paths = []
        for image_path in os.listdir(images_folder):
            if image_path.endswith(".png") or image_path.endswith(".jpg"):
                image_paths.append(os.path.join(images_folder, image_path))
        return image_paths
