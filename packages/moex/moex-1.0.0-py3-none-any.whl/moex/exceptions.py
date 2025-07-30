# -*- coding: utf-8 -*-

__all__ = ("HandlersSearchError", "TemplateRenderError", "TemplateSearchError")


class HandlersError(Exception):
    """Base class for handlers errors
    """


class TemplatesRepositoryError(Exception):
    """Base class for templates errors
    """


class HandlersSearchError(HandlersError):
    """Handlers Search Error
    """
    def __init__(self, *args):
        """Unpack args and call parent method
        """
        super().__init__(*args)
        self.output_format = args[0]
        self.formats = args[1]

    def __str__(self):
        """Str method

        Returns
        -------
        str
            String representation
        """
        return f"Can't find handler for format: {self.output_format}. Choose one of: {self.formats}"


class TemplateRenderError(TemplatesRepositoryError):
    """Template Render Error
    """
    def __init__(self, *args):
        """Unpack args and call parent method
        """
        super().__init__(*args)
        self.diff = args[0]
        self.path = args[1]

    def __str__(self):
        """Str method

        Returns
        -------
        str
            String representation
        """
        return f"You forget set up params: {self.diff} for template: {self.path}"


class TemplateSearchError(TemplatesRepositoryError):
    """Template Search Error
    """
    def __init__(self, *args):
        """Unpack args and call parent method
        """
        super().__init__(*args)
        self.template_id = args[0]

    def __str__(self):
        """Str method

        Returns
        -------
        str
            String representation
        """
        return f"Can't find template with id: {self.template_id}"
