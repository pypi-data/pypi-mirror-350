from typing import Any
from .baseParser import BaseParser


class TitleParser(BaseParser):
    async def __call__(self, feed_element) -> Any:
        """
        Extracts the title of a given feed element.

        If the title of the feed element is not None, it is returned.
        Otherwise, "None" is returned.

        :param feed_element: The feed element to extract the title from
        :return: The title of the feed element, or "None"
        :raises: ValueError if an error occurs during the execution of the task
        """
        try:
            if feed_element['title'] != None:
                return feed_element['title']
            else:
                return "None"
        except Exception as ex:
            ValueError