import pygame
from pygame.locals import *
import random as rd

print("Test for GIT")

class Ordet:
    def __init__(self, ord):
        self.ord = ord.lower()
        self.antallGjett = 0
        self.gjettetOrd = ["-"] * len(ord)
        self.lengde = len(ord)
        self.bildeFil = "Bilder/hangman0.png"


    def getOrd(self):
        return self.ord
    

    def sjekkeGjett(self, gjett):
        gjett = gjett.lower()
        if gjett in self.ord:

            indekser = []
            indeks = 0
            for i in self.ord:
                if i == gjett:
                    indekser.append(indeks)
                indeks += 1

            for index in indekser:
                self.gjettetOrd[index] = gjett
        else:
            self.antallGjett += 1

    def visOrd(self):
        vis = "".join(self.gjettetOrd)
        return vis

    def sjekkeFulltOrd(self):
        if "".join(self.gjettetOrd) == self.ord:
            return True
        else:
            return False


    def riktigBilde(self):
        if hovedord.antallGjett==0:
            bildefil = "Bilder/hangman0.png"
        elif hovedord.antallGjett == 1:
            bildefil = "Bilder/hangman1.png"
        elif hovedord.antallGjett == 2:
            bildefil = "Bilder/hangman2.png"
        elif hovedord.antallGjett == 3:
            bildefil = "Bilder/hangman3.png"
        elif hovedord.antallGjett == 4:
            bildefil = "Bilder/hangman4.png"
        elif hovedord.antallGjett == 5:
            bildefil = "Bilder/hangman5.png"
        elif hovedord.antallGjett >= 6:
            bildefil = "Bilder/hangman6.png"


        return bildefil

class Spiller:
    def __init__(self,navn):
        self.navn = "Spiller " + str(navn)
        self.score = 0
    

    def addPoeng(self):
        self.score+=1
    
    def getPoeng(self):
        return self.score

    def getNavn(self):
        return self.navn

class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = text

    def draw(self, screen):
        font = pygame.font.Font(None, 25)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(self.image, self.rect)
        screen.blit(text, text_rect)

def opprettScoreBoard(spillere,riktigSpiller):
        ##Tegner scorekortet
        pygame.draw.rect(VINDU, (64, 224, 208), pygame.Rect(0, 0, 0.2 * VINDU.get_width(), VINDU.get_height()))
        score_surface = LITEN_FONT.render("Score", True, (0, 0, 0))
        score_rect = score_surface.get_rect()
        score_rect.centerx = 0.1 * VINDU.get_width()
        score_rect.top = 150
        VINDU.blit(score_surface, score_rect)


        spiller_sin_tur_surface = LITEN_FONT.render(f"Det er {riktigSpiller.getNavn()} sin tur",True,(0,0,0))
        spiller_sin_tur_rect = spiller_sin_tur_surface.get_rect()
        spiller_sin_tur_rect.centerx = 0.1*VINDU.get_width()
        spiller_sin_tur_rect.top = 70
        VINDU.blit(spiller_sin_tur_surface,spiller_sin_tur_rect)

        for i in range(len(spillere)):
            spiller=spillere[i]
            spiller_surface = LITEN_FONT.render(spiller.getNavn(), True, (0, 0, 0))
            spiller_rect = spiller_surface.get_rect()
            spiller_rect.left = 20
            spiller_rect.top = 220 + i * 100
            VINDU.blit(spiller_surface, spiller_rect)

            poeng_surface = LITEN_FONT.render(str(spiller.getPoeng()), True, (0, 0, 0))
            poeng_rect = poeng_surface.get_rect()
            poeng_rect.right = score_rect.right
            poeng_rect.top = spiller_rect.top
            VINDU.blit(poeng_surface, poeng_rect)

def opprettSpillere(antall_spillere):
    spillere = []
    for i in range(antall_spillere):
        spiller = Spiller(i+1)
        spillere.append(spiller)

    return spillere

def bestemOrd(inputFiler):
    i = rd.randint(0,len(inputFiler)-1)

    fil = inputFiler[i]
    fil = f"Database/{fil}"
    with open(fil,"r",encoding="utf-8") as innfil:
        linjer = innfil.readlines()
        tilfeldig_linje = rd.choice(linjer)
    
    return tilfeldig_linje.strip()





INPUTFILER = ['ordliste_banneord.txt','ordliste_ssb_norske_fornavn.txt']

pygame.init()
VINDU = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Hangman")
BASIS_FONT = pygame.font.SysFont('sans-serrif', 65)
LITEN_FONT = pygame.font.SysFont('sans-serrif', 20)



ferdig = False
spillStartet = False

spillerTeller = 0

tilbakeKnapp = Button("Tilbake", 10, 10, 100, 50, (0, 0, 255))

while True:

    VINDU.fill((255, 255, 255))

    ## Brukeren skal først legge til hvor mange som skal spille.
    while not spillStartet:
        text_surface = BASIS_FONT.render("Velg antall spillere (1-4):", True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        VINDU.blit(text_surface,(250,0))



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    antall_spillere = int(event.unicode)
                    if 1 <= antall_spillere <= 4:

                        spillere = opprettSpillere(antall_spillere)


                        spillerTeller=0
                        hovedord = Ordet(bestemOrd(INPUTFILER))
                        spillStartet = True
                        gjetteteBokstaver = []
                        break



        pygame.display.update()    
        
                        
    if not ferdig:

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN and event.key not in [pygame.K_ESCAPE, pygame.K_F4]:
                gjett = event.unicode
                if gjett.isalpha() and gjett not in gjetteteBokstaver:
                    hovedord.sjekkeGjett(gjett)
                    gjetteteBokstaver.append(gjett)

                    spillerTeller+=1
                    if spillerTeller>antall_spillere-1:
                        spillerTeller = 0
            

            #Hvis tilbakeknappen trykkes har ikke spillet startet igjenn.
            if event.type == MOUSEBUTTONDOWN:
                mus_pos = pygame.mouse.get_pos()
                if tilbakeKnapp.rect.collidepoint(mus_pos):
                    spillStartet=False

        bildefil = hovedord.riktigBilde()

        bilde = pygame.image.load(bildefil)
        VINDU.blit(bilde, (300, 0))

        text_surface = BASIS_FONT.render(hovedord.visOrd(), True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.centerx = VINDU.get_rect().centerx+50
        text_rect.bottom = 590
        VINDU.blit(text_surface, text_rect)

        ##Oprrettet scoreBoard
        opprettScoreBoard(spillere,spillere[spillerTeller])

        #Tegner tilbakeknapp:
        tilbakeKnapp.draw(VINDU)


        if hovedord.sjekkeFulltOrd():
            text_surface = BASIS_FONT.render("Du vant! Trykk en knapp for å spille", True, (0, 255, 0))
            VINDU.blit(text_surface, (0, 200))
            ferdig = True
            

        if hovedord.antallGjett >= 6:
            text_surface = LITEN_FONT.render(f"Du tapte! Trykk en knapp for å spille igjen. Riktig ord var {hovedord.getOrd()}", True, (255, 0, 0))
            VINDU.blit(text_surface, (0, 200))

            ferdig = True
        

    else:
        VINDU.fill((255,255,255))
        VINDU.blit(text_surface,(0,200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                ferdig = False
                hovedord=Ordet(bestemOrd(INPUTFILER)) ##NYTT ORD
                spillerTeller = 0 #Resetter turnusen


    pygame.display.update()