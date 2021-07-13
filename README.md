# Game-of-Life

GoL is the first attempt. It is non-interactive, i.e., you have to specify the points individually in the code which you want to start with life in them. It then runs and displays using matplotlib

The second attempt was made using PyGame. You can use your mouse to add/remove life in the grid and press a key to start and stop the evolution. The nature of PyGame makes adding interactive buttons a little difficult and the implementation can be clunky, so I made another attempt.

The third iteration uses tkinter. It removes the need for bound keys which need instructions by adding buttons and a sidebar. Life can still be added/removed using the mouse left and right buttons.

The core idea behind time evolution is same in all 3 cases. I represent the visible world using a 2D numpy array called grid with 0 denoting no life and 1 denoting the presence of life. I then define a 3x3 'neighbourhood kernel' with all ones except at the center. Convolving the kernel with the grid with 0 padding to keep the convolution the same size as grid gives the 'neighbour map' which gives the live neighbours adjacent to that cell. Using the grid and neighbour map, we can implement the rules of the game and generate a new grid for the evolution of the next generation.
