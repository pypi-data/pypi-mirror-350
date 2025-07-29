import asyncio
from .baseParser import BaseParser
from bs4 import BeautifulSoup

html_in_description = ['<br>', '<body>', '<head>', '<html>', 'src=', '<p>']

class DescriptionParser(BaseParser):
    async def __call__(self, feed_element):
        """
        Calls the html_in_description method, which takes a string as an argument and removes
        all the html tags from the string and returns the result.

        If the description of the feed element is not None, it checks if any of the strings
        in the html_in_description list are in the description. If they are, it calls the
        html_in_description method and returns the result. If not, it just returns the
        description.

        If the description of the feed element is None, it just returns None.

        :param feed_element: The feed element to parse
        :type feed_element: dict
        :return: The parsed description
        :rtype: str
        :raises ValueError: If an error occurs during the execution of the task
        """
        try:
            if feed_element['description'] != None:
                for el in html_in_description:
                    if el in str(feed_element['description']):
                        return  await self.html_in_description(feed_element['description'])
                return feed_element['description']
            else:
                return None
        except Exception as ex:
            ValueError

    
    async def html_in_description(self, feed_element):
        """
        This method takes a string as an argument, removes all the html tags from the string,
        extracts the first image and text from the string, and returns the result as a json object.

        The json object contains two keys: 'img' and 'description'. The 'img' key contains the link to the image,
        and the 'description' key contains the text of the string.

        :param feed_element: The string to parse
        :type feed_element: str
        :return: The parsed string as a json object
        :rtype: dict
        :raises ValueError: If an error occurs during the execution of the task
        """
        try:
            async_task = asyncio.gather(
                self.get_img(feed_element),
                self.get_text(feed_element)
            )
            task = await async_task
            return {'img': str(task[0]),
                    'description': task[1]}
        except Exception as ex:
            ValueError

        
    async def get_img(self, feed):
        """
        This method takes a string as an argument, parses the string to extract the link to the first image,
        and returns the link as a string.

        :param feed: The string to parse
        :type feed: str
        :return: The link to the first image as a string
        :rtype: str
        :raises ValueError: If an error occurs during the execution of the task
        """
        try:
            soup = BeautifulSoup(feed, 'lxml')
            soup_f = soup.find(name='img').get('src')
            return soup_f
        except Exception as ex:
            ValueError
    

    async def get_text(self, feed):
        """
        This method takes a string as an argument, parses the string to extract the text,
        and returns the text as a string after removing all the html tags.

        :param feed: The string to parse
        :type feed: str
        :return: The text without html tags as a string
        :rtype: str
        :raises ValueError: If an error occurs during the execution of the task
        """
        try:
            soup = BeautifulSoup(feed, 'lxml')
            text = soup.get_text()
            return text
        except Exception as ex:
            ValueError

    