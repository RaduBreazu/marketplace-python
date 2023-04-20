"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

# The stream of natural numbers
def naturals(n):
    while True:
        n = n + 1
        yield n


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    available_products = {} # dictionary of the form (producer_id : [products])
    carts = {} # dictionary of the form (cart_id : (producer_id : product))

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        new_id = 0

        while True:
            new_id = next(naturals(new_id))
            if new_id not in Marketplace.available_products.keys():
                Marketplace.available_products[new_id] = []
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
        if len(Marketplace.available_products[producer_id]) >= self.queue_size_per_producer:
            return False
        Marketplace.available_products[producer_id].append(product)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        new_id = 0

        while True:
            new_id = next(naturals(new_id))
            if new_id not in Marketplace.carts.keys():
                Marketplace.carts[new_id] = {}
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
        for i in Marketplace.available_products.keys():
            if product in Marketplace.available_products[i]:
                Marketplace.available_products[i].remove(product)
                Marketplace.carts[cart_id].append({"producer_id" : i, "product": product})
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
        for i in Marketplace.carts[cart_id].keys():
            if Marketplace.carts[cart_id][i] == product:
                # we do not care about the number of products already published by the producer
                Marketplace.carts[cart_id].remove(product)
                Marketplace.available_products[i].append(product)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        lst = Marketplace.carts[cart_id]
        Marketplace.carts.__delitem__(cart_id)  # delete the cart associated with cart_id
        return lst
