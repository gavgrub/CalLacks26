import pygame, sys
from os import path

# Set up assets
imgDir = path.join(path.dirname(__file__), 'assets/img')

# Define Colors
BACKGROUND = (112, 62, 69)
UILIGHT = (231, 181, 189)
UIDARK = (157, 119, 132)
WHITE = (255, 255, 255)

# Draw Text Code
fontName = pygame.font.match_font(path.join(path.dirname(__file__), 'assets/Sansation.tff'))
def drawText(surf, text, size, x, y, color=WHITE, pos="left"):
    font = pygame.font.Font(fontName, int(size))
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect()
    match pos:
        case "left":
            textRect.topleft = (x, y)
        case "right":
            textRect.topright = (x, y)
    surf.blit(textSurface, textRect)

# Function which creates a slider
def makeSlider(xSize, ySize, color=UIDARK):
    slider = pygame.Surface((xSize, ySize), pygame.SRCALPHA)
    pygame.draw.rect(slider, color, (0, 0, xSize, ySize), border_radius=20)
    return slider

# This function resizes the window
def resize(size = 6):
    global UISIZE, WIDTH, HEIGHT, FPS
    global musicImg, timeBackground, soundBackground, muteImg, volumeImg
    global screen

    UISIZE = size
    WIDTH = int(75 * UISIZE)
    HEIGHT = int(1.5 * 75 * UISIZE)
    FPS = 60

    # Setup screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    # Rescale images

    # Music background
    noteSize = WIDTH * 0.75
    noteImg = pygame.image.load(path.join(imgDir, "play.png"))
    noteImg = pygame.transform.scale(noteImg, (noteSize / 2, noteSize / 2))
    musicImg = pygame.Surface((noteSize, noteSize), pygame.SRCALPHA)
    pygame.draw.rect(musicImg, UIDARK, (0, 0, noteSize, noteSize), border_radius=20)
    musicImg.blit(noteImg, (noteSize / 4, noteSize / 4))

    # Slider Background
    timeBackground = makeSlider(noteSize, UISIZE * 4, UIDARK)
    soundBackground = makeSlider(noteSize * 0.8, UISIZE * 4, UIDARK)

    # Mute Icon
    muteImg = pygame.image.load(path.join(imgDir, "mute.png"))
    muteImg = pygame.transform.scale(muteImg, (UISIZE * 4, UISIZE * 4))

    # Volume Icon
    volumeImg = pygame.image.load(path.join(imgDir, "mute.png"))
    volumeImg = pygame.transform.scale(volumeImg, (UISIZE * 4, UISIZE * 4))

# This function draws the UI to the screen
def drawUI():
    x = WIDTH / 2 - musicImg.get_width() / 2
    y = WIDTH / 2 + musicImg.get_width() / 2 + UISIZE * 6

    screen.fill(BACKGROUND)

    screen.blit(musicImg, (x, x))

    drawText(screen, "Song 2", UISIZE * 8, x, y)

    y += UISIZE * 8
    drawText(screen, "A cool guy", UISIZE * 7, x, y, UILIGHT)

    y += UISIZE * 9
    screen.blit(timeBackground, (x, y))

    y += UISIZE * 7
    drawText(screen, "Time 1", UISIZE * 4, x, y, UILIGHT)
    drawText(screen, "Time 2", UISIZE * 4, x + musicImg.get_width(), y, UILIGHT, "right")

    y += UISIZE * 7
    screen.blit(soundBackground, (WIDTH / 2 - soundBackground.get_width() / 2, y))
    screen.blit(muteImg, (x, y))
    screen.blit(volumeImg, (x + musicImg.get_width() - volumeImg.get_width(), y))

    pygame.display.flip()
    
#Create Window
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Music Player")
clock = pygame.time.Clock()

# Set the size of the window
resize(6)

#Game Loop
while True:

    #Keep looping at the right speed
    clock.tick(FPS)

    #Process input
    for event in pygame.event.get():

        # Close window
        if event.type == pygame.QUIT:
            sys.exit()

        # Resize window
        if event.type == pygame.VIDEORESIZE:
            resize(event.w / 75)

    #Draw To Screen
    drawUI()