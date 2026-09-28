"""Download product images from a website's Special Offers page."""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin

import aiofiles
import aiohttp
import requests
from bs4 import BeautifulSoup


HOME_URL = "http://technolife.ir"
USER_AGENT = "Mozilla/5.0 (compatible; AsyncImageDownloader/0.1)"
OUTPUT_DIR = Path("images")

HEADERS = {"User-Agent": USER_AGENT}


@dataclass(frozen=True)
class Product:
    """Information required to download a product image."""

    name: str
    image_url: str


def get_html(url: str) -> str:
    """Fetch and return HTML from a URL.

    The initial page retrieval is synchronous because the project only
    needs a small number of sequential HTML requests before the
    concurrent image-download phase.
    """
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return response.text


def find_special_offers_url(home_url: str) -> str:
    """Find the Special Offers page URL on the homepage."""
    content = get_html(home_url)
    soup = BeautifulSoup(content, "html.parser")

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.endswith("special/special"):
            return urljoin(home_url, href)

    raise ValueError("Could not find the Special Offers page.")


def extract_products(url: str, home_url: str = HOME_URL) -> list[Product]:
    """Extract product names and image URLs from a page."""
    content = get_html(url)
    soup = BeautifulSoup(content, "html.parser")
    products: list[Product] = []

    for image in soup.find_all("img"):
        image_url = image.get("src")
        name = image.get("title")

        if not image_url or not name or "product" not in image_url:
            continue

        products.append(
            Product(
                name=name,
                image_url=urljoin(home_url, image_url),
            )
        )

    return products


def safe_filename(name: str) -> str:
    """Convert a product name into a filesystem-friendly filename."""
    invalid_characters = '<>:"/\\|?*'
    cleaned = "".join("," if char in invalid_characters else char for char in name)
    cleaned = " ".join(cleaned.split()).strip(" .")

    return cleaned or "image"


async def download_product(
    session: aiohttp.ClientSession,
    product: Product,
    output_dir: Path,
) -> Path:
    """Download one product image and save it to the output directory."""
    destination = output_dir / f"{safe_filename(product.name)}.png"

    async with session.get(product.image_url) as response:
        response.raise_for_status()
        data = await response.read()

    async with aiofiles.open(destination, "wb") as file:
        await file.write(data)

    return destination


async def download_products(
    products: Iterable[Product],
    output_dir: Path = OUTPUT_DIR,
) -> list[Path]:
    """Download product images concurrently."""
    output_dir.mkdir(parents=True, exist_ok=True)
    products = list(products)

    timeout = aiohttp.ClientTimeout(total=30)

    async with aiohttp.ClientSession(
        headers=HEADERS,
        timeout=timeout,
    ) as session:
        tasks = [
            download_product(session, product, output_dir)
            for product in products
        ]
        return await asyncio.gather(*tasks)


async def main() -> None:
    """Find products and download their images."""
    special_offers_url = find_special_offers_url(HOME_URL)
    products = extract_products(special_offers_url)

    print(f"Found {len(products)} product images.")

    start = time.perf_counter()
    downloaded = await download_products(products)
    elapsed = time.perf_counter() - start

    print(f"Downloaded {len(downloaded)} images in {elapsed:.2f} seconds.")


if __name__ == "__main__":
    asyncio.run(main())
