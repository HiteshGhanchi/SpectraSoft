"""
SpectraSoft — Database Models
==============================
One table per analytical group stores ALL 13 pages of data as JSON columns.
This matches exactly how the old PDAWin software stored everything in one
Access database (DefAnainf.mdb) per technique group.

Design decision: One row per analytical group, all pages as JSON.
This keeps queries simple — to load a technique, you fetch one row.
To save any page change, you update one row.
"""

from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean
from sqlalchemy.sql import func
from core.database import Base


class AnalyticalGroup(Base):
    """
    One row = one complete analytical technique (e.g. "LAS 2023").
    All 13 pages of settings stored as JSON columns.
    """
    __tablename__ = "analytical_groups"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    name         = Column(String(100), nullable=False, unique=True, index=True)
    display_order = Column(Integer, default=0)  # for Arrange functionality
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    updated_at   = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Page 1 — Analytical Condition
    # Stores: analytical_method, purge times, sources, preburn, integ, clean,
    #         level_cut_information (monitor elements, H/L level %)
    page_01_condition = Column(JSON, default=dict)

    # Page 2 — Attenuator Information
    # Stores: list of {element, wavelength, att_value} rows
    page_02_attenuator = Column(JSON, default=dict)

    # Page 3 — Element Information
    # Stores: ch_value (int), list of {ele_name, range_min, range_max,
    #         is_internal_standard, chemic_ele, element} rows
    page_03_element = Column(JSON, default=dict)

    # Page 4 — Channel Information
    # Stores: list of {ele_name, w_length, seq, w_no,
    #         internal_element, internal_value} rows
    page_04_channel = Column(JSON, default=dict)

    # Page 5 — Measurement Mode
    # Stores: list of {ele_name, pi_mode, method, m, n, i, area} rows
    page_05_measurement = Column(JSON, default=dict)

    # Page 6 — Recalibration Information
    # Stores: list of {ele_name, sample_high, sample_low, sample_k,
    #         target_high, target_low, target_k, range_high, range_low, range_k,
    #         alpha, beta, k_coef} rows
    page_06_recalibration = Column(JSON, default=dict)

    # Page 7 — Working Curve and Matrix Coefficient
    # Stores: list of {ele_name, divide, no, range_min, range_max, unit,
    #         order, std, coef_a, coef_b, coef_c, coef_d,
    #         matrix_left: [{d_l, ele_name, coefficient}],
    #         matrix_right: [{d_l, ele_name, coefficient}]} rows
    page_07_working_curve = Column(JSON, default=dict)

    # Page 8 — 100% Correction
    # Stores: list of {ele_name, value} rows (value = Y / N / I)
    page_08_correction = Column(JSON, default=dict)

    # Page 9 — Standard Information
    # Stores: list of {ele_name, lower, upper, trace} rows
    page_09_standard = Column(JSON, default=dict)

    # Page 10 — Display and Printout Format
    # Stores: {disp_print: [{ele_name, order, magn, int, deci}],
    #          trans: [{ele_name, order, magn, int, deci}]}
    page_10_display = Column(JSON, default=dict)

    # Page 11 — Master Curve Information
    # Stores: list of {ele_name, mc_sample, target, d1, d2, ac, mc, flag} rows
    page_11_master_curve = Column(JSON, default=dict)

    # Page 12 — Analytical Mode
    # Stores: {common, cont: {...}, int: {...}, recal: {...}}
    page_12_analytical_mode = Column(JSON, default=dict)

    # Page 13 — Control Chart Information
    # Stores: {control_line, sigma_line, sigma_value, center_line,
    #          class_mark, display_scale, control_range_type,
    #          elements: [{ele_name, target, ctrl_l, ctrl_h, scale_l, scale_h}]}
    page_13_control_chart = Column(JSON, default=dict)

    def __repr__(self):
        return f"<AnalyticalGroup(id={self.id}, name='{self.name}')>"

    def to_dict(self):
        """Return a simple dict for UI use."""
        return {
            "id":           self.id,
            "name":         self.name,
            "display_order": self.display_order,
        }