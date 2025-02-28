## @package test
# 
#  @author  Rodrigo Pedroso Mendes
#  @version V1.0
#  @date    24/02/23 01:05:02
#
#  #LICENSE# 
#    
#  Copyright (c) 2023 Rodrigo Pedroso Mendes
#
#  Permission is hereby granted, free of charge, to any  person   obtaining  a 
#  copy of this software and associated  documentation files (the "Software"), 
#  to deal in the Software without restriction, including  without  limitation 
#  the rights to use, copy, modify,  merge,  publish,  distribute, sublicense, 
#  and/or sell copies of the Software, and  to  permit  persons  to  whom  the 
#  Software is furnished to do so, subject to the following conditions:        
#   
#  The above copyright notice and this permission notice shall be included  in 
#  all copies or substantial portions of the Software.                         
#   
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,  EXPRESS OR 
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE  WARRANTIES  OF  MERCHANTABILITY, 
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
#  AUTHORS OR COPYRIGHT HOLDERS BE  LIABLE FOR ANY  CLAIM,  DAMAGES  OR  OTHER 
#  LIABILITY, WHETHER IN AN ACTION OF  CONTRACT, TORT  OR  OTHERWISE,  ARISING 
#  FROM, OUT OF OR IN CONNECTION  WITH  THE  SOFTWARE  OR  THE  USE  OR  OTHER  
#  DEALINGS IN THE SOFTWARE. 
#    
################################################################################
import sys
sys.path.insert(0, "../")
import unittest
from vagen.veriloga import *


class TestVA(unittest.TestCase):

    ############################################################################
    # Real
    ############################################################################
    def testReal(self):
        a = Real(Integer('a'))
        b = Real(Real('b'))
        c = Real(Bool('c'))
        d = Real(1.5)
        
        self.assertEqual(type(a), Real)
        self.assertEqual(type(b), Real)
        self.assertEqual(type(c), Real)
        self.assertEqual(type(d), Real)
        self.assertEqual(str(a), 'a')  
        self.assertEqual(str(b), 'b')         
        self.assertEqual(str(c), 'c ? {:e} : {:e}'.format(1,0))  
        self.assertEqual(str(d), "{:e}".format(1.5))  
        
    def testRealSum(self):
        a = Real('a')
        b = Real('b')
        c = 5.99
        self.assertEqual(a.getValue(), "a")
        self.assertEqual(type(a + b), Real)
        self.assertEqual(type(b + a), Real)
        self.assertEqual(type(b + c), Real)
        self.assertEqual(type(c + a), Real)
        self.assertEqual(str(a + b), '( a )+( b )')
        self.assertEqual(str(b + a), '( b )+( a )')
        self.assertEqual(str(b + c), '( b )+( {:e} )'.format(c))
        self.assertEqual(str(c + a), '( {:e} )+( a )'.format(c))
        
    def testRealSub(self):
        a = Real('a')
        b = Real('b')
        c = 6.91
        self.assertEqual(type(a - b), Real)
        self.assertEqual(type(b - a), Real)
        self.assertEqual(type(b - c), Real)
        self.assertEqual(type(c - a), Real)
        self.assertEqual(str(a - b), '( a )-( b )')
        self.assertEqual(str(b - a), '( b )-( a )')
        self.assertEqual(str(b - c), '( b )-( {:e} )'.format(c))
        self.assertEqual(str(c - a), '( {:e} )-( a )'.format(c))

    def testRealTrueDiv(self):
        a = Real('a')
        b = Real('b')
        c = 6.91
        self.assertEqual(type(a/b), Real)
        self.assertEqual(type(b/a), Real)
        self.assertEqual(type(b/c), Real)
        self.assertEqual(type(c/a), Real)
        self.assertEqual(str(a/b), '( a )/( b )')
        self.assertEqual(str(b/a), '( b )/( a )')
        self.assertEqual(str(b/c), '( b )/( {:e} )'.format(c))
        self.assertEqual(str(c/a), '( {:e} )/( a )'.format(c))
        
    def testRealMul(self):
        a = Real('a')
        b = Real('b')
        c = 6.91
        self.assertEqual(type(a*b), Real)
        self.assertEqual(type(b*a), Real)
        self.assertEqual(type(b*c), Real)
        self.assertEqual(type(c*a), Real)
        self.assertEqual(str(a*b), '( a )*( b )')
        self.assertEqual(str(b*a), '( b )*( a )')
        self.assertEqual(str(b*c), '( b )*( {:e} )'.format(c))
        self.assertEqual(str(c*a), '( {:e} )*( a )'.format(c))
        
    def testRealPow(self):
        a = Real('a')
        b = Real('b')
        c = 6.91
        self.assertEqual(type(a**b), Real)
        self.assertEqual(type(b**a), Real)
        self.assertEqual(type(b**c), Real)
        self.assertEqual(type(c**a), Real)
        self.assertEqual(str(a**b), 'pow(a, b)')
        self.assertEqual(str(b**a), 'pow(b, a)')
        self.assertEqual(str(b**c), 'pow(b, {:e})'.format(c))
        self.assertEqual(str(c**a), 'pow({:e}, a)'.format(c))

    def testRealGt(self):
        a = Real('a')
        b = Real('b')
        c = 6.91
        self.assertEqual(type(a > b), Bool)
        self.assertEqual(type(b > a), Bool)
        self.assertEqual(type(b > c), Bool)
        self.assertEqual(type(c > a), Bool)
        self.assertEqual(str(a > b), '( a )>( b )')
        self.assertEqual(str(b > a), '( b )>( a )')
        self.assertEqual(str(b > c), '( b )>( {:e} )'.format(c))
        self.assertEqual(str(c > a), '( a )<( {:e} )'.format(c))

    def testRealLt(self):
        a = Real('a')
        b = Real('b')
        c = 6.91
        self.assertEqual(type(a < b), Bool)
        self.assertEqual(type(b < a), Bool)
        self.assertEqual(type(b < c), Bool)
        self.assertEqual(type(c < a), Bool)
        self.assertEqual(str(a < b), '( a )<( b )')
        self.assertEqual(str(b < a), '( b )<( a )')
        self.assertEqual(str(b < c), '( b )<( {:e} )'.format(c))
        self.assertEqual(str(c < a), '( a )>( {:e} )'.format(c))
        
    def testRealLe(self):
        a = Real('a')
        b = Real('b')
        c = 6.91
        self.assertEqual(type(a <= b), Bool)
        self.assertEqual(type(b <= a), Bool)
        self.assertEqual(type(b <= c), Bool)
        self.assertEqual(type(c <= a), Bool)
        self.assertEqual(str(a <= b), '( a )<=( b )')
        self.assertEqual(str(b <= a), '( b )<=( a )')
        self.assertEqual(str(b <= c), '( b )<=( {:e} )'.format(c))
        self.assertEqual(str(c <= a), '( a )>=( {:e} )'.format(c))
        
    def testRealGe(self):
        a = Real('a')
        b = Real('b')
        c = 6.91
        self.assertEqual(type(a >= b), Bool)
        self.assertEqual(type(b >= a), Bool)
        self.assertEqual(type(b >= c), Bool)
        self.assertEqual(type(c >= a), Bool)
        self.assertEqual(str(a >= b), '( a )>=( b )')
        self.assertEqual(str(b >= a), '( b )>=( a )')
        self.assertEqual(str(b >= c), '( b )>=( {:e} )'.format(c))
        self.assertEqual(str(c >= a), '( a )<=( {:e} )'.format(c))
        
    def testRealEq(self):
        a = Real('a')
        b = Real('b')
        c = 6.91
        self.assertEqual(type(a == b), Bool)
        self.assertEqual(type(b == a), Bool)
        self.assertEqual(type(b == c), Bool)
        self.assertEqual(type(c == a), Bool)
        self.assertEqual(str(a == b), '( a )==( b )')
        self.assertEqual(str(b == a), '( b )==( a )')
        self.assertEqual(str(b == c), '( b )==( {:e} )'.format(c))
        self.assertEqual(str(c == a), '( a )==( {:e} )'.format(c)) 
           
    def testRealNeq(self):
        a = Real('a')
        b = Real('b')
        c = 6.91
        self.assertEqual(type(a != b), Bool)
        self.assertEqual(type(b != a), Bool)
        self.assertEqual(type(b != c), Bool)
        self.assertEqual(type(c != a), Bool)
        self.assertEqual(str(a != b), '( a )!=( b )')
        self.assertEqual(str(b != a), '( b )!=( a )')
        self.assertEqual(str(b != c), '( b )!=( {:e} )'.format(c))
        self.assertEqual(str(c != a), '( a )!=( {:e} )'.format(c))   
 
    def testRealUnary(self):
        a = Real('a')
        self.assertEqual(type(-a), Real)
        self.assertEqual(type(+a), Real)
        self.assertEqual(type(abs(a)), Real)
        self.assertEqual(str(-a), '-( a )') 
        self.assertEqual(str(+a), '+( a )')  
        self.assertEqual(str(abs(a)), 'abs(a)')             
        
            
    ############################################################################
    # Integer
    ############################################################################  
    def testInteger(self):
        a = Integer(Integer('a'))
        b = Integer(Real('b'))
        c = Integer(Bool('c'))
        d = Integer(1.5)
        
        self.assertEqual(type(a), Integer)
        self.assertEqual(type(b), Integer)
        self.assertEqual(type(c), Integer)
        self.assertEqual(type(d), Integer)
        self.assertEqual(str(a), 'a')  
        self.assertEqual(str(b), '_rtoi(b)')         
        self.assertEqual(str(c), 'c ? 1 : 0')  
        self.assertEqual(str(d), '1')  
                                           
    def testIntegerSum(self):
        a = Integer('a')
        b = Integer('b')
        c = 5
        self.assertEqual(a.getValue(), "a")
        self.assertEqual(type(a + b), Integer)
        self.assertEqual(type(b + a), Integer)
        self.assertEqual(type(b + c), Integer)
        self.assertEqual(type(c + a), Integer)
        self.assertEqual(str(a + b), '( a )+( b )')
        self.assertEqual(str(b + a), '( b )+( a )')
        self.assertEqual(str(b + c), '( b )+( {:d} )'.format(c))
        self.assertEqual(str(c + a), '( {:d} )+( a )'.format(c))

    def testIntegerSub(self):
        a = Integer('a')
        b = Integer('b')
        c = 6
        self.assertEqual(type(a - b), Integer)
        self.assertEqual(type(b - a), Integer)
        self.assertEqual(type(b - c), Integer)
        self.assertEqual(type(c - a), Integer)
        self.assertEqual(str(a - b), '( a )-( b )')
        self.assertEqual(str(b - a), '( b )-( a )')
        self.assertEqual(str(b - c), '( b )-( {:d} )'.format(c))
        self.assertEqual(str(c - a), '( {:d} )-( a )'.format(c))

    def testIntegerTrueDiv(self):
        a = Integer('a')
        b = Integer('b')
        c = 6
        self.assertEqual(type(a/b), Integer)
        self.assertEqual(type(b/a), Integer)
        self.assertEqual(type(b/c), Integer)
        self.assertEqual(type(c/a), Integer)
        self.assertEqual(str(a/b), '( a )/( b )')
        self.assertEqual(str(b/a), '( b )/( a )')
        self.assertEqual(str(b/c), '( b )/( {:d} )'.format(c))
        self.assertEqual(str(c/a), '( {:d} )/( a )'.format(c))
        
    def testIntegerMul(self):
        a = Integer('a')
        b = Integer('b')
        c = 6
        self.assertEqual(type(a*b), Integer)
        self.assertEqual(type(b*a), Integer)
        self.assertEqual(type(b*c), Integer)
        self.assertEqual(type(c*a), Integer)
        self.assertEqual(str(a*b), '( a )*( b )')
        self.assertEqual(str(b*a), '( b )*( a )')
        self.assertEqual(str(b*c), '( b )*( {:d} )'.format(c))
        self.assertEqual(str(c*a), '( {:d} )*( a )'.format(c))
  
    def testIntegerMod(self):
        a = Integer('a')
        b = Integer('b')
        c = 6
        self.assertEqual(type(a%b), Integer)
        self.assertEqual(type(b%a), Integer)
        self.assertEqual(type(b%c), Integer)
        self.assertEqual(type(c%a), Integer)
        self.assertEqual(str(a%b), '( a )%( b )')
        self.assertEqual(str(b%a), '( b )%( a )')
        self.assertEqual(str(b%c), '( b )%( {:d} )'.format(c))
        self.assertEqual(str(c%a), '( {:d} )%( a )'.format(c))
              
    def testIntegerPow(self):
        a = Integer('a')
        b = Integer('b')
        c = 6
        self.assertEqual(type(a**b), Integer)
        self.assertEqual(type(b**a), Integer)
        self.assertEqual(type(b**c), Integer)
        self.assertEqual(type(c**a), Integer)
        self.assertEqual(str(a**b), '_rtoi(pow(a, b))')
        self.assertEqual(str(b**a), '_rtoi(pow(b, a))')
        self.assertEqual(str(b**c), '_rtoi(pow(b, {:d}))'.format(c))
        self.assertEqual(str(c**a), '_rtoi(pow({:d}, a))'.format(c))

    def testIntegerRShift(self):
        a = Integer('a')
        b = Integer('b')
        c = 6
        self.assertEqual(type(a>>b), Integer)
        self.assertEqual(type(b>>a), Integer)
        self.assertEqual(type(b>>c), Integer)
        self.assertEqual(type(c>>a), Integer)
        self.assertEqual(str(a>>b), '( a )>>( b )')
        self.assertEqual(str(b>>a), '( b )>>( a )')
        self.assertEqual(str(b>>c), '( b )>>( {:d} )'.format(c))
        self.assertEqual(str(c>>a), '( {:d} )>>( a )'.format(c))
        
    def testIntegerLShift(self):
        a = Integer('a')
        b = Integer('b')
        c = 6
        self.assertEqual(type(a<<b), Integer)
        self.assertEqual(type(b<<a), Integer)
        self.assertEqual(type(b<<c), Integer)
        self.assertEqual(type(c<<a), Integer)
        self.assertEqual(str(a<<b), '( a )<<( b )')
        self.assertEqual(str(b<<a), '( b )<<( a )')
        self.assertEqual(str(b<<c), '( b )<<( {:d} )'.format(c))
        self.assertEqual(str(c<<a), '( {:d} )<<( a )'.format(c))     

    def testIntegerAnd(self):
        a = Integer('a')
        b = Integer('b')
        c = 6
        self.assertEqual(type(a&b), Integer)
        self.assertEqual(type(b&a), Integer)
        self.assertEqual(type(b&c), Integer)
        self.assertEqual(type(c&a), Integer)
        self.assertEqual(str(a&b), '( a )&( b )')
        self.assertEqual(str(b&a), '( b )&( a )')
        self.assertEqual(str(b&c), '( b )&( {:d} )'.format(c))
        self.assertEqual(str(c&a), '( {:d} )&( a )'.format(c))
        
    def testIntegerOr(self):
        a = Integer('a')
        b = Integer('b')
        c = 6
        self.assertEqual(type(a|b), Integer)
        self.assertEqual(type(b|a), Integer)
        self.assertEqual(type(b|c), Integer)
        self.assertEqual(type(c|a), Integer)
        self.assertEqual(str(a|b), '( a )|( b )')
        self.assertEqual(str(b|a), '( b )|( a )')
        self.assertEqual(str(b|c), '( b )|( {:d} )'.format(c))
        self.assertEqual(str(c|a), '( {:d} )|( a )'.format(c))
        
    def testIntegerXor(self):
        a = Integer('a')
        b = Integer('b')
        c = 6
        self.assertEqual(type(a^b), Integer)
        self.assertEqual(type(b^a), Integer)
        self.assertEqual(type(b^c), Integer)
        self.assertEqual(type(c^a), Integer)
        self.assertEqual(str(a^b), '( a )^( b )')
        self.assertEqual(str(b^a), '( b )^( a )')
        self.assertEqual(str(b^c), '( b )^( {:d} )'.format(c))
        self.assertEqual(str(c^a), '( {:d} )^( a )'.format(c))  
                   
    def testIntegerGt(self):
        a = Integer('a')
        b = Integer('b')
        c = 6
        self.assertEqual(type(a > b), Bool)
        self.assertEqual(type(b > a), Bool)
        self.assertEqual(type(b > c), Bool)
        self.assertEqual(type(c > a), Bool)
        self.assertEqual(str(a > b), '( a )>( b )')
        self.assertEqual(str(b > a), '( b )>( a )')
        self.assertEqual(str(b > c), '( b )>( {:d} )'.format(c))
        self.assertEqual(str(c > a), '( a )<( {:d} )'.format(c))

    def testIntegerLt(self):
        a = Integer('a')
        b = Integer('b')
        c = 6
        self.assertEqual(type(a < b), Bool)
        self.assertEqual(type(b < a), Bool)
        self.assertEqual(type(b < c), Bool)
        self.assertEqual(type(c < a), Bool)
        self.assertEqual(str(a < b), '( a )<( b )')
        self.assertEqual(str(b < a), '( b )<( a )')
        self.assertEqual(str(b < c), '( b )<( {:d} )'.format(c))
        self.assertEqual(str(c < a), '( a )>( {:d} )'.format(c))
        
    def testIntegerLe(self):
        a = Integer('a')
        b = Integer('b')
        c = 6
        self.assertEqual(type(a <= b), Bool)
        self.assertEqual(type(b <= a), Bool)
        self.assertEqual(type(b <= c), Bool)
        self.assertEqual(type(c <= a), Bool)
        self.assertEqual(str(a <= b), '( a )<=( b )')
        self.assertEqual(str(b <= a), '( b )<=( a )')
        self.assertEqual(str(b <= c), '( b )<=( {:d} )'.format(c))
        self.assertEqual(str(c <= a), '( a )>=( {:d} )'.format(c))
        
    def testIntegerGe(self):
        a = Integer('a')
        b = Integer('b')
        c = 6
        self.assertEqual(type(a >= b), Bool)
        self.assertEqual(type(b >= a), Bool)
        self.assertEqual(type(b >= c), Bool)
        self.assertEqual(type(c >= a), Bool)
        self.assertEqual(str(a >= b), '( a )>=( b )')
        self.assertEqual(str(b >= a), '( b )>=( a )')
        self.assertEqual(str(b >= c), '( b )>=( {:d} )'.format(c))
        self.assertEqual(str(c >= a), '( a )<=( {:d} )'.format(c))
        
    def testIntegerEq(self):
        a = Integer('a')
        b = Integer('b')
        c = 6
        self.assertEqual(type(a == b), Bool)
        self.assertEqual(type(b == a), Bool)
        self.assertEqual(type(b == c), Bool)
        self.assertEqual(type(c == a), Bool)
        self.assertEqual(str(a == b), '( a )==( b )')
        self.assertEqual(str(b == a), '( b )==( a )')
        self.assertEqual(str(b == c), '( b )==( {:d} )'.format(c))
        self.assertEqual(str(c == a), '( a )==( {:d} )'.format(c)) 
           
    def testIntegerNeq(self):
        a = Integer('a')
        b = Integer('b')
        c = 6
        self.assertEqual(type(a != b), Bool)
        self.assertEqual(type(b != a), Bool)
        self.assertEqual(type(b != c), Bool)
        self.assertEqual(type(c != a), Bool)
        self.assertEqual(str(a != b), '( a )!=( b )')
        self.assertEqual(str(b != a), '( b )!=( a )')
        self.assertEqual(str(b != c), '( b )!=( {:d} )'.format(c))
        self.assertEqual(str(c != a), '( a )!=( {:d} )'.format(c))  
        
    def testIntegerUnary(self):
        a = Integer('a')
        self.assertEqual(type(-a), Integer)
        self.assertEqual(type(+a), Integer)
        self.assertEqual(type(abs(a)), Integer)
        self.assertEqual(type(~a), Integer)
        self.assertEqual(str(-a), '-( a )') 
        self.assertEqual(str(+a), '+( a )')  
        self.assertEqual(str(abs(a)), 'abs(a)')  
        self.assertEqual(str(~a), '~( a )')  

        
    ############################################################################
    # Bool
    ############################################################################  
    def testBool(self):
        a = Bool(Integer('a'))
        b = Bool(Real('b'))
        c = Bool(Bool('c'))
        d = Bool(1.5)
        
        self.assertEqual(type(a), Bool)
        self.assertEqual(type(b), Bool)
        self.assertEqual(type(c), Bool)
        self.assertEqual(type(d), Bool)
        self.assertEqual(str(a), '( a )!=( 0 )')  
        self.assertEqual(str(b), '( b )!=( {:e} )'.format(0))         
        self.assertEqual(str(c), 'c')  
        self.assertEqual(str(d), '1')  
        
    def testBoolAnd(self):
        a = Bool('a')
        b = Bool('b')
        self.assertEqual(a.getValue(), "a")
        self.assertEqual(type(a&b), Bool)
        self.assertEqual(type(b&a), Bool)
        self.assertEqual(type(b&True), Bool)
        self.assertEqual(type(True&a), Bool)
        self.assertEqual(type(b&False), bool)
        self.assertEqual(type(False&a), bool)
        self.assertEqual(str(a&b), '( a )&&( b )')
        self.assertEqual(str(b&a), '( b )&&( a )')
        self.assertEqual(str(b&True), 'b')
        self.assertEqual(str(True&a), 'a')
        self.assertEqual(b&False, False)
        self.assertEqual(False&a, False)
                
    def testBoolOr(self):
        a = Bool('a')
        b = Bool('b')
        self.assertEqual(type(a|b), Bool)
        self.assertEqual(type(b|a), Bool)
        self.assertEqual(type(b|True), bool)
        self.assertEqual(type(True|a), bool)
        self.assertEqual(type(b|False), Bool)
        self.assertEqual(type(False|a), Bool)
        self.assertEqual(str(a|b), '( a )||( b )')
        self.assertEqual(str(b|a), '( b )||( a )')
        self.assertEqual(b|True, True)
        self.assertEqual(True|a, True)
        self.assertEqual(str(b|False), 'b')
        self.assertEqual(str(False|a), 'a')
        
    def testBoolXor(self):
        a = Bool('a')
        b = Bool('b')
        self.assertEqual(type(a^b), Bool)
        self.assertEqual(type(b^a), Bool)
        self.assertEqual(type(b^True), Bool)
        self.assertEqual(type(True^a), Bool)
        self.assertEqual(type(b^False), Bool)
        self.assertEqual(type(False^a), Bool)
        self.assertEqual(str(a^b), '( ( a )&&( !( b ) ) )||( ( !( a ) )&&( b ) )')
        self.assertEqual(str(b^a), '( ( b )&&( !( a ) ) )||( ( !( b ) )&&( a ) )')
        self.assertEqual(str(b^True), '!( b )')
        self.assertEqual(str(True^a), '!( a )')
        self.assertEqual(str(b^False), 'b')
        self.assertEqual(str(False^a), 'a')        
            
    def testBoolUnary(self):
        a = Bool('a')
        self.assertEqual(type(~a), Bool)
        self.assertEqual(str(~a), '!( a )')  

    ############################################################################
    # Variables
    ############################################################################ 
    def testIntVar(self):
        a = IntegerVar('a')
        self.assertEqual(isinstance(a, Integer), True)
        self.assertEqual(str(a), 'a')     
        self.assertEqual(type(a.eq(10)), Cmd)
        self.assertEqual(str(a.eq(2)), 'a = 2')     
        self.assertEqual(str(a.eq(Integer('b'))), 'a = b')  
        self.assertEqual(str(a.dec()), 'a = a - 1') 
        self.assertEqual(str(a.inc()), 'a = a + 1') 
                        
    def testRealVar(self):
        a = RealVar('a')
        self.assertEqual(isinstance(a, Real), True)
        self.assertEqual(str(a), 'a')     
        self.assertEqual(type(a.eq(10)), Cmd)
        self.assertEqual(str(a.eq(2)), 'a = {:e}'.format(2))
        self.assertEqual(str(a.eq(1.99)), 'a = {:e}'.format(1.99))
        self.assertEqual(str(a.eq(Real('b'))), 'a = b')       
 
    def testBoolVar(self):
        a = BoolVar('a')
        self.assertEqual(isinstance(a, Bool), True)
        self.assertEqual(str(a), 'a')     
        self.assertEqual(type(a.eq(False)), Cmd)
        self.assertEqual(str(a.eq(True)), 'a = 1')
        self.assertEqual(str(a.eq(Bool('b'))), 'a = b')       
        self.assertEqual(str(a.toggle()), 'a = !a')  
         
    ############################################################################
    # Event
    ############################################################################ 
    def testEvent(self):
        a = Event('a')
        b = Event('b')
        self.assertEqual(str(a), 'a')
        self.assertEqual(str(a | b | a), 'a or b or a')
        
    def testCross(self):
        a = Cross(1.0 - 2.0, 'rising')
        b = Cross(1.95 - 2.0, 'falling')
        c = Cross(1.9 - 2.0, 'both')    
        d = Cross(Real('a') - Real('b'), 'both')  
        e = Cross(Real('a') - Real('b'), 'both', 0.5)   
        f = Cross(Real('a') - Real('b'), 'both', 0.6, 0.3)  
        g = Cross(Real('a') - 5.7, 'both', Real('c'), Real('d'))      
        self.assertEqual(isinstance(a, Event), True) 
        self.assertEqual(str(a), 'cross({:e}, 1)'.format(-1))
        self.assertEqual(str(b), 'cross({:e}, -1)'.format(-0.05))
        self.assertEqual(str(c), 'cross({:e}, 0)'.format(-0.1))
        self.assertEqual(str(d), 'cross(( a )-( b ), 0)')
        self.assertEqual(str(e), 'cross(( a )-( b ), 0, {:e})'.format(0.5))
        self.assertEqual(str(f), 'cross(( a )-( b ), 0, {:e}, {:e})'.format(0.6, 0.3))       
        self.assertEqual(str(g), 'cross(( a )-( {:e} ), 0, c, d)'.format(5.7))  

    def testAbove(self):
        a = Above(1.0  - 2.0)
        b = Above(1.95 - 2.0)
        c = Above(1.9  - 2.0)    
        d = Above(Real('a') - Real('b'))  
        e = Above(Real('a') - Real('b'), 0.5)   
        f = Above(Real('a') - Real('b'), 0.6, 0.3)  
        g = Above(Real('a') - 5.7, Real('c'), Real('d'))      
        self.assertEqual(isinstance(a, Event), True) 
        self.assertEqual(str(a), 'above({:e})'.format(-1))
        self.assertEqual(str(b), 'above({:e})'.format(-0.05))
        self.assertEqual(str(c), 'above({:e})'.format(-0.1))
        self.assertEqual(str(d), 'above(( a )-( b ))')
        self.assertEqual(str(e), 'above(( a )-( b ), {:e})'.format(0.5))
        self.assertEqual(str(f), 'above(( a )-( b ), {:e}, {:e})'.format(0.6, 0.3))       
        self.assertEqual(str(g), 'above(( a )-( {:e} ), c, d)'.format(5.7))
        
    def testTimer(self):
        a = Timer(1.0)
        b = Timer(1.95, 0.5)
        c = Timer(1.9, 2.0, 0.6)    
        d = Timer(Real('a'), Real('b'), 1.2)  
        e = Timer(Real('a'), 0.5, Real('b'))     
        self.assertEqual(isinstance(a, Event), True) 
        self.assertEqual(str(a), 'timer({:e})'.format(1))
        self.assertEqual(str(b), 'timer({:e}, {:e})'.format(1.95, 0.5))
        self.assertEqual(str(c), 'timer({:e}, {:e}, {:e})'.format(1.9, 2, 0.6))
        self.assertEqual(str(d), 'timer(a, b, {:e})'.format(1.2))
        self.assertEqual(str(e), 'timer(a, {:e}, b)'.format(0.5))

    def testInitialStep(self):
        a = InitialStep()
        b = InitialStep("ac", "dc", "ic")
        c = InitialStep("tran")   
        self.assertEqual(isinstance(a, Event), True) 
        self.assertEqual(str(a), 'initial_step')
        self.assertEqual(str(b), 'initial_step("ac", "dc", "ic")')
        self.assertEqual(str(c), 'initial_step("tran")')
        
    def testFinalStep(self):
        a = FinalStep()
        b = FinalStep("pac", "pnoise", "pss")
        c = FinalStep("pxf")   
        self.assertEqual(isinstance(a, Event), True) 
        self.assertEqual(str(a), 'final_step')
        self.assertEqual(str(b), 'final_step("pac", "pnoise", "pss")')
        self.assertEqual(str(c), 'final_step("pxf")')       
                                                  
    ############################################################################
    # Command
    ############################################################################ 
    def testCmd(self):
        a = Cmd('a')
        b = CmdList(CmdList(Cmd('a')), Cmd('b'), Cmd('c'))
        b.append(CmdList(Cmd('d'), Cmd('e')), Cmd('f'))
        b.append(Cmd('g'))
        self.assertEqual(str(a), 'a')
        self.assertEqual(str(a.getVA(0)), 'a;\n')       
        self.assertEqual(str(a.getVA(1)), '    a;\n')      
        self.assertEqual(str(a.getVA(2)), '        a;\n') 
        self.assertEqual(isinstance(b, Cmd), True)
        self.assertEqual(str(b), 'a, b, c, d, e, f, g')
        self.assertEqual(type(b.flat()), list)
        self.assertEqual(', '.join([str(x) for x in b.flat()]), 'a, b, c, d, e, f, g')
        self.assertEqual(len(b), 6)
        self.assertEqual(len(b.flat()), 7)
        self.assertEqual(str(b.getVA(0)), 'a;\nb;\nc;\nd;\ne;\nf;\ng;\n')            
        self.assertEqual(str(b.getVA(1)), '    a;\n    b;\n    c;\n    d;\n    e;\n    f;\n    g;\n') 
        
    ############################################################################
    # Block
    ############################################################################ 
    def testBlock(self):   
        a = block("head1")(CmdList(Cmd('d'), Cmd('e')), Cmd('f'))
        b = block("head2")(Cmd('f'))
        c = block("head3")()
        self.assertEqual(isinstance(a, CmdList), True)
        self.assertEqual(a.getHeader(), "head1")
        self.assertEqual(str(a.getVA(0)), 'head1 begin\n    d;\n    e;\n    f;\nend\n')  
        self.assertEqual(str(a.getVA(1)), '    head1 begin\n        d;\n        e;\n        f;\n    end\n') 
        self.assertEqual(str(b.getVA(0)), 'head2\n    f;\n')    
        self.assertEqual(str(b.getVA(1)), '    head2\n        f;\n')  
        self.assertEqual(str(c.getVA(0)), 'head3;\n')  
        self.assertEqual(str(c.getVA(1)), '    head3;\n')
        
    ############################################################################
    # At
    ############################################################################ 
    def testAt(self):   
        a = At(Event("head1"))(Cmd('f'))
        self.assertEqual(isinstance(a, Block), True) 
        self.assertEqual(str(a.getVA(0)), '@( head1 )\n    f;\n')  
        self.assertEqual(str(a.getVA(1)), '    @( head1 )\n        f;\n')    
        
    ############################################################################
    # Analysis
    ############################################################################ 
    def testAnalysis(self):   
        a = analysis("sp")
        b = analysis("static", "tdr", "xf")
        self.assertEqual(type(a), Bool) 
        self.assertEqual(str(a), 'analysis("sp")')  
        self.assertEqual(str(b), 'analysis("static", "tdr", "xf")')  

    ############################################################################
    # AcStim
    ############################################################################ 
    def testAcStim(self):   
        a = acStim(1)
        b = acStim(1.7)
        c = acStim(Real('a'), 3.0)
        d = acStim(Real('a'), Real('b'), "pac")
        self.assertEqual(type(a), Real) 
        self.assertEqual(str(a), 'ac_stim("ac", {:e}, {:e})'.format(1, 0)) 
        self.assertEqual(str(b), 'ac_stim("ac", {:e}, {:e})'.format(1.7, 0))
        self.assertEqual(str(c), 'ac_stim("ac", a, {:e})'.format(3.0)) 
        self.assertEqual(str(d), 'ac_stim("pac", a, b)')      
        
    ############################################################################
    # Loop
    ############################################################################       
    def testLoop(self):
        a = Repeat(11)()
        self.assertEqual(isinstance(a, Block), True)
        self.assertEqual(a.getVA(0), "repeat( 11 );\n")
        self.assertEqual(str(a.getN()), "11")   
        a = While(Bool('a'))()
        b = While(False)()
        self.assertEqual(isinstance(a, Block), True)
        self.assertEqual(a.getVA(0), "while( a );\n") 
        self.assertEqual(str(a.getCond()), "a")      
        self.assertEqual(b.getVA(0), "while( 0 );\n") 
        a = For(CmdList(), False, Cmd(""))()
        b = For(CmdList(Cmd('a'), Cmd('b')), Bool('a'), Cmd("c"))() 
        self.assertEqual(isinstance(a, Block), True)
        self.assertEqual(a.getVA(0), "for( ; 0;  );\n") 
        self.assertEqual(b.getVA(0), "for( a, b; a; c );\n") 
        self.assertEqual(str(b.getCond()), "a") 
        self.assertEqual(str(b.getStart()), "a, b") 
        self.assertEqual(str(b.getInc()), "c") 
                        
    ############################################################################
    # Conditions
    ############################################################################ 
    def testCond(self):           
        a = If(True)(Cmd('a'))    
        b = If(Bool('a'))(Cmd('c'))         
        c = If(False)(Cmd('c')).Else(Cmd('d'))   
        self.assertEqual(isinstance(a, Cmd), True)
        self.assertEqual(str(b.getCond()), "a")  
        self.assertEqual(a.getVA(0), "if( 1 )\n    a;\n")
        self.assertEqual(b.getVA(0), "if( a )\n    c;\n")
        self.assertEqual(c.getVA(0), "if( 0 )\n    c;\nelse\n    d;\n")
        self.assertEqual(str(c.getBlock(True)), "c")
        self.assertEqual(str(c.getBlock(False)), "d")      
          
    ############################################################################
    # testCase
    ############################################################################    
    def testCase(self):
        a = Case(Real('a'))(
                (1.0, 
                    Cmd('d'), 
                    Cmd('f')
                ), 
                (2, 
                    Cmd('g')
                ),
                (Real('a'), 
                    Cmd('d'), 
                    Cmd('f')
                ), 
            )  
        b = Case(Integer('b'))(
                (Integer('a'), 
                    Cmd('d'), 
                    Cmd('f')
                ), 
                (2, 
                    Cmd('g')
                )
            )     
        c = Case(Bool('b'))(
                (Bool('a'), 
                    Cmd('d'), 
                    Cmd('f')
                ), 
                (False, 
                    Cmd('g')
                )
            )      
        d = Case(1.0)(
                (None,
                    Cmd('a')
                )
            )  
        e = Case(1)()          
        f = Case(False)()          
        self.assertEqual(isinstance(a, Cmd), True)
        self.assertEqual(a.getVA(0), "case( a )\n    {:e}: begin\n        d;\n".format(1) +\
                         "        f;\n    end\n    {:e}:\n        g;\n    a: begin\n".format(2) +\
                         "        d;\n        f;\n    end\nendcase\n") 
        self.assertEqual(b.getVA(0), "case( b )\n    a: begin\n        d;\n        f;\n    end\n    2:\n        g;\nendcase\n")
        self.assertEqual(c.getVA(0), "case( b )\n    a: begin\n        d;\n        f;\n    end\n    0:\n        g;\nendcase\n")
        self.assertEqual(d.getVA(0), "case( {:e} )\n    default:\n        a;\nendcase\n".format(1))
        self.assertEqual(e.getVA(0), "case( 1 )\nendcase\n")
        self.assertEqual(f.getVA(0), "case( 0 )\nendcase\n")
        self.assertEqual(str(b.getBlockList()[0]), "d, f")        
        self.assertEqual(str(b.getBlockList()[1]), "g")   
        
    ############################################################################
    # messages
    ############################################################################    
    def testMsg(self):
        a = Strobe("a")
        b = Strobe("b", Real('c'), 1.97, 4, True, Bool('d'), Integer('e'))
        self.assertEqual(type(a), Cmd)   
        self.assertEqual(str(a), '$strobe("a")')       
        self.assertEqual(str(b), '$strobe("b", c, {:e}, 4, 1, d, e)'.format(1.97))           
        a = Write("a")
        b = Write("b", Real('c'), 1.97, 4, True, Bool('d'), Integer('e'))
        self.assertEqual(type(a), Cmd)   
        self.assertEqual(str(a), '$write("a")')       
        self.assertEqual(str(b), '$write("b", c, {:e}, 4, 1, d, e)'.format(1.97))  
        a = Error("a")
        b = Error("b", Real('c'), 1.97, 4, True, Bool('d'), Integer('e'))
        self.assertEqual(type(a), Cmd)   
        self.assertEqual(str(a), '$error("a")')       
        self.assertEqual(str(b), '$error("b", c, {:e}, 4, 1, d, e)'.format(1.97))    
        a = Fatal("a")
        b = Fatal("b", Real('c'), 1.97, 4, True, Bool('d'), Integer('e'))
        self.assertEqual(type(a), Cmd)   
        self.assertEqual(str(a), '$fatal(0, "a")')       
        self.assertEqual(str(b), '$fatal(0, "b", c, {:e}, 4, 1, d, e)'.format(1.97))  
        a = Fopen("ab")   
        self.assertEqual(type(a), Integer)   
        self.assertEqual(str(a), '$fopen("ab")')   
        a = Fclose(Integer('f'))   
        self.assertEqual(type(a), Cmd)   
        self.assertEqual(str(a), '$fclose(f)')
        a = Fstrobe(Integer('f'), "a")
        b = Fstrobe(Integer('f'), "b", Real('c'), 1.97, 4, True, Bool('d'), Integer('e'))
        self.assertEqual(type(a), Cmd)   
        self.assertEqual(str(a), '$fstrobe(f, "a")')       
        self.assertEqual(str(b), '$fstrobe(f, "b", c, {:e}, 4, 1, d, e)'.format(1.97))           
        a = Fwrite(Integer('d'), "a")
        b = Fwrite(Integer('d'), "b", Real('c'), 1.97, 4, True, Bool('d'), Integer('e'))
        self.assertEqual(type(a), Cmd)   
        self.assertEqual(str(a), '$fwrite(d, "a")')       
        self.assertEqual(str(b), '$fwrite(d, "b", c, {:e}, 4, 1, d, e)'.format(1.97))          
        
    ############################################################################
    # simControl
    ############################################################################    
    def testSimControl(self):
        a = Discontinuity()
        b = Discontinuity(2)
        self.assertEqual(type(a), Cmd)   
        self.assertEqual(str(a), '$discontinuity(0)')       
        self.assertEqual(str(b), '$discontinuity(2)')               
        a = Finish()    
        self.assertEqual(type(a), Cmd)   
        self.assertEqual(str(a), '$finish')     
        a = BoundStep(1e-3)
        b = BoundStep(Real('a'))
        self.assertEqual(type(a), Cmd)
        self.assertEqual(str(a), '$bound_step({:e})'.format(1e-3))   
        self.assertEqual(str(b), '$bound_step(a)')  
        a = lastCrossing(Real('a'), Real('b'), 'both')
        b = lastCrossing(Real('a'), Real('b'), 'rising')
        c = lastCrossing(Real('a'), Real('b'), 'falling')
        d = lastCrossing(Real('a'), 1, 'both')
        e = lastCrossing(Real('a'), 1.87, 'both')
        self.assertEqual(type(a), Real)
        self.assertEqual(str(a), 'last_crossing(a - b, 0)') 
        self.assertEqual(str(b), 'last_crossing(a - b, 1)') 
        self.assertEqual(str(c), 'last_crossing(a - b, -1)') 
        self.assertEqual(str(d), 'last_crossing(a - {:e}, 0)'.format(1)) 
        self.assertEqual(str(e), 'last_crossing(a - {:e}, 0)'.format(1.87)) 
        
    ############################################################################
    # testRandon
    ############################################################################    
    def testRandon(self):  
        seed = IntegerVar('seed')
        a = random(seed)
        b = uDistInt(seed, 0, 1)
        c = uDistReal(seed, 0.2, 1.2)
        d = gaussDistInt(seed, 0, 1)
        e = gaussDistReal(seed, 0.2, 1.2)
        f = expDistInt(seed, 0)
        g = expDistReal(seed, 0.2)    
        h = poissonDistInt(seed, 0)
        i = poissonDistReal(seed, 0.2) 
        self.assertEqual(type(a), Integer) 
        self.assertEqual(type(b), Integer) 
        self.assertEqual(type(c), Real) 
        self.assertEqual(type(d), Integer) 
        self.assertEqual(type(e), Real) 
        self.assertEqual(type(f), Integer) 
        self.assertEqual(type(g), Real) 
        self.assertEqual(type(h), Integer) 
        self.assertEqual(type(i), Real) 
        self.assertEqual(str(a), "$random(seed)") 
        self.assertEqual(str(b), "$dist_uniform(seed, 0, 1)") 
        self.assertEqual(str(c), "$rdist_uniform(seed, {:e}, {:e})".format(0.2, 1.2)) 
        self.assertEqual(str(d), "$dist_normal(seed, 0, 1)") 
        self.assertEqual(str(e), "$rdist_normal(seed, {:e}, {:e})".format(0.2, 1.2)) 
        self.assertEqual(str(f), "$dist_exponential(seed, 0)") 
        self.assertEqual(str(g), "$rdist_exponential(seed, {:e})".format(0.2)) 
        self.assertEqual(str(h), "$dist_poisson(seed, 0)") 
        self.assertEqual(str(i), "$rdist_poisson(seed, {:e})".format(0.2))      
          
    ############################################################################
    # testConstants
    ############################################################################          
    def testConstants(self):
        self.assertEqual(type(temp), Real)  
        self.assertEqual(str(temp), "$temperature")            
        self.assertEqual(type(abstime), Real)  
        self.assertEqual(str(abstime), "$abstime")  
        self.assertEqual(type(vt), Real)  
        self.assertEqual(str(vt), "$vt")  
        
    ############################################################################
    # testmath
    ############################################################################        
    def testMath(self):    
     
        self.assertEqual(type(cos(1.2)), Real)
        self.assertEqual(str(cos(1.1)), "cos({:e})".format(1.1))
        self.assertEqual(type(sin(1.2)), Real)
        self.assertEqual(str(sin(1.1)), "sin({:e})".format(1.1))
        self.assertEqual(type(tan(1.2)), Real)
        self.assertEqual(str(tan(1.1)), "tan({:e})".format(1.1))
        
        self.assertEqual(type(acos(1.2)), Real)
        self.assertEqual(str(acos(1.1)), "acos({:e})".format(1.1))
        self.assertEqual(type(asin(1.2)), Real)
        self.assertEqual(str(asin(1.1)), "asin({:e})".format(1.1))
        self.assertEqual(type(atan(1.2)), Real)
        self.assertEqual(str(atan(1.1)), "atan({:e})".format(1.1))
        
        self.assertEqual(type(cosh(1.2)), Real)
        self.assertEqual(str(cosh(1.1)), "cosh({:e})".format(1.1))
        self.assertEqual(type(sinh(1.2)), Real)
        self.assertEqual(str(sinh(1.1)), "sinh({:e})".format(1.1))
        self.assertEqual(type(tanh(1.2)), Real)
        self.assertEqual(str(tanh(1.1)), "tanh({:e})".format(1.1))
        
        self.assertEqual(type(acosh(1.2)), Real)
        self.assertEqual(str(acosh(1.1)), "acosh({:e})".format(1.1))
        self.assertEqual(type(sinh(1.2)), Real)
        self.assertEqual(str(asinh(1.1)), "asinh({:e})".format(1.1))
        self.assertEqual(type(atanh(1.2)), Real)
        self.assertEqual(str(atanh(1.1)), "atanh({:e})".format(1.1))  
             
        self.assertEqual(type(hypot(1.2, 1.1)), Real)
        self.assertEqual(str(hypot(1.2, 1.1)), "hypot({:e}, {:e})".format(1.2, 1.1))
        self.assertEqual(type(atan2(1.2, 1.1)), Real)
        self.assertEqual(str(atan2(1.2, 1.1)), "atan2({:e}, {:e})".format(1.2, 1.1))

        self.assertEqual(type(exp(1.2)), Real)
        self.assertEqual(str(exp(1.1)), "exp({:e})".format(1.1))
        self.assertEqual(type(limexp(1.2)), Real)
        self.assertEqual(str(limexp(1.1)), "limexp({:e})".format(1.1))        
        self.assertEqual(type(sqrt(1.2)), Real)
        self.assertEqual(str(sqrt(1.1)), "sqrt({:e})".format(1.1))
        self.assertEqual(type(log(1.2)), Real)
        self.assertEqual(str(log(1.1)), "log({:e})".format(1.1))
        self.assertEqual(type(ln(1.2)), Real)
        self.assertEqual(str(ln(1.1)), "ln({:e})".format(1.1))  
        
        self.assertEqual(type(ceil(1.2)), Real)
        self.assertEqual(str(ceil(1.2)), "ceil({:e})".format(1.2))
        self.assertEqual(type(floor(1.2)), Real)
        self.assertEqual(str(floor(1.2)), "floor({:e})".format(1.2))

        self.assertEqual(type(idt(1.2)), Real)
        self.assertEqual(str(idt(1.2)), "idt({:e}, {:e})".format(1.2, 0))
        self.assertEqual(type(ddt(1.2)), Real)
        self.assertEqual(str(ddt(1.2)), "ddt({:e})".format(1.2))  
        
        self.assertEqual(type(transition(1.2)), Real)
        self.assertEqual(str(transition(1.2)), 
                         "transition({:e}, {:e}, {:e}, {:e})".format(1.2, 0, 1e-6, 1e-6))  
        self.assertEqual(str(transition(1.2, Real('a'))), 
                         "transition({:e}, a, {:e}, {:e})".format(1.2, 1e-6, 1e-6))          
        self.assertEqual(str(transition(Real('a'), 1, 2, 3)), 
                         "transition(a, {:e}, {:e}, {:e})".format(1, 2, 3))     
        self.assertEqual(str(transition(Real('a'), Real('b'), Real('c'), Real('d'))), 
                         "transition(a, b, c, d)")    
        self.assertEqual(type(smooth(False)), Real)
        self.assertEqual(str(smooth(True)), 
        "( ( tanh(( ( {:e} )*( transition({:e}, {:e}, {:e}, {:e}) ) )-( {:e} )) )/( {:e} ) )+( {:e} )".format(6, 1, 0, 1e-6*2.070002, 1e-6*2.070002, 3, 1.99011, 0.5))  
                                                  
        self.assertEqual(type(absDelay(1.2, 0)), Real)
        self.assertEqual(str(absDelay(1.2, 0)), "absdelay({:e}, {:e})".format(1.2, 0))   
        self.assertEqual(str(absDelay(Real('a'), Real('b'))), "absdelay(a, b)")                          

        self.assertEqual(type(slew(1.2)), Real)
        self.assertEqual(str(slew(1.2)), "slew({:e}, {:e}, {:e})".format(1.2, 10e-6, 10e-6))   
        self.assertEqual(str(slew(1.2, 0, 0)), "slew({:e}, {:e}, {:e})".format(1.2, 0, 0)) 
        self.assertEqual(str(slew(Real('a'), Real('b'), Real('c'))), "slew(a, b, c)")             
                    
        self.assertEqual(type(ternary(False, 1.9, 1)), Real)
        self.assertEqual(type(ternary(False, 1, 1)), Integer)
        self.assertEqual(type(ternary(False, True, False)), Bool)
        self.assertEqual(type(ternary(Bool('a'), Real('b'), Real('c'))), Real)
        self.assertEqual(type(ternary(Bool('a'), Integer('b'), Integer('c'))), Integer)
        self.assertEqual(type(ternary(Bool('a'), Bool('b'), Bool('c'))), Bool)
        self.assertEqual(str(ternary(False, 1.9, 1)), "0 ? {:e} : {:e}".format(1.9, 1))
        self.assertEqual(str(ternary(True, 1, 2)), "1 ? 1 : 2")
        self.assertEqual(str(ternary(False, True, False)), "0 ? 1 : 0")
        self.assertEqual(str(ternary(Bool('a'), Real('b'), Real('c'))), "a ? b : c")
        self.assertEqual(str(ternary(Bool('a'), Integer('b'), Integer('c'))), "a ? b : c")
        self.assertEqual(str(ternary(Bool('a'), Bool('b'), Bool('c'))), "a ? b : c")
        
    ############################################################################
    # testElectrical
    ############################################################################        
    def testElectrical(self):  
        el1 = Electrical("a")   
        el2 = Electrical("b")
        br1 = Branch(el1, el2)    
        self.assertEqual(str(el1.v), "V(a)")
        self.assertEqual(str(el1.i), "I(a)")
        self.assertEqual(br1.getName(), "a, b")
        self.assertEqual(type(el1.vCont(1)), Cmd)
        self.assertEqual(type(el1.iCont(2)), Cmd)
        self.assertEqual(type(el1.vAttr(3)), Cmd)
        self.assertEqual(type(el1.iAttr(4)), Cmd)
        self.assertEqual(type(el1.vInd(True)), Cmd)
        self.assertEqual(type(el1.iInd(False)), Cmd)
        self.assertEqual(str(el1.vCont(1)), "V(a) <+ {:e}".format(1))
        self.assertEqual(str(el1.iCont(2)), "I(a) <+ {:e}".format(2))
        self.assertEqual(str(el1.vAttr(3)), "V(a) = {:e}".format(3))
        self.assertEqual(str(el1.iAttr(4)), "I(a) = {:e}".format(4))
        self.assertEqual(str(el1.vInd(True)), "V(a) : 1")
        self.assertEqual(str(el1.iInd(False)), "I(a) : 0")
        self.assertEqual(str(el1.vCont(Real('a'))), "V(a) <+ a")
        self.assertEqual(str(el1.iCont(Real('b'))), "I(a) <+ b")
        self.assertEqual(str(el1.vAttr(Real('c'))), "V(a) = c")
        self.assertEqual(str(el1.iAttr(Real('d'))), "I(a) = d")
        self.assertEqual(str(el1.vInd(Bool('e'))), "V(a) : e")
        self.assertEqual(str(el1.iInd(Bool('f'))), "I(a) : f") 
        self.assertEqual(str(br1.vCont(3.4)), "V(a, b) <+ {:e}".format(3.4))      

    ############################################################################
    # testVariable
    ############################################################################        
    def testVarFunc(self):
        mod = Module("test")
        var1 = mod.var()
        var2 = mod.var(name = "a")
        var3 = mod.var(vType = Real, name = "b")
        var4 = mod.var(vType = Bool, name = "c")    
        self.assertEqual(type(var1), IntegerVar)   
        self.assertEqual(type(var2), IntegerVar)   
        self.assertEqual(type(var3), RealVar)   
        self.assertEqual(type(var4), BoolVar)        
        self.assertEqual(str(var1), "_$1")   
        self.assertEqual(str(var2), "a")   
        self.assertEqual(str(var3), "b")   
        self.assertEqual(str(var4), "c")
        self.assertEqual(mod.variables, [('_$1', 'integer'), \
                                         ('a', 'integer'), \
                                         ('b', 'real'), \
                                         ('c', 'integer')])

    ############################################################################
    # testParemters
    ############################################################################        
    def testParFunc(self):
        mod = Module("test")
        par1 = mod.par(2, "d")
        par2 = mod.par(1.0, "a")
        par3 = mod.par(Real('a'), "b")
        par4 = mod.par(Integer('b'), "c")    
        self.assertEqual(type(par1), Integer)   
        self.assertEqual(type(par2), Real)   
        self.assertEqual(type(par3), Real)   
        self.assertEqual(type(par4), Integer)        
        self.assertEqual(str(par1), "d")   
        self.assertEqual(str(par2), "a")   
        self.assertEqual(str(par3), "b")   
        self.assertEqual(str(par4), "c")
        self.assertEqual(mod.parameters, [('d', 'integer', '2'), \
                                          ('a', 'real', '{:e}'.format(1)), \
                                          ('b', 'real', 'a'), \
                                          ('c', 'integer', 'b')])
        
    ############################################################################
    # testElFunc
    ############################################################################        
    def testElFunc(self):  
        mod = Module("test")
        el1 = mod.electrical()
        el2 = mod.electrical(name = "a")            
        el3 = mod.electrical(name = "b", width = 3, direction = "input") 
        el4 = mod.electrical(name = "c", direction = "inout") 
        el5 = mod.electrical(name = "d", direction = "input") 
        el6 = mod.electrical(name = "e", direction = "output") 
        self.assertEqual(type(el1), Electrical)
        self.assertEqual(type(el2), Electrical)
        self.assertEqual(type(el3), list)
        self.assertEqual(type(el3[0]), Electrical)
        self.assertEqual(type(el3[1]), Electrical)
        self.assertEqual(type(el3[2]), Electrical)
        self.assertEqual(type(el4), Electrical)
        self.assertEqual(type(el5), Electrical)
        self.assertEqual(type(el6), Electrical)
        self.assertEqual(el1.getName(), "_$1") 
        self.assertEqual(el2.getName(), "a")      
        self.assertEqual(el3[0].getName(), "b[0]")   
        self.assertEqual(el3[1].getName(), "b[1]")   
        self.assertEqual(el3[2].getName(), "b[2]")      
        self.assertEqual(el4.getName(), "c")      
        self.assertEqual(el5.getName(), "d")      
        self.assertEqual(el6.getName(), "e")           
        self.assertEqual(mod.nodes, [("_$1", 1),\
                                     ("a", 1),\
                                     ("b", 3),\
                                     ("c", 1),\
                                     ("d", 1),\
                                     ("e", 1)])
        self.assertEqual(mod.ports, [("b", 3, "input"),\
                                     ("c", 1, "inout"),\
                                     ("d", 1, "input"),\
                                     ("e", 1, "output")])                                     
         
    ############################################################################
    # testGetVaFunc
    ############################################################################        
    def testGetVaFunc(self): 
        mod = Module("teste")
        par = mod.par(2, "par1")
        var = mod.var()
        el1 = mod.electrical()
        el2 = mod.electrical(direction="input")
        mod.endAnalog(var.eq(4), var.eq(44))
        mod.analog(var.eq(3), var.eq(33))
        mod.beginningAnalog(var.eq(2), var.eq(22))              
        ref = '''`include "constants.vams"
`include "disciplines.vams"

/******************************************************************************
 *                             Module declaration                             * 
 ******************************************************************************/
module teste(_$3);

/******************************************************************************
 *                                   Ports                                    * 
 ******************************************************************************/
input _$3;

/******************************************************************************
 *                                 Disciplines                                * 
 ******************************************************************************/
electrical _$2;
electrical _$3;

/******************************************************************************
 *                             Build-in functions                             * 
 ******************************************************************************/
analog function integer _rtoi;
input in;
real in;
begin
    _rtoi = floor(in + 0.5);
end
endfunction

/******************************************************************************
 *                                 Parameters                                 * 
 ******************************************************************************/
parameter integer par1 = 2;

/******************************************************************************
 *                                 Variables                                  * 
 ******************************************************************************/
integer _$1;

/******************************************************************************
 *                                Analog block                                * 
 ******************************************************************************/
analog begin
    _$1 = 2;
    _$1 = 22;
    _$1 = 3;
    _$1 = 33;
    _$1 = 4;
    _$1 = 44;
end
endmodule'''
        self.assertEqual(mod.getVA()[323:], ref)
                                                                                                                                                     
if __name__ == '__main__':
    unittest.main()
    

