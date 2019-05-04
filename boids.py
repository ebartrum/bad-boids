"""
A deliberately bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""

from matplotlib import pyplot as plt
from matplotlib import animation
import random

num_boids = 50
fly_nbh=100
speed_nbh = 10000
boids_xlims = (-450, 50.0)
boids_ylims = (300, 600.0)
boids_x_velocity_lims = (0,10.0)
boids_y_velocity_lims = (-20.0,20.0)
plt_limits = (-500,1500)
animation_frames = 50
animation_interval = 50
to_middle_rate = 0.01

boids_x=[random.uniform(*boids_xlims) for x in range(num_boids)]
boids_y=[random.uniform(*boids_ylims) for x in range(num_boids)]
boid_x_velocities=[
        random.uniform(*boids_x_velocity_lims) for x in range(num_boids)]
boid_y_velocities=[
        random.uniform(*boids_y_velocity_lims) for x in range(num_boids)]
boids=(boids_x,boids_y,boid_x_velocities,boid_y_velocities)

def fly_towards_middle(boids):
    xs,ys,xvs,yvs=boids
    for i in range(num_boids):
        for j in range(num_boids):
            xvs[i]=xvs[i]+(xs[j]-xs[i])*to_middle_rate/num_boids
            yvs[i]=yvs[i]+(ys[j]-ys[i])*to_middle_rate/num_boids
    return boids
    
def fly_away_from_nearby(boids):
    xs,ys,xvs,yvs=boids
    for i in range(num_boids):
        for j in range(num_boids):
            if (xs[j]-xs[i])**2 + (ys[j]-ys[i])**2 < fly_nbh:
                xvs[i]=xvs[i]+(xs[i]-xs[j])
                yvs[i]=yvs[i]+(ys[i]-ys[j])
    return boids
    
def update_boids(boids, fly_nbh=100, speed_nbh=10000, 
        to_middle_rate=0.01, speed_match_rate=0.125):
    xs,ys,xvs,yvs=boids
    # Fly towards the middle
    boids = fly_towards_middle(boids)
    # Fly away from nearby boids
    boids = fly_away_from_nearby(boids)
    # Try to match speed with nearby boids
    for i in range(num_boids):
        for j in range(num_boids):
            if (xs[j]-xs[i])**2 + (ys[j]-ys[i])**2 < speed_nbh:
                xvs[i]=(xvs[i]+(xvs[j]-xvs[i]) *
                        speed_match_rate/num_boids)
                yvs[i]=(yvs[i]+(yvs[j]-yvs[i]) *
                        speed_match_rate/num_boids)
    # Move according to velocities
    for i in range(num_boids):
        xs[i]=xs[i]+xvs[i]
        ys[i]=ys[i]+yvs[i]

figure=plt.figure()
axes=plt.axes(xlim=plt_limits, ylim=plt_limits)
scatter=axes.scatter(boids[0],boids[1])

def animate(frame):
   update_boids(boids, fly_nbh, speed_nbh, to_middle_rate)
   scatter.set_offsets(list(zip(boids[0],boids[1])))

anim = animation.FuncAnimation(figure, animate, frames=animation_frames,
        interval=animation_interval)

if __name__ == "__main__":
    plt.show()
