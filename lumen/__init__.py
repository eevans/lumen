
import pygame, sys
from pygame.locals import *
from time import time
from io import ParallelIO
from os.path import abspath, join, dirname

DEFAULT_BG = abspath(join(dirname(__file__), 'images', 'background.png'))
DEFAULT_BG_SIZE = (1024,546)

class Markers(object):
    ordered_channels = (K_a, K_s, K_d, K_f, K_j, K_k, K_l, K_SEMICOLON)
    # TODO: these channels values need to be configurable
    channels = {}
    channels[K_a] = (273,160)
    channels[K_s] = (237,285)
    channels[K_d] = (713,243)
    channels[K_f] = (889,290)
    channels[K_j] = (189,216)
    channels[K_k] = (385,359)
    channels[K_l] = (357,216)
    channels[K_SEMICOLON] = (11,492)
    image = pygame.image.load(abspath(join(dirname(__file__),
                                      'images',
                                      'marker.png')))
    
    def __init__(self):
        self.state = {}
        self.dirty = False
    
    def up(self, key):
        if self.state.has_key(key):
            del self.state[key]
            self.dirty = True
    
    def down(self, key):
        self.state[key] = self.channels[key]
        self.dirty = True
    
    def update(self, screen, callback=None):
        for pos in self.state.values():
            screen.blit(self.image, pos)
            
        if self.dirty and callback: 
            bits = []
            for k in self.ordered_channels:
                if self.state.has_key(k): bits.append(True)
                else: bits.append(False)
            callback(bits)
            
        self.dirty = False
        
class Player(object):
    def __init__(self, track, trackmap, background=DEFAULT_BG,
                 bgsize=DEFAULT_BG_SIZE):
        pygame.mixer.pre_init(44100)
        pygame.init()
        
        # TODO: validate paths, filetypes, bgsize, etc
        self.markers = Markers()
        self.trackmap = trackmap
        
        self.screen = pygame.display.set_mode(bgsize)
        self.background = pygame.image.load(background)
        self.clock = pygame.time.Clock()
        
        pygame.mixer.music.load(track)
        pygame.display.set_caption("Lumen Player")
        
    def play(self, fudge=0, simulated=False):
        f = open(self.trackmap, 'r')
        cols = f.readline().strip().split()
        stamp = int(cols[0])
        
        output = ParallelIO(mock=simulated)
        pygame.mixer.music.play()
        
        while True:
            while ((stamp - fudge) < pygame.mixer.music.get_pos()):
                if (cols[1].lower() == "true"): self.markers.down(K_a)
                else: self.markers.up(K_a)
                if (cols[2].lower() == "true"): self.markers.down(K_s)
                else: self.markers.up(K_s)
                if (cols[3].lower() == "true"): self.markers.down(K_d)
                else: self.markers.up(K_d)
                if (cols[4].lower() == "true"): self.markers.down(K_f)
                else: self.markers.up(K_f)
                if (cols[5].lower() == "true"): self.markers.down(K_j)
                else: self.markers.up(K_j)
                if (cols[6].lower() == "true"): self.markers.down(K_k)
                else: self.markers.up(K_k)
                if (cols[7].lower() == "true"): self.markers.down(K_l)
                else: self.markers.up(K_l)
                if (cols[8].lower() == "true"): self.markers.down(K_SEMICOLON)
                else: self.markers.up(K_SEMICOLON)
                cols = f.readline().strip().split()
                if not len(cols): break
                stamp = int(cols[0])
        
            for event in pygame.event.get():
                if (event.type == QUIT) or \
                        ((event.type == KEYDOWN) and (event.key in (K_ESCAPE, K_q))):
                    sys.exit()
    
            def outputs(bits):
                for (i, bit) in enumerate(bits):
                    if not bit: output.set(i+1)
                    else: output.unset(i+1)
             
            self.screen.blit(self.background, (0,0))
            self.markers.update(self.screen, outputs)
            pygame.display.flip()
    
    def record(self):
        playing = paused = False
        f = open(self.trackmap, 'w')
        
        while True:
            self.clock.tick(30)
        
            for event in pygame.event.get():
                if (event.type == QUIT) or \
                        ((event.type == KEYDOWN) and (event.key in (K_ESCAPE, K_q))):
                    sys.exit()
        
                if (event.type == KEYDOWN and event.key in Markers.channels.keys()):
                    self.markers.down(event.key)
                if (event.type == KEYUP and event.key in Markers.channels.keys()):
                    self.markers.up(event.key)
                    
                # Pause/play audio track
                if (event.type == KEYDOWN and event.key == K_p):
                    if (not playing):
                        pygame.mixer.music.play()
                        playing = True
                    elif paused:
                        pygame.mixer.music.unpause()
                        paused = False
                    else:
                        pygame.mixer.music.pause()
                        paused = True
    
            def print_series(b):
                assert len(b) == 8
                stamp = pygame.mixer.music.get_pos()
                print >>f, "%-10d %-5s %-5s %-5s %-5s %-5s %-5s %-5s %-5s" % \
                        (stamp, b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7])
                 
            self.screen.blit(self.background, (0,0))
            self.markers.update(self.screen, print_series)
            pygame.display.flip()
            
            