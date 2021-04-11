import re

from re import findall
from instapy.julien.caption_data import PostData

from selenium.common.exceptions import WebDriverException

from instapy.like_util import get_media_edge_comment_string
from instapy.util import web_address_navigator, update_activity, evaluate_mandatory_words


def get_post_caption(
        browser,
        post_link,
        logger,
):
    """
    Check the given link if it is appropriate

    :param browser: The selenium webdriver instance
    :param post_link:
    :param logger: the logger instance
    :return: tuple oo
        string: the post description
        boolean: True if sucess False otherwise
    """

    # Check URL of the webpage, if it already is post's page, then do not
    # navigate to it again
    web_address_navigator(browser, post_link)

    # Check if the Post is Valid/Exists
    try:
        post_page = browser.execute_script(
            "return window.__additionalData[Object.keys(window.__additionalData)[0]].data"
        )

    except WebDriverException:  # handle the possible `entry_data` error
        try:
            browser.execute_script("location.reload()")
            update_activity(browser, state=None)

            post_page = browser.execute_script(
                "return window._sharedData.entry_data.PostPage[0]"
            )

        except WebDriverException:
            post_page = None

    if post_page is None:
        logger.warning("Unavailable Page: {}".format(post_link.encode("utf-8")))
        return None, False

    # Gets the description of the post's link
    graphql = "graphql" in post_page
    post_data = PostData()

    if graphql:
        media = post_page["graphql"]["shortcode_media"]
        post_data.post_id = media["id"]
        post_data.short_link = media["shortcode"]
        post_data.creation_timestamp = media["taken_at_timestamp"]
        post_data.owner_account = media["owner"]["username"]
        is_video = media["is_video"]

        user_name = media["owner"]["username"]
        image_text = media["edge_media_to_caption"]["edges"]
        image_text = image_text[0]["node"]["text"] if image_text else None
        media_edge_string = get_media_edge_comment_string(media)
        # double {{ allows us to call .format here:
        try:
            browser.execute_script(
                "window.insta_data = window.__additionalData[Object.keys(window.__additionalData)[0]].data"
            )
        except WebDriverException:
            browser.execute_script(
                "window.insta_data = window._sharedData.entry_data.PostPage[0]"
            )
        # Maybe not useful see if needed
        owner_comments = browser.execute_script(
            """
            latest_comments = window.insta_data.graphql.shortcode_media.{}.edges;
            if (latest_comments === undefined) {{
                latest_comments = Array();
                owner_comments = latest_comments
                    .filter(item => item.node.owner.username == arguments[0])
                    .map(item => item.node.text)
                    .reduce((item, total) => item + '\\n' + total, '');
                return owner_comments;}}
            else {{
                return null;}}
        """.format(
                media_edge_string
            ),
            user_name,
        )

    else:
        media = post_page[0]["shortcode_media"]
        is_video = media["is_video"]
        user_name = media["owner"]["username"]
        image_text = media["caption"]
        # Maybe not useful see if needed
        owner_comments = browser.execute_script(
            """
            latest_comments = window._sharedData.entry_data.PostPage[
            0].media.comments.nodes;
            if (latest_comments === undefined) {
                latest_comments = Array();
                owner_comments = latest_comments
                    .filter(item => item.user.username == arguments[0])
                    .map(item => item.text)
                    .reduce((item, total) => item + '\\n' + total, '');
                return owner_comments;}
            else {
                return null;}
        """,
            user_name,
        )

    if owner_comments == "":
        owner_comments = None

    # Append owner comments to description as it might contain further tags
    if image_text is None:
        image_text = owner_comments

    elif owner_comments:
        image_text = image_text + "\n" + owner_comments

    # If the image still has no description gets the first comment
    if image_text is None:
        if graphql:
            media_edge_string = get_media_edge_comment_string(media)
            image_text = media[media_edge_string]["edges"]
            image_text = image_text[0]["node"]["text"] if image_text else None

        else:
            image_text = media["comments"]["nodes"]
            image_text = image_text[0]["text"] if image_text else None

    if image_text is None:
        image_text = "No description"
    post_data.caption = image_text
    logger.info("Post id : {}".format(post_data.post_id))
    logger.info("Link: {}".format(post_data.short_link.encode("utf-8")))
    logger.info("Creation timestamp: {}".format(post_data.creation_timestamp))
    logger.info("Owner Account: {}".format(user_name.encode("utf-8")))
    logger.info("Description : {}".format(post_data.caption.encode("utf-8")))

    return post_data, True
