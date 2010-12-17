
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