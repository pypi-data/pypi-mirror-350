# -*- coding: utf-8 -*-

# lefschetz-family
# Copyright (C) 2021  Eric Pichon-Pharabod

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sage.all

from ore_algebra import *

from sage.modules.free_module_element import vector
from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
from sage.matrix.constructor import matrix
from sage.rings.integer_ring import ZZ
from sage.matrix.special import identity_matrix

from sage.functions.other import floor
from sage.functions.other import ceil
from sage.arith.misc import gcd

from sage.symbolic.relation import solve
from sage.symbolic.ring import SR

from .monodromyRepresentation import MonodromyRepresentation


import logging
import time

logger = logging.getLogger(__name__)


class MonodromyRepresentationEllipticSurface(MonodromyRepresentation):

    @property
    def types(self):
        if not hasattr(self, "_types"):
            types = [self.monodromy_class(M) for M in self.monodromy_matrices]
            types = [t + str(n) if t in ["I", "I*"] else t for t, _, n in types]
            self._types = types
        return self._types
    
    def desingularise_matrix(self, M):
        ty, base_change, nu = self.monodromy_class(M)
        decomposition = self.fibre_confluence[ty]
        mats =  [base_change * M * base_change.inverse() for M in decomposition[:-1]]
        mats += [base_change * decomposition[-1] * base_change.inverse()] * nu
        mats = [M.change_ring(ZZ) for M in mats]
        return mats

    @property
    def self_intersection_section(self):
        if not hasattr(self, '_self_intersection_section'):
            chi = ZZ((len(self.extensions_desingularisation)+ZZ(4))/ZZ(12))
            self._self_intersection_section = -chi
        return self._self_intersection_section
    
    @property
    def add(self):
        if not hasattr(self, '_add'):
            self._add = 2
        return self._add

    classes = {
        "I":matrix([[1,1],[0,1]]),
        "II":matrix([[1,1],[-1,0]]),
        "III":matrix([[0,1],[-1,0]]),
        "IV":matrix([[0,1],[-1,-1]]),
        "I*":matrix([[-1,-1],[0,-1]]),
        "II*":matrix([[0,-1],[1,1]]),
        "III*":matrix([[0,-1],[1,0]]),
        "IV*":matrix([[-1,-1],[1,0]]),
    }

    U = matrix([[1,1],[0,1]])
    V = matrix([[1,0],[-1,1]])

    fibre_confluence = {
        "I": [U],
        "II": [U, V],
        "III": [V,U,V],
        "IV": [U,V]*2,
        "I*": [U,V]*3+[U],
        "II*": [U,V]*5,
        "III*": [U,V]*3+[V,U,V],
        "IV*": [U,V]*4
    }

    @classmethod
    def monodromy_class(cls, M):
        M=M.change_ring(ZZ)
        if M.trace()==2:
            if M==identity_matrix(2):
                return "I", identity_matrix(2), 0
            else:
                return "I", cls.normalize_Iv(M)[0], cls.normalize_Iv(M)[1]
        if M.trace()==1:
            if M[0,1]>0:
                return "II", cls.find_conjugation(M, cls.classes["II"])[0], 1
            else:
                return "II*", cls.find_conjugation(M, cls.classes["II*"])[0], 1
        if M.trace()==0:
            try:
                bc = cls.find_conjugation(M, cls.classes["III"])[0]
                return "III", bc, 1
            except:
                bc = cls.find_conjugation(M, cls.classes["III*"])[0]
                return "III*", bc, 1
        if M.trace()==-1:
            try:
                bc = cls.find_conjugation(M, cls.classes["IV"])[0]
                return "IV", bc, 1
            except:
                bc = cls.find_conjugation(M, cls.classes["IV*"])[0]
                return "IV*", bc, 1
        if M.trace()==-2:
            if M==-identity_matrix(2):
                return "I*", identity_matrix(2), 0
            else:
                return "I*", cls.normalize_Ivstar(M)[0], cls.normalize_Ivstar(M)[1]
    

    @classmethod
    def normalize_Iv(cls, M):
        vanishing = (M-1).transpose().image().basis()[0]
        v = gcd(vanishing)
        v = ZZ(gcd(vanishing))
        vanishing = vanishing/v
        vanishing = vanishing.change_ring(ZZ)
        D, U, V = (M-1).smith_form()
        compl = V*vector([1,0])
        if (M-1)*compl != vanishing*v:
            compl = -compl
        assert (M-1)*compl == vanishing*v, "could not find permuting vector"
        bc = matrix([vanishing, compl]).transpose()
        if bc.det()!=1:
            bc = matrix([-vanishing, compl]).transpose()
        assert bc.det()==1, "could not find permuting vector"
        return bc, v
    
    @classmethod
    def normalize_Ivstar(cls, M):
        vanishing = (M+1).transpose().image().basis()[0]
        v = ZZ(gcd(vanishing))
        vanishing = vanishing/v
        vanishing = vanishing.change_ring(ZZ)
        D, U, V = (M+1).smith_form()
        compl = V*vector([1,0])
        if (M+1)*compl != vanishing*v:
            compl = -compl
        assert (M+1)*compl == vanishing*v, "could not find permuting vector"
        bc = matrix([vanishing, compl]).transpose()
        if bc.det()!=1:
            bc = matrix([-vanishing, compl]).transpose()
        assert bc.det()==1, "could not find permuting vector"
        return bc, v
    
    @classmethod
    def find_conjugation(cls, M1, M2):
        R = PolynomialRing(ZZ, ['a','b','c','d'])
        [a,b,c,d] = R.gens()
        bci = matrix([[a,b],[c,d]])
        eqs = (bci*M1 - M2*bci).coefficients() + [a*d-b*c-1]
        I = R.ideal(eqs)
        eq = I.elimination_ideal([a,b]).gens()[0]
        
        x = SR('x')
        discr = eq.coefficient(c)**2 - 4*eq.coefficient(c**2)*eq(c=0)
        possible_ds = range(ceil(solve(discr(d=x)>0,x)[0][0].right_hand_side()), floor(solve(discr(d=x)>0,x)[0][1].right_hand_side())+1)
        Qt = PolynomialRing(ZZ, 't')
        t=Qt.gens()[0]
        
        sols=[]
        for dv in possible_ds:
            possible_cs = eq(d=dv, c=t).roots(multiplicities=False)
            if len(possible_cs)>0:
                for cv in possible_cs:
                    I2 = R.ideal(eqs+[c-cv, d-dv])
                    av = -I2.elimination_ideal([b,c,d]).gens()[0](a=0)
                    bv = -I2.elimination_ideal([a,c,d]).gens()[0](b=0)
                    sols += [matrix([[av,bv],[cv,dv]])]    
        return [(s**-1).change_ring(ZZ) for s in sols]