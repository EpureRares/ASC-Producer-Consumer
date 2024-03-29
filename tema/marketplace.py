"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Lock, RLock


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
        self.number_producers = 0
        self.actual_consumer = 0
        self.available_products = []
        self.consumers = []
        self.product_locks = []
        self.registration_lock = [Lock(), Lock()]

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.registration_lock[0]:
            producer_id = self.number_producers
            self.number_producers += 1
            self.available_products.append([])
            self.product_locks.append(RLock())

        return str(producer_id)

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        prod_id = int(producer_id)
        is_queue_full = False
        var = (self.available_products[prod_id])

        """
        producatorul adauga elemente doar in coada sa 
        prin variabila is_queue_full se verifica daca
        s-a ajuns la dimensiunea maxima a cozii
        """
        with self.product_locks[prod_id]:
            if len(var) < self.queue_size_per_producer:
                self.available_products[prod_id].append((product, None))
            else:
                is_queue_full = True

        return not is_queue_full

    def new_cart(self):
        """
        Creates a new cart for the consumer
        :returns an int representing the cart_id
        """
        with self.registration_lock[1]:
            cart_id = self.actual_consumer
            self.actual_consumer += 1

        self.consumers.append(cart_id)

        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """

        """
        consumatorul cauta in toate cozile pana cand gaseste elementelul pe care le cauta
        doar un consumator sau doar un producator are acces la un moment dat 
        la o anumita coada
        pentru a marca un element intr-un cos de cumparaturi se adauga id-ul cosului langa
        produsul respectiv
        """
        for i in range(len(self.available_products)):
            with self.product_locks[i]:

                for j in range(len(self.available_products[i])):
                    (product_type, cart) = self.available_products[i][j]

                    if product_type == product and cart is None:
                        self.available_products[i][j] = (product_type, cart_id)
                        return True

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        """
        pentru a elimina un element din cos se cauta in toate cozile elementul
        respectiv care are asociat id-ul cosului de cumparaturi
        """
        for i in range(len(self.available_products)):
            with self.product_locks[i]:
                for j in range(len(self.available_products[i])):
                    (product_type, cart) = self.available_products[i][j]

                    if product_type == product and cart == cart_id:
                        self.available_products[i][j] = (product_type, None)
                        return

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        list_bought = []

        for i in range(len(self.available_products)):
            with self.product_locks[i]:
                for j in range(len(self.available_products[i]) - 1, -1, -1):
                    (product, cart) = self.available_products[i][j]

                    if cart == cart_id:
                        list_bought.append(product)
                        self.available_products[i].pop(j)

        return list_bought
