import argparse
import os
from collections import defaultdict

from tools.images.BMPReader import BMPReader
from tools.images.Steganographer import Steganographer


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
        Steganographer.recover(images[0], k)


    except FileNotFoundError:
        print(f"El directorio {directory} no existe")
        return
    except ValueError as e:
        print(e)
        return


if __name__ == "__main__":
    CLI.main()
