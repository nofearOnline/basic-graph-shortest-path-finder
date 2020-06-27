from queue import Queue

__author__ = "Or Navon"

MODE = "PROD"

class Name:
    """
    This object contains the person name(first and last)
    with default name as name last name
    """

    def __init__(self, first = "Name", last = "Last Name"):
        self.first_name = first
        self.last_name = last

    def __eq__(self, other):
        """
        checks if first and last name are equal
        """
        return self.__dict__ == other.__dict__

    def __str__(self):
        """
        for debug mode.
        """
        return self.first_name + ", " + self.last_name
        

class Address:
    """
    This object contains the person's address(city and street)
    with default address City Street
    """

    def __init__(self, city = "City", street = "Street"):
        self.city = city
        self.street = street

    def __eq__(self, other):
        """
        checks if first and last name are equal
        """
        return self.__dict__ == other.__dict__

    def __str__(self):
        """
        for debug mode.
        """
        return self.city + ", " + self.street

        
class Person:
    """
    This object contains the person name and address.
    """

    def __init__(self, name = Name(), address = Address()):
        self.name = name
        self.address = address

    def __str__(self):
        """
        for debug mode.
        """
        return "[" + str(self.name) + ": " + str(self.address) + "]"

    def __eq__(self, other):
        return self.name == other.name and self.address == other.address


class PersonNotExist(Exception):
    """
    This is an exception that declares that the person do not exist.
    """
    pass 

class ConnectionNotExist(Exception):
    """
    This is an exception that declares that there is no path between two persons.
    """
    pass 


class PersonNode:
    """
        This object represent a node in the graph.
        PersonNode contain the associate person object and the connections he has.
        connections is a PersonNode list of all the PersonNode people
        with the same full name or full address.
    """

    def __init__(self, person):
        self.person = person
        self.connections = []


class ConnectionMap:
    
    def __init__(self, people):
        """
            get people which is a list of Person objects and build node graph from the list.
            graph beeing build by the connections term(see the PersonNode docs).
        """

        assert isinstance(people, list), "Wrong input was given to connection map"

        # check that the list of connection is a list of Persons objects
        for human in people:
            assert isinstance(human, type(Person())), "Wrong input was given to connection map, "\
                                                      + str(type(Person())) + " expected, "\
                                                      + str(type(human)) + " given."

        self.node_list = []
        """
            building the graph
        """
        for person in people:
            this_node = PersonNode(person)
            
            for node in self.node_list:
                if this_node.person.name == node.person.name or \
                   this_node.person.address == node.person.address:
                    
                    this_node.connections.append(node)
                    node.connections.append(this_node)

            self.node_list.append(this_node)

    def find_min_relation_level(self, person_a, person_b):
        """
            This function is the main aim of this module.
            it finds the shortest path from one node to another in the graph.
        """
        try:
            node_a = self.find_node(person_a)
        except(PersonNotExist):
            print("this person does not exist in the persons list")

        order_queue = Queue()
        checked_nodes = []

        order_queue.put([node_a, 0])

        while not order_queue.empty():
            current_node, distance = order_queue.get()
            if MODE == "DEBUG":
                print("cycle")
            if current_node.person == person_b:
                if MODE == "DEBUG":
                    print("found")
                return distance
            else:
                if current_node in checked_nodes:
                    continue
                else:
                    checked_nodes.append(current_node)
                    if MODE == "DEBUG":
                        print(current_node.person)
                    distance += 1
                    for node in current_node.connections:
                        order_queue.put([node, distance])

        raise ConnectionNotExist
                
            
    def print_connections(self):
        """
            This function prints all the connection of certain node
        """
        for node in self.node_list:
            print(str(node.person) + str(node.connections))


    def find_node(self, person):
        """
            This function gets person object and returns its associated node in the graph
        """
        for node in self.node_list:
            if node.person == person:
                return node

        raise PersonNotExist


def main():
    unit_test()
    


def unit_test():
    print("unit test start")
    a = Person()
    b = Person(Name(), Address("c","d"))
    b2 = Person(Name("Tom", "Riddle"), Address("uk","ue"))
    b3 = Person(Name("Mishu", "Mashu"), Address("c","d"))
    b4 = Person(Name("Mishu", "Mashu"), Address("uk","ue"))
    b5 = Person(Name(), Address("uk","ue"))
    b6 = Person(Name("unconnected", "alone"), Address("For","Ever"))
    c = ConnectionMap([a, b, b2, b3, b4])
    c2 = ConnectionMap([a, b, b2, b3, b4, b5, Person()])
    try:
        print("The distance between them is: " + str(c.find_min_relation_level(a, b3)))
    except (ConnectionNotExist):
        print ("there is no connection between the two")


if __name__ == "__main__": 
    main()