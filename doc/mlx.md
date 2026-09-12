# MiniLibX Python — Documentation rapide

Wrapper Python de MiniLibX permettant de créer des fenêtres, dessiner, charger des images et gérer le clavier/souris.

## 1. Importation

```python
from mlx import Mlx

m = Mlx()
```

---

## 2. Initialisation

```python
mlx = m.mlx_init()
```

Initialise la connexion avec le système graphique.

À appeler avant toute autre fonction MLX.

```python
m.mlx_release(mlx)
```

Libère les ressources à la fin du programme.

---

## 3. Créer une fenêtre

```python
win = m.mlx_new_window(mlx, 800, 600, "Ma fenêtre")
```

Paramètres :

```text
mlx_new_window(mlx, largeur, hauteur, titre)
```

Effacer :

```python
m.mlx_clear_window(mlx, win)
```

Détruire :

```python
m.mlx_destroy_window(mlx, win)
```

---

## 4. Dessiner

Le point `(0, 0)` est en haut à gauche.

```text
(0,0) ───────────────► x
  │
  │
  │
  ▼
  y
```

### Pixel

```python
m.mlx_pixel_put(mlx, win, x, y, color)
```

Exemple :

```python
m.mlx_pixel_put(mlx, win, 100, 50, 0xFF0000)
```

Dessine un pixel rouge.

### Texte

```python
m.mlx_string_put(mlx, win, x, y, color, "Hello")
```

---

## 5. Couleurs

Une couleur est représentée par un entier :

```python
0xAARRGGBB
```

Exemples :

```python
BLACK = 0xFF000000
WHITE = 0xFFFFFFFF
RED   = 0xFFFF0000
GREEN = 0xFF00FF00
BLUE  = 0xFF0000FF
```

---

## 6. Images

Pour créer une image en mémoire :

```python
img = m.mlx_new_image(mlx, 800, 600)
```

Pour accéder aux pixels :

```python
data = m.mlx_get_data_addr(img, ...)
```

Puis afficher l'image :

```python
m.mlx_put_image_to_window(mlx, win, img, 0, 0)
```

Pour supprimer l'image :

```python
m.mlx_destroy_image(mlx, img)
```

### Charger une image

PNG :

```python
img = m.mlx_png_file_to_image(mlx, "image.png")
```

XPM :

```python
img = m.mlx_xpm_file_to_image(mlx, "image.xpm")
```

---

## 7. Boucle principale

```python
m.mlx_loop(mlx)
```

Lance la boucle d'événements.

**Cette fonction ne retourne normalement pas** tant que `mlx_loop_exit()` n'est pas appelé.

---

## 8. Clavier

```python
def key_event(keycode, param):
    print(keycode)

m.mlx_key_hook(win, key_event, None)
```

La fonction reçoit :

```python
key_event(keycode, param)
```

`keycode` identifie la touche.

---

## 9. Souris

```python
def mouse_event(button, x, y, param):
    print(button, x, y)

m.mlx_mouse_hook(win, mouse_event, None)
```

Paramètres :

```text
button → bouton utilisé
x      → position X
y      → position Y
param  → donnée personnalisée
```

---

## 10. Fonction exécutée en boucle

```python
def loop(param):
    # exécuté lorsqu'il n'y a pas d'événement

m.mlx_loop_hook(mlx, loop, None)
```

Utile pour :

* animations ;
* jeu ;
* mises à jour régulières ;
* déplacements continus.

---

## 11. Quitter la boucle

```python
m.mlx_loop_exit(mlx)
```

Exemple :

```python
def key_event(keycode, param):
    if keycode == 65307:  # Échap
        m.mlx_loop_exit(mlx)
```

---

# Exemple minimal complet

```python
from mlx import Mlx

def key_event(keycode, param):
    if keycode == 65307:
        m.mlx_loop_exit(mlx)

def mouse_event(button, x, y, param):
    print(f"Click : {x}, {y}")

m = Mlx()

mlx = m.mlx_init()
win = m.mlx_new_window(mlx, 800, 600, "MLX Python")

m.mlx_pixel_put(mlx, win, 100, 100, 0xFF0000)
m.mlx_string_put(mlx, win, 20, 30, 0xFFFFFF, "Hello MLX")

m.mlx_key_hook(win, key_event, None)
m.mlx_mouse_hook(win, mouse_event, None)

m.mlx_loop(mlx)

m.mlx_destroy_window(mlx, win)
m.mlx_release(mlx)
```

# API à retenir

| Fonction                    | Rôle                        |
| --------------------------- | --------------------------- |
| `Mlx()`                     | Créer l'objet MLX           |
| `mlx_init()`                | Initialiser MLX             |
| `mlx_release()`             | Libérer MLX                 |
| `mlx_new_window()`          | Créer une fenêtre           |
| `mlx_destroy_window()`      | Détruire une fenêtre        |
| `mlx_clear_window()`        | Effacer une fenêtre         |
| `mlx_pixel_put()`           | Dessiner un pixel           |
| `mlx_string_put()`          | Afficher du texte           |
| `mlx_new_image()`           | Créer une image             |
| `mlx_get_data_addr()`       | Accéder aux pixels          |
| `mlx_put_image_to_window()` | Afficher une image          |
| `mlx_png_file_to_image()`   | Charger un PNG              |
| `mlx_xpm_file_to_image()`   | Charger un XPM              |
| `mlx_destroy_image()`       | Détruire une image          |
| `mlx_key_hook()`            | Événement clavier           |
| `mlx_mouse_hook()`          | Événement souris            |
| `mlx_loop_hook()`           | Fonction exécutée en boucle |
| `mlx_loop()`                | Démarrer la boucle          |
| `mlx_loop_exit()`           | Arrêter la boucle           |

## Structure typique d'un programme

```text
Mlx()
  │
  ├── mlx_init()
  │
  ├── mlx_new_window()
  │
  ├── création / chargement des images
  │
  ├── configuration des événements
  │     ├── mlx_key_hook()
  │     ├── mlx_mouse_hook()
  │     └── mlx_loop_hook()
  │
  ├── mlx_loop()
  │
  └── nettoyage
        ├── mlx_destroy_image()
        ├── mlx_destroy_window()
        └── mlx_release()
```

**Pour un projet graphique, les fonctions à maîtriser en priorité sont :**

```text
mlx_init
mlx_new_window
mlx_new_image
mlx_get_data_addr
mlx_put_image_to_window
mlx_key_hook
mlx_mouse_hook
mlx_loop
mlx_loop_exit
```

