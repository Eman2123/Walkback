import csv

from walkback import download


class FakeResponse:
    headers = {"Content-Length": "6"}

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return None

    def raise_for_status(self):
        pass

    def iter_content(self, chunk_size):
        yield b"abc"
        yield b"def"


def test_fetch_reports_progress_and_updates_manifest(
    tmp_path, monkeypatch, capsys
):
    url = "https://example.test/data.zip"
    destination = tmp_path / "data.zip"
    manifest_path = tmp_path / "manifest.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as manifest:
        writer = csv.DictWriter(
            manifest, fieldnames=download.MANIFEST_FIELDS
        )
        writer.writeheader()
        writer.writerow(
            {
                "source": "test",
                "url": url,
                "checksum_sha256": "TBD",
                "access_date": "TBD",
                "notes": "",
            }
        )

    monkeypatch.setattr(
        download.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(),
    )

    result = download.fetch(
        url, destination, chunk_size=3, manifest_path=manifest_path
    )

    assert result == destination
    assert destination.read_bytes() == b"abcdef"
    assert "100.0%" in capsys.readouterr().err
    with manifest_path.open(newline="", encoding="utf-8") as manifest:
        row = next(csv.DictReader(manifest))
    assert row["checksum_sha256"] != "TBD"
