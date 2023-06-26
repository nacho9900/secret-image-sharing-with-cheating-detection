from .GF251 import GF251


class PolynomialGF251:
    """
    Represent a Polynomial in GF(251).
    """

    def __init__(self, coefficients: list[int]):
        """
        :param coefficients: a list of coefficients of the polynomial in GF(251) sorted by degree.
        """
        # c0 + c1x + c2x^2 + ... + cnx^n
        self.coefficients = [GF251.convert_to_gf251(c) for c in coefficients]
        self.degree = len(coefficients) - 1

    @staticmethod
    def interpolate(points: list[tuple[int, int]]) -> 'PolynomialGF251':
        """
        Generate the coefficients of the polynomial using Gauss-Jordan elimination.
        :return: a list of coefficients of the polynomial in GF(251) sorted by degree.
        """

        # Sort the points by x coordinate
        points.sort(key=lambda punto: punto[0])

        # Separate the x and y coordinates
        xs, ys = map(list, zip(*points))

        # System size
        n = len(points)

        # Vandermonde matrix (A)
        A = []
        for x in xs:
            row = [1]
            for i in range(1, n):
                row.append(GF251.multiply(row[-1], x))
            A.append(row)

        # Gauss-Jordan
        for i in range(n):
            # Make sure the pivot is not 0
            if A[i][i] == 0:
                for j in range(i + 1, n):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]  # Swap rows
                        ys[i], ys[j] = ys[j], ys[i]  # Swap ys
                        break
                else:
                    raise ValueError("El sistema de ecuaciones no tiene solución única")

            # Make the pivot 1
            inv_diagonal = GF251.inverse(A[i][i])
            for j in range(i, n):
                A[i][j] = GF251.multiply(A[i][j], inv_diagonal)
            ys[i] = GF251.multiply(ys[i], inv_diagonal)

            # Make the rest of the column 0
            for j in range(n):
                if i != j:
                    factor = A[j][i]
                    for k in range(i, n):
                        A[j][k] = GF251.subtract(A[j][k], GF251.multiply(factor, A[i][k]))
                    ys[j] = GF251.subtract(ys[j], GF251.multiply(factor, ys[i]))

        # The coefficients are the values of ys after Gauss-Jordan
        # c0 + c1x + c2x^2 + ... + cnx^n
        return PolynomialGF251(ys)

    def evaluate(self, x: int) -> int:
        """
        Evaluate the polynomial at x.
        :param x: the x value to evaluate the polynomial at.
        :return: the y value of the polynomial at x.
        """
        y = 0
        for i in range(self.degree + 1):
            y = GF251.add(y, GF251.multiply(self.coefficients[i], pow(x, i, 251)))
        return y

    def __str__(self):
        polynomial = ""
        for c in range(self.degree + 1):
            if c == 0:
                polynomial += str(self.coefficients[c])
            else:
                polynomial += f" + {self.coefficients[c]}x^{c}"
        return polynomial
