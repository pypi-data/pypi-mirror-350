import importlib
import os
import warnings
import json

from codecraft.dump import dump  # noqa: F401

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

CODECRAFT_SITE_URL = "https://codecraft.chat"
CODECRAFT_APP_NAME = "CodeCraft"

os.environ["OR_SITE_URL"] = CODECRAFT_SITE_URL
os.environ["OR_APP_NAME"] = CODECRAFT_APP_NAME
os.environ["LITELLM_MODE"] = "PRODUCTION"

# `import litellm` takes 1.5 seconds, defer it!

VERBOSE = False


class LazyLiteLLM:
    _lazy_module = None

    def __getattr__(self, name):
        if name == "_lazy_module":
            return super()
        self._load_litellm()
        return getattr(self._lazy_module, name)

    def _load_litellm(self):
        if self._lazy_module is not None:
            return

        if VERBOSE:
            print("Loading litellm...")

        # Patch json.load to prevent encoding errors before importing litellm
        original_json_load = json.load
        
        def utf8_json_load(fp, *args, **kwargs):
            if hasattr(fp, 'encoding') and fp.encoding is None:
                content = fp.read()
                if isinstance(content, bytes):
                    content = content.decode('utf-8', errors='replace')
                return json.loads(content, *args, **kwargs)
            return original_json_load(fp, *args, **kwargs)
        
        json.load = utf8_json_load

        self._lazy_module = importlib.import_module("litellm")

        self._lazy_module.suppress_debug_info = True
        self._lazy_module.set_verbose = False
        self._lazy_module.drop_params = True
        self._lazy_module._logging._disable_debugging()


litellm = LazyLiteLLM()

__all__ = [litellm]
