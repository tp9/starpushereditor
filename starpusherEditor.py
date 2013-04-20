#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *

FPS = 30 # frames per second to update the screen
WINDOWWIDTH = 800 # width of the program's window, in pixels
WINDOWHEIGHT = 800 # height in pixels
BOARDWIDTH = 10 # number of tiles per column
BOARDHEIGHT = 10 # number of tiles per row
MARGIN = 20
TILESIZE = 60

# set margins
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * TILESIZE)) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * TILESIZE)) / 2)

CAM_MOVE_SPEED = 5 # how many pixels per frame the camera moves

BRIGHTBLUE  = (  0, 170, 255)
WHITE       = (255, 255, 255)
DARKGRAY    = ( 40,  40,  40)
BLUE        = (  0,  50, 255)
YELLOW      = (255, 255,   0)
BGCOLOR     = BRIGHTBLUE
TEXTCOLOR   = WHITE
HIGHLIGHTCOLOR = BLUE
WALLCOLOR   = YELLOW


def main():
    global DISPLAYSURF
    # set initial position of the game window
    os.environ['SDL_VIDEO_WINDOW_POS'] = "40,40"
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Star Pusher Editor')
    mouseX = 0
    mouseY = 0
    mouseImageX = 0
    mouseImageY = 0
    leftButtonClicked = False
    rightButtonClicked = False
    cameraX = 0
    cameraY = 0
    cameraLeft = False
    cameraRight = False
    cameraUp = False
    cameraDown = False
    objectIter = 0
    mapTiles = [[None] * BOARDHEIGHT for i in range(BOARDWIDTH)]
    # image dictionaries
    OBJECTIMAGES = ['#', '$', '@', '.']
    IMAGESDICT = {'uncovered goal': pygame.image.load('img\RedSelector.png'),
                  'star': pygame.image.load('img\Star.png'),
                  'wall': pygame.image.load('img\Wall_Block_Tall.png'),
                  'princess': pygame.image.load('img\princess.png')}
    MOUSEIMAGES = [IMAGESDICT['wall'],
                    IMAGESDICT['star'],
                    IMAGESDICT['princess'],
                    IMAGESDICT['uncovered goal']]
    
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        # draw tiles
        for tileX in range(BOARDWIDTH):
            for tileY in range(BOARDHEIGHT):
                left, top = leftTopCoordsTile(tileX, tileY)
                if mapTiles[tileX][tileY] == '#':
                    pygame.draw.rect(DISPLAYSURF, WALLCOLOR, (left, top, 
                                     TILESIZE, TILESIZE))
                elif mapTiles[tileX][tileY] != None:
                    imgRect = pygame.Rect((tileX * TILESIZE + XMARGIN, 
                                           tileY * TILESIZE + YMARGIN, 
                                           TILESIZE, TILESIZE))
                    if mapTiles[tileX][tileY] == '$':
                        DISPLAYSURF.blit(IMAGESDICT['star'], imgRect)
                    elif mapTiles[tileX][tileY] == '@':
                        DISPLAYSURF.blit(IMAGESDICT['princess'], imgRect)
                    elif mapTiles[tileX][tileY] == '.':
                        DISPLAYSURF.blit(IMAGESDICT['uncovered goal'], imgRect)
        # draw tile outlines
        for x in range(0, (BOARDWIDTH + 1) * TILESIZE, TILESIZE):
            pygame.draw.line(DISPLAYSURF, DARKGRAY, (x + XMARGIN, YMARGIN), 
                (x + XMARGIN, WINDOWHEIGHT - YMARGIN))
        for y in range(0, (BOARDHEIGHT + 1) * TILESIZE, TILESIZE):
            pygame.draw.line(DISPLAYSURF, DARKGRAY, (XMARGIN, y + YMARGIN), 
                (WINDOWWIDTH - XMARGIN, y + YMARGIN))
        # event handler
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_DELETE:
                    print 'delete level' # reset the level
                elif event.key == K_n:
                    print 'new level'
                elif event.key == K_s:
                    print 'save file'
                elif event.key == K_PAGEUP:
                    print 'previous level'
                elif event.key == K_PAGEDOWN:
                    print 'next level'
            elif event.type == MOUSEBUTTONUP:
                if event.button == 5:
                    objectIter -= 1
                    if objectIter < 0:
                        objectIter = len(OBJECTIMAGES) - 1
                elif event.button == 4:
                    objectIter += 1
                    if objectIter >= len(OBJECTIMAGES):
                        objectIter = 0
                elif event.button == 1:
                    leftButtonClicked = True
                    clickX, clickY = event.pos
                elif event.button == 3:
                    rightButtonClicked = True
                    clickX, clickY = event.pos
            elif event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos
                
        tileX, tileY = getTileAtPixel(mouseX, mouseY)
        if tileX != None:
            drawHighlightTile(tileX, tileY)
            mouseImageX = mouseX - (MOUSEIMAGES[objectIter].get_width() / 2)
            mouseImageY = mouseY - (MOUSEIMAGES[objectIter].get_height() / 2)
            DISPLAYSURF.blit(MOUSEIMAGES[objectIter], (mouseImageX,mouseImageY))
            if leftButtonClicked:
                # print 'place item at', tileX, tileY
                mapTiles[tileX][tileY] = OBJECTIMAGES[objectIter]
                leftButtonClicked = False
            if rightButtonClicked:
                # print 'delete item', tileX, tileY
                mapTiles[tileX][tileY] = None
                rightButtonClicked = False
                
        pygame.display.update()

        
def leftTopCoordsTile(tilex, tiley):
    '''
    returns left and top pixel coords
    tilex: int
    tiley: int
    return: tuple (int, int)
    '''
    left = tilex * TILESIZE + XMARGIN
    top = tiley * TILESIZE + YMARGIN
    return (left, top)

    
def getTileAtPixel(x, y):
    '''
    returns tile coordinates of pixel at top left, defaults to (None, None)
    x: int
    y: int
    return: tuple (tilex, tiley)
    '''
    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT):
            left, top = leftTopCoordsTile(tilex, tiley)
            tile_rect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tile_rect.collidepoint(x, y):
                return (tilex, tiley)
    return (None, None)
    
    
def drawHighlightTile(tilex, tiley):
    '''
    tilex: int
    tiley: int
    '''
    left, top = leftTopCoordsTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR,
                    (left, top, TILESIZE, TILESIZE), 4)
                

if __name__=='__main__':
    main()