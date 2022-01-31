class Person:
    def __init__(self, addr, client) -> None:
        self.addr = addr
        self.client = client
        self.name = None

    def set_name(self, name):
        self.name = name

    def __repr__(self) -> str:
        return f"Person{self.addr}, {self.name}"