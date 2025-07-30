# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "jinja2",
#     "toml",
#     "PyYAML",
# ]
# ///

import argparse
import importlib.machinery
import importlib.util
import json
import pickle
import re
import sys
from io import StringIO
from os import chdir, environ, pathsep
from pathlib import Path
from pprint import pprint
from typing import Any, Callable, Generator, Optional, Type, get_type_hints

import jinja2

INCLUDE_PATH_ENVIRONMENT_VARIABLE = 'JINJA_TEMPLATE_DIRS'
PRELOAD_ENVIRONMENT_VARIABLE = 'HOKORA_MODULES'

PYTHON_MODULE_EXTENSIONS = (
    'py',
    'pyc',
    'pyd',
    'so',
)

EPILOG = f"""

ENVIRONMENT VARIABLES

  $JINJA_TEMPLATE_DIRS
    A {pathsep}-separated list of additional template include paths, which
    will be searched to handle {{%extends %}}, {{%include %}} and {{%import %}}
    tags unless --no-include-env is passed at the command line.

  $HOKORA_MODULES
    Additional python modules (honoring $PYTHONPATH) to import at load time.
    These can be used to extend the functionality of hokora if they contain
    subclasses of DataFormat or HokoraFeature.
"""


def dynamic_import(filename_or_module_name: str | Path, module_name=None):
    if isinstance(filename_or_module_name, str):
        try:
            return __import__(filename_or_module_name)
        except ModuleNotFoundError:
            pass

    try:
        path = Path(filename_or_module_name).resolve()
    except OSError:
        raise ModuleNotFoundError(module_name or filename_or_module_name)

    if not module_name:
        module_name = path.name.split('.')[0]

    if path.is_file() and not any(
        path.name.endswith(f'.{x}') for x in PYTHON_MODULE_EXTENSIONS
    ):
        # importlib's spec_from_file_location will balk unless it can
        # recognize a file by extension, but shebang'd python scripts on unix
        # systems won't necessarily have any extension.
        loader0 = importlib.machinery.SourceFileLoader(module_name, str(path))
        spec = importlib.util.spec_from_loader(module_name, loader0)
    else:
        spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None:
        raise ModuleNotFoundError(module_name)
    loader = spec.loader
    if loader is None:
        raise ImportError(module_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    loader.exec_module(module)
    return module


class HokoraFeature:
    abstract: bool = True

    @classmethod
    def find_all(cls) -> Generator[Type['HokoraFeature'], None, None]:
        queue = [HokoraFeature.__subclasses__()]
        while queue:
            for cls in queue.pop(0):
                if cls.__dict__.get('abstract'):
                    queue.append(cls.__subclasses__())
                else:
                    cls.abstract = False
                    yield cls

    @classmethod
    def configure_argparse(cls, parser: argparse.ArgumentParser):
        pass

    @classmethod
    def argparse_namespace_to_instance(
        cls, args, template_path: Optional[Path] = None
    ) -> 'HokoraFeature':
        hints = get_type_hints(cls)
        return cls(
            template_path=template_path,
            **{k: v for k, v in args.__dict__.items() if k in hints},
        )

    def __init__(self, template_path: Optional[Path], **kw):
        self.template_path = template_path
        for k, v in kw.items():
            setattr(self, k, v)

    def update_jinja_include_paths(self, paths: list):
        pass

    def update_jinja_environment_init_args(self, kw: dict):
        pass

    def update_jinja_environment(self, env: jinja2.Environment):
        pass

    def update_template_context(self, context: dict):
        pass

    def postprocess_output(self, output: str) -> str:
        return output


class AbstractFeature(HokoraFeature):
    abstract = True


class NonAbstractFeature(AbstractFeature):
    pass


class DataFormat(HokoraFeature):
    abstract: bool = True
    extensions: tuple[str, ...] = tuple[str, ...]()
    _dump: Optional[Callable] = None
    name: str

    @classmethod
    def filter_name(self) -> Optional[str]:
        if self._dump or self.filter != DataFormat.filter:
            return self.name
        return None

    def __init_subclass__(cls):
        super().__init_subclass__()
        if not cls.__dict__.get('name') and not cls.__dict__.get('abstract'):
            cls.name = cls.__name__.replace('DataFormat', '').lower()

    def load_as_context(self, path: Path, key: Optional[str]):
        with open(path) as f:
            loaded = self._load(f)
        if isinstance(loaded, dict) or key is not None:
            return loaded
        if key is None:
            key = path.name.split('.')[0]
        return {key: loaded}

    def _load(self, fd):
        raise NotImplementedError(
            f'Subclass {type(self)} must override _load or load_as_context'
        )

    def update_jinja_environment(self, env: jinja2.Environment):
        if filter_name := self.filter_name():
            env.filters[filter_name] = self.filter

    def filter(self, value) -> str:
        if self._dump is None:
            raise NotImplementedError(
                f'Subclass {type(self)} must override _dump or filter'
            )
        with StringIO() as sio:
            self._dump(value, sio)
            return sio.getvalue()


class JsonDataFormat(DataFormat):
    extensions = ('json',)
    _load = staticmethod(json.load)

    def _dump(self, obj, stream):
        json.dump(obj, stream, indent=2)


class PythonDataFormat(DataFormat):
    extensions = PYTHON_MODULE_EXTENSIONS
    _dump = staticmethod(pprint)

    def load_as_context(self, path, key):
        return dynamic_import(path, key).__dict__


class PickleDataFormat(DataFormat):
    extensions = ('pkl', 'pickle')
    _load = staticmethod(pickle.load)
    _dump = staticmethod(pickle.dump)


try:
    try:
        import toml

        _toml_dump = staticmethod(toml.dump)
    except ModuleNotFoundError:
        import tomllib as toml  # type: ignore
except ModuleNotFoundError:
    pass
else:

    class TomlDataFormat(DataFormat):
        extensions = ('toml',)
        _load = staticmethod(toml.load)
        try:
            _dump = staticmethod(toml.dump)
        except AttributeError:
            pass


try:
    import yaml
except ModuleNotFoundError:
    pass
else:

    class YamlDataFormat(DataFormat):
        extensions = ('yaml', 'yml')
        _load = staticmethod(yaml.safe_load)
        _dump = staticmethod(yaml.dump)


class ExternalContext(HokoraFeature):
    context: dict

    @classmethod
    def configure_argparse(cls, parser: argparse.ArgumentParser):
        ctx = parser.add_argument_group('Jinja Context Variables')
        ctx.add_argument(
            '--context',
            '-c',
            action='append',
            default=[],
            help=(
                'Read the given file for context values to supply as jinja '
                'variables. Use key=filename if you want to namespace the '
                'data, like {{key.somevar}}. See AVAILABLE CONTEXT FORMATS '
                'below for supported file extensions.'
            ),
        )
        ctx.add_argument(
            '--environ',
            '-e',
            dest='context',
            action='append_const',
            const=dict(environ),
            help='Make environment variables available as jinja variables',
        )

    @classmethod
    def argparse_namespace_to_instance(
        cls, args, template_path: Optional[Path] = None
    ) -> 'HokoraFeature':
        context = {}
        for entry in args.context:
            if isinstance(entry, dict):
                context.update(entry)
                continue
            if not isinstance(entry, str):
                raise TypeError(f'{entry!r} is neither dict nor str')
            key, equals, filename = entry.partition('=')
            if not equals:
                filename = key
                key = ''

            filename, *args = filename.split(pathsep)
            kw = {}
            for a in args:
                k, eq, v = a.partition('=')
                if eq:
                    kw[k] = v
                elif k.startswith('-'):
                    kw[k[1:]] = False
                else:
                    kw[k] = True

            if not (ext := kw.pop('type', None)):
                _, dot, ext = filename.rpartition('.')
                if not dot:
                    raise ValueError(f"Can't detect format of {filename!r}")

            for fmt in DataFormat.__subclasses__():
                if ext.lower() in fmt.extensions:
                    loader_class = fmt
                    break
            else:
                raise ValueError(f'Unknown file type {ext}')

            loader = loader_class(template_path=template_path, **kw)
            value = loader.load_as_context(Path(filename), key)

            if key:
                context[key] = value
            else:
                context.update(value)
        return cls(template_path=template_path, context=context)

    def update_template_context(self, context: dict):
        context.update(self.context)


class TemplateSearchPaths(HokoraFeature):
    paths: list[Path]

    @classmethod
    def configure_argparse(cls, parser: argparse.ArgumentParser):
        group = parser.add_argument_group('Template search paths')
        group.add_argument(
            '-C',
            help=(
                'Change directories to this folder and interpret all paths as '
                'relative to it.'
            ),
            action='store',
        )
        group.add_argument(
            '--no-include-env',
            help=(
                f"Don't parse ${INCLUDE_PATH_ENVIRONMENT_VARIABLE} for "
                'include folders'
            ),
            action='store_true',
        )
        group.add_argument(
            '--no-include-cwd',
            help=(
                "Don't include the current working directory in the search path"
            ),
            action='store_true',
        )
        group.add_argument(
            '--no-include-template-dir',
            help="Don't include the template's folder in the search path.",
            action='store_true',
        )
        group.add_argument(
            '--include',
            '-I',
            help='Add this folder to the template include path',
            action='append',
            default=[],
        )

    @classmethod
    def argparse_namespace_to_instance(
        cls, args, template_path: Optional[Path] = None
    ) -> 'HokoraFeature':
        if args.C:
            chdir(args.C)
        paths = [Path(x).resolve() for x in args.include]
        if not args.no_include_env:
            env = environ.get(INCLUDE_PATH_ENVIRONMENT_VARIABLE, '')
            paths.extend(Path(e) for e in env.split(pathsep) if e)
        if template_path is not None and not args.no_include_template_dir:
            paths.append(template_path.parent)
        if not args.no_include_cwd:
            paths.append(Path('.'))

        return cls(
            template_path=template_path,
            paths=[p.resolve() for p in paths if p.is_dir()],
        )

    def update_jinja_include_paths(self, paths: list):
        paths.extend(self.paths)


class Autoescape(HokoraFeature):
    autoescape: bool | Callable = jinja2.select_autoescape(
        default_for_string=False
    )

    @classmethod
    def configure_argparse(cls, parser: argparse.ArgumentParser):
        parser.add_argument(
            '--autoescape',
            action=argparse.BooleanOptionalAction,
            default=cls.autoescape,
            help='whether to escape HTML entities in jinja expressions',
        )

    def update_jinja_environment_init_args(self, kw):
        kw['autoescape'] = self.autoescape


class StripShebang(HokoraFeature):
    strip_shebang: bool = False

    @classmethod
    def configure_argparse(cls, parser: argparse.ArgumentParser):
        parser.add_argument(
            '--strip-shebang',
            action=argparse.BooleanOptionalAction,
            help='remove the first line of the output if it is a bash shebang',
        )

    def postprocess_output(self, output: str) -> str:
        if self.strip_shebang and output.startswith('#!'):
            return output.partition('\n')[-1]
        return output


class CleanWhitespace(HokoraFeature):
    clean_whitespace: bool = False
    line_endings: Optional[str] = None

    # https://en.wikipedia.org/wiki/Newline#Unicode
    UNICODE_LINE_BREAKS = (
        ('\u0085', 'NEL'),
        ('\u000a', 'LF', r'\n'),
        ('\u000b', 'VT'),
        ('\u000c', 'FF', r'\f'),
        ('\u000d', 'CR', r'\r'),
        ('\u2028', 'LS'),
        ('\u2029', 'PS'),
    )

    @classmethod
    def parse_line_ending_string(cls, user_input: str) -> str:
        if user_input:
            out = user_input
            ok_chars = set()
            for char, *codewords in cls.UNICODE_LINE_BREAKS:
                ok_chars.add(char)
                codewords += (r'\u%04x' % ord(char), r'\x%02x' % ord(char))
                out = re.sub(
                    '|'.join(re.escape(x) for x in codewords), char, out
                )
            return out
        return user_input

    @classmethod
    def configure_argparse(cls, parser: argparse.ArgumentParser):
        parser.add_argument(
            '--clean-whitespace',
            '-w',
            action=argparse.BooleanOptionalAction,
            help='Remove trailing whitespace from lines of the output',
        )
        parser.add_argument(
            '--line-endings',
            nargs='?',
            default=None,
            const='\r\n' if sys.platform == 'win32' else '\n',
            action='store',
            type=cls.parse_line_ending_string,
            help='Normalize line endings of the output. Options include'
            'CRLF (windows), LF (unix, modern mac), CR (classic mac).'
            'If passed without an argument, the default for your platform'
            'will be used',
        )

    def postprocess_output(self, output: str) -> str:
        # re.split will return (line1, line1-trailing-whitespace, line2, line2-
        # trailing-whitespace, ...) because of the capture group surrounding
        # the regex
        return ''.join(
            (self.line_endings or clump)
            if n % 2
            else (clump.rstrip() if self.clean_whitespace else clump)
            for n, clump in enumerate(re.split(r'((?=[\r\n])\r?\n?)', output))
        )


def make_argument_parser():
    formats = list[Type[DataFormat]]()
    features = list[Type[HokoraFeature]]()
    for feature_class in HokoraFeature.find_all():
        if issubclass(feature_class, DataFormat):
            formats.append(feature_class)
        elif (
            getattr(feature_class, '__doc__', '')
            and feature_class.__module__ != __name__
        ):
            features.append(feature_class)

    with StringIO() as sio:
        sio.write(EPILOG.replace('\n', '\n ', 1))
        if features:
            sio.write('\n \nENABLED FEATURES\n\n')
            for f in features:
                name = f.__name__
                sio.write(f'  {name}{getattr(f, "__doc__", "") or ""}\n')
        sio.write('\n \nAVAILABLE CONTEXT FORMATS\n\n')
        for f in formats:
            exts = ', '.join(f'*.{x}' for x in f.extensions)
            with StringIO('%74s' % (exts,)) as name_builder:
                if filter_name := f.filter_name():
                    name_builder.seek(20)
                    name_builder.write('{{ ... | %s }}' % (filter_name,))
                name_builder.seek(0)
                name_builder.write(f.name)
                name = name_builder.getvalue()
            sio.write(f'  {name}{getattr(f, "__doc__", "") or ""}\n')
        main = argparse.ArgumentParser(
            prog='hokora',
            description='Hokora: Standalone Jinja2 template renderer',
            epilog=sio.getvalue(),
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    main.add_argument('template', nargs='?', help='path to template to render')
    for feature_class in HokoraFeature.find_all():
        feature_class.configure_argparse(main)
    return main


class ExplicitPathTemplate(str):
    path: Path


class PathLoader(jinja2.FileSystemLoader):
    def get_source(self, environment, template):
        if isinstance(template, ExplicitPathTemplate):
            with open(template.path) as fd:
                return fd.read(), template, True
        return super().get_source(environment, template)


class HelpfulDefault(HokoraFeature):
    _filters: dict[str, Callable] = {'repr': repr}
    _context: dict[str, Any] = {'hokora': sys.modules[__name__]}

    @classmethod
    def filter(cls, func):
        cls._filters[func.__name__] = func
        return func

    @classmethod
    def function(cls, func):
        cls._context[func.__name__] = func
        return func

    def update_jinja_environment(self, env: jinja2.Environment):
        for k, v in self._filters.items():
            env.filters.setdefault(k, v)

    def update_template_context(self, context: dict):
        context.setdefault('template_path', self.template_path)
        for k, v in self._context.items():
            context.setdefault(k, v)


@HelpfulDefault.filter
def sub(text, pat, replacement, *a, **kw):
    return re.sub(pat, replacement, str(text), *a, **kw)


@HelpfulDefault.filter
def snip(text, start, end=None, index=0, inclusive=None):
    if inclusive is None:
        if isinstance(index, (bool, tuple)):
            inclusive = index
            index = 0
        else:
            inclusive = (isinstance(start, int), False)
    if isinstance(inclusive, bool):
        inclusive = (inclusive, inclusive)
    if isinstance(start, int) or isinstance(end, int) or end is None:
        if index:
            raise ValueError(
                "|snip's index= argument only works with text markers"
            )
    buf = list[str]()
    on = False
    for n, line in enumerate(str(text).split('\n'), start=1):
        if on:
            if (isinstance(end, int) and n >= end) or (
                isinstance(end, str) and re.search(end, line)
            ):
                on = False
                if index:
                    index -= 1
                    buf.clear()
                else:
                    buf.append(line if inclusive[1] else '')
                    return '\n'.join(buf)
        else:
            if (isinstance(start, int) and n == start) or (
                isinstance(start, str) and re.search(start, line)
            ):
                on = True
                if not inclusive[0]:
                    continue
        if on:
            buf.append(line)
    if on and end is None:
        return '\n'.join(buf)
    return ''


@HelpfulDefault.function
def read(path):
    with open(path) as fd:
        return fd.read()


def create_jinja_environment(features: list[HokoraFeature]):
    include_paths = list[Path]()
    for feat in features:
        feat.update_jinja_include_paths(include_paths)

    environment_kw = {
        'loader': PathLoader(include_paths),
    }

    for feat in features:
        feat.update_jinja_environment_init_args(environment_kw)

    environment = jinja2.Environment(**environment_kw)  # type: ignore

    for feat in features:
        feat.update_jinja_environment(environment)

    return environment


def args_to_templates(
    args,
) -> list[tuple[jinja2.Template, list[HokoraFeature], Optional[Path]]]:
    if args.template and args.template != '-':
        template_path = Path(args.template).resolve()
        if not template_path.exists():
            raise FileNotFoundError(args.template)
    else:
        template_path = None

    features = [
        feat.argparse_namespace_to_instance(args, template_path)
        for feat in HokoraFeature.find_all()
    ]

    environment = create_jinja_environment(features)
    template: jinja2.Template
    if template_path is None:
        if sys.stdin.isatty():
            eof = 'Ctrl+Z, Enter' if sys.platform == 'win32' else 'Ctrl+D'
            sys.stderr.write(f'Type your template ({eof} when done)\n')
            sys.stderr.flush()
        template = environment.from_string(sys.stdin.read())
    else:
        ept = ExplicitPathTemplate(template_path)
        ept.path = template_path
        template = environment.get_template(ept)

    return [(template, features, None)]


def main():
    for mod in environ.get(PRELOAD_ENVIRONMENT_VARIABLE, '').split(pathsep):
        if mod:
            dynamic_import(mod)
    args = make_argument_parser().parse_args()
    for template, features, render_dest in args_to_templates(args):
        assert not render_dest, 'TODO: support rendering to file'
        context: dict[str, Any] = {}
        for feat in features:
            feat.update_template_context(context)

        rendered = template.render(context)

        for feat in features:
            rendered = feat.postprocess_output(rendered)

        print(rendered)


if __name__ == '__main__':
    main()
