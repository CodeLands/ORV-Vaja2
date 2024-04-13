import unittest

import cv2 as cv
import numpy as np

from naloga2 import (filtriraj_sobel_horizontalno,
                     filtriraj_z_gaussovim_jedrom, konvolucija)


class TestImageFilters(unittest.TestCase):
    def test_konvolucija(self):
        # Test za preverjanje konvolucijske funkcije z enostavnim jedrom
        slika = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=np.float32)
        jedro = np.array([[1]], dtype=np.float32)
        rezultat = konvolucija(slika, jedro)
        np.testing.assert_array_equal(
            rezultat,
            slika,
            "Konvolucija z enotskim jedrom bi morala vrniti originalno sliko.",
        )

    def test_filtriraj_z_gaussovim_jedrom(self):
        # Preprost test za Gaussov filter
        slika = np.zeros((5, 5), dtype=np.float32)
        slika[2, 2] = 1
        sigma = 1.0
        filtrirana_slika = filtriraj_z_gaussovim_jedrom(slika, sigma)
        self.assertGreater(
            filtrirana_slika[2, 2],
            0,
            "Središče filtrirane slike bi moralo biti večje od 0.",
        )
        self.assertLess(
            filtrirana_slika[0, 0],
            filtrirana_slika[2, 2],
            "Vrednosti od središča se morajo zmanjševati.",
        )


    def test_filtriraj_sobel_horizontalno(self):
        # Set up an image with a clear horizontal gradient
        slika = np.full((3, 3), 128, dtype=np.float32)
        slika[:, 2] = 255  # Increase the right side to introduce a horizontal gradient
        slika[:, 1] = 0    # Decrease the left side to enhance the gradient

        # Apply the Sobel filter to detect the horizontal gradient
        filtrirana_slika = filtriraj_sobel_horizontalno(slika)

        # Now, expect the output to be in grayscale with values between 0 to 255
        # Check that the center value is greater than the average corner values,
        # indicating the detection of the horizontal gradient.
        center_value = filtrirana_slika[1, 1]
        corner_values = np.array([filtrirana_slika[0, 0], filtrirana_slika[0, 2], filtrirana_slika[2, 0], filtrirana_slika[2, 2]])
        average_corner_value = np.mean(np.abs(corner_values))

        # Adjust the assertion to reflect expectations for a normalized grayscale image
        self.assertGreater(center_value, average_corner_value, "Središče filtrirane slike bi moralo imeti višjo vrednost od povprečja vogalnih vrednosti zaradi horizontalnega gradienta.")


if __name__ == "__main__":
    unittest.main()
