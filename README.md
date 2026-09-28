# Asynchronous Image Downloader

A small Python project for practicing asynchronous programming by collecting product images from the **Special Offers** section of an e-commerce website and downloading them concurrently.

The original exercise was written to explore the combination of:

- `asyncio` for concurrency
- `aiohttp` for asynchronous HTTP requests
- `aiofiles` for asynchronous file I/O
- `BeautifulSoup` for HTML parsing
- `requests` for the initial synchronous page requests

## Features

- Finds the website's Special Offers page from the homepage.
- Extracts product names and image URLs from the page.
- Downloads multiple product images concurrently.
- Saves downloaded images to a local `images/` directory.
- Uses a single `aiohttp.ClientSession` for the download batch.
- Keeps configuration outside the download logic.
- Uses `pathlib` for platform-independent filesystem handling.

## Project structure

```text
asynchronous-image-downloader/
├── src/
│   └── image_downloader/
│       ├── __init__.py
│       └── downloader.py
├── tests/
│   └── test_downloader.py
├── .gitignore
├── README.md
├── pyproject.toml
└── requirements.txt
```

## Requirements

- Python 3.10+
- Internet access
- A target website whose HTML structure matches the selectors used by this exercise

## Installation

Clone the repository and move into the project directory:

```bash
git clone https://github.com/mehranhadd/Asynchronous-image-downloader-practice.git
cd Asynchronous-image-downloader-practice
```

Create and activate a virtual environment:

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the downloader as a module:

```bash
python -m image_downloader.downloader
```

Downloaded images are stored in:

```text
images/
```

The output directory is created automatically if it does not already exist.

## How it works

The program follows four main steps:

1. **Fetch the homepage**

   A synchronous `requests` call retrieves the homepage because only one initial page needs to be fetched.

2. **Find the Special Offers page**

   `BeautifulSoup` parses the homepage and searches for the link to the Special Offers section.

3. **Extract products**

   The Special Offers HTML is parsed to find product images, their URLs, and their names.

4. **Download concurrently**

   `asyncio.gather()` schedules the image downloads concurrently. `aiohttp` performs the HTTP requests and `aiofiles` writes the downloaded data asynchronously.

The important distinction is that the HTML discovery is mostly sequential, while the independent image downloads are the part that benefits from concurrency.

## Example

A simplified execution looks like:

```text
Fetching Special Offers page...
Found 20 product images.
Downloading images...
Downloaded 20 images in 3.42 seconds.
```

The exact number of images and execution time depend on the target website and network conditions.

## Design decisions

### Why use `requests` for HTML retrieval?

The project only needs a small number of sequential HTML requests before the download phase begins. Using `requests` keeps that part straightforward.

### Why use `aiohttp` for images?

The image downloads are independent of one another, so they are a good candidate for asynchronous I/O. Multiple requests can be in progress without creating a separate thread for each download.

### Why use one `ClientSession`?

A single `aiohttp.ClientSession` can be reused for the whole download batch. This avoids creating a new HTTP session for every image and allows the HTTP client to reuse connections.

### Why use `pathlib`?

`pathlib.Path` makes filesystem operations clearer and avoids depending on a personal absolute path.

## Limitations

This project is intentionally a learning exercise rather than a production-ready web scraper.

In particular:

- The HTML selectors depend on the structure of the target website.
- The downloader currently expects product image URLs to be available in `img` elements.
- The downloaded files use `.png` based on the original exercise; this does not inspect the server's actual `Content-Type`.
- The project does not implement retries or sophisticated rate limiting.
- The target website may change its HTML structure or access policy over time.

## Possible improvements

Some natural next steps for the project would be:

- Add retry handling for failed downloads.
- Respect the image's actual file extension/content type.
- Add configurable concurrency limits.
- Add structured logging.
- Add more comprehensive tests.
- Make the target URL configurable through command-line arguments.
- Add a progress indicator.
- Add CI with GitHub Actions.

## Learning goals

This project was created as a practical exercise in:

- asynchronous programming with Python
- concurrent I/O
- asynchronous HTTP clients
- asynchronous file operations
- HTML parsing
- separating application logic into reusable functions
