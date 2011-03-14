from django.test import TestCase
from ticketing.models import Ticketing

import logging
log = logging.getLogger(__name__)

class TicketingTest(TestCase):
    
    def test_create(self):
        t = Ticketing.objects.create()
        self.assertTrue(t.id)
        self.assertTrue(t.ticket)
        self.assertTrue(t.stub)
        self.assertTrue(t.id == t.ticket)
    
    def test_create_two(self):
        t0 = Ticketing.objects.create()
        self.assertTrue(t0.ticket > 0, "Ticket %s is not greater than zero!" % t0)
        
        t1 = Ticketing.objects.create()
        self.assertTrue(t1.ticket > 0, "Ticket %s is not greater than zero!" % t1)
        self.assertTrue(t1.ticket > t0.ticket, "Ticket %s is not greater than ticket %s!" % (t1, t0))
    
    def test_create_n(self):
        import random
        n = int((random.random() + 1) * 100)
        
        t0 = Ticketing.objects.create()
        self.assertTrue(t0.ticket > 0, "Ticket %s is not greater than zero!" % t0)
        
        for i in range(0, n):
            t1 = Ticketing.objects.create()
            self.assertTrue(t1.ticket > 0, "Ticket %s is not greater than zero!" % t1)
            self.assertTrue(t1.ticket > t0.ticket, "Ticket %s is not greater than ticket %s!" % (t1, t0))
            t0 = t1
    
    def test_get_tickets(self):
        t0 = Ticketing.objects.get_ticket()
        self.assertTrue(t0, "Ticket %s is does not evaulate to true!" % t0)
        self.assertTrue(t0 > 0, "Ticket %s is not greater than zero!" % t0)
        
        t1 = Ticketing.objects.get_ticket()
        self.assertTrue(t1, "Ticket %s is does not evaulate to true!" % t1)
        self.assertTrue(t1 > 0, "Ticket %s is not greater than zero!" % t1)
        self.assertTrue(t1 > t0, "Ticket %s is not greater than Ticket %s!" % (t1, t0))
    
    def test_get_n(self):
        import random
        n = int((random.random() + 1) * 100)
        
        t0 = Ticketing.objects.get_ticket()
        self.assertTrue(t0 > 0, "Ticket %s is not greater than zero!" % t0)
        
        for i in range(0, n):
            t1 = Ticketing.objects.get_ticket()
            self.assertTrue(t1 > 0, "Ticket %s is not greater than zero!" % t1)
            self.assertTrue(t1 > t0, "Ticket %s is not greater than ticket %s!" % (t1, t0))
            t0 = t1
    
    def test_get_ticket_shortcut(self):
        from ticketing.models import get_ticket
        t0 = get_ticket()
        self.assertTrue(t0, "Ticket %s is does not evaulate to true!" % t0)
        self.assertTrue(t0 > 0, "Ticket %s is not greater than zero!" % t0)
        
        t1 = get_ticket()
        self.assertTrue(t1, "Ticket %s is does not evaulate to true!" % t1)
        self.assertTrue(t1 > 0, "Ticket %s is not greater than zero!" % t1)
        self.assertTrue(t1 > t0, "Ticket %s is not greater than Ticket %s!" % (t1, t0))
    
    def test_get_ticket_shortcut_n_times(self):
        import random
        n = int((random.random() + 1) * 100)
        
        from ticketing.models import get_ticket
        
        t0 = get_ticket()
        self.assertTrue(t0 > 0, "Ticket %s is not greater than zero!" % t0)
        
        for i in range(0, n):
            t1 = get_ticket()
            self.assertTrue(t1 > 0, "Ticket %s is not greater than zero!" % t1)
            self.assertTrue(t1 > t0, "Ticket %s is not greater than ticket %s!" % (t1, t0))
            t0 = t1
    

