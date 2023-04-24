"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from functools import reduce

from threading import Lock
from copy import deepcopy

import logging
import logging.handlers
import time

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer

        # Synchronization variables
        self.lock_producer_id = Lock()
        self.lock_consumer_id = Lock()
        self.lock_add_products = Lock()
        self.lock_remove_products = Lock()

        # Data structures to store the products
        self.available_products = {} # dictionary of the form (producer_id : [products])
        self.carts = {} # dictionary of the form (cart_id : (producer_id : [products]))

        # Initialize logging
        self.logger = logging.getLogger("logger")
        self.logger.setLevel(logging.INFO)
        self.handler = logging.handlers.RotatingFileHandler("marketplace.log",
                                                            maxBytes=2**24, # 16 MB
                                                            backupCount=20)
        self.handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter) # add formatter to handler
        logging.Formatter.converter = time.gmtime # use GMT time for logging
        self.logger.addHandler(self.handler) # add handler to logger


    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.lock_producer_id:
            self.logger.info("Entered register_producer()")

            new_id = 0
            while True:
                new_id = new_id + 1
                if new_id not in list(self.available_products.keys()):
                    self.available_products[new_id] = []
                    self.logger.info("Allocated ID %d for new producer", new_id)
                    return new_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        with self.lock_add_products:
            log_info = "Entered publish() with producer_id = %d and product = %s"
            self.logger.info(log_info, producer_id, str(product))

            if len(self.available_products[producer_id]) >= self.queue_size_per_producer:
                return False
            self.available_products[producer_id].append(product)
            return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.lock_consumer_id:
            self.logger.info("Entered new_cart()")

            new_id = 0
            while True:
                new_id = new_id + 1
                if new_id not in list(self.carts.keys()):
                    self.carts[new_id] = {}
                    self.logger.info("Allocated ID %d for new cart", new_id)
                    return new_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        with self.lock_remove_products:
            log_info = "Entered add_to_cart() with cart_id = %d and product = %s"
            self.logger.info(log_info, cart_id, str(product))

            # we cannot iterate over self.available_products, since it changes during the loop
            aux = deepcopy(self.available_products)
            for i in aux.keys():
                # try to find the product in one of the producers' queues
                if product in aux[i] and product in self.available_products[i]:
                    self.available_products[i].remove(product)
                    try:
                        self.carts[cart_id][i].append(product)
                    except KeyError:
                        self.carts[cart_id][i] = [product]

                    self.logger.info("Added %s to cart %d", str(product), cart_id)
                    return True

        # the product has not been found
        self.logger.info("Could not add %s to cart %d", str(product), cart_id)
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        with self.lock_add_products:
            log_info = "Entered add_to_cart() with cart_id = %d and product = %s"
            self.logger.info(log_info, cart_id, str(product))

            aux = deepcopy(self.carts[cart_id])
            for i in aux.keys():
                # find the consumer's product (it must exist in the cart)
                if product in aux[i]:
                    # even if producer's queue is full, we must insert the consumer's product
                    self.carts[cart_id][i].remove(product)
                    self.available_products[i].append(product)

                    self.logger.info("Removed %s from cart %d", str(product), cart_id)
                    return

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        self.logger.info("Entered place_order() with cart_id = %d", cart_id)

        lst = reduce(lambda acc, elem: acc + elem, list(self.carts[cart_id].values()))
        del self.carts[cart_id]  # delete the cart associated with cart_id

        self.logger.info("Returned cart: %s", str(lst))
        return lst
