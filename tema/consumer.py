"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time

name = 'name'
add_command = 'add'
remove_command = 'remove'
field_type = 'type'
field_product = 'product'
field_quantity = 'quantity'


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
        self.name = kwargs[name]
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        for cart in self.carts:
            id_cart = self.marketplace.new_cart()
            for action in cart:
                product = action[field_product]
                quantity = action[field_quantity]

                """
                se executa un anumit tip de instructiune
                din lista de cumparaturi, iar in cazul unei operatii 
                de adaugare elemetele sunt adaugate unu cate unu
                """
                if action[field_type] == add_command:
                    while quantity > 0:
                        if self.marketplace.add_to_cart(id_cart, product):
                            quantity -= 1
                        else:
                            time.sleep(self.retry_wait_time)

                elif action[field_type] == remove_command:
                    while quantity > 0:
                        self.marketplace.remove_from_cart(id_cart, product)
                        quantity -= 1

            """
            in cazul in care s-au consumat toate elementele dintr-o
            lista de cumparaturi se elimina cosul din marketplace
            si se afiseaza toate elementele consumate
            """
            products = self.marketplace.place_order(id_cart)
            for product in products:
                command = self.name + " bought " + str(product)
                print(command, end='\n')

            self.marketplace.consumers.remove(id_cart)
