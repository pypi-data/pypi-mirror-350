
class UrlSanitizer():
    def sanitize(self, url):
        url = url.strip()
        if url.startswith("https://arxiv.org"):
            url = url.replace("https://", "http://")
        return url
