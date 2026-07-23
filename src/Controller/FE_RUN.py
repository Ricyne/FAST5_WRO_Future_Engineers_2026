from FE_Functions import*

hub = PrimeHub()
global ep, es
ep = 0
es = 0
steer.reset_angle()
def portview():
    move.reset_angle(0)
    while True:
        print("_________    Battery     _________")
        print("battery voltage:", hub.battery.voltage()/1000)
        print("battery percentage:", Battery())
        print("_________    Motor       _________")
        print("steer enc:", steer.angle())
        print("move enc:", move.angle())
        print("move dist:", dist_cal(move.angle()))
        print("_________    Gyro        _________")
        print("gyro:", ReTheta(0))  
        print("_________    Ultrasonic  _________")
        print("Left Ultra:", sL.distance())
        print("Right Ultra:", sR.distance())
        print("_________    camera      _________")
        val = Camera.read(0)
        print("color:", val[2])
        print("x/y:", val[0], "/", val[1])
        print("mid black percentage:", val[3])
        print("camera error:", Cam_err(90, 1))
        wait(500)
        print("\x1b[H\x1b[2J",end="")
def Steer(angle):
    global ep, es
    error = angle - steer.angle()
    es = error + es
    controller = error*5 + es*0.1

    steer.dc(controller)

    ep = error
    wait(10)

def main_open():
    hub.imu.reset_heading(0)
    direction = 0
    Line_count = 0
    steer.run_target(2000, 0, Stop.HOLD, True)
    while Line_count < 24:
        color = Color_read()
        Line_count = Color_line_count(color)
        if direction == 0:
            direction = color
        angle = ReTheta(Ultra_err(200)+ Steer_err(75)*direction)
        if abs(angle) < 20: 
            pwr = 100
        else: 
            pwr = 70
        Move(pwr)
        Steer(angle)

    move.reset_angle(0)
    while move.angle() < 600:
        color = Color_read()
        Line_count = Color_line_count(color)
        if direction == 0:
            direction = color
        angle = ReTheta(Ultra_err(200)+ Steer_err(75)*direction)
        if abs(angle) < 20: 
            pwr = 100
        else: 
            pwr = 50
        Move(pwr)
        Steer(angle)

    move.dc(0)

def main_obstacle():
    hub.imu.reset_heading(0)
    direction = 0
    Line_count = 0
    steer.run_target(2000, 0, Stop.HOLD, True)

    while Line_count < 6:
        color = Color_read()
        Line_count = Color_line_count(color)
        if direction == 0:
            direction = color
        angle = ReTheta(Cam_err(90,direction))
        if abs(angle) < 25: 
            pwr = 70
        else: 
            pwr = 50
        Move(pwr)
        Steer(angle)

    move.reset_angle(0)
    while move.angle() < 600:
        color = Color_read()
        Line_count = Color_line_count(color)
        if direction == 0:
            direction = color
        angle = ReTheta(Cam_err(90,direction))
        if abs(angle) < 20: 
            pwr = 95
        else: 
            pwr = 70
        Move(pwr)
        Steer(angle)
    move.dc(0)


sL.lights.on(100)
sR.lights.on(100)
main_obstacle()

# portview()
    