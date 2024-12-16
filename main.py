import numpy, pygame, sys
from pygame.locals import *
from matplotlib import pyplot as plt

# accepts initial conditions as parameters
def spring_dampener(displacement, velocity) :
    if displacement == 0:
        print("no displacement")
        return

    d       = .25               # damping constant
    omega   = 2 * numpy.pi      # natural frequency

    # RECALL: Z = k / m
    #       : omega = d / m
    # assigning values to Z and omega is the same as assigning values to spring constant (k) and mass (m)
    # we use those abbreviations because it's nice

    # this is the matrix we get from suspending the variables in our system (x, xdot) after 
    # obtaining our 2nd order DE
    system = numpy.array([
        [0, 1],
        [-omega ** 2, -2 * d * omega] # -2dw = Z
    ])

    # strategy : approximate dx/dt = Ax by using a finite time step for dt
    #   dx = Ax * dt
    # this gives us an update rule for our differential equation which is much nicer to code
    # if k specifies which time step we are on, we can write
    #   x_{k+1} = x_k + Ax_k * dt (time k is given by k * dt, where dt is the size of the timestep)
    dt = 0.01       # time step
    T = 10          # total time to simulate for
    N = int(T / dt) # number of time steps

    vbar = [displacement, velocity]

    # solution array, where each column corresponds to a time step
    # solns = [[0, 0] for x in range(0, N)]
    solns = numpy.zeros((2,N))
    solns[:, 0] = vbar

    for step in range(N - 1) :
        # solns[:, step + 1] = (numpy.eye(2) + dt * system) @ solns[:,step]
        solns[:, step + 1] = solns[:, step] + dt * (system @ solns[:, step])

    # PLOTTING
    t = numpy.linspace(0, T, N)
    plt.figure(figsize=(20, 4))
    plt.subplot(1, 2, 1)
    plt.plot(t, solns[0, :], 'k')
    plt.xlabel('Time [s]')
    plt.ylabel('Position [m]')
    plt.grid(True)
    plt.legend([f'Starting condition: {displacement} units of displacement'])

    plt.subplot(1, 2, 2)
    plt.plot(solns[0, :], solns[1, :], 'k')
    plt.xlabel('Position [m]')
    plt.ylabel('Velocity [m/s]')
    plt.legend([f'Starting condition: {displacement} units of displacement'])
    plt.savefig("graphs.png")
    return solns

# ===================
WIN_WIDTH = 900     # 180 tiles across
WIN_HEIGHT = 600    # 120 tiles down
WIN_SCALE = 1.5
TILE_SIZE = 5

display_window = pygame.display.set_mode((WIN_WIDTH * WIN_SCALE, WIN_HEIGHT * WIN_SCALE), 0, 32)
raw_window = pygame.Surface((WIN_WIDTH,WIN_HEIGHT))

clock = pygame.time.Clock()

frame_start = 0
frame_end = pygame.time.get_ticks()
dt = frame_end - frame_start

playing = True
simulating = False
setting_position = False
release = False
positions = None

wall_zero = 300
mass_zero = 600
r_wall = pygame.Rect(0, 0, wall_zero, 600)
r_mass = pygame.Rect(mass_zero, WIN_HEIGHT/2 - 25, 50, 50)

# step counter
k = 0
# 1 unit of displacement : 50 pixels of displacement
visual_scale = 50

def getScaledClick() :
    return tuple(i / WIN_SCALE  for i in pygame.mouse.get_pos())

# GREEN MASS = CAN MOVE
green = (0, 255, 0)
# PURPLE MASS = SIMULATING
purple = (75,0,130)

render_color = green

while playing:
    raw_window.fill((0,0,0))
    gap = 0
    
    # starting point line
    pygame.draw.line(raw_window, (0,0,200), (mass_zero, 0), (mass_zero, 600))

    # spring line
    pygame.draw.line(raw_window, (0,200,200), (wall_zero, WIN_HEIGHT/2), (r_mass.x, WIN_HEIGHT/2), 5)

    for event in pygame.event.get() :
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN : 
            if event.key == K_ESCAPE:
                playing = False
        if event.type == MOUSEBUTTONDOWN :
            if not simulating:
                click_pos = getScaledClick()
                if pygame.Rect.collidepoint(r_mass, click_pos) :
                    # find gap between click location and mass x value
                    gap = click_pos[0] - r_mass.x
                    setting_position = True

        if event.type == MOUSEBUTTONUP:
            # set release position as initial conditions
            if setting_position :
                setting_position = False
                release = True
                simulating = True
            

    if release:
        print("Initial condition:", (r_mass.x - mass_zero)/visual_scale)
        positions = spring_dampener((r_mass.x - mass_zero)/visual_scale, 0)

    if setting_position :
        # determine where to put the box relative to where the new mouse position is (ie s.t. the gap is the same)
        new_mouse_pos = getScaledClick()
        new_mass_x = new_mouse_pos[0] - gap
        r_mass.x = new_mass_x
    if simulating :
        # pick the correct value from the diff eq solution for this time step 
        dx = positions[0, k] * visual_scale
        r_mass.x = mass_zero + dx

        
    pygame.draw.rect(raw_window, (254, 0, 0), r_wall)
    pygame.draw.rect(raw_window, render_color, r_mass)

    scaled_window = pygame.transform.scale(raw_window, display_window.get_size())
    display_window.blit(scaled_window, (0,0))
    pygame.display.update()
    # ==============================
    frame_end = pygame.time.get_ticks()
    dt = frame_end - frame_start
    clock.tick(60)

    if simulating and k < (10/0.01) - 1 :
        k += 1 
        
        render_color = purple

        if positions.any() :
            if abs(positions[1, k]) < .0001 :
                print("Negligible velocity reached - terminating!")
                simulating = False
    else :
        # print("Done simulating!")
        render_color = green
        simulating = False
        k = 0

    release = False


pygame.quit()