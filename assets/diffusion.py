import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.ndimage import maximum_filter


L = 100
T = 100
N = 100
M = 1000
R = 30
# DISK_POSITION = (5 * L / 6, L / 2)
DISK_POSITION = (L / 2, L / 2)

dt = T / M
dx = L / N
c = dt / dx**2
x = np.linspace(0, L, N)
y = np.linspace(0, L, N)


def disk(x, y, r=R):
    return np.sqrt((x - DISK_POSITION[0]) ** 2 + (y - DISK_POSITION[1]) ** 2) < r


def starfish(x, y):
    frequency = 5
    amplitude = 0.2
    scale = R
    r = np.sqrt((x - DISK_POSITION[0]) ** 2 + (y - DISK_POSITION[1]) ** 2)
    offset = 1 + amplitude * np.sin(
        frequency * np.arctan2(y - DISK_POSITION[1], x - DISK_POSITION[0])
    )

    return r < scale * offset


def hollow_disk(x, y):
    return disk(x, y) and not disk(x, y, r=R / 2)


def find_edges(domain):
    kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    boundaries = signal.convolve2d(domain, kernel, mode="same")
    return (boundaries > 0) & (domain == 0)


def reflect_at_edges(u, domain):
    edges = find_edges(domain)
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    reflected_u = u.copy()

    for d_row, d_col in directions:
        shifted_domain = np.roll(domain, shift=(d_row, d_col), axis=(0, 1)).astype(bool)
        shifted_u = np.roll(u, shift=(d_row, d_col), axis=(0, 1))
        mask = edges & shifted_domain
        reflected_u[mask] = shifted_u[mask]

    return reflected_u


def solve_diffusion(u):
    for k in range(M):
        u[1:-1, 1:-1] += c * (
            u[2:, 1:-1] + u[:-2, 1:-1] + u[1:-1, 2:] + u[1:-1, :-2] - 4 * u[1:-1, 1:-1]
        )
    return u


def solve_diffusion2(u, boundary="fill"):
    filter = np.array([[0, c, 0], [c, 1 - 4 * c, c], [0, c, 0]])
    for k in range(M):
        u = signal.convolve2d(u, filter, mode="same", boundary=boundary)
    return u


def solve_diffusion3(u, domain):
    filter = np.array([[0, c, 0], [c, 1 - 4 * c, c], [0, c, 0]])
    for k in range(M):
        u = reflect_at_edges(u, domain)
        u = signal.convolve2d(u, filter, mode="same", boundary="symm")
        u = np.where(domain, u, 0)

    return u


domain = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        domain[i, j] = hollow_disk(x[i], y[j])

u = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        u[i, j] = domain[i, j] if i >= N // 2 else 0


fig, ax = plt.subplots(1, 2)

ax[0].imshow(u)
ax[0].set_title("t=0")
ax[0].axis("off")

print(u.sum())
u = solve_diffusion3(u, domain)
print(u.sum())
ax[1].set_title("t=100")
ax[1].imshow(u)
ax[1].axis("off")

plt.show()
# plt.tight_layout()
# plt.savefig("diffusion_hollow_disk.png", bbox_inches="tight")
