import os
import codecs
import hashlib

from django.conf import settings

from compressor.filters import CompilerFilter
from compressor.exceptions import FilterError

class SassSimpleFilter(CompilerFilter):

    def input(self, **kwargs):
        sass_binary = settings.SASS_BINARY_PATH
        if sass_binary is None or not os.path.exists(sass_binary):
            raise FilterError( "Please set path to `sass` binary - settings.SASS_BINARY_PATH")

        input_is_not_file = self.infile is None and self.filename is None and "{infile}" in self.command
        if input_is_not_file:
            raise FilterError(type(self).__name__ + " can't compile embedded SASS or SCSS. Please use another compiler filter.")

        cachefilename = self.get_cachefilename(self.filename)
        if not os.path.exists(cachefilename):
            raise FilterError("Compiled CSS can't be found: %s" % cachefilename)

        cache = codecs.open(cachefilename, "r", "utf-8")
        return cache.read()

    @staticmethod
    def get_cachefilename(filename):
        cached_name = hashlib.md5(filename).hexdigest()
        return os.path.join(settings.COMPRESS_ROOT, settings.COMPRESS_OUTPUT_DIR, cached_name + '.css')
