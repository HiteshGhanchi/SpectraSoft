# https://app.eraser.io/workspace/zyjpVPN1yASJE0esOk0H
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

    page_01_condition      = Column(JSON, default=dict)
    page_02_attenuator     = Column(JSON, default=dict)
    page_03_element        = Column(JSON, default=dict)
    page_04_channel        = Column(JSON, default=dict)
    page_05_measurement    = Column(JSON, default=dict)
    page_06_recalibration  = Column(JSON, default=dict)
    page_07_working_curve  = Column(JSON, default=dict)
    page_08_correction     = Column(JSON, default=dict)
    page_09_standard       = Column(JSON, default=dict)
    page_10_display        = Column(JSON, default=dict)
    page_11_master_curve   = Column(JSON, default=dict)
    page_12_analytical_mode = Column(JSON, default=dict)
    page_13_control_chart  = Column(JSON, default=dict)

    def __repr__(self):
        return f"<AnalyticalGroup(id={self.id}, name='{self.name}')>"

    def to_dict(self):
        return {
            "id":            self.id,
            "name":          self.name,
            "display_order": self.display_order,
        }


class SourceCode(Base):
    """
    16 fixed rows (entry_no 0-15).
    entry_no is the hardware command value sent over UART.
    name is user-editable label shown in dropdowns.
    """
    __tablename__ = "source_codes"

    entry_no = Column(Integer, primary_key=True)  # 0-15, no autoincrement
    name     = Column(String(100), default="")

    def __repr__(self):
        return f"<SourceCode(entry_no={self.entry_no}, name='{self.name}')>"