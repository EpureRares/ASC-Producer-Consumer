"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Lock, Event, RLock

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
        self.start_work = Event()
        self.registration_lock = Lock()
        self.create_cart_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.registration_lock:
            producer_id = self.number_producers
            self.number_producers += 1
            self.available_products.append([])
            self.product_locks.append(Lock())

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

        with self.product_locks[prod_id]:
            if len(var) < self.queue_size_per_producer:
                self.available_products[prod_id].append((product, RLock(), None))
            else:
                is_queue_full = True

        return not is_queue_full

    def new_cart(self):
        """
        Creates a new cart for the consumer
        :returns an int representing the cart_id
        """
        with self.create_cart_lock:
            cart_id = self.actual_consumer
            self.actual_consumer += 1

            if self.actual_consumer == 1:
                self.start_work.set()

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

        for i in range(len(self.available_products)):
            with self.product_locks[i]:
                for j in range(len(self.available_products[i])):
                    (product_type, lock, cart) = self.available_products[i][j]
                    if lock.acquire(blocking=False) and product_type == product and cart is None:
                        lock.acquire(blocking=True)
                        self.available_products[i][j] = (product_type, lock, cart_id)
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

        for i in range(len(self.available_products)):
            for j in range(len(self.available_products[i])):
                (product_type, lock, cart) = self.available_products[i][j]

                if lock.acquire(blocking=False) and product_type == product and cart == cart_id:
                    lock.acquire(blocking=True)
                    self.available_products[i][j] = (product_type, RLock(), None)
                    lock.release()
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
                    (product, lock, cart) = self.available_products[i][j]

                    if cart == cart_id:
                        list_bought.append(product)
                        self.available_products[i].pop(j)

        return list_bought
