# Quick Start Guide

```python .md#_
from pptxlib import App
App().presentations.close()
```

This guide demonstrates the core features of pptxlib through practical examples.
You'll learn how to create a presentation with multiple slides and shapes.

## Creating a New App

Initialize the PowerPoint application using the [`App`][pptxlib.app.App] class:

```python exec="1" source="material-block"
from pptxlib import App

app = App()
app
```

Access the collection of presentations through the
[`presentations`][pptxlib.presentation.Presentations] attribute:

```python exec="1" source="material-block"
app.presentations
```

## Creating a New Presentation

Create a new presentation using the
[`add`][pptxlib.presentation.Presentations.add] method:

```python exec="1" source="material-block"
pr = app.presentations.add()
pr
```

Access specific presentations by index:

```python exec="1" source="material-block"
app.presentations[0]
```

## Adding a Title Slide

Create a title slide by specifying the `"Title"` layout:

```python exec="1" source="material-block"
slide = pr.slides.add(layout="Title")
slide.title = "Welcome to pptxlib"
```

Verify the slide collection and title:

```python exec="1" source="material-block"
pr.slides
```

```python exec="1" source="material-block"
pr.slides[0].title
```

## Adding Content Slides

Add content slides with different layouts:

```python exec="1" source="material-block"
slide = pr.slides.add(layout="TitleOnly")
slide.title = "First Slide"
```

The layout parameter is optional - it defaults to the previous slide's layout:

```python exec="1" source="material-block"
slide = pr.slides.add()
slide.title = "Second Slide"
```

View all slides in the presentation:

```python exec="1" source="material-block"
pr.slides
```

## Selecting Slides

Select a slide for display:

```python exec="1" source="material-block"
slide.select()
```

Clear the selection:

```python exec="1" source="material-block"
app.unselect()
```

## Working with Shapes

Add a rectangle shape to the slide with precise positioning:

```python exec="1" source="material-block"
shape = slide.shapes.add("Rectangle", 100, 100, 200, 100)
shape
```

## Quit the App

Always ensure proper cleanup by quitting the application:

```python exec="1" source="material-block"
app.quit()
```
