"""
Transformation pass to bundle updated variables in for loops
into a single variable.
"""

from typing import Optional

from ..analysis.define_use import DefineUse
from .ssa import SSA
from ..analysis.verify import VerifyIR
from ..ir import *
from ..utils import Gensym

class _ForBundlingInstance(DefaultTransformVisitor):
    """Single-use instance of the ForBundling pass."""
    func: FuncDef
    gensym: Gensym

    def __init__(self, func: FuncDef, names: set[NamedId]):
        self.func = func
        self.gensym = Gensym(reserved=names)

    def apply(self) -> FuncDef:
        return self._visit_function(self.func, {})

    #
    #  a_1 = phi(a_0, a_2)
    #  ...
    #  z_1 = phi(z_0, z_2)
    #
    # ==>
    #
    #  t_0 = (a_0, ..., z_0)
    #  t_1 = phi(t_0, t_2)
    #  for <var> in <iterable>:
    #     a_1, ..., z_1 = t_1
    #     <stmts> ...
    #     t_2 = (a_2, ..., z_2)
    #  a_1, ..., z_1 = t_1
    #
    # - violates SSA invariant
    #

    def _visit_for(self, stmt: ForStmt, ctx: None):  
        if len(stmt.phis) <= 1:
            stmt, _ = super()._visit_for(stmt, None)
            return StmtBlock([stmt])
        else:
            # create a new phi variable
            phi_name = self.gensym.fresh('t')
            phi_init = self.gensym.fresh('t')
            phi_update = self.gensym.fresh('t')
            phi_ty = AnyType() # TODO: infer type

            # construct the tuple of phi variables
            phi_vars = [Var(phi.lhs) for phi in stmt.phis]
            init_stmt = SimpleAssign(phi_init, AnyType(), TupleExpr(*phi_vars))

            # recurse on iterable
            iter_expr = self._visit_expr(stmt.iterable, None)

            # deconstruct unified phi variable
            phi_names = [phi.name for phi in stmt.phis]
            deconstruct_stmt = TupleUnpack(TupleBinding(phi_names), AnyType(), Var(phi_name))

            # construct the update tuple of phi variables
            phi_updates = [Var(phi.rhs) for phi in stmt.phis]
            update_stmt = SimpleAssign(phi_update, AnyType(), TupleExpr(*phi_updates))

            # put it all together
            body, _ = self._visit_block(stmt.body, None)
            phis = [PhiNode(phi_name, phi_init, phi_update, phi_ty)]
            for_body = StmtBlock([deconstruct_stmt, *body.stmts, update_stmt])
            for_stmt = ForStmt(stmt.var, stmt.ty, iter_expr, for_body, phis)

            # decompose the unified phi variable (again)
            deconstruct_stmt = TupleUnpack(TupleBinding(phi_names), AnyType(), Var(phi_name))
            return StmtBlock([init_stmt, for_stmt, deconstruct_stmt])

    def _visit_block(self, block: StmtBlock, ctx: None):
        stmts: list[Stmt] = []
        for stmt in block.stmts:
            if isinstance(stmt, ForStmt):
                b = self._visit_for(stmt, None)
                stmts.extend(b.stmts)
            else:
                stmt, _ = self._visit_statement(stmt, None)
                stmts.append(stmt)
        return StmtBlock(stmts), None

class ForBundling:
    """
    Transformation pass to bundle updated variables in for loops.

    This pass rewrites the IR to bundle updated variables in for loops
    into a single variable. This transformation ensures there is only
    one phi node per while loop.
    """

    @staticmethod
    def apply(func: FuncDef, names: Optional[set[NamedId]] = None) -> FuncDef:
        if names is None:
            uses = DefineUse.analyze(func)
            names = set(uses.keys())
        inst = _ForBundlingInstance(func, names)
        func = inst.apply()
        func = SSA.apply(func)
        VerifyIR.check(func)
        return func
