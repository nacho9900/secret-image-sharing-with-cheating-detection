class SISSImage:
    """
    SISSImage is a class that represents an image in the Secret Image Sharing Scheme.
    """

    def __init__(self, width: int, height: int, shadow_number: int, bytes_per_pixel: int, pixels: bytes,
                 raw_header: bytes, offset: int):
        self.width = width
        self.height = height
        self.shadow_number = shadow_number
        self.bytes_per_pixel = bytes_per_pixel
        self.pixels = pixels
        self.raw_header = raw_header
        self.offset = offset

    def save(self, file_name):
        with open(file_name, 'wb') as f:
            # Write the raw_header
            f.write(self.raw_header)

            # Write out the pixel data
            f.write(self.pixels)
