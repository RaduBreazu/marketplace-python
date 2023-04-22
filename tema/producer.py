"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs) # de testat fara daemon = 
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

    def run(self):
        id = self.marketplace.register_producer()

        while True:
            for (product, quantity, time) in self.products:
                sleep(time)
                for i in range(quantity):
                    while self.marketplace.publish(id, product) is False:
                        sleep(self.republish_wait_time)
                    # print("Producer " + str(id) + " published " + str(product))
                    # print(str(id) + ": " + str(self.marketplace.available_products[id]))
