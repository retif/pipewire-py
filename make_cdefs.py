import io

import pcpp
import pkgconfig
import pycparser.c_ast
# NOTE: need pycparserext b/c of non-standard code (e.g. statement expressions).
import pycparserext.ext_c_parser
import pycparserext.ext_c_generator



class Preprocessor(pcpp.Preprocessor):
    def __init__(self, *args, **kwargs):
        self.exclude_files = kwargs.pop("exclude_files")
        self.include_macros_integers = kwargs.pop("include_macros_integers")
        self.include_macros_strings = kwargs.pop("include_macros_strings")
        self.macros_integers = set()
        self.macros_strings = set()
        super().__init__(*args, **kwargs)
        self.line_directive = None
    def define(self, tokens):
        if isinstance(tokens, str):
            tokens = self.tokenize(tokens)
        if len(tokens) > 1:
            if tokens[1].type in self.t_WS:
                if all(token.type in ("CPP_INTEGER", "CPP_WS", "CPP_LINECONT", "CPP_PLUS", "CPP_MINUS", "CPP_STAR", "CPP_FSLASH", "CPP_PERCENT", "CPP_BAR", "CPP_AMPERSAND", "CPP_TILDE", "CPP_HAT", "CPP_LPAREN", "CPP_RPAREN", "CPP_LSHIFT", "CPP_RSHIFT") for token in tokens[2:]) or tokens[0].value in self.include_macros_integers:
                    self.macros_integers.add(tokens[0].value)
                elif all(token.type in ("CPP_ID", "CPP_STRING", "CPP_WS", "CPP_LINECONT") for token in tokens[2:]) and any(token.type ==  "CPP_STRING" for token in tokens[2:]) or tokens[0].value in self.include_macros_strings:
                    self.macros_strings.add(tokens[0].value)
                else:
                    print("Not a simple macro:", "".join(token.value for token in tokens))
            else:
                print("Macro with arguments:", "".join(token.value for token in tokens))
        super().define(tokens)
    def include(self, tokens):
        if tokens and tokens[0].value == "<" and tokens[1].value not in ("pipewire", "spa"):
            return
        elif tokens and tokens[1].value and "".join(token.value for token in tokens[1:-1]) in self.exclude_files:
            return
        else:
            yield from super().include(tokens)


class Parser(pycparserext.ext_c_parser.GnuCParser):
    initial_type_symbols = pycparserext.ext_c_parser.GnuCParser.initial_type_symbols | {
        "bool", "va_list", "FILE", "off_t",
        "int8_t", "uint8_t", "int16_t", "uint16_t", "int32_t", "uint32_t", "int64_t", "uint64_t",
        "intptr_t", "uintptr_t", "ptrdiff_t", "size_t", "ssize_t",
    }


def has_va_list_arg(n):
    return isinstance(n, pycparserext.ext_c_parser.FuncDeclExt) and any(hasattr(arg, "type") and hasattr(arg.type, "type") and hasattr(arg.type.type, "names") and "va_list" in arg.type.type.names for arg in n.args)


class Generator(pycparserext.ext_c_generator.GnuCGenerator):
    def __init__(self, *args, **kwargs):
        self.exclude_funcs = kwargs.pop("exclude_funcs")
        super().__init__(*args, **kwargs)
    def visit_Enumerator(self, n):
        if n.name.startswith("_"):
            return ""
        return f"{self._make_indent()}{n.name},\n"
    def visit_Decl(self, n):
        if n.name in self.exclude_funcs:
            return ""
        # XXX: support va_list's??
        elif isinstance(n.type, pycparser.c_ast.PtrDecl):
            if has_va_list_arg(n.type.type):
                # Assumed to be in a struct.
                return "..."
        elif has_va_list_arg(n.type):
            return ""
        elif isinstance(n.type, (pycparser.c_ast.ArrayDecl, pycparserext.ext_c_parser.ArrayDeclExt)) and n.init is not None:
            n.init = None
            # XXX: a bit hacky, EllipsisParam is probably not really the correct node.
            n.type.dim = pycparser.c_ast.EllipsisParam()
        return super().visit_Decl(n)
    def visit_FuncDef(self, n):
        return self.visit(n.decl) + ";\n"


def make_cdefs(src, lib, exclude_files=[], include_macros_integers=[], include_macros_strings=[], exclude_macros=[], exclude_funcs=[]):
    p = Preprocessor(exclude_files=exclude_files, include_macros_integers=include_macros_integers, include_macros_strings=include_macros_strings)

    d = pkgconfig.parse(lib)
    for include_dir in d["include_dirs"]:
        p.add_path(include_dir)
    for k, v in d["define_macros"]:
        p.define(k + ("=" + v if v else ""))

    p.define("__attribute__(x)")
    p.define("__extension__")
    for i in "diuoxX":
        for n in (8, 16, 32, 64):
            p.define(f"PRI{i}{n}")
            p.define(f"SCN{i}{n}")
    p.define("va_arg(...) (0)")
    p.parse(src)

    s = io.StringIO()
    p.write(s)

    ast = Parser().parse(s.getvalue())

    g = Generator(exclude_funcs=exclude_funcs)

    s = ["typedef int off_t;\n", g.visit(ast)]

    cbs = []

    available_funcs = set()

    for n in ast.ext:
        if isinstance(n, pycparser.c_ast.FuncDef):
            available_funcs.add(n.decl.name)

    for n in ast.ext:
        if isinstance(n, pycparser.c_ast.Decl) and n.name is None and isinstance(n.type, pycparser.c_ast.Struct):
            # NOTE: to avoid spa_callbacks.
            if n.type.name.count("_") > 1:
                if any(n.type.name.endswith("_" + suffix) for suffix in ("events", "callbacks", "hooks", "methods")):
                    type_name, group_name = n.type.name[:-1].rsplit("_", 1)
                    if not n.type.name.endswith("methods"):
                        s.append('extern "Python" {\n')
                    for decl in n.type.decls:
                        if isinstance(decl.type, pycparser.c_ast.PtrDecl) and not has_va_list_arg(decl.type.type):
                            if isinstance(decl.type.type.type, pycparser.c_ast.PtrDecl):
                                tp = decl.type.type.type.type
                            else:
                                tp = decl.type.type.type
                            if n.type.name.endswith("methods"):
                                tp.declname = f"{type_name}_{tp.declname}"
                                if tp.declname in available_funcs or tp.declname in exclude_funcs:
                                    continue
                            else:
                                s.append("  ")
                                cbs.append((type_name, group_name, tp.declname))
                                tp.declname = f"py_cb_{type_name}_{group_name}_{tp.declname}"
                            s.append(g.visit_FuncDecl(decl.type.type) + ";\n")
                    if not n.type.name.endswith("methods"):
                        s.append("}\n")

    for macro in sorted(p.macros_integers):
        if macro.startswith("PW_") or macro.startswith("SPA_"):
            if macro not in exclude_macros:
                s.append(f"static const int {macro};\n")
    for macro in sorted(p.macros_strings):
        if macro.startswith("PW_") or macro.startswith("SPA_"):
            if macro not in exclude_macros:
                s.append(f"static char * const {macro};\n")

    return ("".join(s), cbs)
