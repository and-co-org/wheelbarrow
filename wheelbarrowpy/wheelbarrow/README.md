
# wheelbarrow
our wheelbarrow. shared tooling, utils, and scripts. 

## Installation
For a local, editable installation:
```bash
uv pip install -e . --system
```

## Usage 

### `albert.pickle_memoize`

```python
from wheelbarrow.albert import pickle_memoize

def make_data():
    # computationally expensive process
    return np.random.rand(100, 100)

data = pickle_memoize("data.pkl", make_data)    # will cache in memory and on disk 
```