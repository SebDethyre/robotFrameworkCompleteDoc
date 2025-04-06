import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage

class AnimatedLabel(ctk.CTkLabel):
    def __init__(self, master, image_paths, size=32, delay=500, back_forward=False, **kwargs):
        """
        Label animé pour changer périodiquement d'image.

        Args:
            master: Fenêtre ou frame parent.
            image_paths: Liste des chemins d'images à afficher.
            size: Taille des images (largeur et hauteur).
            delay: Temps en millisecondes entre chaque image.
            **kwargs: Arguments supplémentaires pour CTkLabel.
        """
        super().__init__(master, text="", **kwargs)
        self.image_paths = image_paths
        self.size = size
        self.delay = delay
        self.current_image_index = 0
        self.running = True
        self.back_forward = back_forward
        self.forward = True

        # Charger les images à l'avance pour optimiser l'animation
        # self.images = [self.load_image(path) for path in self.image_paths]
        self.pil_images = [self.load_image_pil(path) for path in self.image_paths]
        self.images = [CTkImage(img, size=(self.size, self.size)) for img in self.pil_images]


        # Démarrer l'animation
        self.animate()
        
    def load_image_pil(self, image_path):
        """Charge et redimensionne une image PIL."""
        img = Image.open(image_path).convert("RGBA")
        return img.resize((self.size, self.size), Image.LANCZOS)
    
    def load_image(self, image_path):
        """Charge et redimensionne une image pour CTk."""
        img = Image.open(image_path).convert("RGBA")
        img = img.resize((self.size, self.size), Image.LANCZOS)
        return ctk.CTkImage(img, size=(self.size, self.size))

    # def animate(self):
    #     """Animation pour changer d'image en alternant l'ordre."""
    #     if not self.running:
    #         return

    #     # Mettre à jour l'image
    #     self.configure(image=self.images[self.current_image_index])

    #     if self.back_forward:
    #         # Déterminer le prochain index en fonction de la direction
    #         if self.forward:
    #             self.current_image_index += 1
    #             if self.current_image_index >= len(self.images) - 1:
    #                 self.forward = False  # Inverser la direction à la fin
    #         else:
    #             self.current_image_index -= 1
    #             if self.current_image_index <= 0:
    #                 self.forward = True  # Revenir à l'avant au début

    #         # Relancer l'animation après un délai
    #         self.after(self.delay, self.animate)
    #     else:
    #         self.current_image_index = (self.current_image_index + 1) % len(self.images)

    #         # Relancer l'animation après un délai
    #         self.after(self.delay, self.animate)
            
    #     def stop_animation(self):
    #         """Arrêter l'animation."""
    #         self.running = False
    def animate(self):
        """Animation pour changer d'image avec effet de fondu."""
        if not self.running:
            return

        # Initialiser les variables pour l'effet de fondu
        if not hasattr(self, "fade_alpha"):
            self.fade_alpha = 0  # Niveau de transparence initial
            self.fade_forward = True  # Direction du fondu (augmentation ou diminution)

        # Si le fondu n'est pas terminé
        if 0 <= self.fade_alpha <= 255:
            next_image_pil = self.pil_images[self.current_image_index]
            blended_image = self.apply_fade(next_image_pil, self.fade_alpha)

            # Afficher l'image intermédiaire tout en conservant le texte
            self.configure(image=blended_image, text=self.cget("text"))

            # Ajuster l'alpha en fonction de la direction du fondu
            if self.fade_forward:
                self.fade_alpha += 15
                if self.fade_alpha > 255:
                    self.fade_alpha = 255
            else:
                self.fade_alpha -= 15
                if self.fade_alpha < 150:
                    self.fade_alpha = 150

            # Si le fondu est terminé, inverser la direction
            if self.fade_alpha == 255:
                self.fade_forward = False
            elif self.fade_alpha == 150:
                self.fade_forward = True

                # Passer à l'image suivante ou précédente après un cycle complet
                if self.back_forward:
                    if self.forward:
                        self.current_image_index += 1
                        if self.current_image_index >= len(self.images) - 1:
                            self.forward = False  # Inverser la direction des images
                    else:
                        self.current_image_index -= 1
                        if self.current_image_index <= 0:
                            self.forward = True  # Revenir à l'avant au début
                else:
                    self.current_image_index = (self.current_image_index + 1) % len(self.images)

        # Si `back_forward` est désactivé et le fondu atteint 255
        if not self.back_forward and self.fade_alpha == 255:
            # Passer directement à l'image suivante
            self.fade_alpha = 0
            self.current_image_index = (self.current_image_index + 1) % len(self.images)

        # Relancer l'animation après un délai
        self.after(self.delay // 10, self.animate)



    def apply_fade(self, image_pil, alpha):
        """Applique un effet de fondu à une image PIL."""
        base_image = Image.new("RGBA", image_pil.size, (0, 0, 0, 0))  # Image vide transparente
        image_with_alpha = Image.blend(base_image, image_pil, alpha / 255.0)  # Fusionner les deux images

        # Convertir en CTkImage
        return CTkImage(image_with_alpha, size=(self.size, self.size))

