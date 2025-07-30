# Progbarr
[![PyPI - Version](https://img.shields.io/pypi/v/progbarr)](https://pypi.org/project/progbarr/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/progbarr)](https://pypi.org/project/progbarr/)
[![License](https://img.shields.io/pypi/l/progbarr)](https://github.com/haripowesleyt/progbarr/blob/main/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/progbarr)](https://pypi.org/project/progbarr/)

Progbarr is a Python library for **efficiently** creating customizable progress bars in the console.

## Features
- Supports setting **any UNICODE character** for fill, placeholder, or borders
- Supports setting **foreground** and **background color**
- Supports **140+ [HTML color names](https://htmlcolorcodes.com/color-names/)**, **all RGB values**, and **all HEX color codes**

## Installation
```bash
pip install progbarr
```

## Usage
A progress bar is an instance of the `ProgressBar` class.

#### Syntax
```python
with ProgressBar(job, tasks, length, chars, color, bgcolor) as pb:
    for _ in range(tasks):
      # Perform some task
      pb.advance()
```

The table below explains the parameters of the `ProgressBar` constructor:

  | Parameter |Type| Purpose                          |
  |-----------|-|----------------------------------|
  | `job`     | `str`          | Overall job being done           | 
  | `tasks`   | `int`          | Number of tasks to be performed  | 
  | `length`  | `int`          | Length of the progress bar       | 
  | `chars`   | `str`          | Characters used by progress bar  |
  | `color`   | `str` / `None` | Foreground color of progress bar | 
  | `bgcolor` | `str` / `None` | Background color of progress bar | 

#### Notes
- `job` should be in **present participle form** e.g., *"Sleeping"* instead of *"Sleep"*.
- `length` should be **equal to or a factor** of `tasks` for a smooth progress.
- `chars` should be made up of **1 or more characters** (maximum 4) representing **fill**, **placeholder**, **border-left**, and **border-right**, respectively.
- `color` and `bgcolor` are both optional (default is `None`).

#### Example
```python
from time import sleep
from progbarr import ProgressBar

with ProgressBar("Sleeping", 5, 20, "# []", "green", "white") as pb:
    for _ in range(5):
        sleep(1)
        pb.advance()
```
![example](https://raw.githubusercontent.com/haripowesleyt/progbarr/main/assets/gifs/example.gif)

## Benchmarking
The main goal of **progbarr** is to take unnoticeable processing time when displaying a progress bar. This means that the time taken to do looped tasks without a progress bar is **approximately equal** to the time taken to do the tasks with a progress bar. Therefore, the overhead (if any) is negligible.

The example below shows the amount of time taken to perform a sleep of 1 second for 5 times with and without a progress bar.

```python
from time import sleep, time
from progbarr import ProgressBar


def benchmark_with_progressbar():
    with ProgressBar('Sleeping', 5, 20, '# []', None, None) as pb:
        for _ in range(5):
            sleep(1)
            pb.advance()


def benchmark_without_progressbar():
    for _ in range(5):
        sleep(1)


start_time_with_progressbar = time()
benchmark_with_progressbar()
stop_time_with_progressbar = time()

start_time_without_progressbar = time()
benchmark_without_progressbar()
stop_time_without_progressbar = time()

time_taken_with_progressbar = stop_time_with_progressbar - start_time_with_progressbar
time_taken_without_progressbar = stop_time_without_progressbar - start_time_without_progressbar

difference = time_taken_with_progressbar - time_taken_without_progressbar
overhead = round(difference/time_taken_without_progressbar*100,3)

print(f"With progress bar   : {time_taken_with_progressbar}")
print(f"Without progress bar: {time_taken_without_progressbar}")
print(f"Difference          : {difference}")
print(f"Overhead            : {overhead}%")
```

![benchmark](https://raw.githubusercontent.com/haripowesleyt/progbarr/main/assets/images/benchmark.png)

## License
This project is licensed under the **MIT License** – see the [LICENSE](https://raw.githubusercontent.com/haripowesleyt/progbarr/main/LICENSE) file for details.
