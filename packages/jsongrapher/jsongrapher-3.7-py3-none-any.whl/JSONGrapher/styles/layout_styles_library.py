#This is a simple file for storing the automatically loaded trace_styles_collection dictionary for JSONGrapher.
#It is not recommended that a person overwrite this file.

#each dictionary below, like "default" or "Nature" is one 'layout_style'.
#Currently, the style names are case sensitive. In the future, it is likely they will not be case sensitive.
styles_library = {
        "default": {
            "layout": {
                "title": {"font": {"size": 32}, "x": 0.5},
                "xaxis": {"title": {"font": {"size": 27}}, "tickfont": {"size": 23}},
                "yaxis": {"title": {"font": {"size": 27}}, "tickfont": {"size": 23}},
                "legend": {
                    "title": {"font": {"size": 22}},
                    "font": {"size": 22}
                }
            }
        },
        "default3d": {
            "layout": {
                "title": {"font": {"size": 32}, "x": 0.5},
                "xaxis": {"title": {"font": {"size": 12}}, "tickfont": {"size": 12}},
                "yaxis": {"title": {"font": {"size": 12}}, "tickfont": {"size": 12}},
                "zaxis": {"title": {"font": {"size": 12}}, "tickfont": {"size": 12}},
                "legend": {
                    "title": {"font": {"size": 22}},
                    "font": {"size": 22}
                }
            }
        },
        "Nature": {
            "layout": {
                "title": {"font": {"size": 32, "family": "Times New Roman", "color": "black"}},
                "font": {"size": 25, "family": "Times New Roman"},
                "paper_bgcolor": "white",
                "plot_bgcolor": "white",
                "xaxis": {
                    "showgrid": True, "gridcolor": "#ddd", "gridwidth": 1,
                    "linecolor": "black", "linewidth": 2, "ticks": "outside",
                    "tickwidth": 2, "tickcolor": "black"
                },
                "yaxis": {
                    "showgrid": True, "gridcolor": "#ddd", "gridwidth": 1,
                    "linecolor": "black", "linewidth": 2, "ticks": "outside",
                    "tickwidth": 2, "tickcolor": "black"
                }
            }
        },
        "Science": {
            "layout": {
                "title": {"font": {"size": 32, "family": "Arial", "color": "black"}},
                "font": {"size": 25, "family": "Arial"},
                "paper_bgcolor": "white",
                "plot_bgcolor": "white",
                "xaxis": {
                    "showgrid": True, "gridcolor": "#ccc", "gridwidth": 1,
                    "linecolor": "black", "linewidth": 2, "ticks": "outside",
                    "tickwidth": 2, "tickcolor": "black"
                },
                "yaxis": {
                    "showgrid": True, "gridcolor": "#ccc", "gridwidth": 1,
                    "linecolor": "black", "linewidth": 2, "ticks": "outside",
                    "tickwidth": 2, "tickcolor": "black"
                }
            }
        }
    }


