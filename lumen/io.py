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

from parallel import Parallel

class DummyParallel(object):
    def __init_(self):
        self.data = 0
    
    def setData(self, data):
        self.data = data

class ParallelIO(object):
    def __init__(self, init=0, mock=False):
        self.pp = mock and DummyParallel() or Parallel()
        self.state = init
        self.pp.setData(self.state)

    def is_set(self, out):
        return self.state & CHANS[out-1]

    def set(self, out):
        channel = int(out)
        assert channel <= 8 and channel > 0, "channel: %s" % channel

        if not self.is_set(channel):
            self.state += CHANS[channel-1]
            self.pp.setData(self.state)
            return True

        return False

    def unset(self, out):
        channel = int(out)
        assert channel <= 8 and channel > 0, "channel: %s" % channel

        if self.is_set(channel):
            self.state -= CHANS[channel-1]
            self.pp.setData(self.state)
            return True

        return False

    def __str__(self):
        bits = [self.state & i and "1" or "0" for i in CHANS]
        bits.reverse()  # Network byte order
        return "".join(bits)

    def __repr__(self):
        return "ParallelIO(%s)" % str(self)

CHAN1 = 1
CHAN2 = 2
CHAN3 = 4
CHAN4 = 8
CHAN5 = 16
CHAN6 = 32
CHAN7 = 64
CHAN8 = 128
CHANS = (CHAN1, CHAN2, CHAN3, CHAN4, CHAN5, CHAN6, CHAN7, CHAN8)

# vi:ai ts=4 sw=4 tw=0 et
