from __future__ import annotations

from pptxlib.app import App


def main():
    app = App()
    app.presentations.close()
    pr = app.presentations.add().size(400, 300)

    slide = pr.slides.add()
    shapes = slide.shapes
    s1 = shapes.add("Rectangle", 100, 100, 100, 100)
    s2 = shapes.add("Oval", 150, 150, 90, 80)
    s1.select()
    rng = s2.select(replace=False)
    rng.app.unselect()
    rng.fill.set(color="red", alpha=0.5)


if __name__ == "__main__":
    main()
