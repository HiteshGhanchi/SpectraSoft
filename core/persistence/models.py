"""
SpectraSoft — Database Models
"""

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Index,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from import_data.constants import (
    ANALYTICAL_GROUP_NAME_MAX_LENGTH,
    ELEMENT_NAME_MAX_LENGTH,
    SOURCE_CODE_NAME_MAX_LENGTH,
    WAVELENGTH_MAX_LENGTH,
)
from core.persistence.database import Base


class AnalyticalGroup(Base):
    __tablename__ = "analytical_groups"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    name          = Column(String(ANALYTICAL_GROUP_NAME_MAX_LENGTH), nullable=False, unique=True, index=True)
    display_order = Column(Integer, default=0)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())
    updated_at    = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Page 1: Analytical condition / source timing
    page_01_source = Column(JSON, default=dict)

    # Page 2: Attenuator values
    page_02_attenuator = Column(JSON, default=dict)

    # Page 3: Channel order / ISE mapping
    page_03_channel = Column(JSON, default=dict)

    # Page 4: Drift targets and alpha/beta/k
    page_04_drift = Column(JSON, default=dict)

    # Page 5: Final working curve coefficients a,b,c,d
    page_05_wc = Column(JSON, default=dict)

    # Job 7 storage:
    # Drift-corrected intensity measurements for working curve standards.
    page_05_wc_measurements = Column(JSON, default=dict)

    # Regression storage:
    # Certified chemical values for standards.
    page_05_chemical_standards = Column(JSON, default=dict)

    # Later correction pages
    page_06_matrix = Column(JSON, default=dict)
    page_07_master = Column(JSON, default=dict)
    page_08_display = Column(JSON, default=dict)
    page_09_purity = Column(JSON, default=dict)

    def __repr__(self):
        return f"<AnalyticalGroup(id={self.id}, name='{self.name}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "display_order": self.display_order,
        }


class WorkingStandard(Base):
    """One group-scoped physical working-curve standard registration."""

    __tablename__ = "working_standards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    analytical_group_id = Column(
        Integer, ForeignKey("analytical_groups.id"), nullable=False, index=True
    )
    sample_name = Column(String(100), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    values = relationship(
        "WorkingStandardValue", back_populates="standard", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("length(trim(sample_name)) > 0", name="ck_working_standard_name"),
        UniqueConstraint(
            "analytical_group_id", "sample_name", name="uq_working_standard_group_sample"
        ),
    )


class WorkingStandardValue(Base):
    """Known chemical value for one standard and one analytical element."""

    __tablename__ = "working_standard_values"

    id = Column(Integer, primary_key=True, autoincrement=True)
    standard_id = Column(Integer, ForeignKey("working_standards.id"), nullable=False, index=True)
    element_key = Column(String(100), nullable=False)
    known_value = Column(Float, nullable=False)

    standard = relationship("WorkingStandard", back_populates="values")

    __table_args__ = (
        UniqueConstraint(
            "standard_id", "element_key", name="uq_working_standard_value_element"
        ),
    )


class WorkingCurveMeasurement(Base):
    """Latest accepted Job 7 corrected intensity per standard and element."""

    __tablename__ = "working_curve_measurements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    analytical_group_id = Column(
        Integer, ForeignKey("analytical_groups.id"), nullable=False, index=True
    )
    standard_id = Column(Integer, ForeignKey("working_standards.id"), nullable=False, index=True)
    element_key = Column(String(100), nullable=False)
    corrected_intensity = Column(Float, nullable=False)
    burn_count = Column(Integer, nullable=False, default=0)
    measured_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            "standard_id", "element_key", name="uq_working_measurement_standard_element"
        ),
    )


class WorkingCurve(Base):
    """Versioned curve metadata for one group and element."""

    __tablename__ = "working_curves"

    id = Column(Integer, primary_key=True, autoincrement=True)
    analytical_group_id = Column(
        Integer, ForeignKey("analytical_groups.id"), nullable=False, index=True
    )
    element_key = Column(String(100), nullable=False)
    name = Column(String(120), nullable=False)
    curve_type = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="inactive")
    point_count = Column(Integer, nullable=False, default=0)
    r2 = Column(Float)
    rmse = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    retired_at = Column(DateTime(timezone=True))

    coefficients = relationship(
        "WorkingCurveCoefficient", back_populates="curve", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index(
            "uq_working_curve_active_group_element",
            "analytical_group_id",
            "element_key",
            unique=True,
            sqlite_where=text("status = 'active'"),
        ),
    )


class WorkingCurveCoefficient(Base):
    """Polynomial coefficients for a versioned working curve."""

    __tablename__ = "working_curve_coefficients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    curve_id = Column(Integer, ForeignKey("working_curves.id"), nullable=False, index=True)
    a = Column(Float, nullable=False, default=0.0)
    b = Column(Float, nullable=False, default=0.0)
    c = Column(Float, nullable=False, default=1.0)
    d = Column(Float, nullable=False, default=0.0)

    curve = relationship("WorkingCurve", back_populates="coefficients")


class MatrixCorrection(Base):
    """Versioned matrix correction for one target/interfering pair."""

    __tablename__ = "matrix_corrections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    analytical_group_id = Column(
        Integer, ForeignKey("analytical_groups.id"), nullable=False, index=True
    )
    target_element_key = Column(String(100), nullable=False)
    interfering_element_key = Column(String(100), nullable=False)
    correction_type = Column(String(1), nullable=False)
    coefficient = Column(Float, nullable=False, default=0.0)
    status = Column(String(20), nullable=False, default="inactive")
    version_name = Column(String(120), nullable=False)
    source_working_curve_id = Column(
        Integer, ForeignKey("working_curves.id"), nullable=True, index=True
    )
    point_count = Column(Integer, nullable=False, default=0)
    r2 = Column(Float)
    rmse = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    retired_at = Column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint(
            "correction_type IN ('L', 'D')",
            name="ck_matrix_correction_type",
        ),
        Index(
            "uq_matrix_correction_active_pair",
            "analytical_group_id",
            "target_element_key",
            "interfering_element_key",
            "correction_type",
            unique=True,
            sqlite_where=text("status = 'active'"),
        ),
    )


class AnalysisResult(Base):
    """Filed Job X/Job Y result with traceable method and burn data."""

    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    analytical_group_id = Column(
        Integer, ForeignKey("analytical_groups.id"), nullable=False, index=True
    )
    job = Column(String(10), nullable=False)
    sample_name = Column(String(120), nullable=False, index=True)
    occurred_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    burns = Column(JSON, nullable=False, default=list)
    averages = Column(JSON, nullable=False, default=dict)
    final_concentrations = Column(JSON, nullable=False, default=dict)
    flags = Column(JSON, nullable=False, default=dict)
    method_snapshot = Column(JSON, nullable=False, default=dict)


class ProductSpecification(Base):
    """Group-scoped product limits used for result flags and reports."""

    __tablename__ = "product_specifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    analytical_group_id = Column(Integer, ForeignKey("analytical_groups.id"), nullable=False, index=True)
    product_name = Column(String(120), nullable=False)
    element_key = Column(String(100), nullable=False)
    lower_limit = Column(Float)
    upper_limit = Column(Float)
    trace_limit = Column(Float)


class RControlSetting(Base):
    """Quadratic repeated-burn width allowance per group and element."""

    __tablename__ = "r_control_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    analytical_group_id = Column(Integer, ForeignKey("analytical_groups.id"), nullable=False, index=True)
    element_key = Column(String(100), nullable=False)
    a = Column(Float, nullable=False, default=0.0)
    b = Column(Float, nullable=False, default=0.0)
    c = Column(Float, nullable=False, default=0.0)


class ResultCalculationSetting(Base):
    """Optional result-calculation switches kept separate from group JSON."""

    __tablename__ = "result_calculation_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    analytical_group_id = Column(Integer, ForeignKey("analytical_groups.id"), nullable=False, unique=True)
    settings = Column(JSON, nullable=False, default=dict)


class InstrumentConfiguration(Base):
    """The installed emission-unit configuration for the whole instrument."""

    __tablename__ = "instrument_configuration"

    id = Column(Integer, primary_key=True)
    emission_unit_type = Column(String(20), nullable=False)

    __table_args__ = (
        CheckConstraint("id = 1", name="ck_instrument_configuration_singleton"),
        CheckConstraint(
            "emission_unit_type IN ('HPSG_300', 'HVS')",
            name="ck_instrument_configuration_emission_unit",
        ),
    )

    def __repr__(self):
        return (
            f"<InstrumentConfiguration(id={self.id}, "
            f"emission_unit_type='{self.emission_unit_type}')>"
        )


class SourceCode(Base):
    """
    16 fixed rows, entry_no 0-15.

    entry_no is the hardware command value sent over UART.
    name is the user-editable label shown in dropdowns.
    """
    __tablename__ = "source_codes"

    entry_no = Column(Integer, primary_key=True)
    name = Column(String(SOURCE_CODE_NAME_MAX_LENGTH), default="")

    def __repr__(self):
        return f"<SourceCode(entry_no={self.entry_no}, name='{self.name}')>"


class MasterElement(Base):
    """
    Master list of all elements the spectrometer supports.

    Users can add/edit/remove entries from the Settings page.
    Page 02 Attenuator and other pages pull from this table.

    itg_no is the hardware channel identifier.
    """
    __tablename__ = "master_elements"

    itg_no = Column(Integer, primary_key=True)
    ele_name = Column(String(ELEMENT_NAME_MAX_LENGTH), nullable=False)
    wavelength = Column(String(WAVELENGTH_MAX_LENGTH), default="")

    def __repr__(self):
        return f"<MasterElement(itg_no={self.itg_no}, ele_name='{self.ele_name}')>"
