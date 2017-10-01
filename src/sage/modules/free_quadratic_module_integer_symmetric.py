#*****************************************************************************
#       Copyright (C) 2017 Simon Brandhorst <sbrandhorst@web.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.rings.integer_ring import ZZ
from sage.rings.rational_field import QQ
from sage.modules.free_quadratic_module import FreeQuadraticModule_submodule_with_basis_pid, FreeQuadraticModule
from sage.matrix.constructor import matrix
from sage.arith.misc import gcd

###############################################################################
#
# Constructor functions
#
###############################################################################

def IntegralLattice(inner_product_matrix, basis=None, already_echelonized=False, check=True):
    r"""
    Return the integral lattice spanned by ``basis`` in the ambient space.

    A lattice is a finitely generated free abelian group `L \cong \Z^r` equipped
    with a non-degenerate, symmetric bilinear form `L \times L \colon \rightarrow \Z`.
    Here, lattices have an ambient quadratic space `\Q^n` and a distinguished basis.

    INPUT:
    
    - ``inner_product_matrix`` -- a symmetric matrix over the rationals

    - ``basis`` -- a list of elements of ambient or a matrix
    
    TODO:
    
    - Make sure inner_product_matrix is a matrix

    EXAMPLES::

        sage: from sage.modules.free_quadratic_module_integer_symmetric import IntegralLattice
        sage: IntegralLattice(Matrix(ZZ,2,2,[0,1,1,0]))
        Lattice of degree 2 and rank 2 over Integer Ring
        Basis matrix:
        [1 0]
        [0 1]
        Inner product matrix:
        [0 1]
        [1 0]

    We can specify a basis as well::

        sage: IntegralLattice(Matrix(ZZ,2,2,[0,1,1,0]),basis=[vector([1,1])])
        Lattice of degree 2 and rank 1 over Integer Ring
        Basis matrix:
        [1 1]
        Inner product matrix:
        [0 1]
        [1 0]
    """
    if basis is None:
        basis = matrix.identity(QQ, inner_product_matrix.ncols())
    if inner_product_matrix != inner_product_matrix.transpose():
        raise ValueError("Argument inner_product_matrix must be symmetric\n%s" % inner_product_matrix)

    A = FreeQuadraticModule(ZZ, inner_product_matrix.ncols(),
                            inner_product_matrix=inner_product_matrix)
    return FreeQuadraticModule_integer_symmetric(ambient=A, basis=basis,
                                                 inner_product_matrix=inner_product_matrix,
                                                 already_echelonized=False)

###############################################################################
#
# Base class for Lattices
#
###############################################################################

class FreeQuadraticModule_integer_symmetric(FreeQuadraticModule_submodule_with_basis_pid):
    r"""
    This class represents non-degenerate, integral, symmetric free quadratic `\Z`-modules.

    EXAMPLES::

        sage: from sage.modules.free_quadratic_module_integer_symmetric import IntegralLattice
        sage: IntegralLattice(Matrix(ZZ,2,2,[0,1,1,0]),basis=[vector([1,1])])
        Lattice of degree 2 and rank 1 over Integer Ring
        Basis matrix:
        [1 1]
        Inner product matrix:
        [0 1]
        [1 0]
    """
    def __init__(self, ambient, basis, inner_product_matrix, check=True, already_echelonized=False):
        r"""
        Create the integral lattice spanned by ``basis`` in the ambient space.
        
        INPUT:
        
        - ``ambient`` --
        
        - ``basis`` --
        
        - ``inner_product_matrix`` -- 

        TESTS::

            sage: from sage.modules.free_quadratic_module_integer_symmetric import IntegralLattice
            sage: L = IntegralLattice(Matrix(ZZ,2,2,[0,1,1,0]))
            sage: TestSuite(L).run()
        """
        FreeQuadraticModule_submodule_with_basis_pid.__init__(self, ambient, basis, inner_product_matrix, check=True, already_echelonized=False)
        if self.determinant() == 0:
            raise ValueError("Lattices must be nondegenerate. Use FreeQuadraticModule instead")
        if self.gram_matrix().base_ring() != ZZ:
            if self.gram_matrix().denominator() != 1:
                raise ValueError("Lattices must be integral. Use FreeQuadraticModule instead")

    def _repr_(self):
        r"""
        The print representation of this lattice.

        EXAMPLES::

            sage: from sage.modules.free_quadratic_module_integer_symmetric import IntegralLattice
            sage: A2 = IntegralLattice(matrix(ZZ,2,2,[2,-1,-1,2]))
            sage: A2
            Lattice of degree 2 and rank 2 over Integer Ring
            Basis matrix:
            [1 0]
            [0 1]
            Inner product matrix:
            [ 2 -1]
            [-1  2]
        """
        if self.is_sparse():
            s = "Sparse lattice of degree %s and rank %s over %s\n"%(
                self.degree(), self.rank(), self.base_ring()) + \
                "Basis matrix:\n%s\n" % self.basis_matrix() + \
                "Inner product matrix:\n%s" % self.inner_product_matrix()
        else:
            s = "Lattice of degree %s and rank %s over %s\n"%(
                self.degree(), self.rank(), self.base_ring()) + \
                "Basis matrix:\n%s\n" % self.basis_matrix() + \
                "Inner product matrix:\n%s" % self.inner_product_matrix()
        return s

    def is_even(self):
        r"""
        Returns true if the diagonal entries of the Gram matrix are even.

        EXAMPLES::

            sage: from sage.modules.free_quadratic_module_integer_symmetric import IntegralLattice
            sage: L = IntegralLattice(Matrix(ZZ,2,2,[-1,1,1,2]))
            sage: L.is_even()
            False
            sage: L = IntegralLattice(Matrix(ZZ,2,2,[2,-1,-1,2]))
            sage: L.is_even()
            True
        """
        for d in self.gram_matrix().diagonal():
            if d % 2 != 0:
                return False
        return True

    def dual_lattice(self):
        r"""
        Return the dual lattice as a :class:`FreeQuadraticModule`

        Let `L` be a lattice. Its dual lattice is

        .. MATH::

            L^\vee = \{x \in L \otimes \QQ : \langle x, l \rangle \forall y \in L \}.

        EXAMPLES::

            sage: from sage.modules.free_quadratic_module_integer_symmetric import IntegralLattice
            sage: L = IntegralLattice(Matrix(ZZ,2,2,[2,-1,-1,2]))
            sage: Ldual=L.dual_lattice()
            sage: Ldual
            Free module of degree 2 and rank 2 over Integer Ring
            Echelon basis matrix:
            [1/3 2/3]
            [  0   1]

        Since our lattices are always integral, a lattice is contained in its dual::

            sage: L.is_submodule(Ldual)
            True
        """
        return self.span(self.gram_matrix().inverse()*self.basis_matrix())

    def discriminant_group(self, s=0):
        r"""
        Return the discriminant group `L^\vee / L` of this lattice.

        INPUT:

        - ``s`` -- an integer

        EXAMPLES::

            sage: from sage.modules.free_quadratic_module_integer_symmetric import IntegralLattice
            sage: L = IntegralLattice(Matrix(ZZ,2,2,[2,1,1,-2])*2)
            sage: L.discriminant_group()
            Finitely generated module V/W over Integer Ring with invariants (2, 10)
            sage: L.discriminant_group(2)
            Finitely generated module V/W over Integer Ring with invariants (2, 2)
            sage: L.discriminant_group(5)
            Finitely generated module V/W over Integer Ring with invariants (5)

        TESTS::

            sage: from sage.modules.free_quadratic_module_integer_symmetric import IntegralLattice
            sage: L = IntegralLattice(Matrix(ZZ,2,2,[0,1,1,0]))
            sage: L.discriminant_group()
            Finitely generated module V/W over Integer Ring with invariants ()
        """
        D = self.dual_lattice() / self
        d = D.annihilator().gen()
        a = d.prime_to_m_part(s)
        Dp_gens = [a*g for g in D.gens()]
        return D.submodule(Dp_gens)

    def signature(self):
        r"""
        Return the signature of this lattice, which is defined as
        the difference between the number of positive eigenvalues and
        the number of negative eigenvalues in the Gram matrix.

        EXAMPLES::

            sage: from sage.modules.free_quadratic_module_integer_symmetric import IntegralLattice
            sage: U = IntegralLattice(Matrix(ZZ,2,2,[0,1,1,0]))
            sage: U.signature()
            0
        """
        from sage.quadratic_forms.quadratic_form import QuadraticForm
        return QuadraticForm(QQ, self.gram_matrix()).signature()

    def signature_pair(self):
        r"""
        Returns the signature tuple `(n_+,n_-)` of this lattice.

        Here `n_+` (resp. `n_-`) is the number of positive (resp. negative)
        eigenvalues of the Gram matrix.

        EXAMPLES::

            sage: from sage.modules.free_quadratic_module_integer_symmetric import IntegralLattice
            sage: A2 = IntegralLattice(Matrix(ZZ,2,2,[2,-1,-1,2]))
            sage: A2.signature_pair()
            (2, 0)
        """
        from sage.quadratic_forms.quadratic_form import QuadraticForm
        return QuadraticForm(QQ, self.gram_matrix()).signature_vector()[:2]

    def direct_sum(self, M):
        r"""
        Return the direct sum of this lattice with ``M``.
        
        INPUT: 
        
        - ``M`` -- a module over `\Z`

        EXAMPLES::

            sage: from sage.modules.free_quadratic_module_integer_symmetric import IntegralLattice
            sage: A = IntegralLattice(matrix([1]))
            sage: A.direct_sum(A)
            Lattice of degree 2 and rank 2 over Integer Ring
            Basis matrix:
            [1 0]
            [0 1]
            Inner product matrix:
            [1|0]
            [-+-]
            [0|1]
        """
        IM = matrix.block_diagonal([self.inner_product_matrix(), M.inner_product_matrix()])
        ambient = FreeQuadraticModule(ZZ, self.degree() + M.degree(), inner_product_matrix=IM)
        smzero = matrix.zero(self.rank(), M.degree())
        mszero = matrix.zero(M.rank(), self.degree())
        basis = self.basis_matrix().augment(smzero).stack(mszero.augment(M.basis_matrix()))
        ipm = ambient.inner_product_matrix()
        return FreeQuadraticModule_integer_symmetric(
            ambient=ambient, basis=basis, inner_product_matrix=ipm, already_echelonized=False)

    def is_primitive(self, M):
        r"""
        Return whether ``M`` is a primitive submodule of this lattice.

        A `\Z`-submodule ``M`` of a `\Z`-module `L` is called primitive if
        the quotient ``L/M`` is torsion free.
        
        INPUT:
        
        - ``M`` -- a module 
        
        TODO:
        
        - Check that M is the right type 
        
        - make sure there is the same ambient space
        
        - describe the input M in more detail

        EXAMPLES::

            sage: from sage.modules.free_quadratic_module_integer_symmetric import IntegralLattice
            sage: U = IntegralLattice(Matrix(ZZ,2,2,[0,1,1,0]))
            sage: L1 = U.span([vector([1,1])])
            sage: L2 = U.span([vector([1,-1])])
            sage: U.is_primitive(L1)
            True
            sage: U.is_primitive(L2)
            True
            sage: U.is_primitive(L1+L2)
            False

        We can also compute the index::

            sage: (L1+L2).index_in(U)
            2
        """
        return (gcd((self/M).invariants()) == 0)

    def orthogonal_complement(self, M):
        r"""
        Return the orthogonal complement of ``M`` in this lattice.
        
        INPUT:
        
        - ``M`` --
        
        TODO:
        
        - make sure the input is a free module 
        
        - make sure there is the same ambient space
        
        - describe the input M in more detail

        EXAMPLES::

            sage: from sage.modules.free_quadratic_module_integer_symmetric import IntegralLattice
            sage: L = IntegralLattice(Matrix(ZZ,2,2,[2,1,1,-2]))
            sage: S = L.span([vector([1,1])])
            sage: L.orthogonal_complement(S)
            Lattice of degree 2 and rank 1 over Integer Ring
            Basis matrix:
            [1 3]
            Inner product matrix:
            [ 2  1]
            [ 1 -2]
        """
        K = (self.inner_product_matrix() * M.basis_matrix().transpose()).kernel()
        K.base_extend(QQ)
        return self.sublattice(self.intersection(K).basis())

    def sublattice(self, basis):
        r"""
        Return the sublattice spanned by ``basis``.

        INPUT:

        - ``basis`` --
        
        TODO:
        
        - Check that basis input is of the right type
        
        - describe the input in more detail 

        EXAMPLES::

            sage: from sage.modules.free_quadratic_module_integer_symmetric import IntegralLattice
            sage: U = IntegralLattice(Matrix(ZZ,2,2,[0,1,1,0]))
            sage: S = U.sublattice([vector([1,1])])
            sage: S
            Lattice of degree 2 and rank 1 over Integer Ring
            Basis matrix:
            [1 1]
            Inner product matrix:
            [0 1]
            [1 0]
            sage: U.sublattice([vector([1,-1])/2])
            Traceback (most recent call last):
            ...
            ValueError: Lattices must be integral. Use FreeQuadraticModule instead
            
            sage: S.sublattice([vector([1,-1])])
            Traceback (most recent call last):
            ...
            ValueError: Argument basis (= [(1, -1)]) does not span a submodule of this lattice

        """
        M = FreeQuadraticModule_integer_symmetric(
            ambient=self.ambient_module(), basis=basis,
            inner_product_matrix=self.inner_product_matrix(),
            already_echelonized=False)
        if not M.is_submodule(self):
            raise ValueError("Argument basis (= %s) does not span a submodule of this lattice" % basis)
        return M

    def overlattice(self, gens):
        r"""
        Return the lattice spanned by this lattice and ``gens``.

        INPUT:

        - ``gens`` -- a list of elements of this lattice, or a rational matrix
        
        TODO:
        
        - make sure input ``gens`` is of the right type

        EXAMPLES::

            sage: from sage.modules.free_quadratic_module_integer_symmetric import IntegralLattice
            sage: L = IntegralLattice(Matrix(ZZ,2,2,[2,0,0,2]))
            sage: M = L.overlattice([vector([1,1])/2])
            sage: M.gram_matrix()
            [1 1]
            [1 2]
        """
        basis = (self + self.span(gens)).basis()
        return FreeQuadraticModule_integer_symmetric(
            ambient=self.ambient_module(), basis=basis,
            inner_product_matrix=self.inner_product_matrix(),
            already_echelonized=False)

    def genus(self):
        r"""
        Return the genus of this lattice.

        EXAMPLES::

            sage: from sage.modules.free_quadratic_module_integer_symmetric import IntegralLattice
            sage: L = IntegralLattice(Matrix(ZZ,2,2,[0,1,1,0]))
            sage: L.genus()
            Genus of [0 1]
            [1 0]
        """
        from sage.quadratic_forms.genera.genus import Genus
        return Genus(self.gram_matrix())
