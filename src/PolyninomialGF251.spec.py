from tools.math.PolynomialGF251 import PolynomialGF251

if __name__ == "__main__":
    poly = PolynomialGF251([(1, 5), (2, 9), (3, 7), (4, 244)])
    print(poly)
    poly = PolynomialGF251([(1, 8), (2, 17), (3, 32)])
    print(poly)
