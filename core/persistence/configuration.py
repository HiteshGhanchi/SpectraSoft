"""Persistence helpers for singleton instrument configuration."""

from core.persistence.models import InstrumentConfiguration
from import_data.constants import (
    DEFAULT_EMISSION_UNIT_TYPE,
    EMISSION_UNIT_TYPES,
)


INSTRUMENT_CONFIGURATION_ID = 1


def _validate_emission_unit_type(emission_unit_type: str) -> str:
    value = str(emission_unit_type).strip().upper()
    if value not in EMISSION_UNIT_TYPES:
        supported = ", ".join(EMISSION_UNIT_TYPES)
        raise ValueError(
            f"Unsupported emission unit '{emission_unit_type}'. "
            f"Supported: {supported}"
        )
    return value


def get_or_create_instrument_configuration(session) -> InstrumentConfiguration:
    """Return the one instrument configuration row, creating its default."""
    configs = session.query(InstrumentConfiguration).order_by(
        InstrumentConfiguration.id
    ).all()
    if len(configs) > 1:
        raise ValueError("Instrument configuration must contain exactly one row")
    config = session.get(InstrumentConfiguration, INSTRUMENT_CONFIGURATION_ID)
    if config is None:
        config = InstrumentConfiguration(
            id=INSTRUMENT_CONFIGURATION_ID,
            emission_unit_type=DEFAULT_EMISSION_UNIT_TYPE,
        )
        session.add(config)
        session.commit()
        session.refresh(config)
    else:
        _validate_emission_unit_type(config.emission_unit_type)
    return config


def set_emission_unit_type(session, emission_unit_type: str) -> InstrumentConfiguration:
    """Validate and persist the installed emission-unit type."""
    value = _validate_emission_unit_type(emission_unit_type)
    config = get_or_create_instrument_configuration(session)
    config.emission_unit_type = value
    session.commit()
    session.refresh(config)
    return config
