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
        self.id = None
        self.name = kwargs['name']
        self.products = products
        self.surplus_product = (None, None)
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

    def run(self):

        self.id = self.marketplace.register_producer()
        self.marketplace.start_work.wait()
        index = 0
        while len(self.marketplace.consumers) > 0:
            index %= len(self.products)

            print(index)
            (product, quantity, delay) = self.products[index]

            while quantity > 0 and len(self.marketplace.consumers) > 0:
                if self.marketplace.publish(self.id, product):
                    quantity -= 1
                else:
                    time.sleep(self.republish_wait_time)

            index += 1
