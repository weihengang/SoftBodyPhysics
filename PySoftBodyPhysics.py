import turtle as t
import math as m
tscreen = t.Screen()
tscreen.colormode(255)
tscreen.bgcolor((0, 0, 0))
tscreen.tracer(0)
t.hideturtle()
t.color((255, 255, 255))
t.up()
line = t.Turtle()
line.color((150, 150, 150))
line.hideturtle()
line.up()
line.goto(-500, -350)
line.down()
line.goto(500, -350)
line.up()
line.goto(500, -350)
line.down()
line.goto(500, 350)
line.up()
line.goto(-500, -350)
line.down()
line.goto(-500, 350)
line.up()
line.goto(-500, 350)
line.down()
line.goto(500, 350)
tscreen.update()
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.previous_y = y
        self.previous_x = x
        self.x_acceleration = 0
        self.y_acceleration = 0
    def update_position(self):
        self.y_acceleration *= 0.99
        self.x_acceleration *= 0.99
        if (self.y > 320):
            self.y = 319
            self.y_acceleration *= -1
        if (self.x < -480):
            self.x = -479
            self.x_acceleration *= -1
        if (self.x > 480):
            self.x = 479
            self.x_acceleration *= -1
        if (self.y < -350):
            self.y = -350
            self.y_acceleration = 5
        current_y = self.y
        current_x = self.x
        self.y_acceleration += -5
        self.y += ((self.y - self.previous_y) + self.y_acceleration) / 110
        self.x += ((self.x - self.previous_x) + self.x_acceleration) / 110
        self.previous_y = current_y
        self.previous_x = current_x
    def y_force(self):
        self.y_acceleration += 300
class Spring:
    SPRING_CONSTANT = 5
    def __init__(self, point1, point2):
        assert type(point1) == Point
        assert type(point2) == Point
        self.point1 = point1
        self.point2 = point2
        self.distance = m.sqrt(pow(point1.x - point2.x, 2) + pow(point1.y - point2.y, 2))
        self.current_distance = self.distance
    def constrain_points(self):
        current_distance = m.sqrt(pow(self.point1.x - self.point2.x, 2) + pow(self.point1.y - self.point2.y, 2))
        self.current_distance = current_distance
        force = Spring.SPRING_CONSTANT * (current_distance - self.distance)
        pointa = (self.point1.x, self.point1.y)
        pointb = (self.point2.x, self.point2.y)
        vector_ab = (pointb[0] - pointa[0], pointb[1] - pointa[1])
        magnitude = m.sqrt(pow(vector_ab[0], 2) + pow(vector_ab[1], 2))
        unit_ab = (vector_ab[0] / magnitude * force, vector_ab[1] / magnitude * force)
        self.point1.x_acceleration += unit_ab[0] 
        self.point1.y_acceleration += unit_ab[1]
        self.point2.x_acceleration -= unit_ab[0]
        self.point2.y_acceleration -= unit_ab[1]
a = Point(-100, 100)
b = Point(100, 100)
c = Point(100, -100)
d = Point(-100, -100)
e = Point(50, 0)
f = Point(-50, 0)
x = Point(0, 0)
list_Points = [a, b, c, d, e, f, x]
ab = Spring(a, b)
bc = Spring(b, c)
cd = Spring(c, d)
da = Spring(d, a)
af = Spring(a, f)
be = Spring(b, e)
ce = Spring(c, e)
df = Spring(d, f)
ex = Spring(e, x)
fx = Spring(f, x)
ae = Spring(a, e)
de = Spring(d, e)
bf = Spring(b, f)
cf = Spring(c, f)
ax = Spring(a, x)
bx = Spring(b, x)
cx = Spring(c, x)
dx = Spring(d, x)
list_Spring = [ab, bc, cd, da, af, be, ce, df, ex, fx, ae, de, bf, cf, ax, bx, cx, dx]
def jump():
    for i in list_Points:
        i.y_force()
def screen_onclick(x, y):
    FORCE_PORPORTIONAL = 500
    for i in list_Points:
        distance = m.sqrt(pow(i.x - x, 2) + pow(i.y - y, 2))
        constant = FORCE_PORPORTIONAL / distance
        unit_mx = (x - i.x) * constant
        unit_my = (y - i.y) * constant
        i.x_acceleration += unit_mx
        i.y_acceleration += unit_my
def calculate_color(spring):
    assert type(spring) == Spring
    average = int(abs((spring.point1.x_acceleration + spring.point1.y_acceleration + spring.point2.x_acceleration + spring.point2.y_acceleration)) // 4)
    ratio = spring.current_distance / spring.distance
    offset = 150 * ratio
    if (ratio < 1):
        offset *= -1
    color = [average - offset + 100, average + 100, average + offset + 100]
    return_color = []
    for i in color:
        if (i > 255):
            return_color.append(255)
        elif (i < 0):
            return_color.append(0)
        else:
            return_color.append(int(i))
    return tuple(return_color)
def animate():
    t.clear()
    for i in list_Points:
        i.update_position()
    for i in list_Spring:
        i.constrain_points()
        t.up()
        t.goto(i.point1.x, i.point1.y)
        t.dot(10, "white")
        t.down()
        t.color((calculate_color(i)))
        t.goto(i.point2.x, i.point2.y)
        t.dot(10, "white")
    tscreen.update()
    tscreen.ontimer(animate, 1)
animate()
tscreen.onkey(jump, "space")
tscreen.onclick(screen_onclick)
tscreen.listen()
tscreen.mainloop()