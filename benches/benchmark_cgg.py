import numpy as np

import cgpolyencode
encoder = cgpolyencode.GPolyEncoder()

# London bounding box
N = 51.691874116909894
E = 0.3340155643740321
S = 51.28676016315085
W = -0.5103750689005356

num_coords = 1000
coords = zip(
    np.random.uniform(S, N, [num_coords]),
    np.random.uniform(W, E, [num_coords])
    ) 

if __name__ == "__main__":
    for x in range(500):
        encoder.encode(coords)
