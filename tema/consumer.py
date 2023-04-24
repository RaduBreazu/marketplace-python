"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread, Lock
from time import sleep

class Consumer(Thread):
    """
    Class that represents a consumer.
    """
    print_lock = Lock() # the consumers must share the same lock

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.name = kwargs['name']
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        for cart in self.carts:
            cart_id = self.marketplace.new_cart()

            # the cart represents a sequence of actions to be executed
            for action in cart:
                act_type = action["type"]
                quantity = action["quantity"]
                prod = action["product"]

                if act_type == "add":
                    for i in range(quantity):
                        # try adding the product to cart until it becomes available
                        while self.marketplace.add_to_cart(cart_id, prod) is False:
                            sleep(self.retry_wait_time)
                elif act_type == "remove":
                    for i in range(quantity):
                        self.marketplace.remove_from_cart(cart_id, prod)

            # place order and print every product from cart numbered cart_id
            products = self.marketplace.place_order(cart_id)

            with Consumer.print_lock:
                for prod in products:
                    print(self.name + " bought " + str(prod))
