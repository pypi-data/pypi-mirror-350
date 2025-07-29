from .baseParser import BaseParser

class ImageParser(BaseParser):
    def __init__(self) -> None:
        super().__init__()
        self.patern = {
            'media_thumbnail': 'url',
            'enclosures': 'href',
            'media_content': 'url',
            }
    
    async def __call__(self, feed_element):
        """
        Parse the feed element and extract the first image link from it.

        :param feed_element: The feed element to parse
        :return: The first image link found in the feed element
        :raises ValueError: If an error occurs during the execution of the task
        """
        try:

            list_img = []
            for key, value in self.patern.items():
                list_img.append(await self.find_img_link(key, value, feed_element))
            img = [n for n in list_img if n is not None]
            return str(img[0])
        except Exception as ex:
            ValueError


    async def find_img_link(self, patern_1, patern_2, feed_element):
        """
        Find an image link in a given feed element based on two given patterns.

        :param patern_1: The first pattern to look for in the feed element
        :param patern_2: The second pattern to look for in the feed element
        :param feed_element: The feed element to search in
        :return: The found image link
        :raises ValueError: If an error occurs during the execution of the task
        """
        try:
            return feed_element[patern_1][0][patern_2]
        except Exception as ex:
            ValueError