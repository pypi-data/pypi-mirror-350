"""
마크다운을 블로거로 변환 및 업로드하는 패키지의 메인 모듈입니다.
"""

import logging
import sys
import os
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable

import click
from loguru import logger

from .libs.blogger import (
    check_config,
    get_blogger_service,
    get_blogid,
    get_datetime_after,
    get_datetime_after_hour,
    set_blogid,
    list_my_blogs,
    set_client_secret,
    upload_html_to_blogspot,
    upload_to_blogspot,
)
from .libs.click_order import CustomOrderGroup
from .libs.image_uploader import ImageUploader, get_available_services
from .libs.markdown import convert, read_first_header_from_md, upload_markdown_images
from .libs.config_manager import get_config_manager
from .libs.i18n import set_language, get_message, _

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
# logger = logging.getLogger(__name__)

# # 설정 마이그레이션 실행
# try:
#     config_manager = get_config_manager()
#     config_manager.check_migrate_legacy_config()
# except Exception as e:
#     logger.warning(f"설정 마이그레이션 중 오류 발생: {e}")


# 공통 옵션 기본값 및 설명
COMMON_OPTIONS = {
    "tui": {
        "is_flag": True,
        "default": False,
        "help": "TUI(Text User Interface) 모드로 진행 상황을 표시합니다.",
    },
    "blogid": {
        "param": "--blogid",
        "short": "-b",
        "default": None,
        "help": "업로드하려는 블로그 ID 지정. 미지정 시 설정값 사용.",
    },
    "service": {
        "param": "--service",
        "short": "-s",
        "type": click.Choice(get_available_services(), case_sensitive=False),
        "help": "사용할 이미지 업로드 서비스. 미지정 시 랜덤 선택.",
    },
}


# 공통 옵션 적용 헬퍼 함수
def add_options(options: List[str]) -> Callable:
    """옵션들을 명령어에 일관되게 추가하는 데코레이터 함수"""

    def decorator(f):
        for option_name in reversed(options):
            if option_name == "tui":
                f = click.option("--tui", **COMMON_OPTIONS["tui"])(f)
            elif option_name == "blogid":
                f = click.option(
                    COMMON_OPTIONS["blogid"]["param"],
                    COMMON_OPTIONS["blogid"]["short"],
                    default=COMMON_OPTIONS["blogid"]["default"],
                    help=COMMON_OPTIONS["blogid"]["help"],
                )(f)
            elif option_name == "service":
                f = click.option(
                    COMMON_OPTIONS["service"]["param"],
                    COMMON_OPTIONS["service"]["short"],
                    type=COMMON_OPTIONS["service"]["type"],
                    help=COMMON_OPTIONS["service"]["help"],
                )(f)
        return f

    return decorator


@click.command(
    cls=CustomOrderGroup,
    order=[
        "set_blogid",
        "get_blogid",
        "convert",
        "refresh_auth",
        "set_client_secret",
        "publish",
        "upload_image",
        "upload_images",
        "publish_folder",
        "publish_html",
        "list_my_blogs",
    ],
)
def mdb():
    """Markdown to Blogger - 마크다운 파일을 블로거에 발행하는 도구."""
    click.echo("markdown to blogger\nresult:\n\n")


@mdb.command("upload_image", help="이미지를 선택한 서비스에 업로드합니다.")
@click.argument("image_path", type=click.Path(exists=True))
@add_options(["service"])
def run_upload_image(image_path: str, service: Optional[str] = None):
    """지정된 이미지 파일을 이미지 호스팅 서비스에 업로드합니다.

    업로드 성공 시 이미지 URL을 반환합니다.
    서비스를 지정하지 않으면 설정된 기본값 또는 랜덤으로 선택됩니다.
    """
    try:
        uploader = ImageUploader(service=service)
        url = uploader.upload(image_path)
        click.echo(f"업로드 성공: {url}")
    except Exception as e:
        click.echo(f"업로드 실패: {str(e)}", err=True)
        sys.exit(1)


@mdb.command("upload_images", help="마크다운 파일 내의 모든 이미지를 업로드합니다.")
@click.option(
    "--input",
    "-i",
    "input_",
    required=True,
    help="업로드할 이미지가 포함된 마크다운 파일 경로",
)
def run_upload_images(input_):
    """마크다운 파일 내 모든 이미지를 찾아 업로드하고 링크를 업데이트합니다.

    파일 내에서 이미지 링크를 찾아 자동으로 업로드한 뒤 원본 파일의 링크를
    업로드된 URL로 교체합니다.
    """
    # try:
    upload_markdown_images(input_)
    click.echo("이미지 업로드 완료")
    # except Exception as e:
    # click.echo(f"이미지 업로드 실패: {str(e)}", err=True)
    sys.exit(1)


@mdb.command("set_blogid", help="블로그 ID를 설정합니다.")
@click.argument("blogid")
def run_set_blogid(blogid):
    """블로거 블로그 ID를 설정합니다.

    설정된 블로그 ID는 다른 명령어에서 기본값으로 사용됩니다.
    블로그 ID는 블로거 관리 페이지 또는 URL에서 확인할 수 있습니다.
    """
    check_config()
    set_blogid(blogid)
    click.echo(f"블로그 ID가 성공적으로 설정되었습니다: {blogid}")


@mdb.command("get_blogid", help="현재 설정된 블로그 ID를 확인합니다.")
def run_get_blogid():
    """현재 설정된 블로그 ID를 출력합니다."""
    check_config()
    blog_id = get_blogid()
    click.echo(f"현재 설정된 블로그 ID: {blog_id}")

@mdb.command("list_my_blogs", help="현재 계정에서 소유한 블로그들의 id와 url(도메인)을 출력합니다.")
def run_list_my_blogs():
    """현재 계정에서 소유한 블로그들의 id와 url(도메인)을 출력합니다."""
    list_my_blogs()



@mdb.command("convert", help="마크다운 파일을 HTML로 변환합니다.")
@click.option(
    "--input", "-i", "input_", required=True, help="변환할 마크다운 파일 경로"
)
@click.option("--output", "-o", "output_", required=True, help="저장할 HTML 파일 경로")
def run_convert(input_, output_):
    """마크다운 파일을 HTML 파일로 변환합니다.

    코드 하이라이팅, 표, 이미지 등을 포함한 마크다운을 HTML로 변환합니다.
    변환된 HTML은 지정된 출력 파일에 저장됩니다.
    """
    try:
        convert(input_, output_)
        click.echo(f"변환 완료: {input_} -> {output_}")
    except Exception as e:
        click.echo(f"변환 실패: {str(e)}", err=True)
        sys.exit(1)


@mdb.command(
    "set_client_secret", help="Google API 클라이언트 시크릿 파일을 설정합니다."
)
@click.argument("filename", type=click.Path(exists=True))
def run_set_client_secret(filename):
    """Google API 인증을 위한 client_secret.json 파일을 설정합니다.

    블로거 API를 사용하려면 Google Cloud Console에서 발급받은
    클라이언트 시크릿 파일이 필요합니다.
    """
    try:
        set_client_secret(filename)
        click.echo(f"클라이언트 시크릿 파일이 성공적으로 설정되었습니다: {filename}")
    except Exception as e:
        click.echo(f"클라이언트 시크릿 설정 실패: {str(e)}", err=True)
        sys.exit(1)


@mdb.command("refresh_auth", help="Google API 인증 정보를 갱신합니다.")
def run_refresh_auth():
    """Google API 인증 정보를 갱신합니다.

    인증 토큰이 만료되었거나 오류가 발생하는 경우 이 명령어를 사용하여
    인증 정보를 갱신할 수 있습니다.
    """
    try:
        sys.argv[1] = "--noauth_local_webserver"
        get_blogger_service()
        click.echo("인증 정보가 성공적으로 갱신되었습니다.")
    except Exception as e:
        click.echo(f"인증 정보 갱신 실패: {str(e)}", err=True)
        sys.exit(1)


@mdb.command("publish", help="마크다운 파일을 블로거에 발행합니다.")
@click.option(
    "--title",
    "-t",
    required=False,
    help="게시물 제목 (미지정 시 파일의 첫 헤더 사용)",
    default=None,
)
@click.option(
    "--draft",
    "is_draft",
    flag_value=True,
    default=False,
    help="드래프트 모드로 저장 (즉시 발행되지 않음)",
)
@click.option(
    "--after",
    "-af",
    type=click.Choice(
        ["now", "1m", "10m", "1h", "1d", "1w", "1M"], case_sensitive=True
    ),
    default=None,
    prompt=True,
    help="발행 시점 설정 (now: 즉시, 1m: 1분 후, 1h: 1시간 후, 1d: 1일 후 등)",
)
@click.option(
    "--after_hour",
    "-ah",
    type=int,
    default=None,
    help="특정 시간(시간 단위) 후 발행 (예: 3 = 3시간 후)",
)
@add_options(["blogid"])
@click.option(
    "--labels",
    "-l",
    multiple=True,
    help="포스트에 추가할 라벨 (여러 개 가능, 예: -l 파이썬 -l 프로그래밍)",
)
@click.option("--description", "-d", help="검색 엔진용 메타 설명 (SEO 최적화)")
@click.argument("filename", type=click.Path(exists=True))
def run_publish(
    title, filename, is_draft, after, after_hour, blogid, labels, description
):
    """마크다운 파일을 블로거 블로그에 발행합니다.

    파일은 자동으로 HTML로 변환되어 발행되며, 이미지는 별도로 업로드되지 않습니다.
    이미지가 포함된 경우 먼저 upload_images 명령어로 이미지를 업로드하세요.
    """
    blog_id = blogid if blogid else get_blogid()

    if not title:
        title = read_first_header_from_md(filename)
        if title is None:
            logger.error(f"title is None: {filename}")
            sys.exit(1)
        title = title.replace("# ", "")
        logger.info(f"title:{title}")

    datetime_string = (
        get_datetime_after_hour(after_hour)
        if after_hour is not None
        else (
            get_datetime_after(after)
            if after is not None
            else get_datetime_after("now")
        )
    )

    # 라벨이 제공된 경우 리스트로 변환
    labels_list = list(labels) if labels else None

    try:
        post_id = upload_to_blogspot(
            title,
            filename,
            blog_id,
            is_draft=is_draft,
            datetime_string=datetime_string,
            labels=labels_list,
            search_description=description,
        )

        # 발행 상태 메시지
        status = "드래프트로 저장됨" if is_draft else "발행됨"
        publish_time = (
            "즉시"
            if after == "now" and after_hour is None
            else f"{after or after_hour}{'시간' if after_hour else ''} 후"
        )

        click.echo(f"게시물이 성공적으로 {status}. Post ID: {post_id}")
        click.echo(f"발행 시점: {publish_time}")
        if labels_list:
            click.echo(f"라벨: {', '.join(labels_list)}")
    except Exception as e:
        click.echo(f"게시물 업로드 실패: {str(e)}", err=True)
        sys.exit(1)


@mdb.command("publish_html", help="HTML 파일을 블로거에 직접 발행합니다.")
@click.argument("filename", type=click.Path(exists=True))
@click.option("--title", "-t", required=True, help="게시물 제목")
@add_options(["blogid"])
def run_publish_html(title, filename, blogid=None):
    """HTML 파일을 블로거 블로그에 직접 발행합니다.

    마크다운 변환 과정 없이 HTML 파일을 그대로 블로그에 게시합니다.
    이미 작성된 HTML 파일을 빠르게 발행할 때 유용합니다.
    """
    blog_id = blogid if blogid else get_blogid()
    try:
        post_id = upload_html_to_blogspot(title, filename, blog_id)
        click.echo(f"HTML 게시물이 성공적으로 업로드되었습니다. Post ID: {post_id}")
    except Exception as e:
        click.echo(f"HTML 게시물 업로드 실패: {str(e)}", err=True)
        sys.exit(1)


@mdb.command(
    "publish_folder",
    help="폴더 내의 모든 마크다운 파일을 순차적으로 블로거에 발행합니다.",
)
@add_options(["blogid", "service", "tui"])
@click.option(
    "--interval", "-i", default=1, help="발행 간격 (시간 단위, 기본값: 1시간)"
)
@click.option(
    "--draft",
    is_flag=True,
    default=False,
    help="모든 파일을 드래프트로 저장 (즉시 발행되지 않음)",
)
@click.option(
    "--labels",
    "-l",
    multiple=True,
    help="모든 포스트에 추가할 공통 라벨",
)
@click.argument(
    "folder_path", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
def run_publish_folder(blogid, interval, service, tui, draft, labels, folder_path):
    """폴더 내의 모든 마크다운 파일을 순차적으로 블로거에 발행합니다.

    폴더 내 모든 마크다운(.md) 파일을 찾아 블로그에 발행합니다.
    각 파일의 이미지를 자동으로 업로드한 후 발행하며,
    지정된 시간 간격으로 순차적으로 게시됩니다.
    """
    blog_id = blogid if blogid else get_blogid()

    # 라벨이 제공된 경우 리스트로 변환
    labels_list = list(labels) if labels else None

    try:
        folder = Path(folder_path)
        if not folder.exists() or not folder.is_dir():
            click.echo(f"오류: {folder_path}는 유효한 폴더가 아닙니다.", err=True)
            sys.exit(1)

        seoul_timezone = timezone(timedelta(hours=9))
        current_dt = datetime.now(seoul_timezone)

        # 폴더 내 모든 마크다운 파일 수집
        file_list = list(folder.glob("*.md"))
        if not file_list:
            click.echo(f"경고: 폴더에 마크다운 파일이 없습니다: {folder_path}")
            return

        total_files = len(file_list)
        success_count = 0
        error_count = 0

        with click.progressbar(
            file_list, label=f"폴더 내 {total_files}개 파일 처리 중", show_pos=True
        ) as files:
            for idx, file in enumerate(files, 1):
                try:
                    # 파일 정보 준비
                    file_path = file.resolve()
                    file_name = file.name
                    file_title = read_first_header_from_md(file_path)

                    if not file_title:
                        logger.warning(
                            f"제목을 찾을 수 없음: {file_name}, 파일 이름을 제목으로 사용합니다."
                        )
                        file_title = file.stem  # 확장자 없는 파일명 사용
                    else:
                        file_title = file_title.replace("# ", "")

                    # 게시 시간 계산
                    target_dt = current_dt + timedelta(hours=interval * idx)
                    datetime_string = target_dt.isoformat(timespec="seconds")

                    # 이미지 업로드 처리
                    logger.info(f"Uploading images from file: {file_name}")
                    upload_markdown_images(str(file_path))

                    # 포스트 업로드
                    logger.info(
                        f"Publishing '{file_title}' to blog ID: {blog_id} at {datetime_string}"
                    )
                    upload_to_blogspot(
                        file_title,
                        file_path,
                        blog_id,
                        is_draft=draft,
                        datetime_string=datetime_string,
                        labels=labels_list,
                    )
                    success_count += 1
                except Exception as e:
                    logger.error(f"Error processing file {file_name}: {str(e)}")
                    error_count += 1
                    continue

        # 완료 메시지 표시
        if success_count == total_files:
            click.echo(
                f"✅ 모든 파일이 성공적으로 처리되었습니다. (총 {total_files}개)"
            )
        else:
            click.echo(
                f"⚠️ 처리 완료: {success_count}개 성공, {error_count}개 실패 (총 {total_files}개)"
            )
    except Exception as e:
        click.echo(f"폴더 처리 중 오류 발생: {str(e)}", err=True)
        sys.exit(1)
