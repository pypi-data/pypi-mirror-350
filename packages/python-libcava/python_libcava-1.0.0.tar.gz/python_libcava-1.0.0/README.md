# python-libcava
CAVA audio visualizer bindings for python using FIFO

python-libcava should be thread-safe. However this hasn't been thoroughly tested.

# Usage

```python
# Print the pillars for 5 seconds
from libcava import CAVA
from time import sleep

def simple_callback(sample: list[float]):
    # sample: (0.0,1.0,...)
    print(sample)

cava = CAVA(
    bars = 10, # The amount of bars ("pillars") per sample
    callback = simple_callback # Callback function that will receive samples ranging 0-1 
)

cava.start()
sleep(3)
cava.close() # Close the FIFO listener
```

## Adding extra config to [general]

```python
cava = CAVA(
    config="sensitivity = 0"
    # Will be added under [general]
)
```