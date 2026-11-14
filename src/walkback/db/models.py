"""Schema from .10x/decisions/dba/walkback.md. Migrations are generated with Alembic.

Tables: datasets, terrain_tiles, runs, calibration, assumptions, validation_base.
"""
from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Dataset(Base):
    __tablename__ = "datasets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    source_url: Mapped[str] = mapped_column(String(1000))
    sha256: Mapped[str | None] = mapped_column(String(64))
    access_date: Mapped[datetime | None] = mapped_column(DateTime)
    resolution_m: Mapped[float | None] = mapped_column(Float)
    limitation: Mapped[str] = mapped_column(String(1000))


class TerrainTile(Base):
    __tablename__ = "terrain_tiles"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)  # allowlisted in api.py
    dataset_id: Mapped[int | None] = mapped_column(ForeignKey("datasets.id"))
    crop_name: Mapped[str] = mapped_column(String(200))
    resolution_m: Mapped[float] = mapped_column(Float)
    raster_path: Mapped[str] = mapped_column(String(1000))
    bounds_json: Mapped[dict] = mapped_column(JSON)


class Run(Base):
    __tablename__ = "runs"
    __table_args__ = (UniqueConstraint("param_hash", name="uq_runs_param_hash"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True)  # uuid4
    tile_id: Mapped[str] = mapped_column(ForeignKey("terrain_tiles.id"))
    params_json: Mapped[dict] = mapped_column(JSON)
    param_hash: Mapped[str] = mapped_column(String(64))
    region_det_geojson: Mapped[dict | None] = mapped_column(JSON)
    region_cal_geojson: Mapped[dict | None] = mapped_column(JSON)
    region_truth_geojson: Mapped[dict | None] = mapped_column(JSON)
    stats_json: Mapped[dict | None] = mapped_column(JSON)
    runtime_ms: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    calibration: Mapped["Calibration | None"] = relationship(back_populates="run", uselist=False)
    assumptions: Mapped[list["Assumption"]] = relationship(back_populates="run")


class Calibration(Base):
    __tablename__ = "calibration"
    run_id: Mapped[str] = mapped_column(ForeignKey("runs.id"), primary_key=True)
    bins_json: Mapped[list] = mapped_column(JSON)
    brier: Mapped[float] = mapped_column(Float)
    coverage: Mapped[float | None] = mapped_column(Float)
    coverage_ci_low: Mapped[float | None] = mapped_column(Float)
    coverage_ci_high: Mapped[float | None] = mapped_column(Float)

    run: Mapped[Run] = relationship(back_populates="calibration")


class Assumption(Base):
    __tablename__ = "assumptions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("runs.id"))
    name: Mapped[str] = mapped_column(String(100))
    value: Mapped[str] = mapped_column(String(200))
    label: Mapped[str] = mapped_column(String(20))  # measured | derived | assumed

    run: Mapped[Run] = relationship(back_populates="assumptions")


class ValidationBase(Base):
    __tablename__ = "validation_base"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tile_id: Mapped[str] = mapped_column(ForeignKey("terrain_tiles.id"))
    summary_json: Mapped[dict] = mapped_column(JSON)
    prereg_commit: Mapped[str] = mapped_column(String(64))
