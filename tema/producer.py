"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Thread


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
        super().__init__()
        self.daemon = kwargs['daemon']
        self.name = kwargs['name']
        self.products = products
        self.surplus_product = (None, None)
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

    def run(self):

        id_producer = self.marketplace.register_producer()

        index = 0
        while self.daemon:
            index %= len(self.products)

            (product, quantity, _) = self.products[index]

            while quantity > 0:
                if self.marketplace.publish(id_producer, product):
                    quantity -= 1
                else:
                    time.sleep(self.republish_wait_time)

            index += 1
