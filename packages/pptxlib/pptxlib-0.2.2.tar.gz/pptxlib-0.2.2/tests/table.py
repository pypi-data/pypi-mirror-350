from __future__ import annotations

from datetime import datetime

from pptxlib.app import App
from pptxlib.gantt import GanttChart


def main():
    app = App()
    app.presentations.close()
    pr = app.presentations.add()
    gantt = GanttChart("week", datetime(2025, 5, 21), datetime(2025, 6, 10))
    layout = pr.layouts.add(gantt.frame.name)
    gantt.add_table(layout, 20, 150, bottom=20)
    slide = pr.slides.add(layout=layout)
    gantt.slide = slide
    s1 = gantt.add(datetime(2025, 5, 21), 20)
    s1.font.set(size=12, color="yellow")
    s2 = gantt.add(datetime(2025, 5, 26), 30, color="red")
    s2.font.set(size=12)
    s1.connect(s2).line.set(color="pink", weight=6)

    # # for cell in table.rows[0]:
    # #     cell.shape.font.set(size=10)
    # table.reset_style()

    # texts = ["", "a", "a", "a", "b", "b", "c", "c", "c"]
    # table.rows[0].text(texts, size=22, bold=True, merge=True)

    # print(table.api.Table.Range)

    # api.Fill.ForeColor.RGB = 255
    # api.Fill.Transparency = 0.5
    # rng = ShapeRange(api, row.parent.parent, row.parent.collection)
    # rng.fill.set(color="red", alpha=0.5)
    # rng.app.unselect()

    # rng = table.select()
    # table.api.Table.Cells.Select()
    # api = table.app.api.ActiveWindow.Selection.TextRange
    # api.Font.Size = 10
    # print("a", api)

    # rng.font.set(size=10)
    # rng.fill.set(color="red", alpha=0.5)
    # rng.app.unselect()
    # table.rows[1].api.Select()
    # table.app.api.ActiveWindow.Selection.ShapeRange.Fill.Transparency = 0.5
    # rng = table.select()
    # rng.fill.set(color="red", alpha=0.5)
    # table.app.unselect()

    # table.clear()
    # table.fill.set(color="red", alpha=0.5)
    # print(table.shapes)

    # table.fill("red", alpha=0.5)
    # table.columns[1].fill("blue", alpha=0.5)
    # table.rows.height = [40, 40]
    # for i in range(4):
    #     table[0].borders[i].set(color="red", weight=5, alpha=0.5)
    # table[1, 1].borders[0].set(color="red", weight=5, alpha=0.5)
    # table.columns.borders["bottom"].set(color="green", weight=5, alpha=0.5)
    # table[1].borders["left"].set(color="green", weight=5, alpha=0.5)

    # c = table[0, 0]
    # c.text = "abc"
    # for c in table.columns:
    #     c.width = 100

    # s.select()
    # table.fill("red", (0, 0), (1, 2))
    # print(table[0, 0].shape.api.Fill.Transparency)
    # table[0, 0].shape.api.Fill.Transparency = 1


if __name__ == "__main__":
    main()
