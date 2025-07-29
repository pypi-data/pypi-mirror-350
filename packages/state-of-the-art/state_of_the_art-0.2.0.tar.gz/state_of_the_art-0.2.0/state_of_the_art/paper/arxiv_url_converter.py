

class ArxivUrlConverter:
    def convert_pdf_url_to_abstract_url(self, url):
        if "arxiv.org/pdf/" in url:
            url = url.replace("arxiv.org/pdf/", "arxiv.org/abs/")
            url = url.replace(".pdf", "")
        return url
