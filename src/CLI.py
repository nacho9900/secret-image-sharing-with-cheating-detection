import argparse
import os
from collections import defaultdict

from tools.images.BMPReader import BMPReader
from tools.images.Steganographer import Steganographer
from tools.math.PolynomialGF251 import PolynomialGF251
from tools.math.GF251 import GF251
from tools.images.SISSImage import SISSImage


class CLI:
    @staticmethod
    def main():
        parser = argparse.ArgumentParser(description='Secret Image Sharing CLI')
        parser.add_argument("operation", choices=["d", "r"],
                            help="Operación a realizar: 'd' para distribuir, 'r' para recuperar")
        parser.add_argument("file", help="Nombre del archivo")
        parser.add_argument("k", type=int, help="Indicar k del esquema (k,n)")
        parser.add_argument("directory", help="Directorio de las imágenes")
        args = parser.parse_args()

        if args.k < 3 or args.k > 8:
            print("k debe estar entre 3 y 8")
            return

        if args.operation == "d":
            distribute(args.file, args.k, args.directory)
        else:
            recover(args.file, args.k, args.directory)


def distribute(file, k, directory):
    print(f"Distribuyendo {file} con k {k} en el directorio {directory}")

    try:
        # Read the image
        image = BMPReader.read(file)
        data = image.pixels

        # Block size in pixels
        block_size = (2 * k) - 2

        # Split the image into blocks Bi - i e [1, t]
        blocks = [data[i:i + block_size] for i in range(0, len(data), block_size)]




    except FileNotFoundError:
        print(f"Archivo {file} no encontrado")
        return


def recover(file, k, directory):
    print(f"Recuperando {file} con k {k} en el directorio {directory}")
    image_group = defaultdict(list)
    group_key = None
    try:
        bmp_files = [f for f in os.listdir(directory) if f.endswith('.bmp')]
        # With these files, we need to gather k of them with same width and height
        # We will use BMPReader.read to read the images
        # We will use SISSImage.width and SISSImage.height to check if the images have the same width and height
        for bmp_file in bmp_files:
            image = BMPReader.read(os.path.join(directory, bmp_file))
            key = f"{image.width}x{image.height}"
            image_group[key].append(image)
            if len(image_group[key]) == k:
                group_key = key
                print(f"Found {k} images with width {image.width} and height {image.height}")
                break

        # If we can't find K images with same width and height, then we can't recover the secret image
        # So we need to raise an error
        if group_key is None:
            raise ValueError(f"Couldn't find {k} images with same width and height")

        images = image_group[group_key]

        sub_shadows = []
        for i in range(k):
            sub_shadows.extend(Steganographer.recover_sub_shadows(images[i], k))

        # Group the sub shadows by i
        sub_shadows_i = defaultdict(list)
        for sub_shadow in sub_shadows:
            sub_shadows_i[sub_shadow.i].append(sub_shadow)

        # Build functions
        f_i_list = defaultdict(PolynomialGF251)
        g_i_list = defaultdict(PolynomialGF251)
        for i, sub_shadows_list in sub_shadows_i.items():
            f_i_list[i] = PolynomialGF251.interpolate([(sub_shadow.j, sub_shadow.m) for sub_shadow in sub_shadows_list])
            g_i_list[i] = PolynomialGF251.interpolate([(sub_shadow.j, sub_shadow.d) for sub_shadow in sub_shadows_list])

        # Evaluate if there fake shadows
        secret = recover_secret(f_i_list, g_i_list)
        image = images[0]
        image.save(os.path.join(directory, f"recovered_{file}"))
        image.pixels = bytes(secret)
        image.save(os.path.join(directory, file))

    except FileNotFoundError:
        print(f"El directorio {directory} no existe")
        return
    except ValueError as e:
        print(e)
        return


def recover_secret(f_i_list: dict[int, PolynomialGF251], g_i_list: dict[int, PolynomialGF251]) -> list[int]:
    secret = []
    for i, f_i, g_i in zip(f_i_list.keys(), f_i_list.values(), g_i_list.values()):
        if not satisfies_ri(f_i.coefficients[0], g_i.coefficients[0]):
            raise ValueError(f"La sombra {i} es falsa")
        if not satisfies_ri(f_i.coefficients[1], g_i.coefficients[1]):
            raise ValueError(f"La sombra {i} es falsa")
        secret.extend(f_i.coefficients + g_i.coefficients[2:])
    return secret


def satisfies_ri(a: int, b: int) -> bool:
    for ri in range(1, 251):
        if GF251.add(GF251.multiply(a, ri), b) == GF251.convert_to_gf251(0):
            return True
    return False


if __name__ == "__main__":
    CLI.main()
