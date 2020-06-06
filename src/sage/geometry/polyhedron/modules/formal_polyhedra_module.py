r"""
Formal modules generated by polyhedra.
"""

from sage.combinat.free_module import CombinatorialFreeModule
from sage.modules.with_basis.subquotient import SubmoduleWithBasis, QuotientModuleWithBasis
from sage.categories.graded_modules_with_basis import GradedModulesWithBasis
from sage.categories.polyhedra_modules import PolyhedraModules

class FormalPolyhedraModule(CombinatorialFreeModule):
    r"""
    Class for formal modules generated by polyhedra.

    It is formal because it is free -- it does not know
    about linear relations of polyhedra.

    INPUT:

     - ``base_ring`` - base ring of the module; unrelated to the
       base ring of the polyhedra

     - ``dimension`` - the ambient dimension of the polyhedra

     - ``basis`` - the basis

    EXAMPLES::

        sage: from sage.geometry.polyhedron.modules.formal_polyhedra_module import FormalPolyhedraModule
        sage: def closed_interval(a,b): return Polyhedron(vertices=[[a], [b]])

    A three-dimensional vector space of polyhedra::

        sage: I01 = closed_interval(0, 1); I01.rename("conv([0], [1])")
        sage: I11 = closed_interval(1, 1); I11.rename("{[1]}")
        sage: I12 = closed_interval(1, 2); I12.rename("conv([1], [2])")
        sage: basis = [I01, I11, I12]
        sage: M = FormalPolyhedraModule(QQ, 1, basis=basis); M
        Free module generated by {conv([0], [1]), {[1]}, conv([1], [2])} over Rational Field
        sage: M.get_order()
        [conv([0], [1]), {[1]}, conv([1], [2])]

    A one-dimensional subspace; bases of subspaces just use the indexing
    set `0, \dots, d-1`, where `d` is the dimension::

        sage: M_lower = M.submodule([M(I11)]); M_lower
        Free module generated by {0} over Rational Field
        sage: M_lower.is_submodule(M)
        True
        sage: x = M(I01) - 2*M(I11) + M(I12)
        sage: M_lower.reduce(x)
        [conv([0], [1])] + [conv([1], [2])]
        sage: M_lower.retract.domain() is M
        True
        sage: y = M_lower.retract(M(I11)); y
        B[0]
        sage: M_lower.lift(y)
        [{[1]}]

    Quotient space; bases of quotient space are families indexed by
    elements of the ambient space::

        sage: M_mod_lower = M.quotient_module(M_lower); M_mod_lower
        Free module generated by {conv([0], [1]), conv([1], [2])} over Rational Field
        sage: M_mod_lower.retract(x)
        B[conv([0], [1])] + B[conv([1], [2])]
        sage: M_mod_lower.retract(M(I01) - 2*M(I11) + M(I12)) ==  M_mod_lower.retract(M(I01) + M(I12))
        True

    """

    @staticmethod
    def __classcall__(cls, base_ring, dimension, basis, category=None):
        r"""
        Normalize the arguments for caching.

        TESTS::

            sage: from sage.geometry.polyhedron.modules.formal_polyhedra_module import FormalPolyhedraModule
            sage: FormalPolyhedraModule(QQ, 1, ()) is FormalPolyhedraModule(QQ, 1, [])
            True
        """
        if isinstance(basis, list):
            basis = tuple(basis)
        if category is None:
            category = PolyhedraModules(base_ring) & GradedModulesWithBasis(base_ring)
        return super(FormalPolyhedraModule, cls).__classcall__(cls,
                                                               base_ring=base_ring,
                                                               dimension=dimension,
                                                               basis=basis,
                                                               category=category)

    def __init__(self, base_ring, dimension, basis, category):
        """
        Construct a free module generated by the polyhedra in ``basis``.
        """
        super(FormalPolyhedraModule, self).__init__(base_ring, basis, prefix="", category=category)
