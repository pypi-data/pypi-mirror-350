# Markdown to Blogger

[English](#english) | [한국어](#korean)

[]()

# 마크다운 투 블로거

이 프로젝트는 마크다운 파일을 HTML로 변환하여 Blogger에 게시하는 도구입니다. Python과 Blogger API를 사용하여 마크다운 파일을 블로그 포스트로 쉽게 변환하고 업로드할 수 있습니다.

## 설치 방법

이 도구를 사용하기 전에, Python이 설치되어 있어야 합니다. 그 후에, 필요한 패키지를 설치하기 위해 다음 명령어를 실행하세요:

```bash
poetry install
```

## 사용법

이 도구는 명령줄 인터페이스(CLI)를 통해 다양한 명령어를 제공합니다. 사용 가능한 명령어는 다음과 같습니다:

### 블로그 ID 설정

블로그 ID를 설정하려면 다음 명령어를 사용하세요:

```bash
mdb set_blogid [블로그 ID]
```

### 현재 설정된 블로그 ID 확인

현재 설정된 블로그 ID를 확인하려면 다음 명령어를 사용하세요:

```bash
mdb get_blogid
```

### 마크다운 파일을 HTML로 변환

마크다운 파일을 HTML로 변환하려면 다음 명령어를 사용하세요:

```bash
mdb convert --input [마크다운 파일명] --output [저장될 HTML 파일명]
```

### Client Secret 파일 설정

Google API 사용을 위한 `client_secret.json` 파일을 설정하려면 다음 명령어를 사용하세요:

```bash
mdb set_client_secret [client_secret.json 파일 경로]
```

### 인증 정보 갱신

Google API의 인증 정보를 갱신하려면 다음 명령어를 사용하세요:

```bash
mdb refresh_auth
```

### 마크다운 파일을 Blogger에 게시

마크다운 파일을 Blogger에 직접 게시하려면 다음 명령어를 사용하세요:

```bash
mdb publish [옵션들] [마크다운 파일명]
```

#### 게시 옵션

- `--title` / `-t`: 블로그 게시물의 제목 (선택사항)
- `--draft`: 드래프트로 저장
- `--after` / `-af`: 게시 시점 설정 ("now", "1m", "10m", "1h", "1d", "1w", "1M")
- `--after_hour` / `-ah`: 특정 시간(시간 단위) 후 게시
- `--blogid` / `-b`: 대상 블로그 ID

### 이미지 업로드

단일 이미지를 업로드하려면:

```bash
mdb upload_image [이미지 파일 경로] --service [서비스명]
```

마크다운 파일 내의 모든 이미지를 업로드하려면:

```bash
mdb upload_images --input [마크다운 파일명] --service [서비스명] --tui
```

### 폴더 내 모든 마크다운 파일 게시

폴더 내의 모든 마크다운 파일을 순차적으로 게시하려면:

```bash
mdb publish_folder [폴더 경로] --interval [시간 간격] --service [이미지 서비스명] --tui
```

### HTML 파일을 Blogger에 게시

HTML 파일을 Blogger에 게시하려면 다음 명령어를 사용하세요:

```bash
mdb publish_html --title "[블로그 제목]" [HTML 파일명]
```

## 기여하기

프로젝트에 기여하고 싶으신 분은 GitHub를 통해 Pull Request를 보내주시거나, 이슈를 등록해 주세요.

--------------------------------------------------------------------------------

[]()

# Markdown to Blogger

This project is a tool for converting Markdown files to HTML and publishing them to Blogger. Using Python and the Blogger API, you can easily convert and upload Markdown files as blog posts.

## Installation

Before using this tool, you need to have Python installed. Then, run the following command to install the required packages:

```bash
poetry install
```

## Usage

This tool provides various commands through a Command Line Interface (CLI). Here are the available commands:

### Setting Blog ID

To set the blog ID, use the following command:

```bash
mdb set_blogid [blog ID]
```

### Checking Current Blog ID

To check the currently set blog ID, use:

```bash
mdb get_blogid
```

### Converting Markdown to HTML

To convert a Markdown file to HTML, use:

```bash
mdb convert --input [markdown filename] --output [html filename]
```

### Setting Client Secret File

To set up the `client_secret.json` file for Google API usage:

```bash
mdb set_client_secret [client_secret.json file path]
```

### Refreshing Authentication

To refresh Google API authentication:

```bash
mdb refresh_auth
```

### Publishing Markdown to Blogger

To publish a Markdown file directly to Blogger:

```bash
mdb publish [options] [markdown filename]
```

#### Publishing Options

- `--title` / `-t`: Blog post title (optional)
- `--draft`: Save as draft
- `--after` / `-af`: Set publishing time ("now", "1m", "10m", "1h", "1d", "1w", "1M")
- `--after_hour` / `-ah`: Publish after specific hours
- `--blogid` / `-b`: Target blog ID

### Image Upload

To upload a single image:

```bash
mdb upload_image [image file path] --service [service name]
```

To upload all images in a Markdown file:

```bash
mdb upload_images --input [markdown filename] --service [service name] --tui
```

### Publishing All Markdown Files in a Folder

To sequentially publish all Markdown files in a folder:

```bash
mdb publish_folder [folder path] --interval [time interval] --service [image service name] --tui
```

### Publishing HTML to Blogger

To publish an HTML file to Blogger:

```bash
mdb publish_html --title "[blog title]" [HTML filename]
```

## Contributing

If you'd like to contribute to the project, please send a Pull Request through GitHub or register an issue.
