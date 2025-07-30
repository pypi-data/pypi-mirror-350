import codecs
import pathlib
import shutil
from datetime import datetime, timedelta, timezone

import httplib2
from bs4 import BeautifulSoup
from googleapiclient import discovery
from loguru import logger
from markdown2 import Markdown
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

from .config_manager import (
    CLIENT_SECRET_PATH,
    CONFIG_BASE_DIR,
    CREDENTIAL_STORAGE_PATH,
    get_config_manager,
)

SCOPE = "https://www.googleapis.com/auth/blogger"

DEFAULT_MARKDOWN_EXTRAS = [
    "highlightjs-lang",
    "fenced-code-blocks",
    "footnotes",
    "tables",
    "code-friendly",
    "smarty-pants",
    "metadata",
]


def extract_article(fn):
    """
    Extracts the title and content of an article from an HTML file.

    Args:
        fn (str): The path to the HTML file.

    Returns:
        dict: A dictionary containing the extracted title and content.
            - title (str): The title of the article.
            - content (str): The HTML content of the article.

    """
    with codecs.open(fn, "r", "utf_8") as fp:
        html = fp.read()
        html = html.replace("<!doctype html>", "")
        soup = BeautifulSoup(html, "html.parser")
        title = soup.select("title")[0].text
        article = soup.select("body")[0]
        return {"title": title, "content": article.prettify()}


def authorize_credentials():
    """
    Authorizes the credentials required for accessing the specified scope.

    Returns:
        Credentials: The authorized credentials.

    """
    validate_credential_path()
    storage = Storage(CREDENTIAL_STORAGE_PATH)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET_PATH, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, storage, http=http)
    return credentials


def get_blogger_service():
    credentials = authorize_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = "https://{api}.googleapis.com/$discovery/rest?version={apiVersion}"
    return discovery.build("blogger", "v3", http=http, discoveryServiceUrl=discoveryUrl)


def list_my_blogs():
    """
    현재 계정에서 소유한 블로그들의 id와 url(도메인)을 출력합니다.
    """
    service = get_blogger_service()
    result = service.blogs().listByUser(userId="self").execute()
    blogs = result.get("items", [])
    if not blogs:
        print("소유한 블로그가 없습니다.")
        return []
    for blog in blogs:
        print(f"블로그 이름: {blog.get('name')}")
        print(f"블로그 ID: {blog.get('id')}")
        print(f"블로그 URL: {blog.get('url')}")
        print("-" * 40)
    return [(blog.get("id"), blog.get("url")) for blog in blogs]


def _get_blogger_connection(blog_id=None):
    """
    Blogger 서비스에 연결하고 기본 설정을 반환합니다.

    Args:
        blog_id (str, optional): 블로그 ID. None인 경우 설정에서 가져옵니다.

    Returns:
        tuple: (service, users, posts, blog_id) 튜플
    """
    validate_credential_path()
    service = get_blogger_service()
    users = service.users()
    thisuser = users.get(userId="self").execute()
    logger.info(f"""This user's display name is: {thisuser["displayName"]}""")
    posts = service.posts()

    if blog_id is None:
        blog_id = get_blogid()

    return service, users, posts, blog_id


def validate_credential_path():
    """
    Validates the existence of the credential storage directory and file.
    """
    target_dir = pathlib.Path(CONFIG_BASE_DIR)
    if not target_dir.exists():
        target_dir.mkdir(parents=True, exist_ok=True)

    target_path = pathlib.Path(CREDENTIAL_STORAGE_PATH)
    if not target_path.exists():
        target_path.touch()


def check_config():
    """설정 파일을 확인하고, 없는 경우 기본 설정으로 생성합니다."""
    # 설정 관리자가 자동으로 필요한 설정을 초기화합니다
    get_config_manager()


def set_blogid(value):
    """블로그 ID를 설정합니다."""
    get_config_manager().set_blog_id(value)
    logger.info(f"블로그 ID가 설정되었습니다: {value}")


def get_blogid():
    """저장된 블로그 ID를 반환합니다."""
    return get_config_manager().get_blog_id()


def set_client_secret(fn):
    """클라이언트 시크릿 파일을 설정 디렉토리에 복사합니다."""
    shutil.copy(fn, CLIENT_SECRET_PATH)
    logger.info(f"클라이언트 시크릿 파일이 설정되었습니다: {CLIENT_SECRET_PATH}")


def upload_to_blogspot(
    title,
    fn,
    BLOG_ID,
    is_draft=False,
    datetime_string=None,
    labels=None,
    search_description=None,
) -> str:
    """
    Uploads a blog post to the specified Blogspot blog.

    Args:
        title (str): The title of the blog post.
        fn (str): The path to the Markdown file.
        BLOG_ID (str): The ID of the Blogspot blog.
        is_draft (bool, optional): Whether the post should be saved as a draft. Defaults to False.
        datetime_string (str, optional): The datetime string to set for the post. Defaults to None.
        labels (List[str], optional): List of labels/tags for the post. Defaults to None.
        search_description (str, optional): Meta description for SEO. Defaults to None.

    Returns:
        str: The ID of the uploaded blog post.
    """
    _, _, posts, _ = _get_blogger_connection(BLOG_ID)

    with codecs.open(fn, "r", "utf_8") as fp:
        markdowner = Markdown(extras=DEFAULT_MARKDOWN_EXTRAS)
        html = markdowner.convert(fp.read())
        payload = {
            "title": title,
            "content": html,
            "published": datetime_string,
        }

        # 라벨이 제공된 경우 추가
        if labels:
            payload["labels"] = labels

        # 검색 설명이 제공된 경우 추가
        if search_description:
            # 메타 설명 태그를 컨텐츠 시작 부분에 삽입
            meta_description = (
                f'<meta name="description" content="{search_description}"/>\n'
            )
            payload["content"] = meta_description + payload["content"]

        output = posts.insert(blogId=BLOG_ID, body=payload, isDraft=is_draft).execute()
        logger.info(f"id:{output['id']}\nstatus:{output['status']}")
        return output["id"]  # return postid


def upload_html_to_blogspot(title, fn, BLOG_ID):
    """
    Uploads an HTML file as a blog post to the specified Blogspot blog.

    Args:
        title (str): The title of the blog post.
        fn (str): The path to the HTML file.
        BLOG_ID (str): The ID of the Blogspot blog.

    Returns:
        str: The ID of the uploaded blog post.
    """
    _, _, posts, _ = _get_blogger_connection(BLOG_ID)

    with codecs.open(fn, "r", "utf_8") as fp:
        html = fp.read()
        payload = {"title": title, "content": html}
        output = posts.insert(blogId=BLOG_ID, body=payload, isDraft=False).execute()
        logger.info(f"id:{output['id']}\nstatus:{output['status']}")
        return output["id"]


def get_datetime_after(after_string):
    """
    Returns the ISO-formatted datetime string after a specified time interval.

    Args:
        after_string (str): The time interval string.
            - "now": Returns the current datetime.
            - "1m": Returns the datetime after 1 minute.
            - "10m": Returns the datetime after 10 minutes.
            - "1h": Returns the datetime after 1 hour.
            - "1d": Returns the datetime after 1 day.
            - "1w": Returns the datetime after 1 week.
            - "1M": Returns the datetime after 1 month.
            - Or an integer for hours.

    Returns:
        str: The ISO-formatted datetime string.
    """
    seoul_timezone = timezone(timedelta(hours=9))
    current_dt = datetime.now(seoul_timezone)

    # 숫자만 있는 경우 시간으로 처리
    if after_string and after_string.isdigit():
        return get_datetime_after_hour(int(after_string))

    match after_string:
        case "now":
            target_dt = current_dt
        case "1m":
            target_dt = current_dt + timedelta(minutes=1)
        case "10m":
            target_dt = current_dt + timedelta(minutes=10)
        case "1h":
            target_dt = current_dt + timedelta(hours=1)
        case "1d":
            target_dt = current_dt + timedelta(days=1)
        case "1w":
            target_dt = current_dt + timedelta(days=7)
        case "1M":
            target_dt = current_dt + timedelta(days=30)
        case _:
            target_dt = current_dt

    return target_dt.isoformat(timespec="seconds")


def get_datetime_after_hour(hour):
    """
    Returns the ISO-formatted datetime string after specified hours.

    Args:
        hour (int): Hours to add to current time.

    Returns:
        str: The ISO-formatted datetime string.
    """
    if hour is None:
        return get_datetime_after("now")

    seoul_timezone = timezone(timedelta(hours=9))
    current_dt = datetime.now(seoul_timezone)
    target_dt = current_dt + timedelta(hours=hour)
    return target_dt.isoformat(timespec="seconds")
