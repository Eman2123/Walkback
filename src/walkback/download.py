"""Download source datasets and record checksums in data/manifest.csv."""

import csv
import hashlib
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


MANIFEST_PATH = Path("data/manifest.csv")

MANIFEST_FIELDS = [
    "source",
    "url",
    "checksum_sha256",
    "access_date",
    "notes",
]


def _format_size(size: int) -> str:
    """Format a byte count using a human-readable binary unit."""
    value = float(size)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if value < 1024 or unit == "TiB":
            return f"{value:.1f} {unit}"
        value /= 1024


def _write_progress(downloaded: int, expected_size: int | None) -> None:
    if expected_size is not None:
        percent = (
            100.0 if expected_size == 0 else downloaded / expected_size * 100
        )
        width = 30
        filled = (
            width
            if expected_size == 0
            else min(width, int(width * downloaded / expected_size))
        )
        progress = (
            f"{percent:5.1f}% [{'#' * filled}{'-' * (width - filled)}] "
            f"{_format_size(downloaded)} / {_format_size(expected_size)}"
        )
    else:
        progress = f"{_format_size(downloaded)} downloaded"

    sys.stderr.write(f"\rDownloading: {progress}")
    sys.stderr.flush()


def sha256(path: Path, chunk: int = 1 << 20) -> str:
    """Calculate SHA-256 without loading the entire file into memory."""
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)

    return h.hexdigest()


def update_manifest(
    url: str,
    checksum: str,
    manifest_path: Path,
) -> None:
    """Update the matching manifest entry after successful download."""

    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    if manifest_path.exists():
        with manifest_path.open(
            "r", newline="", encoding="utf-8"
        ) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

    found = False
    access_date = datetime.now(timezone.utc).date().isoformat()

    for row in rows:
        if row.get("url") == url:
            row["checksum_sha256"] = checksum
            row["access_date"] = access_date
            found = True
            break

    if not found:
        raise ValueError(
            f"URL not found in manifest: {url}"
        )

    temp_path = manifest_path.with_suffix(".csv.tmp")

    try:
        with temp_path.open(
            "w", newline="", encoding="utf-8"
        ) as f:
            writer = csv.DictWriter(
                f,
                fieldnames=MANIFEST_FIELDS,
            )
            writer.writeheader()
            writer.writerows(rows)

        os.replace(temp_path, manifest_path)

    finally:
        if temp_path.exists():
            temp_path.unlink()


def fetch(
    url: str,
    dest: Path,
    retries: int = 3,
    timeout: tuple = (20, 120),
    chunk_size: int = 1024 * 1024,
    manifest_path: Path = MANIFEST_PATH,
) -> Path:
    """
    Stream a download, retry failures, calculate checksum,
    and update the dataset manifest.
    """

    if retries < 1:
        raise ValueError("retries must be at least 1")

    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)

    temp_path = dest.with_name(dest.name + ".part")

    for attempt in range(1, retries + 1):
        try:
            downloaded = 0
            progress_started = False

            with requests.get(
                url,
                stream=True,
                timeout=timeout,
            ) as response:

                response.raise_for_status()

                expected_size = response.headers.get(
                    "Content-Length"
                )
                expected_bytes = (
                    int(expected_size) if expected_size is not None else None
                )
                last_progress = time.monotonic()
                _write_progress(downloaded, expected_bytes)
                progress_started = True

                with temp_path.open("wb") as f:
                    for chunk in response.iter_content(
                        chunk_size=chunk_size
                    ):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            now = time.monotonic()
                            if (
                                now - last_progress >= 0.5
                                or downloaded == expected_bytes
                            ):
                                _write_progress(downloaded, expected_bytes)
                                last_progress = now

                    f.flush()
                    os.fsync(f.fileno())

                if downloaded != expected_bytes:
                    _write_progress(downloaded, expected_bytes)
                sys.stderr.write("\n")
                progress_started = False

                if (
                    expected_bytes is not None
                    and downloaded != expected_bytes
                ):
                    raise IOError(
                        "Downloaded file size does not match "
                        "Content-Length."
                    )

            checksum = sha256(temp_path)

            os.replace(temp_path, dest)

            update_manifest(
                url=url,
                checksum=checksum,
                manifest_path=manifest_path,
            )

            return dest

        except (requests.RequestException, OSError, ValueError):

            if progress_started:
                sys.stderr.write("\n")
            if temp_path.exists():
                temp_path.unlink()

            if attempt == retries:
                raise

            time.sleep(2 ** (attempt - 1))

    raise RuntimeError("Download failed.")