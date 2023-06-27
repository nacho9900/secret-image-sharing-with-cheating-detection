from .SISSImage import SISSImage


class BMPReader:
    @staticmethod
    def read(path: str, name: str) -> SISSImage:
        with open(path, 'rb') as f:
            bmp = f.read()

        # Check the signature
        if bmp[0:2] != b'BM':
            raise ValueError(f"El archivo {path} no es un archivo BMP válido")

        # file_size = read_le32(bmp, 2)
        pixels_offset = BMPReader.read_le32(bmp, 10)
        image_width = BMPReader.read_le32(bmp, 18)
        image_height = BMPReader.read_le32(bmp, 22)
        bits_per_pixel = BMPReader.read_le(bmp, 28)
        # This is shadow number in SISSImage
        bfReserved1 = BMPReader.read_le(bmp, 6)
        image_size = BMPReader.read_le32(bmp, 34)
        name = name

        raw_header = bmp[0:pixels_offset]

        if bits_per_pixel != 8:
            raise ValueError(f"El archivo BMP {path} debe tener 8 bits por pixel")

        return SISSImage(width=image_width, height=image_height, shadow_number=bfReserved1,
                         bytes_per_pixel=bits_per_pixel, pixels=bmp[pixels_offset:pixels_offset + image_size],
                         raw_header=raw_header, offset=pixels_offset, name=name)

    @staticmethod
    def read_le(file, offset: int) -> int:
        return int.from_bytes(file[offset:offset + 2], byteorder='little')

    @staticmethod
    def read_le32(file, offset: int) -> int:
        return int.from_bytes(file[offset:offset + 4], byteorder='little')
