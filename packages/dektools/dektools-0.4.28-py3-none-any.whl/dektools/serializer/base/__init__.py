import os
import codecs
from io import BytesIO, StringIO
from ...file import sure_parent_dir, normal_path

DEFAULT_VALUE = type('default_value', (), {})


class SerializerBase:
    _persist_str = True
    _dumps_io = StringIO

    def __init__(self, encoding=None):
        self.encoding = encoding or "utf-8"

    def loads(self, s):
        if isinstance(s, str):
            s = s.encode(self.encoding)
        return self.load(BytesIO(s))

    def load(self, file, encoding=None, default=DEFAULT_VALUE):
        if not hasattr(file, 'read'):
            if not os.path.isfile(file) and default is not DEFAULT_VALUE:
                return default
            if self._persist_str:
                with codecs.open(file, encoding=encoding or self.encoding) as f:
                    return self._load_file(f)
            else:
                with open(file, 'rb') as f:
                    return self._load_file(f)
        else:
            return self._load_file(file)

    def _load_file(self, file):
        raise NotImplementedError

    def dumps(self, obj):
        file = self._dumps_io()
        self.dump(file, obj)
        return file.getvalue()

    def dump(self, file, obj, encoding=None, **kwargs):
        if not hasattr(file, 'write'):
            file = normal_path(file)
            sure_parent_dir(file)
            if self._persist_str:
                with codecs.open(file, 'w', encoding=encoding or self.encoding) as f:
                    self._dump_file(obj, f, kwargs)
            else:
                with open(file, 'wb') as f:
                    self._dump_file(obj, f, kwargs)
        else:
            self._dump_file(obj, file, kwargs)

    def _dump_file(self, obj, file, kwargs):
        raise NotImplementedError
