import matplotlib.pyplot as plt
import numpy as np
day = 60*60*24
# константы
G = 6.67408e-11 # гравитационная постоянная
au = 1.496e11 # расстояние от земли до солнца

class CelBody(object):
    # Природные константы
    def __init__(self, id, name, x0, v0, mass, color, lw):
        # Название тела
        self.id = id
        self.name = name
        # масса
        self.M = mass
        # Исходное положение
        self.x0 = np.asarray(x0, dtype=float)
        self.x = self.x0.copy()
        # Начальная скорость (au/s)
        self.v0 = np.asarray(v0, dtype=float)
        self.v = self.v0.copy()
        self.a = np.zeros([3], dtype=float)
        self.color = color
        self.lw = lw

# Все тела

t = 0
dt = 0.1*day

Bodies = [
    CelBody(0, 'Sun', [0, 0, 0], [0, 0, 0], 1.989e30, 'yellow', 10),
    CelBody(1, 'Earth', [-1*au, 0, 0], [0, 29783, 0], 5.9742e24, 'blue', 3),
    CelBody(2, 'Venus', [0, 0.723 * au, 0], [ 35020, 0, 0], 4.8685e24, 'red', 2),
    ]

paths = [ [ b.x[:2].copy() ] for b in Bodies]

# Цикл в течение года
v = 0
while t < 365.242*day:
    # вычисление ускорения, скорости и положения
    for body in Bodies:
        body.a *= 0
        for other in Bodies:
            if (body == other): continue
            rx = body.x - other.x
            r3 = sum(rx**2)**1.5
            body.a += -G*other.M*rx/r3

    for n, planet in enumerate(Bodies):
        planet.v += planet.a*dt
        planet.x += planet.v*dt
        paths[n].append( planet.x[:2].copy() )
        
    if t > v:
        print("t=%f"%t)
        for b in Bodies: print("%10s %s"%(b.name,b.x))
        v += 30.5*day
    t += dt

plt.figure(figsize=(8,8))
for n, planet in enumerate(Bodies): 
    px, py=np.array(paths[n]).T; 
    plt.plot(px, py, color=planet.color, lw=planet.lw)
plt.show()