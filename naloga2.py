import cv2 as cv
import numpy as np

def konvolucija(slika, jedro):
    višina, širina = slika.shape
    višina_jedra, širina_jedra = jedro.shape
    
    # Ustvarjanje izhodne slike polne ničel
    izhod = np.zeros((višina, širina), dtype=np.float32)
    
    # Računanje robov za padding
    pad_height = višina_jedra // 2
    pad_width = širina_jedra // 2
    
    # Dodajanje paddinga k vhodni sliki
    padded_image = np.pad(slika, ((pad_height, pad_height), (pad_width, pad_width)), mode='constant', constant_values=0)
    
    # Izvajanje konvolucije
    for i in range(višina):
        for j in range(širina):
            # Izračun konvolucije za vsako slikovno piko
            izhod[i, j] = np.sum(jedro * padded_image[i:i+višina_jedra, j:j+širina_jedra])
    
    return izhod

def filtriraj_z_gaussovim_jedrom(slika,sigma):
    '''Filtrira sliko z Gaussovim jedrom..'''
    pass

def filtriraj_sobel_smer(slika):
    '''Filtrira sliko z Sobelovim jedrom in označi gradiente v orignalni sliki glede na ustrezen pogoj.'''
    pass

if __name__ == '__main__':    
    pass
