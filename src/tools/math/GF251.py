class GF251:
    INVERSES = [pow(i, 251 - 2, 251) for i in range(1, 251)]

    @staticmethod
    def divide(a: int, b: int):
        return GF251.multiply(a, GF251.inverse(b))

    @staticmethod
    def inverse(a: int):
        return GF251.INVERSES[a - 1]

    @staticmethod
    def multiply(a: int, b: int):
        return (a * b) % 251

    @staticmethod
    def add(a: int, b: int):
        return (a + b) % 251

    @staticmethod
    def subtract(a: int, b: int):
        return (a - b) % 251

    @staticmethod
    def convert_to_gf251(a: int):
        return a % 251
