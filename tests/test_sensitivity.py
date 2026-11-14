from walkback.sensitivity import CONFIDENCE_GRID, ROUGHNESS_GRID, run_sensitivity, write_outputs
from walkback.tiles import synthetic_tile


def test_grid_has_nine_rows_and_one_default(tmp_path):
    rows = run_sensitivity(synthetic_tile(), habitat_row=49, habitat_col=50)
    assert len(rows) == len(ROUGHNESS_GRID) * len(CONFIDENCE_GRID) == 9
    assert sum(1 for r in rows if r["is_default"]) == 1
    default = next(r for r in rows if r["is_default"])
    assert (default["roughness"], default["confidence"]) == (0.5, 0.9)


def test_outputs_written(tmp_path):
    rows = run_sensitivity(synthetic_tile(), habitat_row=49, habitat_col=50)
    csv_path, md_path = write_outputs(rows, "test tile", tmp_path)
    assert csv_path.read_text().count("\n") == 10  # header + 9 rows
    text = md_path.read_text()
    assert "Default setting" in text and "Highest coverage" in text
