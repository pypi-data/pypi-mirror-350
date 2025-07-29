from ._version import __version__


def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": "escobar"
    }]


def _jupyter_server_extension_points():
    return [{
        "module": "escobar"
    }]


def _load_jupyter_server_extension(server_app):
    """
    Register the server extension handlers
    """
    from .handlers import setup_handlers
    setup_handlers(server_app.web_app)
    server_app.log.info("Registered escobar server extension")
