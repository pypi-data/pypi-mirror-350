# Dash Background Manager Redis

Redis-based background callback manager for Dash applications.

## Version Compatibility

- **Version 0.1.x**: Compatible with Dash 2.x (2.0.0 <= dash < 3.0.0)
- **Version 0.2.x**: Compatible with Dash 3.x (dash >= 3.0.0)

## Installation

```bash
pip install dash-bgmgr-redis
```

> **Note:** This configuration is recommended for development environments. For production, consider using Redis Cluster, Redis Sentinel, or other high-availability solutions with proper connection parameters, security settings, and monitoring.


## Features

- Redis-based background task management
- Cache support with configurable expiration
- Easy integration with existing Dash applications


## Quick Start

```python
from dash_bgmgr_redis import NewRedisBgManager

# Create Redis background manager
bg_mgr = NewRedisBgManager(
    redisUrl="redis://localhost:6379/0",
    prefix="myapp:",
    expire=3600
)

# Use with Dash app
app = dash.Dash(__name__, background_callback_manager=bg_mgr)
```

## Requirements

- Python 3.7+
- dash>=3.0.0,<4.0.0
- redis>=4.0.0
- psutil>=5.0.0
- multiprocess>=0.70.0

## Usage

### Basic Usage

```python
import dash
from dash import html, dcc, Input, Output, callback
from dash_bgmgr_redis import NewRedisBgManager
import time

# Setup background manager (development example)
bg_mgr = NewRedisBgManager(redisUrl="redis://localhost:6379/0")
app = dash.Dash(__name__, background_callback_manager=bg_mgr)

@callback(
    Output("result", "children"),
    Input("button", "n_clicks"),
    background=True,
    running=[(Output("button", "disabled"), True, False)],
    progress=[Output("progress", "value"), Output("progress", "max")],
)
def long_task(set_progress, n_clicks):
    if not n_clicks:
        return "Click the button to start"
    
    total = 10
    for i in range(total):
        time.sleep(1)
        set_progress((i + 1, total))
    
    return f"Task completed! Button clicked {n_clicks} times"

app.layout = html.Div([
    html.Button("Start Task", id="button"),
    dcc.Progress(id="progress"),
    html.Div(id="result")
])

if __name__ == "__main__":
    app.run_server(debug=True)
```

### Advanced Usage with Caching

```python
from dash_bgmgr_redis import RedisCache, RedisBgManager

# Create cache instance
cache = RedisCache(
    redis_url="redis://localhost:6379/0",
    prefix="cache:",
    expire=3600
)

# Create manager with cache
bg_mgr = RedisBgManager(
    cache=cache,
    cacheBy=[lambda: "user_session_id"],
    expire=1800
)
```

## API Reference

### NewRedisBgManager

Quick setup function for Redis background manager.

**Parameters:**
- `redisUrl` (str): Redis connection URL
- `prefix` (str, optional): Key prefix for Redis entries. Default: 'app:'
- `expire` (int, optional): Default expiration time in seconds. Default: 3600
- `cacheBy` (list, optional): Cache key functions
- `**kwargs`: Additional Redis connection parameters

### RedisCache

Redis-based cache implementation.

**Parameters:**
- `redis_url` (str): Redis connection URL
- `prefix` (str, optional): Key prefix. Default: 'cache:'
- `expire` (int, optional): Default expiration time
- `**kwargs`: Additional Redis parameters

**Methods:**
- `set(key, value, expire=None)`: Store value
- `get(key, default=None)`: Retrieve value
- `delete(key)`: Remove key
- `clear()`: Clear all keys with prefix
- `touch(key, expire=None)`: Update expiration

### RedisBgManager

Main background callback manager class.

**Parameters:**
- `cache` (RedisCache): Redis cache instance
- `cacheBy` (list, optional): Cache key functions
- `expire` (int, optional): Cache expiration time

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
