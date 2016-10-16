import math
import bitstring
from itertools import product
from rflib import *

FREQ = 0 #frequency
DRATE = 0 #baud, or data rate
NUM_TIMES = 0 #num times to send transmit per code

def configure(d):
    try:
        d.setMdmModulation(MOD_ASK_OOK)
        d.setFreq(FREQ)
        d.setMdmSyncMode(0)
        d.setMdmDRate(DRATE)
        d.setMaxPower()
    except Exception, e:
        d.setModeIDLE()
        sys.exit("Error configuring: %s" % str(e))

def convert_pwm(bin_str):
    low = '1000'
    high = '1110'
    pwm_str = ''
    for c in bin_str:
        if c == '1':
            pwm_str += high
        else:
            pwm_str += low
    return pwm_str

def transmit(d, pwm_str):
    pwm_ook = bitstring.BitArray(bin=pwm_str).tobytes()
    count = 1
    for i in range(NUM_TIMES):
        print "trasmitting %s" % pwm_str
        try:
            d.makePktFLEN(len(pwm_ook))
            d.RFxmit(pwm_ook)
        except Exception, e:
            d.setModeIDLE()
            sys.exit("Error trasmitting: %s" % str(e))
        
d = RfCat()
configure(d)

chars = '01'
to_attempt = product(chars, repeat=10)
count = 0
for attempt in to_attempt:
    bin_str = ''.join(attempt)
    pwm_str = convert_pwm(bin_str)
    transmit(d, pwm_str)
    count += 1

print "Transmitted %i values" % count
d.setModeIDLE()
