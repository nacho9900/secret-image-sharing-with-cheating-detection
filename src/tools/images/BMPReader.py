from .SISSImage import SISSImage

class BMPReader:
    @staticmethod
    def read(path: str) -> SISSImage:
        with open(path, 'rb') as f:
            bmp = f.read()

        # Check the signature
        if bmp[0:2] != b'BM':
            raise ValueError('Not a bitmap file')

        # file_size = read_le32(bmp, 2)
        pixels_offset = BMPReader.read_le32(bmp, 10)
        image_width = BMPReader.read_le32(bmp, 18)
        image_height = BMPReader.read_le32(bmp, 22)
        bits_per_pixel = BMPReader.read_le(bmp, 28)
        # This is shadow number in SISSImage
        bfReserved1 = BMPReader.read_le(bmp, 6)
        image_size = BMPReader.read_le32(bmp, 34)

        raw_header = bmp[0:pixels_offset]

        if bits_per_pixel != 8:
            raise ValueError('Only 8-bit bitmaps are supported')

        return SISSImage(width=image_width, height=image_height, shadow_number=bfReserved1,
                         bytes_per_pixel=bits_per_pixel, pixels=bmp[pixels_offset:pixels_offset + image_size],
                         raw_header=raw_header)

    @staticmethod
    def read_le(file, offset: int) -> int:
        return int.from_bytes(file[offset:offset + 2], byteorder='little')

    @staticmethod
    def read_le32(file, offset: int) -> int:
        return int.from_bytes(file[offset:offset + 4], byteorder='little')

# image = BMPReader.read('src/tools/images/data/Albertshare.bmp')
#
# print(f"width: {image.width}")
# print(f"height: {image.height}")
# print(f"ri: {image.ri}")
# print(f"bytes_per_pixel: {image.bytes_per_pixel}")
# print(f"pixels: {image.pixels}")
# print(f"raw_header: {image.raw_header}")
