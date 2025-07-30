from ..res import path_js
from .polyfill import btoa

try:
    from .expression.quickjs import exec_js

    exec_js_safe = exec_js
except ImportError:
    from .expression.playwright import exec_js, exec_js_safe


def minify_js(s, safe=False):
    func = exec_js_safe if safe else exec_js
    return func(
        """var result = minify_sync(atob('%s'), {output:{comments: false}});return result.code""" % btoa(s),
        paths=[path_js / 'terser.js'])
