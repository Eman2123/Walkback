from walkback.compute import compute_run
from walkback.tiles import synthetic_tile
from walkback.validation.report import status_line, write_report

PARAMS = {"habitat_row": 50, "habitat_col": 50, "budget_s": 900, "speed_mps": 0.5,
          "cutoff_deg": 20.0, "confidence": 0.9, "roughness": 0.5}


def test_status_line_follows_the_numbers():
    assert "SHORTFALL" in status_line(0.0)
    assert "meets" in status_line(0.97)
    assert "could not be computed" in status_line(None)


def test_report_written_with_required_sections(tmp_path):
    result = compute_run(synthetic_tile(), PARAMS)
    path = write_report(result, tmp_path / "validation_report.md")
    text = path.read_text(encoding="utf-8")
    for section in ["## Headline", "## Reliability", "## Assumptions used", "## Limits"]:
        assert section in text
    assert "assumed" in text and "Brier score" in text
