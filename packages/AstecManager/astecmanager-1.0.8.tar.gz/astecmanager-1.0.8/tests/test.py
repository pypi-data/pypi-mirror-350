from AstecManager.libs.data import imread,imsave
import numpy as np
from skimage.morphology import binary_opening, ball , binary_closing,binary_erosion,binary_dilation
from skimage.filters import threshold_otsu
from skimage.measure import label,regionprops
import matplotlib.pyplot as plt
from scipy import ndimage as ndi

fused_raw_image = "/Users/benjamin/Data/Embryos/250310-Marie/FUSE_RAW/250310-Marie_fuse_t010.nii"
output_membrane_image = "/Users/benjamin/Data/Embryos/250310-Marie/FUSE_SPLIT_MEMBRANES/250310-Marie_fuse_t010.nii"
output_nucleus_image = "/Users/benjamin/Data/Embryos/250310-Marie/FUSE_SPLIT_NUCLEUS/250310-Marie_fuse_t010.nii"

inputimage = imread(fused_raw_image)
thresh = threshold_otsu(inputimage)
binary_image = inputimage > thresh

# 2. Définition de l'élément structurant pour l'ouverture
# Un "ball" (sphère) est approprié pour des noyaux ronds
rayon = 2  # Ajuste ce rayon en fonction de la taille approximative des noyaux
selem = ball(rayon)
step_count = 2
# 3. Application de l'ouverture binaire
mask_noyaux_fermeture = binary_image
for i in range(step_count):
    mask_noyaux_fermeture = binary_erosion(binary_image, footprint=selem)

for i in range(step_count):
    mask_noyaux_fermeture = binary_dilation(binary_image, footprint=selem)

# 4. Visualisation (optionnel, pour vérifier le résultat sur une coupe 2D)
slice_z = inputimage.shape[2] // 2

# Exemple de séparation (on met à zéro l'intensité où le masque des noyaux est False)
image_sans_noyaux = inputimage.copy()

image_1d = inputimage.flatten()
imglabeled = label(image_sans_noyaux)
regions = regionprops(imglabeled)

max_size = -1
max_size_label = -1
for region in regions:
    if region.area >= max_size:
        max_size = region.area
        max_size_label = region.label

mask_noyaux_fermeture[imglabeled==max_size_label] = False

# 2. Utilisr la fonction unique de NumPy pour trouver les valeurs uniques et leurs occurrences
valeurs_uniques, comptes = np.unique(image_1d, return_counts=True)
# 3. Trouver l'indice de la valeur avec le compte le plus élevé
indice_max_comptes = np.argmax(comptes)
# 4. Récupérer la valeur de pixel la plus présente
valeur_plus_frequente = valeurs_uniques[indice_max_comptes]
image_sans_noyaux[mask_noyaux_fermeture] = valeur_plus_frequente

fig_sep, axes_sep = plt.subplots(1, 2, figsize=(10, 5))
axes_sep[0].imshow(inputimage[:, :, slice_z], cmap='gray')
axes_sep[0].set_title('Image originale (coupe)')
axes_sep[1].imshow(image_sans_noyaux[:, :, slice_z], cmap='gray')
axes_sep[1].set_title('Image sans les noyaux (coupe)')
plt.tight_layout()
plt.show()