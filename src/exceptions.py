class BaseProjectException(Exception):
    def __init__(self, message, error_code=None, *args, **kwargs):
        self.error_code = error_code
        self.message = message
        super().__init__(message, *args)

    def to_dict(self):
        """Convert exception to dict for API responses"""
        return {"error_code": self.error_code, "message": self.message}


class ImproperlyConfiguredException(BaseProjectException):
    def __init__(self, message, parameter_name, *args, **kwargs):
        super().__init__(
            message, error_code="IMPROPERLY_CONFIGURED_ERROR", *args, **kwargs
        )
        self.field_name = parameter_name


class InsufficientRulesException(BaseProjectException):
    def __init__(self, *args, **kwargs):
        super().__init__(
            error_code="RULES_SET_INCORRECT",
            message="Insufficient number of rules or rules improperly set. "
            "At least one rule is required.",
            *args,
            **kwargs,
        )


class InvalidOperationException(BaseProjectException):
    def __init__(self, message, *args, **kwargs):
        super().__init__(
            error_code="INVALID_OPERATION", message=message, *args, **kwargs
        )


class InvalidClassificationEngineException(BaseProjectException):
    def __init__(self, message, *args, **kwargs):
        super().__init__(
            error_code="INVALID_CLASSIFICATION_ENGINE",
            message=message,
            *args,
            **kwargs,
        )


class EmptyDatasetException(BaseProjectException):
    def __init__(self, message, *args, **kwargs):
        super().__init__(
            error_code="EMPTY_DATASET", message=message, *args, **kwargs
        )
