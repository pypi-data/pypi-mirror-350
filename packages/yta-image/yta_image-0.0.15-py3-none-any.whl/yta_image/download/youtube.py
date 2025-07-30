from yta_web_scraper import ChromeScraper
from yta_general_utils.dataclasses import FileReturn
from yta_temp import Temp
from PIL import Image


class YoutubeImageDownloader:
    """
    Class to download images from the Youtube
    website.
    """

    @staticmethod
    def download_youtube_video_comments(
        url: str,
        number_of_comments: int = 5
    ) -> list[FileReturn]:
        """
        Download (if possible) the 'number_of_comments' first
        comments of the Youtube video with the given 'url'. It
        will scrap the web page and screenshot those comments.

        The amount of comments available could be lower than 
        the 'number_of_comments' requested or even zero.

        This method will return an array containing all the
        comment images obtained, that could be empty if no one
        was available.
        """
        if not url:
            raise Exception('No "url" provided.')
        
        # TODO: Check if url is a valid Youtube url

        if not number_of_comments:
            number_of_comments = 5

        scraper = ChromeScraper(False)
        # Example of url: 'https://www.youtube.com/watch?v=OvUj2WsADjI'
        scraper.go_to_web_and_wait_until_loaded(url)
        # We need to scroll down to let the comments load
        # TODO: This can be better, think about a more specific strategy
        # about scrolling
        scraper.scroll_down(1000)
        scraper.wait(1)
        scraper.scroll_down(1000)
        scraper.wait(1)

        # We need to make sure the comments are load
        scraper.find_element_by_element_type_waiting('ytd-comment-thread-renderer')
        comments = scraper.find_elements_by_element_type('ytd-comment-thread-renderer')

        if len(comments) >= number_of_comments:
            comments[:5]

        # We remove the header bar to avoid being over our comments in some cases
        youtube_top_bar = scraper.find_element_by_id_waiting('masthead-container')
        scraper.remove_element(youtube_top_bar)

        screenshots = []

        screenshots = []
        for comment in comments:
            # TODO: I need to close the 'No, gracias' 'Probar 1 mes' popup
            scraper.scroll_to_element(comment)
            style = 'width: 500px; padding: 10px;'
            scraper.set_element_style(comment, style)
            filename = Temp.get_wip_filename('tmp_comment_screenshot.png')
            scraper.screenshot_element(comment, filename)
            screenshots.append(FileReturn(
                Image.open(filename),
                filename
            ))

        return screenshots


"""
When I get the 'innerText' attribute from a comment,
I receive it with a specific structure:

print(comment.get_attribute('innerText'))
# I can handle the information from this innertext
# If I split by \n:

# 1st is author (@pabloarielcorderovillacort2149)
# 2nd is date (hace 6 meses)
# 3rd and next ones are comment text
# Penultimate is the number of likes (number)
# Last one is 'Responder'
#
# This below is an example of a read comment:
#
# @pabloarielcorderovillacort2149
# hace 6 meses
# No puedo esperar tu siguiente vídeo.

# Andy Serkis es una joya de actor, Gollum y Cesar son mis personajes favoritos de este actor.
# 3
# Responder
"""