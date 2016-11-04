import optparse
import sys
import tokenize
from collections import namedtuple
import re

import ast

__version__ = '0.1.0'

Error = namedtuple('Error', ['lineno', 'code', 'message'])

class Crawler(ast.NodeVisitor):

    def __init__(self, desired_bases, desired_funcs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.desired_bases = desired_bases
        self.desired_funcs = desired_funcs
        self.results = []

    def visit_FuncDef(self, node):
        pass

    def consolidateName(self, node):
        if isinstance(node, ast.Attribute):
            return "%s.%s" % (self.consolidateName(node.value), node.attr)
        elif isinstance(node, ast.Name):
            return node.id
        else:
            print(node)
            return "<%s>" % node.__class__.__name__

    def visit_RequestFuncDef(self, node):
        return [self.consolidateName(decorator) for decorator in node.decorator_list]

    def visit_ClassDef(self, node):
        if not any([base.id in self.desired_bases for base in node.bases]):
            return
        for func in node.body:
            if func.name not in self.desired_funcs:
                continue
            result = self.visit_RequestFuncDef(func)
            self.results.append((func, result))

    def get_results(self):
        return self.results

    def get_errors(self):
        errors = []
        for (func, decorators) in self.results:
            if not any([re.search(r"^permission", decorator) for decorator in decorators]):
                errors.append(Error(func.lineno, 'H800', "endpoint requires permission definition."))
        return errors

class WebcheckPlugin(object):
    """WebCheckker static analysis"""
    name = 'flake8_webcheck'
    version = __version__
    _code = 'H80'
    _error_tmpl = "H80 %r has no permission declaration"
    run_webcheck = False

    def __init__(self, tree, filename):
        self.tree = tree

    @classmethod
    def add_options(cls, parser):
        flag = '--webcheck'
        kwargs = {
            'default': False,
            'action': 'store_true',
            'help': 'Run Webchecks',
            'parse_from_config': 'True',
        }
        config_opts = getattr(parser, 'config_options', None)
        parser.add_option(flag, **kwargs)

        parser.add_option("-c", "--classname", dest="classname",
                        help="base class to check for decorators",
                        default="BaseHandler")
        parser.add_option("-f", "--funcs", dest="funcs",
                        help="functions to check for decorators",
                        default="index,get,put,patch,post,delete")
        parser.add_option("-d", "--decorator", dest="decorator",
                        help="decorator to check for existance",
                        default="permission")


    @classmethod
    def parse_options(cls, options):
        cls.run_webcheck = int(options.webcheck)
        cls.classname = options.classname
        cls.funcs = options.funcs.split(",")

    def run(self):
        if not self.run_webcheck:
            return

        crawler = Crawler(self.classname, self.funcs)
        crawler.visit(self.tree)

        for error in crawler.get_errors():
            yield (error.lineno, 0, "%s %s" % (error.code, error.message), type(self))

def _read(filename):
    """Read the source code."""
    try:
        with open(filename, 'rb') as f:
            (encoding, _) = tokenize.detect_encoding(f.readline)
    except (LookupError, SyntaxError, UnicodeError):
        # Fall back if file encoding is improperly declared
        with open(filename, encoding='latin-1') as f:
            return f.read()
    with open(filename, 'r', encoding=encoding) as f:
        return f.read()


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    opar = optparse.OptionParser()
    WebcheckPlugin.add_options(opar)
    options, args = opar.parse_args(argv)

    if len(args) < 1:
        print("Usage: %s <file>" % sys.argv[0])
    code = _read(args[0])
    tree = compile(code, args[0], "exec", ast.PyCF_ONLY_AST)

    crawler = Crawler(options.classname, options.funcs.split(","))
    crawler.visit(tree)
    results = crawler.get_results()

    print(crawler.get_results())
    print(crawler.get_errors())

if __name__ == '__main__':
    main(sys.argv[1:])
