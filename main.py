from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor
from numpy import abs
from perlin_noise import PerlinNoise
from ursina import duplicate

app = Ursina()


# widndow params
window.color = color.rgb(0, 200, 255)
window.exit_button.visible = False
window.fps_counter.visible = False
window.borderless = False
window.fullscreen = False
window.title = "minecraft"


scene.fog_color = color.rgb(0, 210, 255)
scene.fog_density = 0.04

grassStrokeTex = load_texture('grass.jpg')
woodStrokeTex = load_texture('wood.jpg')


terrain = Entity(model=None, collider=None)


# block breaker
#blockBreaker = Entity(model = None, collider = None)

#def breakBlock():
#    if player.cursor.lookAt(blockBreaker) and input('left mouse down'):
#        destroy(blockBreaker)




#perlin nosie
noise = PerlinNoise(octaves=2, seed=32767)

amp = 6
freq = 24


jeff = Entity(model = 'cube', color = color.green, texture = grassStrokeTex)
wireTex = load_texture('wire.png')

bte = Entity(model='cube', texture=wireTex)


def buildTool():
    bte.position = round(player.position + camera.forward * 3)
    bte.y += 2
    bte.y = round(bte.y)
    bte.x = round(bte.x)
    bte.z = round(bte.z)

def build():
    e = duplicate(bte)
    e.collider = 'cube'
    e.texture = woodStrokeTex
    e.shake(duration=0.1, speed=0.01)

def mine():
    e = mouse.hovered_entity
    destroy(e)

def input(key):
    if key == 'q' or key == 'escape':
        exit()

    if key == 'left mouse up':
        build()



def update():
    global PrevZ, PrevX
    if abs(player.z - PrevZ) > 1 or abs(player.x - PrevX) > 1:
        generateShell()

    buildTool()


shellies = []
shellWidth = 28

for i in range(shellWidth*shellWidth):
    bud = Entity(model='cube', collider='box', texture = grassStrokeTex)
    shellies.append(bud)

def generateShell():
    global shellWidth, amp, freq
    for i in range(len(shellies)):
        x = shellies[i].x = floor((i/shellWidth) + player.x - 0.5*shellWidth)
        z = shellies[i].z = floor((i%shellWidth) + player.z - 0.5*shellWidth)
        shellies[i].y = floor((noise([x/freq,z/freq]))*amp)

#blockBreaker.parent = butt

player = FirstPersonController()
player.cursor.visible = False
player.x = player.z = 5
player.y = 12
player.gravity = 0.5
PrevZ = player.z
PrevX = player.x

generateShell()


app.run()