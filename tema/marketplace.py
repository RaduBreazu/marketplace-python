"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from functools import reduce

from threading import Lock
from copy import deepcopy


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    curr_prod_id = 0
    curr_cons_id = 0

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer

        self.lock_producer_id = Lock()
        self.lock_consumer_id = Lock()
        self.lock_data_structures = Lock()
        self.available_products = {} # dictionary of the form (producer_id : [products])
        self.carts = {} # dictionary of the form (cart_id : (producer_id : [products]))

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.lock_producer_id:
            Marketplace.curr_prod_id = Marketplace.curr_prod_id + 1
            self.available_products[Marketplace.curr_prod_id] = []
            return Marketplace.curr_prod_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        with self.lock_data_structures:
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
            Marketplace.curr_cons_id = Marketplace.curr_cons_id + 1
            self.carts[Marketplace.curr_cons_id] = {}
            return Marketplace.curr_cons_id
            

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        with self.lock_data_structures:
            aux = deepcopy(self.available_products)
            for i in aux.keys():
                if product in aux[i] and product in self.available_products[i]:
                    self.available_products[i].remove(product)
                    try:
                        self.carts[cart_id][i].append(product)
                    except KeyError:
                        self.carts[cart_id][i] = [product]
                    # print("Consumer " + str(cart_id) + " bought " + str(product))
                    # print("carts: " + str(self.carts))
                    return True
        
        # the product has not been found
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        with self.lock_data_structures:
            aux = deepcopy(self.carts[cart_id])
            for i in aux.keys():
                if product in aux[i]:
                    # we do not care about the number of products already published by the producer
                    self.carts[cart_id][i].remove(product)
                    self.available_products[i].append(product)
                    # print("Consumer " + str(cart_id) + " quit product " + str(product))
                    # print("carts: " + str(self.carts))

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        lst = reduce(lambda acc, elem: acc + elem, list(self.carts[cart_id].values()))
        self.carts.__delitem__(cart_id)  # delete the cart associated with cart_id
        return lst
