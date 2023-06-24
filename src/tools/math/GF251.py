class GF251:
    @staticmethod
    def divide(a: int, b: int):
        return GF251.multiply(a, GF251.inverse(b))

    @staticmethod
    def inverse(a: int):
        return pow(a, 251 - 2, 251)

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
