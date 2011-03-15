from ticketing import conf
from django.test import TestCase
from ticketing.models import get_ticket

import logging
log = logging.getLogger(__name__)

class TicketingTest(TestCase):
    
    def test_get_ticket(self):
        t = get_ticket()
        self.assertTrue(t)
        self.assertTrue(t > 0, "Ticket %s is not greater than zero!" % t)
    
    def test_get_tickets(self):
        t0 = get_ticket()
        self.assertTrue(t0 > 0, "Ticket %s is not greater than zero!" % t0)
        
        t1 = get_ticket()
        self.assertTrue(t1 > 0, "Ticket %s is not greater than zero!" % t1)
        self.assertTrue(t1 > t0, "Ticket %s is not greater than ticket %s!" % (t1, t0))
    
    def test_get_n_tickets(self):
        import random
        n = int((random.random() + 1) * 100)
        
        t0 = get_ticket()
        self.assertTrue(t0 > 0, "Ticket %s is not greater than zero!" % t0)
        
        for i in range(0, n):
            t1 = get_ticket()
            self.assertTrue(t1 > 0, "Ticket %s is not greater than zero!" % t1)
            self.assertTrue(t1 > t0, "Ticket %s is not greater than ticket %s!" % (t1, t0))
            t0 = t1
    
    def test_get_from_sequence(self):
        self.assertTrue(len(conf.SEQUENCES) > 1, "There aren't multiple sequences to test! - %s" % str(conf.SEQUENCES))
        last_seq = 2
        for seq in conf.SEQUENCES:
            t0 = get_ticket(seq)
            self.assertTrue(t0 > 0, "Ticket %s [for sequence %s] is not greater than zero!" % (t0, seq))
            self.assertTrue(t0 < last_seq, "Ticket %s [for sequence %s] is not less than previous sequence %s!" % (t0, seq, last_seq))
            for i in range(0, 10):
                t1 = get_ticket(seq)
                self.assertTrue(t1 > 0, "Ticket %s [for sequence %s] is not greater than zero!" % (t1, seq))
                self.assertTrue(t1 > t0, "Ticket %s [for sequence %s] is not greater than ticket %s!" % (t1, seq, t0))
                t0 = t1
            last_seq = t0
    
    def test_get_sequences_in_order(self):
        self.assertTrue(len(conf.SEQUENCES) > 1, "There aren't multiple sequences to test! - %s" % str(conf.SEQUENCES))
        for i in range(1, 10):
            for seq in conf.SEQUENCES:
                t = get_ticket(seq)
                self.assertTrue(t > 0, "Ticket %s [for sequence %s] is not greater than zero!" % (t, seq))
                self.assertTrue(t == i, "Ticket %s [for sequence %s] is not the expected value of %s!" % (t, seq, i))
    
    def test_bad_sequence(self):
        from ticketing.exceptions import BadSequenceName
        self.assertRaises(BadSequenceName, get_ticket, ('bad_sequence', ))
    


