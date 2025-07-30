import fnmatch
from jinja2.ext import Extension


try:
    from jinja2 import pass_eval_context as eval_context
except ImportError:
    from jinja2 import evalcontextfilter as eval_context


@eval_context
def _fnmatch(eval_ctx, value, pattern):
    return fnmatch.fnmatch(value, pattern)


class FnMatchExtension(Extension):

    def __init__(self, environment):
        super(FnMatchExtension, self).__init__(environment)
        environment.filters['fnmatch'] = _fnmatch
