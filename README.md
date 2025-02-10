# pyzitadelle

<a id="readme-top"></a> 

<div align="center">  
  <p align="center">
    PyZITADELLE is a quick asynchronous framework for testing python applications
    <br />
    <a href="https://alexeev-prog.github.io/pyzitadelle/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#-why-choose-pyzitadelle">Why Choose pyzitadelle?</a>
    ·
    <a href="#-key-features">Key Features</a>
    ·
    <a href="#-getting-started">Getting Started</a>
    ·
    <a href="#-usage-examples">Basic Usage</a>
    ·
    <a href="#-specifications">Specification</a>
    ·
    <a href="https://alexeev-prog.github.io/pyzitadelle/">Documentation</a>
    ·
    <a href="https://github.com/alexeev-prog/pyzitadelle/blob/main/LICENSE">License</a>
  </p>
</div>
<br>
<p align="center">
    <img src="https://img.shields.io/github/languages/top/alexeev-prog/pyzitadelle?style=for-the-badge">
    <img src="https://img.shields.io/github/languages/count/alexeev-prog/pyzitadelle?style=for-the-badge">
    <img src="https://img.shields.io/github/license/alexeev-prog/pyzitadelle?style=for-the-badge">
    <img src="https://img.shields.io/github/stars/alexeev-prog/pyzitadelle?style=for-the-badge">
    <img src="https://img.shields.io/github/issues/alexeev-prog/pyzitadelle?style=for-the-badge">
    <img src="https://img.shields.io/github/last-commit/alexeev-prog/pyzitadelle?style=for-the-badge">
</p>


## Check Other My Projects

 + [SQLSymphony](https://github.com/alexeev-prog/SQLSymphony) - simple and fast ORM in sqlite (and you can add other DBMS)
 + [Burn-Build](https://github.com/alexeev-prog/burn-build) - simple and fast build system written in python for C/C++ and other projects. With multiprocessing, project creation and caches!
 + [OptiArch](https://github.com/alexeev-prog/optiarch) - shell script for fast optimization of Arch Linux
 + [libnumerixpp](https://github.com/alexeev-prog/libnumerixpp) - a Powerful C++ Library for High-Performance Numerical Computing
 + [libnumerixpy](https://github.com/alexeev-prog/libnumerixpy) - a Powerful Python Library for High-Performance Numerical Computing
 + [pycolor-palette](https://github.com/alexeev-prog/pycolor-palette) - display beautiful log messages, logging, debugging.
 + [shegang](https://github.com/alexeev-prog/shegang) - powerful command interpreter (shell) for linux written in C
 + [pyEchoNext](https://github.com/alexeev-prog/pyEchoNext) - lightweight, fast and scalable web framework for Python

## 🤔 Why Choose PyZitadelle?

- **🔥 Featherweight Performance**: No bloat, just speed! Our framework is designed to optimize performance, making it a breeze to create and scale your applications without the overhead.
  
- **💼 Unmatched Scalability**: Handle thousands of connections effortlessly! Echonext is built for performance in high-demand environments, making it the perfect choice for startups or enterprise applications.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 📚 Key Features

- Intuitive API: Pythonic, object-oriented interface for interacting with routes and views.
- Performance Optimization: Lazy loading, eager loading, and other techniques for efficient web queries.
- Comprehensive Documentation: Detailed usage examples and API reference to help you get started.
- Modular Design: Clean, maintainable codebase that follows best software engineering practices.
- Extensive Test Coverage: Robust test suite to ensure the library's reliability and stability.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🚀 Getting Started

pyEchoNext is available on [PyPI](https://pypi.org/project/pyzitadelle). Simply install the package into your project environment with PIP:

```bash
pip install pyzitadelle
```

Once installed, you can start using the library in your Python projects. Check out the [documentation](https://alexeev-prog.github.io/pyzitadelle) for detailed usage examples and API reference.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 💻 Usage Examples
You can view examples at [examples directory](./examples).

```python
ffrom pyzitadelle.standard import Argument
from pyzitadelle.test_case import TestCase, expect, expectfail, skip

firstcase = TestCase()
debug = False


def add(a: int, b: int) -> int:
  return a + b


@firstcase.test(comment="async test example", count_of_launchs=2)
async def example_test1(a: int = 2):
  expect(add(1, a), a + 1, "1 + 2 should be equal to 3")
  return a + 1


@firstcase.test(
  comment="example with Argument",
  tags=["assert"],
  arguments=(Argument(args=[2]), Argument(args=[3])),
)
def example_test2(a: int):
  assert add(a, 2) == a + 2
  return a + 2


@skip
@firstcase.test()
def example_test3():
  expect(add(1, 2), 4, "1 + 2 should be equal to 3")
  return 4


@firstcase.test()
@skip(reason="not completed", when=debug)
def example_test4():
  expect(add(10, 2), 12, "10 + 2 should be equal to 12")
  return 12


@firstcase.test(comment="use each", tags=["assert"])
@expectfail("each dont work")
def example_test5(a: int = 2):
  assert add(1, a) == a + 2
  return a + 1


@firstcase.test(tags=["assert"])
def example_test6():
  assert add(20, 40) == 60
  return 60


firstcase.run()
```

### Debug

```python
from pyzitadelle.debug import debug_measurement


def fac(n):
  if n == 1:
    return 1
  return fac(n - 1) * n


@debug_measurement("ex_debug")
def test(num: int):
  for i in range(num**5):
    num = num**i

  return num


print(test(6))

```

### Simplest

```python
from pyzitadelle.test_case import TestCase, expect

firstcase = TestCase()


def add(a: int, b: int) -> int:
  return a + b


@firstcase.test()
async def example_test1():
  expect(add(1, 2), 3, "1 + 2 should be equal to 3")


@firstcase.test()
def example_test2():
  expect(add(1, 2), 3, "1 + 2 should be equal to 3")


@firstcase.test()
def example_test3():
  expect(add(1, 2), 3, "1 + 2 should be equal to 3")


@firstcase.test()
def example_test4():
  expect(add(10, 2), 12, "10 + 2 should be equal to 12")


@firstcase.test()
def example_test5():
  assert add(1, 2) == 3


firstcase.run()

```


## 💻 Specifications

```
pyzitadelle/
├── coverage.py
├── debug
│  ├── __init__.py
│  └── measurement.py
├── exceptions.py
├── fixtures.py
├── __init__.py
├── reporter.py
├── sessions.py
├── standard.py
├── test_case.py
└── utils.py

2 directories, 11 files
```
