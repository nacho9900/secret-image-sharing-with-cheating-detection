class SISSImage:
    """
    SISSImage is a class that represents an image in the Secret Image Sharing Scheme.
    """

    def __init__(self, width: int, height: int, shadow_number: int, bytes_per_pixel: int, pixels: bytes,
                 raw_header: bytes):
        self.width = width
        self.height = height
        self.ri = shadow_number
        self.bytes_per_pixel = bytes_per_pixel
        self.pixels = pixels
        self.raw_header = raw_header
