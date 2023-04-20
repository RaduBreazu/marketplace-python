"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

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
        Thread.__init__(self, name = kwargs['name'])
        self.name = kwargs['name']
        self.ops = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        for elem in self.ops:
            cart_id = self.marketplace.new_cart()

            for dictionary in elem:
                for i in range(dictionary["quantity"]):
                    match (type):
                        case "add":
                            self.marketplace.add_to_cart(cart_id, dictionary["product"])
                        case "remove":
                            self.marketplace.remove_from_cart(cart_id, dictionary["product"])