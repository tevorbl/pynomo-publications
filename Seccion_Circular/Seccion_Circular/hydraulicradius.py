"""
    newhydraulicradius.py

    Nomograph to calculate hydraulic radius of unity radius circular pipe

    Copyright (C) 2023 Daniel Boulet.0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
import numpy as np
from pyx import *

outputfile = sys.argv[0].split(".")[0] + ".pdf"
sys.path.insert(0, "..")
text.set(text.LatexEngine)

from pynomo.nomographer import Nomographer


def height2theta(u):
    return 2.0 * np.arccos(1 - u / 100 * 2.0)


N_params_1 = {
    "u_min": -1.0,
    "u_max": +1.0,
    "function": lambda u: u,
    # "title": r"$u$",
    "tick_levels": 1,
    "tick_text_levels": 1,
    "scale_type": "manual arrow",
    "tick_side": "left",
    "manual_axis_data": {0: "Start"},
    "arrow_length": 1.0,
    # 'reference':True
}

N_params_2 = {
    "u_min": 0.0,
    "u_max": 0.65,
    "function": lambda u: 2 * u - 1,
    "title": r"$\frac{R_h}{r}$",
    "tick_levels": 3,
    "tick_text_levels": 2,
    "tick_side": "left",
}

N_params_3 = {
    "u_min": 0.0,
    "u_max": 99.9999,
    "function_3": lambda u: height2theta(u),
    "function_4": lambda u: np.sin(height2theta(u)),
    "title": r"Fluid height ($\%$ of total)",
    "tick_levels": 4,
    "tick_text_levels": 3,
    "scale_type": "linear smart",
    "title_draw_center": True,
}

block_1_params = {
    "block_type": "type_10",
    # "width": 10.0,
    # "height": 10.0,
    "f1_params": N_params_1,
    "f2_params": N_params_2,
    "f3_params": N_params_3,
    "isopleth_values": [
        [0, "x", 25],
        [0, "x", 75],
        [0, 0.2, "x"],
        [0, 0.5, "x"],
        [0, 0.35, "x"],
    ],
}


def post(c):
    center = (14, 3)
    radius = 2.5
    phi = (np.deg2rad(180 + 30), np.deg2rad(-30))
    p1 = (radius * np.cos(phi[0]) + center[0], radius * np.sin(phi[0]) + center[1])
    p2 = (radius * np.cos(phi[1]) + center[0], radius * np.sin(phi[1]) + center[1])
    c.stroke(
        path.circle(center[0], center[1], radius),
        [style.linewidth.thick, style.linestyle.solid, color.cmyk.Sepia],
    )
    c.stroke(
        path.line(center[0], center[1], p1[0], p1[1]),
        [style.linewidth.thin, style.linestyle.dashed, color.cmyk.Sepia],
    )
    c.stroke(
        path.line(center[0], center[1], p2[0], p2[1]),
        [style.linewidth.thin, style.linestyle.dashed, color.cmyk.Sepia],
    )
    c.stroke(
        path.line(p1[0], p1[1], p2[0], p2[1]),
        [style.linewidth.thick, style.linestyle.solid, color.cmyk.Sepia],
    )
    c.stroke(
        path.path(path.arc(center[0], center[1], radius * 0.25, 210, 330)),
        [style.linewidth.thick, style.linestyle.solid, color.cmyk.Sepia],
    )
    c.stroke(
        path.path(path.arc(center[0], center[1], radius + 0.1, 210, 330)),
        [style.linewidth.thick, style.linestyle.solid, color.cmyk.Sepia],
    )
    c.text(
        center[0],
        center[1] - 1,
        r"$\theta$",
        [color.cmyk.Sepia],
    )
    c.text(
        center[0],
        center[1] - 2,
        r"\large $A$",
        [color.cmyk.Sepia],
    )
    c.text(
        center[0],
        center[1] - radius - 0.5,
        r"\large $P$",
        [color.cmyk.Sepia],
    )
    c.stroke(
        path.line(
            center[0] + radius + 0.4,
            center[1] - radius,
            center[0] + radius + 0.4,
            center[1] + radius,
        ),
        [style.linewidth.thin, style.linestyle.solid, color.cmyk.Sepia],
    )
    c.text(
        center[0] + radius + 1 - 0.5,
        center[1],
        r"\large $H$",
        [color.cmyk.Sepia],
    )

    c.stroke(
        path.line(
            center[0] - radius - 0.4,
            center[1] - radius,
            center[0] - radius - 0.4,
            p1[1],
        ),
        [style.linewidth.thin, style.linestyle.solid, color.cmyk.Sepia],
    )
    c.text(
        center[0] - radius - 1 + 0.2,
        p1[1] - 0.75,
        r"\large $h$",
        [color.cmyk.Sepia],
    )


main_params = {
    "filename": outputfile,
    # "paper_height": 10.0,
    # "paper_width": 10.0,
    "block_params": [block_1_params],
    "transformations": [("rotate", 0.01), ("scale paper",)],
    # "title_str": r"$u+vw+w=0$",
    # "make_grid": True,
    "title_y": 23.0,
    "title_x": 5.0,
    "extra_texts": [
        {
            "x": 1.0,
            "y": 21.0,
            "text": r"\noindent \huge Hydraulic Radius \par \normalsize \medskip \noindent Nomograph to calculate hydraulic radius in unity-radius pipe as a percentage of total capacity. \par \medskip   \noindent \copyright    Daniel Boulet  2023",
            "width": 7.50,
        },
        {
            "x": 1.0,
            "y": 18,
            "text": r"\noindent Instructions: \
				\par \normalsize \medskip \noindent Draw a line from the ``Start'' through fluid height (as a percentage of maximum) to determine $R_h$ per unit radius.",
            "width": 10.0,
        },
        {
            "x": 1.0,
            "y": 6,
            "text": r"\noindent \large Theory: \
				\par \medskip \noindent \normalsize Hydraulic radius of a circular pipe is given by the formula: \
				\par \medskip \noindent \Large $R_h = \frac{A}{P}$ \
				\medskip \par \noindent \normalsize where $R_h$ is the hydraulic radius, $A$ is the cross-sectional area of the flow and $P$ is the \
				``wetted'' perimeter. \
				\par \medskip \noindent \normalsize The cross-sectional area of flow is given by the formula: \
				\par \medskip \noindent \Large $A=\frac{\theta - sin(\theta)}{2}$ \par \medskip \normalsize \noindent and ``wetted'' perimeter is \
				\par \medskip \noindent \Large $P=\theta$. \normalsize \par \medskip \normalsize \noindent Finally, $\theta$ (in radians) is determined by the following formula: \
				\par \medskip \noindent \Large $\theta=2 \times \arccos(1-2 \times \frac{h}{H})$.",
            # \par \medksip \noindent \normalsize and \par \medskip \noindent \Large $P=A$",
            "width": 10.0,
        },
    ],
    "post_func": post,
}
Nomographer(main_params)
