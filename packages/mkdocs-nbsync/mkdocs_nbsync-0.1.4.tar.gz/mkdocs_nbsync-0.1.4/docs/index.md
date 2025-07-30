# mkdocs-nbsync

<div class="grid cards" markdown>

- :material-notebook-edit: **Notebooks from Markdown**
  Extend standard markdown syntax to automatically generate notebooks from
  documentation
  [:octicons-arrow-right-24: Markdown Features](#notebooks-from-markdown)

- :material-language-python: **Python File Integration**
  Directly reference external Python files and reuse functions or classes
  [:octicons-arrow-right-24: Python Integration](#python-file-integration)

- :material-image-edit: **Code Execution in Images**
  Execute code within image notation for dynamic visualizations
  [:octicons-arrow-right-24: Dynamic Visualization](#code-execution-in-images)

- :material-refresh-auto: **Dynamic Updates**
  Real-time synchronization between notebooks and documentation
  [:octicons-arrow-right-24: Dynamic Updates](#dynamic-updates-and-execution)

</div>

## What is mkdocs-nbsync?

mkdocs-nbsync is an innovative MkDocs plugin that treats Jupyter notebooks,
Python scripts, and Markdown files as first-class citizens for
documentation. Unlike traditional approaches, mkdocs-nbsync provides equal
capabilities across all file formats, enabling seamless integration
and dynamic execution with real-time synchronization.

It solves common challenges faced by data scientists, researchers, and technical
writers:

- **Development happens in notebooks** - ideal for experimentation and visualization
- **Documentation lives in markdown** - perfect for narrative and explanation
- **Code resides in Python files** - organized and version-controlled
- **Traditional integration is challenging** - screenshots break, exports get outdated

## Inspiration & Comparison

mkdocs-nbsync was inspired by and builds upon the excellent work of two MkDocs
plugins:

- [**markdown-exec**](https://pawamoy.github.io/markdown-exec/) - Provides utilities to execute code blocks in Markdown files
- [**mkdocs-jupyter**](https://mkdocs-jupyter.danielfrg.com/) - Enables embedding Jupyter notebooks in MkDocs

While these plugins offer great functionality, mkdocs-nbsync takes a unified
approach by:

1. **Equal treatment** - Unlike other solutions that prioritize one format, mkdocs-nbsync treats Jupyter notebooks, Python scripts, and Markdown files equally as first-class citizens
2. **Real-time synchronization** - Changes to source files are immediately reflected in documentation
3. **Seamless integration** - Consistent syntax across all file formats allows for flexible documentation workflows
4. **Image syntax code execution** - Unique ability to execute code and embed visualizations anywhere Markdown image syntax (`![alt](url)`) is valid, including tables, lists, and complex layouts

## Acknowledgements

The development of mkdocs-nbsync would not have been possible without the
groundwork laid by markdown-exec and mkdocs-jupyter. We extend our
sincere gratitude to the developers of these projects for their
innovative contributions to the documentation ecosystem.

## Key Features

### Notebooks from Markdown

Extend standard markdown syntax to define notebook cells within your
documentation. Present code and its output results concisely with tabbed
display.

````markdown source="tabbed-nbsync"
```python .md#plot
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(2, 1))
ax.plot([1, 3, 3, 4])
```

![Plot result](){#plot source="above"}
````

### Python File Integration

Directly reference external Python files and reuse defined functions or
classes. Avoid code duplication and improve maintainability.

```python title="plot.py"
--8<-- "scripts/plot.py"
```

```markdown source="tabbed-nbsync"
![Plot result](plot.py){#sqrt source="on"}
```

### Code Execution in Images

Execute Python code directly within image notation and display the results.
This enables easy placement of dynamic visualizations in tables or complex
layouts.

```markdown source="tabbed-nbsync"
|         Sine          |        Cosine         |
| :-------------------: | :-------------------: |
| ![](){`plot(np.sin)`} | ![](){`plot(np.cos)`} |
```

### Code Execution with markdown-exec Style Syntax

mkdocs-nbsync supports the markdown-exec style code blocks with the `exec="1"`
attribute as a compatible approach to code execution. While this syntax
is familiar to markdown-exec users, mkdocs-nbsync executes it through the
Jupyter Notebook engine instead, providing the ability to render diverse
MIME content types (HTML, SVG, images, etc.) directly in your
documentation. This enables richer and more complex outputs than
traditional execution methods.

````markdown source="tabbed-nbsync"
```python exec="1" source="tabbed-left"
import numpy as np
from PIL import Image
x = np.random.randint(0, 255, (50, 200), dtype=np.uint8)
Image.fromarray(x)
```
````

### Dynamic Updates and Execution

Automatic synchronization between notebooks and documentation ensures code
changes are reflected in real-time. View changes instantly in MkDocs serve
mode.

## Getting Started

Follow these steps to get started with mkdocs-nbsync:

1. [Installation](getting-started/installation.md)
2. [Configuration](getting-started/configuration.md)
3. [First Steps](getting-started/first-steps.md)
