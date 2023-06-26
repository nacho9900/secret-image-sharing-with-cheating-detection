from .SISSImage import SISSImage
from ..math.GF251 import GF251


class SubShadow:
    """
    Represent each v_j,i = (m_j,i, d_j,i) in the SIS scheme.
    """

    def __init__(self, m: int, d: int, i: int, j: int):
        # fi(j)
        self.m = m
        # gi(j)
        self.d = d

        # Block number
        self.i = i
        # Shadow Number
        self.j = j

    def __str__(self):
        return f"SubShadow(m={self.m}, d={self.d})"


class Steganographer:
    @staticmethod
    def recover_sub_shadows(image: SISSImage, k: int):
        pixels_amount = image.width * image.height

        # The sub shadow amount is the same as block amount
        sub_shadows_amount = pixels_amount // ((2 * k) - 2)

        # Image pixels
        pixels = image.pixels

        # How many less significant bits are used to store a part of sub shadow
        lsb = 4 if k < 5 else 2

        # Sub shadows parts (A sub shadow is composed of m and d -> 2 bytes)
        ss_parts_amount = (image.bytes_per_pixel * 2) // lsb

        sub_shadows = []

        mask = 0b1111 if k < 5 else 0b11

        for sb_count in range(sub_shadows_amount):
            m = 0
            d = 0
            for part_count in range(ss_parts_amount):
                # Get the LSBs
                lsb_bits = pixels[sb_count * ss_parts_amount + part_count] & mask
                if part_count < ss_parts_amount // 2:
                    m |= lsb_bits << (lsb * (ss_parts_amount // 2 - part_count - 1))
                else:
                    d |= lsb_bits << (lsb * (ss_parts_amount - part_count - 1))
            sub_shadow = SubShadow(GF251.convert_to_gf251(m), GF251.convert_to_gf251(d), sb_count + 1,
                                   image.shadow_number)
            sub_shadows.append(sub_shadow)

        return sub_shadows

    @staticmethod
    def embed_sub_shadows(image: SISSImage, sub_shadows: list[SubShadow], k: int) -> SISSImage:
        pixels_amount = image.width * image.height

        # The sub shadow amount is the same as block amount
        sub_shadows_amount = pixels_amount // ((2 * k) - 2)

        # Image pixels
        pixels = list(image.pixels)

        # How many less significant bits are used to store a part of sub shadow
        lsb = 4 if k < 5 else 2

        # Sub shadows parts (A sub shadow is composed of m and d -> 2 bytes)
        ss_parts_amount = (image.bytes_per_pixel * 2) // lsb

        mask = 0b1111 if k < 5 else 0b11

        for sb_count in range(sub_shadows_amount):
            sub_shadow = sub_shadows[sb_count]

            m = sub_shadow.m
            d = sub_shadow.d

            for part_count in range(ss_parts_amount):
                if part_count < ss_parts_amount // 2:
                    lsb_bits = (m >> (lsb * (ss_parts_amount // 2 - part_count - 1))) & mask
                else:
                    lsb_bits = (d >> (lsb * (ss_parts_amount - part_count - 1))) & mask

                # Clear the LSBs
                pixels[sb_count * ss_parts_amount + part_count] &= ~mask

                # Set the new LSBs
                pixels[sb_count * ss_parts_amount + part_count] |= lsb_bits

        image.pixels = bytes(pixels)
        image.set_shadow_number(sub_shadows[0].j)
        return image
