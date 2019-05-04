"""
A deliberately bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""

from matplotlib import pyplot as plt
from matplotlib import animation
import random

sample_size = 50
boids_xlims = (-450, 50.0)
boids_ylims = (300, 600.0)
boids_x_velocity_lims = (0,10.0)
boids_y_velocity_lims = (-20.0,20.0)

boids_x=[random.uniform(*boids_xlims) for x in range(sample_size)]
boids_y=[random.uniform(*boids_ylims) for x in range(sample_size)]
boid_x_velocities=[
        random.uniform(*boids_x_velocity_lims) for x in range(sample_size)]
boid_y_velocities=[
        random.uniform(*boids_y_velocity_lims) for x in range(sample_size)]
boids=(boids_x,boids_y,boid_x_velocities,boid_y_velocities)

def update_boids(boids):
	xs,ys,xvs,yvs=boids
	# Fly towards the middle
	for i in range(len(xs)):
		for j in range(len(xs)):
			xvs[i]=xvs[i]+(xs[j]-xs[i])*0.01/len(xs)
			yvs[i]=yvs[i]+(ys[j]-ys[i])*0.01/len(xs)
	# Fly away from nearby boids
        fly_nbh = 100
	for i in range(len(xs)):
		for j in range(len(xs)):
			if (xs[j]-xs[i])**2 + (ys[j]-ys[i])**2 < fly_nbh:
				xvs[i]=xvs[i]+(xs[i]-xs[j])
				yvs[i]=yvs[i]+(ys[i]-ys[j])
	# Try to match speed with nearby boids
        speed_nbh = 10000
	for i in range(len(xs)):
		for j in range(len(xs)):
			if (xs[j]-xs[i])**2 + (ys[j]-ys[i])**2 < speed_nbh:
				xvs[i]=xvs[i]+(xvs[j]-xvs[i])*0.125/len(xs)
				yvs[i]=yvs[i]+(yvs[j]-yvs[i])*0.125/len(xs)
	# Move according to velocities
	for i in range(len(xs)):
		xs[i]=xs[i]+xvs[i]
		ys[i]=ys[i]+yvs[i]

figure=plt.figure()
plt_limits = (-500,1500)
axes=plt.axes(xlim=plt_limits, ylim=plt_limits)
scatter=axes.scatter(boids[0],boids[1])

def animate(frame):
   update_boids(boids)
   scatter.set_offsets(list(zip(boids[0],boids[1])))

animation_frames = 50
animation_interval = 50
anim = animation.FuncAnimation(figure, animate, frames=animation_frames,
        interval=animation_interval)

if __name__ == "__main__":
    plt.show()
