"""
SpectraSoft — Database Models
"""

from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from core.database import Base


class AnalyticalGroup(Base):
    __tablename__ = "analytical_groups"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    name          = Column(String(100), nullable=False, unique=True, index=True)
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


class SourceCode(Base):
    """
    16 fixed rows, entry_no 0-15.

    entry_no is the hardware command value sent over UART.
    name is the user-editable label shown in dropdowns.
    """
    __tablename__ = "source_codes"

    entry_no = Column(Integer, primary_key=True)
    name = Column(String(100), default="")

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
    ele_name = Column(String(20), nullable=False)
    wavelength = Column(String(20), default="")

    def __repr__(self):
        return f"<MasterElement(itg_no={self.itg_no}, ele_name='{self.ele_name}')>"