from typing import List, Optional
import pandas as pd
from state_of_the_art.config import config
from state_of_the_art.paper.arxiv_paper import ArxivPaper
from state_of_the_art.paper.paper_downloader import PaperDownloader
from pypdf import PdfReader
from tqdm import tqdm
import os


class ImagesExtractor:

    def __init__(self, write_to_folder: str = config.IMAGES_FOLDER):
        self._write_to_folder = write_to_folder

    def extract_images(self, df: pd.DataFrame) -> List[str]:
        papers_urls = df['abstract_url'].tolist()

        all_images_extracted = []
        for paper_url in tqdm(papers_urls):
            arxiv_paper = ArxivPaper(abstract_url=paper_url)
            images = self.extract_images_from_paper(arxiv_paper)
            all_images_extracted.extend(images)
        return all_images_extracted
    
    def extract_images_from_paper(self,*, paper: ArxivPaper, position: Optional[int] = None, write_to_custom_folder: Optional[str] = None, skip_if_folder_exists: bool = True) -> List[str]:
        """
        Extract images from a paper.
        If position is provided, only the image in the given position will be extracted.
        If position is not provided, all images will be extracted.
        """

        print("Extracting images from paper: {}".format(paper.arxiv_id))
        if position:
            print(f"Position: {position} is set and write_to_folder: {write_to_custom_folder} is set")

        pdf_url = paper.pdf_url

        paper_destination = PaperDownloader().download(pdf_url, force_download=True)
        paper_destination
        if not os.path.exists(paper_destination):
            raise Exception('paper_destination does not exist: {}'.format(paper_destination))

        print('reading pdf: {}'.format(paper_destination))
        reader = PdfReader(paper_destination)

        image_count_in_paper = 0


        if not write_to_custom_folder:
            paper_folder = os.path.join(self._write_to_folder, paper.arxiv_id)
        else:
            paper_folder = write_to_custom_folder

        if skip_if_folder_exists and os.path.exists(paper_folder):
            print(f"Skipping paper {paper.arxiv_id} because folder {paper_folder} exists")
            return self._return_images_from_folder(paper_folder)

        for index, page in enumerate(reader.pages):
            if not os.path.exists(paper_folder):
                os.makedirs(paper_folder)

            try:
                for image_file_object in page.images:
                    if position is not None and int(position) != image_count_in_paper:
                        image_count_in_paper += 1
                        continue
                    image_count_in_paper += 1
                    print('image_file_object: {}'.format(image_file_object))
                    extension = image_file_object.name.split('.')[-1]
                    image_name = str(image_count_in_paper) + '.' + extension

                    with open(paper_folder + '/' + image_name, "wb") as fp:
                        print(image_file_object)
                        fp.write(image_file_object.data)
                        print('wrote image to: {}'.format(image_name))
            except Exception as e:
                print(f"Error extracting images from paper {paper.arxiv_id}: {e}")
                continue
            
        images = self._return_images_from_folder(paper_folder)
        return images

    def _return_images_from_folder(self, folder: str) -> List[str]:
        """
        Return a list of images from a folder.
        """
        #folder = config.IMAGES_FOLDER + '/' + folder
        images = os.listdir(folder)
        # filter out some files by name 
        images = [ folder + '/' + image for image in images if image not in['.gitignore', '.', '..']  ]
        # sort by part of the image name
        images.sort()
        return images
