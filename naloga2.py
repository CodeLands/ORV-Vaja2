import numpy as np

# Main funkcije
def konvolucija(slika, jedro):
    if slika.ndim == 2:
        slika = slika[:, :, np.newaxis]
    
    kernel_height, kernel_width = jedro.shape
    image_height, image_width, num_channels = slika.shape
    pad_height, pad_width = kernel_height // 2, kernel_width // 2
    
    padded_image = np.pad(slika, ((pad_height, pad_height), (pad_width, pad_width), (0, 0)), mode='constant', constant_values=0)
    
    new_image = np.zeros_like(slika)
    
    for i in range(image_height):
        for j in range(image_width):
            for k in range(num_channels):
                new_image[i, j, k] = (jedro * padded_image[i:i+kernel_height, j:j+kernel_width, k]).sum()
    
    if num_channels == 1:
        return new_image[:, :, 0]
    return new_image

def filtriraj_z_gaussovim_jedrom(slika, sigma):
    velikost_jedra = int((2 * sigma) * 2 + 1)
    k = (velikost_jedra - 1) // 2
    gaussovo_jedro = np.fromfunction(lambda x, y: (1 / (2 * np.pi * sigma ** 2)) * np.exp(-((x - k) ** 2 + (y - k) ** 2) / (2 * sigma ** 2)), (velikost_jedra, velikost_jedra), dtype=np.float32)
    #gaussovo_jedro /= gaussovo_jedro.sum()
    
    return konvolucija(slika, gaussovo_jedro)