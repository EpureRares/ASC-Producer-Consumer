"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


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
        super().__init__()
        self.name = kwargs['name']
        self.id_cart = None
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        self.id_cart = self.marketplace.new_cart()

        for cart in self.carts:
            for action in cart:
                product = action['product']
                quantity = action['quantity']

                if action['type'] == 'add':
                    while quantity > 0:
                        if self.marketplace.add_to_cart(self.id_cart, product):
                            quantity -= 1
                        else:
                            time.sleep(self.retry_wait_time)

                elif action['type'] == 'remove':
                    while quantity > 0:
                        self.marketplace.remove_from_cart(self.id_cart, product)
                        quantity -= 1

            products = self.marketplace.place_order(self.id_cart)
            for product in products:
                command = self.name + " bought " + str(product)
                print(command, end='\n')

        self.marketplace.consumers.remove(self.id_cart)

