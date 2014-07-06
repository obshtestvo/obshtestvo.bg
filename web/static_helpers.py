import os

from django.conf import settings
from compressor.filters import CompilerFilter, FilterError
from compressor.cache import get_hashed_mtime, get_hashed_content

class SassFilter(CompilerFilter):
    command = "{binary} {args} {infile} {outfile}"
    type = 'css'
    options = (
        ("binary", settings.SASS_BINARY_PATH),
        ("args", " --compass --sourcemap"),
    )

    def __init__(self, content, attrs, *args, **kwargs):
        super(SassFilter, self).__init__(content, command=self.command, *args, **kwargs)

    def input(self, **kwargs):
        cachefilename = self.get_cachefilename()
        if os.path.isfile(cachefilename):
            cache = open(cachefilename, 'r')
            return cache.read()

        content = super(SassFilter, self).input(**kwargs)
        cache = open(cachefilename, 'w')
        cache.write(content)
        return content

    def get_cachefilename(self):
        if settings.COMPRESS_CSS_HASHING_METHOD == "mtime":
            cached_name = get_hashed_mtime(self.filename)
        elif settings.COMPRESS_CSS_HASHING_METHOD in ("hash", "content"):
            cached_name = get_hashed_content(self.filename)
        else:
            raise FilterError('COMPRESS_CSS_HASHING_METHOD is configured '
                              'with an unknown method (%s).' %
                              settings.COMPRESS_CSS_HASHING_METHOD)

        return os.path.join(settings.COMPRESS_ROOT, settings.COMPRESS_OUTPUT_DIR, cached_name + '.css')
