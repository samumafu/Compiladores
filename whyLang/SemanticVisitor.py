from WhileLangVisitor import WhileLangVisitor

class SemanticVisitor(WhileLangVisitor):

    def __init__(self):
        self.scopes = [{}]
        self.loop_depth = 0

    # ===== UTILIDADES =====
    def enterScope(self):
        self.scopes.append({})

    def exitScope(self):
        self.scopes.pop()

    def declare(self, name, type_):
        if name in self.scopes[-1]:
            print(f"Error: Variable '{name}' redeclarada en el mismo ámbito.")
            return False
        self.scopes[-1][name] = type_
        return True

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    # ===== PROGRAMA =====
    def visitProgram(self, ctx):
        for stmt in ctx.statement():
            self.visit(stmt)

    # ===== DECLARACIÓN =====
    def visitDeclaration(self, ctx):
        var_name = ctx.ID().getText()
        var_type = ctx.getChild(0).getText()

        expr_type = self.visit(ctx.expr())

        if expr_type == 'error_type':
            return 'error_type'

        if var_type != expr_type:
            print(f"Error: Tipos incompatibles en asignación ({var_type} vs {expr_type})")
            return 'error_type'

        self.declare(var_name, var_type)
        return var_type

    # ===== ASIGNACIÓN =====
    def visitAssignment(self, ctx):
        var_name = ctx.ID().getText()

        var_type = self.lookup(var_name)
        if var_type is None:
            print(f"Error: Variable '{var_name}' no declarada.")
            return 'error_type'

        expr_type = self.visit(ctx.expr())

        if var_type != expr_type:
            print(f"Error: Tipos incompatibles en asignación ({var_type} vs {expr_type})")
            return 'error_type'

        return var_type

    # ===== IF =====
    def visitIfStatement(self, ctx):
        cond_type = self.visit(ctx.condition())

        if cond_type != 'int':
            print("Error: La condición del if debe ser de tipo int.")

        all_statements = ctx.statement()

        # bloque IF
        self.enterScope()
        for stmt in all_statements[:len(all_statements)//2] if ctx.ELSE() else all_statements:
            self.visit(stmt)
        self.exitScope()

        # bloque ELSE
        if ctx.ELSE():
            self.enterScope()
            for stmt in all_statements[len(all_statements)//2:]:
                self.visit(stmt)
            self.exitScope()

    # ===== WHILE =====
    def visitWhileStatement(self, ctx):
        cond_type = self.visit(ctx.condition())

        if cond_type != 'int':
            print("Error: La condición del while debe ser de tipo int.")

        self.loop_depth += 1

        self.enterScope()
        for stmt in ctx.statement():
            self.visit(stmt)
        self.exitScope()

        self.loop_depth -= 1

    # ===== BREAK =====
    def visitBreakStatement(self, ctx):
        if self.loop_depth == 0:
            print("Error: 'break' fuera de un while.")

    # ===== CONTINUE =====
    def visitContinueStatement(self, ctx):
        if self.loop_depth == 0:
            print("Error: 'continue' fuera de un while.")

    # ===== CONDICIONES =====
    def visitExprCondition(self, ctx):
        return self.visit(ctx.expr())

    def visitComparisonCondition(self, ctx):
        return self.visit(ctx)

    # ===== EXPRESIONES =====
    def visitIdExpr(self, ctx):
        var_name = ctx.ID().getText()
        var_type = self.lookup(var_name)

        if var_type is None:
            print(f"Error: Variable '{var_name}' no declarada.")
            return 'error_type'

        return var_type

    def visitNumberExpr(self, ctx):
        return 'int'

    def visitStringExpr(self, ctx):
        return 'string'

    def visitParenExpr(self, ctx):
        return self.visit(ctx.expr())

    # ===== ARITMÉTICA =====
    def visitArithmeticExpr(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()

        if left == 'error_type' or right == 'error_type':
            return 'error_type'

        # string + string
        if op == '+' and left == 'string' and right == 'string':
            return 'string'

        # solo enteros
        if left != 'int' or right != 'int':
            print("Error: Operaciones aritméticas solo permitidas con enteros.")
            return 'error_type'

        return 'int'

    # ===== COMPARACIONES =====
    def visitComparisonExpr(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))

        if left == 'error_type' or right == 'error_type':
            return 'error_type'

        if left != right:
            print(f"Error: Comparación entre tipos incompatibles ({left} vs {right}).")
            return 'error_type'

        if left != 'int':
            print(f"Error: Comparaciones solo permitidas entre enteros, no {left}.")
            return 'error_type'

        return 'int'