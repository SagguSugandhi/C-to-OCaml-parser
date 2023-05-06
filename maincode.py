from pycparser import c_ast, parse_file

c_to_ocaml_ops = {
    "=": ":=",
    "==": "=",
    "!=": "<>",
    "<": "<",
    ">": ">",
    "<=": "<=",
    ">=": ">=",
    "+": "+",
    "-": "-",
    "*": "*",
    "/": "/",
    "%": "mod",
    "p++": "p++",
    "p--": "p--",
    "+=": "+=",
    "-=": "-=",
    "!": "not",
    "&&": "&&",
    "||": "||",
    "&": "land",
    "|": "lor",
    "^": "lxor",
    "~": "lnot",
    "<<": "lsl",
    ">>": "lsr",
}

io_functions = {
    "printf": "Printf.printf",
    "scanf": "Scanf.scanf",
    "getchar": "input_char",
    "putchar": "print_char",
}


def convert_to_ocaml(ast: c_ast.Node) -> str:
    if isinstance(ast, c_ast.FileAST):
        fstring = "\n".join(convert_to_ocaml(ext) for ext in ast.ext)
        return f"{fstring}\n"

    elif isinstance(ast, c_ast.Decl):
        storage = ast.storage or []
        name = ast.name


        if isinstance(ast.type, c_ast.FuncDecl):
            if "extern" in storage:
                return f'external {name} : {ast.type.args.params[0].type.type.names[0]} -> {convert_to_ocaml(ast.type)} = "{name}"'
            else:
                if ast.type.args is not None:
                    args = ""
                    for param in ast.type.args.params:
                        if isinstance(param.type, c_ast.PtrDecl):
                            args += f"({param.name} : {param.type.type.type.names[0]} array)"
                        elif isinstance(param, c_ast.ArrayDecl):
                            args += f"({param.name} : {param.type.type.type.names[0]} array)"
                        else:
                            args += f"({param.name} : {param.type.type.names[0]} ref)"
                    return f"let rec {name} {args} ="
                else:
                    return f"let rec {name} () ="
        else:
            if ast.init is not None:
                if isinstance(ast.init, c_ast.Constant):
                    init = f"let {name} = ref ({ast.init.value}) in"
                elif isinstance(ast.init, c_ast.ID):
                    init = f"let {name} = ref !{ast.init.name} in"
                else:
                    init = f"let {name} = ref ({convert_to_ocaml(ast.init)}) in" 
            else:
                init = f"let {name} = ref 0 in"  
            return init

    elif isinstance(ast, c_ast.Typename):
        quals = ast.quals
        align = ast.align
        c_type = convert_to_ocaml(ast.type) if ast.type is not None else ""
        return c_type

    elif isinstance(ast, c_ast.FuncDef):
        storage = ast.decl.storage or []
        if "extern" in storage:
            return f'external {ast.decl.name} : {convert_to_ocaml(ast.decl.type)} = "{ast.decl.name}"'
        else:
            return f"{convert_to_ocaml(ast.decl)}\n{convert_to_ocaml(ast.body)};;"

    elif isinstance(ast, c_ast.Typedef):
        name = ast.name
        quals = ast.quals
        storage = ast.storage
        c_type = convert_to_ocaml(ast.type) if ast.type is not None else ""
        return f"type {name} = {c_type}"

    elif isinstance(ast, c_ast.IdentifierType):
        return " ".join(ast.names)

    elif isinstance(ast, c_ast.TypeDecl):
        return f"{convert_to_ocaml(ast.type)}"

    elif isinstance(ast, c_ast.Assignment):
        if isinstance(ast.lvalue, c_ast.ArrayRef):
            if isinstance(ast.rvalue, c_ast.ID):
                return f"{convert_to_ocaml(ast.lvalue)} <- !{convert_to_ocaml(ast.rvalue)};"
            return f"{convert_to_ocaml(ast.lvalue)} <- {convert_to_ocaml(ast.rvalue)};"
        elif isinstance(ast.rvalue, c_ast.ID):
            if ast.op == "+=":
                return f"{convert_to_ocaml(ast.lvalue)} := !{convert_to_ocaml(ast.lvalue)} + {convert_to_ocaml(ast.rvalue)};"
            elif ast.op == "-=":
                return f"{convert_to_ocaml(ast.lvalue)} := !{convert_to_ocaml(ast.lvalue)} - {convert_to_ocaml(ast.rvalue)};"
            return f"{convert_to_ocaml(ast.lvalue)} {c_to_ocaml_ops[ast.op]} !{convert_to_ocaml(ast.rvalue)};"
        elif isinstance(ast.rvalue, c_ast.Constant):
            if ast.op == "+=":
                return f"{convert_to_ocaml(ast.lvalue)} := !{convert_to_ocaml(ast.lvalue)} + {convert_to_ocaml(ast.rvalue)};"
            elif ast.op == "-=":
                return f"{convert_to_ocaml(ast.lvalue)} := !{convert_to_ocaml(ast.lvalue)} - {convert_to_ocaml(ast.rvalue)};"
            return f"{convert_to_ocaml(ast.lvalue)} {c_to_ocaml_ops[ast.op]} {convert_to_ocaml(ast.rvalue)};"
        elif isinstance(ast.rvalue, c_ast.BinaryOp):
            if ast.op == "+=":
                return f"{convert_to_ocaml(ast.lvalue)} := !{convert_to_ocaml(ast.lvalue)} + {convert_to_ocaml(ast.rvalue)};"
            elif ast.op == "-=":
                return f"{convert_to_ocaml(ast.lvalue)} := !{convert_to_ocaml(ast.lvalue)} - {convert_to_ocaml(ast.rvalue)};"
            return f"{convert_to_ocaml(ast.lvalue)} {c_to_ocaml_ops[ast.op]} {convert_to_ocaml(ast.rvalue)};"
        elif isinstance(ast.lvalue, c_ast.UnaryOp):
            if isinstance(ast.lvalue.expr, c_ast.ID):
                if ast.lvalue.op == "*":
                    if ast.op == "+=":
                        return f"{convert_to_ocaml(ast.lvalue)} := !{convert_to_ocaml(ast.lvalue)} + {convert_to_ocaml(ast.rvalue)};"
                    elif ast.op == "-=":
                        return f"{convert_to_ocaml(ast.lvalue)} := !{convert_to_ocaml(ast.lvalue)} - {convert_to_ocaml(ast.rvalue)};"
                    return f"{convert_to_ocaml(ast.lvalue)} {c_to_ocaml_ops[ast.op]} {convert_to_ocaml(ast.rvalue)};"
        return f"{convert_to_ocaml(ast.lvalue)} {c_to_ocaml_ops[ast.op]} {convert_to_ocaml(ast.rvalue)};"

    elif isinstance(ast, c_ast.Compound):
        statements = ""
        for statement in ast.block_items:
            if isinstance(statement, c_ast.Assignment):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.UnaryOp):
                statements += f"{convert_to_ocaml(statement)};\n"
            elif isinstance(statement, c_ast.FuncCall):
                statements += f"{convert_to_ocaml(statement)};\n"
            elif isinstance(statement, c_ast.If):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.For):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.Decl):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.Return):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.Compound):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.BinaryOp):
                statements += f"{convert_to_ocaml(statement)};\n"
            elif isinstance(statement, c_ast.TernaryOp):
                statements += f"{convert_to_ocaml(statement)};\n"
            elif isinstance(statement, c_ast.ArrayRef):
                statements += f"{convert_to_ocaml(statement)};\n"
            elif isinstance(statement, c_ast.ID):
                statements += f"{convert_to_ocaml(statement)};\n"
            elif isinstance(statement, c_ast.Constant):
                statements += f"{convert_to_ocaml(statement)};\n"
            elif isinstance(statement, c_ast.ExprList):
                statements += f"{convert_to_ocaml(statement)};\n"
            elif isinstance(statement, c_ast.FuncDecl):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.DeclList):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.PtrDecl):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.TypeDecl):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.IdentifierType):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.Typedef):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.Struct):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.Union):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.Enum):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.FuncDef):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.ParamList):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.EllipsisParam):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.ArrayDecl):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.StructRef):
                statements += f"{convert_to_ocaml(statement)};\n"
            elif isinstance(statement, c_ast.Typename):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.Break):
                statements += f"{convert_to_ocaml(statement)};\n"
            elif isinstance(statement, c_ast.Continue):
                statements += f"{convert_to_ocaml(statement)};\n"
            elif isinstance(statement, c_ast.Switch):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.Case):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.Default):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.DoWhile):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.While):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.Goto):
                statements += f"{convert_to_ocaml(statement)};\n"
            elif isinstance(statement, c_ast.Label):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.EmptyStatement):
                statements += f"{convert_to_ocaml(statement)}\n"
            elif isinstance(statement, c_ast.Cast):
                statements += f"{convert_to_ocaml(statement)}\n"
        return f"{statements}"

    elif isinstance(ast, c_ast.For):
        if ast.init is not None:
            if isinstance(ast.init, c_ast.DeclList):
                init_name = ast.init.decls[0].type.declname
                init_val = ast.init.decls[0].init.value
            else:
                init_name = ast.init.lvalue.name
                init_val = ast.init.rvalue.value
            cond = convert_to_ocaml(ast.cond.right)
        next = convert_to_ocaml(ast.next.expr)
        statements = ""
        for stmt in ast.stmt.block_items:
            if isinstance(stmt, c_ast.Assignment):
                statements += f"{convert_to_ocaml(stmt)}\n"
            elif isinstance(stmt, c_ast.UnaryOp):
                statements += f"{convert_to_ocaml(stmt)};\n"
            elif isinstance(stmt, c_ast.BinaryOp):
                statements += f"{convert_to_ocaml(stmt)};\n"
            elif isinstance(stmt, c_ast.FuncCall):
                statements += f"{convert_to_ocaml(stmt)};\n"
            elif isinstance(stmt, c_ast.ArrayRef):
                statements += f"{convert_to_ocaml(stmt)};\n"
            elif isinstance(stmt, c_ast.If):
                statements += f"{convert_to_ocaml(stmt)}\n"
            else:
                statements += f"{convert_to_ocaml(stmt)};\n"
        cond_op = ast.cond.op
        if cond_op == "<":
            cond = int(cond) - 1
        elif cond_op == ">":
            cond = int(cond) + 1
        if cond_op == "!=":
            if ast.next.op == "++":
                if isinstance(ast.cond.right, c_ast.ID):
                    return f"while !{init_name} <> !{ast.cond.right.name} do\n{statements}{init_name} := !{init_name} + 1;\n\ndone;"
                return f"while !{init_name} <> {cond} do\n{statements}{init_name} := !{init_name} + 1;\n\ndone;"
            elif ast.next.op == "--":
                if isinstance(ast.cond.right, c_ast.ID):
                    return f"while !{init_name} <> !{ast.cond.right.name} do\n{statements}{init_name} := !{init_name} - 1;\n\ndone;"
                return f"while !{init_name} <> {cond} do\n{statements}{init_name} := !{init_name} - 1;\ndone;"
        return f"for {init_name} = {init_val} to {cond} do\n{statements}done;"

    elif isinstance(ast, c_ast.BinaryOp):
        if isinstance(ast.left, c_ast.ID):
            if isinstance(ast.right, c_ast.ID):
                return f"(!{convert_to_ocaml(ast.left)} {c_to_ocaml_ops[ast.op]} !{convert_to_ocaml(ast.right)})"
            return f"(!{convert_to_ocaml(ast.left)} {c_to_ocaml_ops[ast.op]} {convert_to_ocaml(ast.right)})"
        elif isinstance(ast.right, c_ast.ID):
            if isinstance(ast.left, c_ast.ID):
                return f"(!{convert_to_ocaml(ast.left)} {c_to_ocaml_ops[ast.op]} !{convert_to_ocaml(ast.right)})"
            return f"({convert_to_ocaml(ast.left)} {c_to_ocaml_ops[ast.op]} !{convert_to_ocaml(ast.right)})"
        return f"({convert_to_ocaml(ast.left)} {c_to_ocaml_ops[ast.op]} {convert_to_ocaml(ast.right)})"

    elif isinstance(ast, c_ast.UnaryOp):
        op = c_to_ocaml_ops[ast.op]
        expr = convert_to_ocaml(ast.expr)
        if op == "p++" or op == "+=":
            return f"{expr} := !{expr} + 1"
        elif op == "p--" or op == "-=":
            return f"{expr} := !{expr} - 1"
        if op == "*":
            # Treat as array
            return f"Array.get {expr}"
        return f"{op}{expr}"

    elif isinstance(ast, c_ast.If): 
        condition = convert_to_ocaml(ast.cond)
        iftrue = convert_to_ocaml(ast.iftrue) if ast.iftrue is not None else ""
        if ast.iffalse is None:
            return f"if {condition} then\nbegin\n{iftrue}\nend;\n"
        iffalse = convert_to_ocaml(ast.iffalse)
        return f"if {condition} then\nbegin\n{iftrue}end\nelse\nbegin\n{iffalse}\nend;\n"

    elif isinstance(ast, c_ast.ID):
        return f"{ast.name}"

    elif isinstance(ast, c_ast.Constant):
        return ast.value

    elif isinstance(ast, c_ast.FuncCall):
        name = convert_to_ocaml(ast.name)
        if name in io_functions:
            name = io_functions[name]
        if ast.args is not None:
            args = ast.args
            if name == "Printf.printf":
                format_string = args[0]
                format_string = format_string.replace("i", "d").replace("f", "f")
                args = f'"%{format_string}" {" ".join(args)}'
            else:
                args_state = ""
                for arg in args:
                    if isinstance(arg, c_ast.Constant):
                        args_state += f"(ref {arg.value}) "
                    if isinstance(arg, c_ast.ID):
                        args_state += f"(ref !{arg.name}) "
                    if isinstance(arg, c_ast.UnaryOp):
                        args_state += f"(ref {convert_to_ocaml(arg)}) "
                    if isinstance(arg, c_ast.BinaryOp):
                        args_state += f"(ref {convert_to_ocaml(arg)}) "
        else:
            args_state = ""
        return f"{name} {args_state}"

    elif isinstance(ast, c_ast.FuncDecl):
        if ast.args is not None:
            args = " ".join(convert_to_ocaml(param) for param in ast.args.params)
        else:
            args = ""
        return f"{args}"

    elif isinstance(ast, c_ast.ParamList):
        return ", ".join(convert_to_ocaml(param) for param in ast.params)

    elif isinstance(ast, c_ast.Return):
        if isinstance(ast.expr, c_ast.Constant):
            return f"\n{convert_to_ocaml(ast.expr)}"
        elif isinstance(ast.expr, c_ast.ID):
            return f"\n!{convert_to_ocaml(ast.expr)}"
        elif isinstance(ast.expr, c_ast.BinaryOp):
            return f"\n{convert_to_ocaml(ast.expr)}" 

    elif isinstance(ast, c_ast.ArrayDecl):
        dim = convert_to_ocaml(ast.dim) if ast.dim is not None else ""
        c_type = convert_to_ocaml(ast.type) if ast.type is not None else ""
        return f"{c_type} array (* {dim} *)"

    elif isinstance(ast, c_ast.ArrayRef):
        name = (
            convert_to_ocaml(ast.name) if ast.name is not None else ""
        )  # Make sure this is correct (name vs. name.name) or convert_to_ocaml
        subscript = convert_to_ocaml(ast.subscript) if ast.subscript is not None else ""
        if isinstance(ast.subscript, c_ast.Constant):
            subscript = int(subscript) - 1
            return f"{name}.({subscript})"
        elif isinstance(ast.subscript, c_ast.ID):
            return f"{name}.(!{subscript})"
        else:
            return f"{name}.({subscript})"

    elif isinstance(ast, c_ast.Alignas):
        alignment = convert_to_ocaml(ast.alignment) if ast.alignment is not None else ""
        return alignment

    elif isinstance(ast, c_ast.Break):
        return "break"

    elif isinstance(ast, c_ast.Case):
        expr = convert_to_ocaml(ast.expr) if ast.expr is not None else ""
        stmts = convert_to_ocaml(ast.stmts) if ast.stmts is not None else ""
        return f"match {expr} with {stmts}"

    elif isinstance(ast, c_ast.Cast):
        to_type = convert_to_ocaml(ast.to_type) if ast.to_type is not None else ""
        expr = convert_to_ocaml(ast.expr) if ast.expr is not None else ""
        return f"({to_type}) {expr}"

    elif isinstance(ast, c_ast.CompoundLiteral):
        c_type = convert_to_ocaml(ast.type) if ast.type is not None else ""
        init = convert_to_ocaml(ast.init) if ast.init is not None else ""
        return f"({c_type}) {init}"

    elif isinstance(ast, c_ast.Continue):  # Again empty
        return "continue"

    elif isinstance(ast, c_ast.DeclList):
        decls = ast.decls
        decl_list = ""
        for decl in decls:
            # decls is a list of Decl objects
            decl_list += f"{convert_to_ocaml(decl)}; \n"
        return decl_list

    elif isinstance(ast, c_ast.Default):
        stmts = convert_to_ocaml(ast.stmts) if ast.stmts is not None else ""
        return f"| _ -> {stmts}"

    elif isinstance(ast, c_ast.DoWhile):
        cond = convert_to_ocaml(ast.cond) if ast.cond is not None else ""
        statements = ""
        for stmt in ast.stmt.block_items:
            if isinstance(stmt, c_ast.Assignment):
                statements += f"{convert_to_ocaml(stmt)}\n"
            elif isinstance(stmt, c_ast.UnaryOp):
                statements += f"{convert_to_ocaml(stmt)};\n"
            elif isinstance(stmt, c_ast.BinaryOp):
                statements += f"{convert_to_ocaml(stmt)};\n"
            elif isinstance(stmt, c_ast.FuncCall):
                statements += f"{convert_to_ocaml(stmt)};\n"
            else:
                statements += f"{convert_to_ocaml(stmt)};\n"
        return f"while {cond} do\n{statements}\ndone;"

    elif isinstance(ast, c_ast.EllipsisParam):
        return "(* ... *)"

    elif isinstance(ast, c_ast.EmptyStatement):
        return "(* empty *)"

    elif isinstance(ast, c_ast.Enum):
        name = ast.name
        values = convert_to_ocaml(ast.values) if ast.values is not None else ""
        return f"type {name} = {values}"

    elif isinstance(ast, c_ast.Enumerator):
        name = ast.name
        value = convert_to_ocaml(ast.value) if ast.value is not None else ""
        return f"| {name} = {value}"

    elif isinstance(ast, c_ast.EnumeratorList):
        enumerators = (
            [convert_to_ocaml(en) for en in ast.enumerators]
            if ast.enumerators is not None
            else ""
        )
        return " | ".join(enumerators)

    elif isinstance(ast, c_ast.ExprList):
        return ", ".join(convert_to_ocaml(expr) for expr in ast.exprs)

    elif isinstance(ast, c_ast.Goto):
        name = ast.name
        return f"goto {name}"

    elif isinstance(ast, c_ast.InitList):
        exprs = (
            ", ".join([convert_to_ocaml(expr) for expr in ast.exprs])
            if ast.exprs is not None
            else ""
        )
        return f"[{exprs}]"

    elif isinstance(ast, c_ast.Label):
        name = ast.name
        stmt = convert_to_ocaml(ast.stmt) if ast.stmt is not None else ""
        return f"{name}:\n{stmt}"

    elif isinstance(ast, c_ast.NamedInitializer):
        name = ".".join(map(convert_to_ocaml, ast.name)) if ast.name is not None else ""
        expr = convert_to_ocaml(ast.expr) if ast.expr is not None else ""
        return f"{name} = {expr}"

    elif isinstance(ast, c_ast.PtrDecl):
        quals = ast.quals
        c_type = convert_to_ocaml(ast.type) if ast.type is not None else ""
        return f"{c_type}"

    elif isinstance(ast, c_ast.StaticAssert):
        cond = convert_to_ocaml(ast.cond) if ast.cond is not None else ""
        message = convert_to_ocaml(ast.message) if ast.message is not None else ""
        return f"assert ({cond}); (* {message} *)"

    elif isinstance(ast, c_ast.Struct):
        return f"{{ {', '.join(convert_to_ocaml(field) for field in ast.decls)} }}"

    elif isinstance(ast, c_ast.StructRef):
        name = convert_to_ocaml(ast.name) if ast.name is not None else ""
        field = convert_to_ocaml(ast.field) if ast.field is not None else ""
        return f"{name}.{field}"

    elif isinstance(ast, c_ast.TernaryOp):
        iftrue = convert_to_ocaml(ast.iftrue) if ast.iftrue is not None else ""
        iffalse = convert_to_ocaml(ast.iffalse) if ast.iffalse is not None else ""
        cond = convert_to_ocaml(ast.cond) if ast.cond is not None else ""
        return f"(if {cond} then {iftrue} else {iffalse})"

    elif isinstance(ast, c_ast.Typedef):
        name = ast.name
        quals = ast.quals
        storage = ast.storage
        c_type = convert_to_ocaml(ast.type) if ast.type is not None else ""
        return f"type {name} = {c_type}"

    elif isinstance(ast, c_ast.Union):
        name = ast.name
        decls = convert_to_ocaml(ast.decls) if ast.decls is not None else ""
        return f"type {name} = [ {decls} ]"

    elif isinstance(ast, c_ast.Pragma):
        string = ast.string
        return f"(* #pragma {string} *)"

    elif isinstance(ast, c_ast.While):
        cond = convert_to_ocaml(ast.cond)
        statements = ""
        for stmt in ast.stmt.block_items:
            if isinstance(stmt, c_ast.Assignment):
                statements += f"{convert_to_ocaml(stmt)}\n"
            elif isinstance(stmt, c_ast.UnaryOp):
                statements += f"{convert_to_ocaml(stmt)};\n"
            elif isinstance(stmt, c_ast.BinaryOp):
                statements += f"{convert_to_ocaml(stmt)};\n"
            elif isinstance(stmt, c_ast.FuncCall):
                statements += f"{convert_to_ocaml(stmt)};\n"
            else:
                statements += f"{convert_to_ocaml(stmt)}\n"
        return f"while {cond} do\nbegin\n{statements}end\ndone;"

    else:
        raise ValueError(f"Unsupported AST node type: {type(ast)}")


if __name__ == "__main__":
    ast = parse_file("sample_c_code/test.c")
    print("This is C's AST:/n")
    print(ast)
    print("\n")
    #print(ast.show())

    ocaml_code = convert_to_ocaml(ast)
    print("This is OCaml code:\n")
    print(ocaml_code)
