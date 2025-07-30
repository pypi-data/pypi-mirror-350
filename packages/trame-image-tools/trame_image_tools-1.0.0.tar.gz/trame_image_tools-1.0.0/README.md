# `trame-image-tools`

A set of [`trame`](https://github.com/kitware/trame) widgets to create a zoom and pan 2D image environment that includes interactive area selection widgets.

![demo_image](demo.png)

## Install
```bash
pip install trame-image-tools
```

## Usage
```python
from trame_image_tools.widgets import (
    TrameImage,
    TrameImageRoi,
    TrameImageLine,
    TrameImageCircle,
    TrameImagePolygon,
    TrameImageGrid,
)

with TrameImage(
    src="https://www.kitware.com/main/wp-content/uploads/2023/10/logo-trame.png",
    size=("size", [800, 210]),
):
    TrameImageGrid(
        spacing=("grid_spacing", [50, 25]),  # [x_tick_spacing, y_tick_spacing]
    )

    TrameImageLine(
        v_model=("line", [200, 50, 300, 150]),  # [x0, y0, x1, y1, ...]
    )

    TrameImageRoi(
        v_model=("roi", [350, 50, 100, 100]),  # [x, y, width, height]
    )

    TrameImageCircle(
        v_model=("circle", [550, 100, 50]),  # [x, y, radius]
    )

    TrameImagePolygon(
        v_model=("polygon", [650, 90, 670, 150, 730, 150, 750, 90, 700, 50]),  # [x0, y0, x1, y1, ...]
    )
```
