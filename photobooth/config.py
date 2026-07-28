from pathlib import Path

# Diretórios do projeto
BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"
PHOTOS_DIR = BASE_DIR / "photos"
FONTS_DIR = BASE_DIR / "fonts"

FONT_REGULAR = FONTS_DIR / "Montserrat-Regular.ttf"
FONT_BOLD = FONTS_DIR / "Montserrat-Bold.ttf"
FONT_COQUETTE = FONTS_DIR / "Butterpop.ttf"

# ---------------------------------------------------------------------------
# Câmera
# ---------------------------------------------------------------------------

# Use o caminho estável de /dev/v4l/by-id/... quando ele estiver disponível.
CAMERA_DEVICE = "/dev/video0"

# A LifeCam VX-7000 informou suporte a MJPG em 640x480 a 30 fps.
CAMERA_FOURCC = "MJPG"
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30
CAMERA_WARMUP_FRAMES = 12

# O preview espelhado é mais natural para quem está diante da câmera.
MIRROR_PREVIEW = True

# False salva a imagem na orientação real da câmera.
# Mude para True para salvar exatamente como aparece no preview.
MIRROR_SAVED_PHOTO = False

JPEG_QUALITY = 95

# ---------------------------------------------------------------------------
# Interface
# ---------------------------------------------------------------------------

APP_TITLE = "Photo Booth"

# 1280x720 costuma ser mais leve para o Raspberry Pi 3B do que Full HD.
DISPLAY_SIZE = (1280, 720)
FULLSCREEN = True
SHOW_MOUSE_CURSOR = True
TARGET_FPS = 20

COUNTDOWN_SECONDS = 3
DONE_SCREEN_SECONDS = 4.0
MIN_PROCESSING_SCREEN_SECONDS = 1.2

# Imagens opcionais. Se não existirem, o programa desenha telas substitutas.
ATTRACT_IMAGE = IMAGES_DIR / "attract.jpg"
PRINTING_IMAGE = IMAGES_DIR / "printing.jpg"
DONE_IMAGE = IMAGES_DIR / "done.jpg"

# ---------------------------------------------------------------------------
# Impressão
# ---------------------------------------------------------------------------

# Opções:
#   "disabled" -> apenas salva a foto; ideal enquanto não há impressora
#   "cups"     -> envia o arquivo ao comando lp
PRINTER_MODE = "disabled"

# None usa a impressora padrão do CUPS.
# Exemplo: PRINTER_NAME = "Minha_Impressora"
PRINTER_NAME = None

# ---------------------------------------------------------------------------
# Aparência
# ---------------------------------------------------------------------------

BACKGROUND_COLOR = (17, 19, 24)
PANEL_COLOR = (25, 28, 35)
TEXT_COLOR = (245, 245, 245)
SECONDARY_TEXT_COLOR = (255, 182, 204)
PRIMARY_BUTTON_COLOR = (255, 182, 204)
PRIMARY_BUTTON_TEXT_COLOR = (255, 255, 255)
SECONDARY_BUTTON_COLOR = (255, 147, 199)
SECONDARY_BUTTON_TEXT_COLOR = (255, 255, 255)
DANGER_BUTTON_COLOR = (120, 45, 45)
COUNTDOWN_COLOR = (255, 255, 255)
COUNTDOWN_SHADOW_COLOR = (0, 0, 0)
