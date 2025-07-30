"""Application exceptions."""


class DataRushError(Exception):
    """Base exception."""


class UnknownTableError(DataRushError):
    """Unknown table error."""


class TemplateAlreadyExistsError(DataRushError):
    """Template already exists error."""
