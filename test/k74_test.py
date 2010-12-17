# Copyright (c) 2010 Eric Evans <eevans@sym-link.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import unittest
from christmux import K74

class K74Test(unittest.TestCase):
    def setUp(self):
        self.k74 = K74(mock=True)
    
    def tearDown(self):
        del self.k74
    
    def test_set(self):
        assert not self.k74.is_set(1), "failed precondition"
        assert not self.k74.is_set(2), "failed precondition"
        assert not self.k74.is_set(8), "failed precondition"
        self.k74.set(1)
        self.k74.set(2)
        self.k74.set(8)
        assert self.k74.is_set(1), "bit 1 not set, should be"
        assert self.k74.is_set(2), "bit 2 not set, should be"
        assert self.k74.is_set(8), "bit 8 not set, should be"
        assert self.k74.pp.data == 131
    
    def test_unset(self):
        self.k74.set(8)
        assert self.k74.is_set(8)
        self.k74.unset(8)
        assert not self.k74.is_set(8)
        
    def test_bad_channel(self):
        self.assertRaises(ValueError, self.k74.set, 'a')
        self.assertRaises(AssertionError, self.k74.set, 10)

# vi:ai sw=4 ts=4 tw=0 et:
