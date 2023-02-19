import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Generate mandelbrot set
def mandelbrot(c, maxiter):
    z = c
    for n in range(maxiter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return 0

# Generate grid
def mandelbrot_set(xmin, xmax, ymin, ymax, xn, yn, maxiter, horizon=2.0):
    X = np.linspace(xmin, xmax, xn, dtype=np.float32)
    Y = np.linspace(ymin, ymax, yn, dtype=np.float32)
    C = X + Y[:, None]*1j
    N = np.zeros(C.shape, dtype=int)
    for i in range(xn):
        for j in range(yn):
            N[j, i] = mandelbrot(C[j, i], maxiter)
    N = np.ma.masked_equal(N, 0)
    return X, Y, N

# Generate image
def mandelbrot_image():
    X, Y, N = mandelbrot_set(-2.25, 0.75, -1.25, 1.25, 3000, 3000, 80)
    plt.figure(figsize=(10, 10))
    plt.axis('off')
    plt.imshow(N, interpolation='nearest', cmap='hot')
    plt.savefig('mandelbrot.png')

# Generate data
def mandelbrot_data():
    X, Y, N = mandelbrot_set(-2.25, 0.75, -1.25, 1.25, 3000, 3000, 80)
    df = pd.DataFrame({'x': X, 'y': Y, 'n': N})
    df.to_csv('mandelbrot.csv', index=False)

# Generate heatmap
def mandelbrot_heatmap():
    df = pd.read_csv('mandelbrot.csv')
    df = df.pivot('y', 'x', 'n')
    plt.figure(figsize=(10, 10))
    sns.heatmap(df)
    plt.savefig('mandelbrot_heatmap.png')

# Generate animation
def mandelbrot_animation():
    from matplotlib import animation
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.axis('off')
    ax.set(xlim=(-2.25, 0.75), ylim=(-1.25, 1.25))
    im = ax.imshow(np.zeros((3000, 3000)), interpolation='nearest', cmap='hot')
    def animate(i):
        X, Y, N = mandelbrot_set(-2.25, 0.75, -1.25, 1.25, 3000, 3000, i)
        im.set_data(N)
    anim = animation.FuncAnimation(fig, animate, frames=80, interval=50)
    anim.save('mandelbrot_animation.gif', writer='imagemagick', fps=20)

# run code
if __name__ == '__main__':
    mandelbrot_image()
    mandelbrot_data()
    mandelbrot_heatmap()
    mandelbrot_animation()