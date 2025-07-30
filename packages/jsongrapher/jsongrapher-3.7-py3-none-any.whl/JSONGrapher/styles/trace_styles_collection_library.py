#This is a simple file for storing the automatically loaded trace_styles_collection dictionary for JSONGrapher.
#It is not recommended that a person overwrite this file.

#each dictionary below is one 'trace_styles_collection'. "default" is the first one.
styles_library = {
    "default": {
        "scatter_spline": {
            "type": "scatter",
            "mode": "lines+markers",
            "line": {"shape": "spline", "width": 2},
            "marker": {"size": 10},
        },
        "scatter_line": {
            "type": "scatter",
            "mode": "lines+markers",
            "line": {"shape": "linear", "width": 2},
            "marker": {"size": 10},
        },
        "line": {
            "type": "scatter",
            "mode": "lines",
            "line": {"shape": "linear", "width": 2},
            "marker": {"size": 10},
        },
        "lines": {
            "type": "scatter",
            "mode": "lines",
            "line": {"shape": "linear", "width": 2},
            "marker": {"size": 10},
        },
        "scatter": {
            "type": "scatter",
            "mode": "markers",
            "marker": {"size": 10},
        },
        "bubble": {
            "type": "scatter",
            "mode": "markers",
            "marker": {
                            "color": "auto",
                            "colorscale": "viridis_r",
                            "showscale": True
                        }
        },        
        "spline": {
            "type": "scatter",
            "mode": "lines",
            "line": {"shape": "spline", "width": 2},
            "marker": {"size": 0},  # Hide markers for smooth curves
        },
        "bar": {
            "type": "bar",
            "marker": {
                            "color": "blue",
                            "opacity": 0.8,
                            "line": {
                                "color": "black",
                                "width": 2
                            }
                        },
        },
        "default": {
            "type": "scatter",
            "mode": "lines+markers",
            "line": {"shape": "spline", "width": 2},
            "marker": {"size": 10},
        },        
        "scatter3d": {
            "mode": "markers",
            "type": "scatter3d",
            "marker": {"color" : "","colorscale":"rainbow", "showscale":True}
        },
        "mesh3d": {
            "type": "mesh3d",
            "intensity" : [],
            "colorscale":"rainbow", 
            "showscale":True
        },
        "heatmap": {
            "type": "heatmap",
            "colorscale": "Viridis",
        }
    },
    "minimalist": {
        "scatter_spline": {
            "type": "scatter",
            "mode": "lines+markers",
            "line": {"shape": "spline", "width": 1},
            "marker": {"size": 6},
        },
        "scatter": {
            "type": "scatter",
            "mode": "lines",
            "line": {"shape": "linear", "width": 1},
            "marker": {"size": 0},
        },
        "spline": {
            "type": "scatter",
            "mode": "lines",
            "line": {"shape": "spline", "width": 1},
            "marker": {"size": 0},
        },
        "bar": {
            "type": "bar",
        },
        "heatmap": {
            "type": "heatmap",
            "colorscale": "Greys",
        }
    },
    "bold": {
        "scatter_spline": {
            "type": "scatter",
            "mode": "lines+markers",
            "line": {"shape": "spline", "width": 4},
            "marker": {"size": 10},
        },
        "scatter": {
            "type": "scatter",
            "mode": "lines+markers",
            "line": {"shape": "spline", "width": 4},
            "marker": {"size": 12},
        },
        "spline": {
            "type": "scatter",
            "mode": "lines",
            "line": {"shape": "spline", "width": 4},
            "marker": {"size": 0},
        },
        "bar": {
            "type": "bar",
        },
        "heatmap": {
            "type": "heatmap",
            "colorscale": "Jet",
        }
    },
    "scatter": { #this style forces all traces into scatter.
        "scatter_spline": {
            "type": "scatter",
            "mode": "markers",
            "marker": {"size": 10},
        },
        "scatter": {
            "type": "scatter",
            "mode": "markers",
            "marker": {"size": 10},
        },
        "spline": {
            "type": "scatter",
            "mode": "markers",
            "marker": {"size": 10},
        },
        "bar": {
            "type": "scatter",
            "mode": "markers",
            "marker": {"size": 10},
        },
        "heatmap": {
            "type": "heatmap",
            "colorscale": "Viridis",
        }
    },
    "scatter_spline": { #this style forces all traces into spline only
        "scatter_spline": {
            "type": "scatter",
            "mode": "lines+markers",
            "line": {"shape": "spline", "width": 2},
            "marker": {"size": 0},
        },
        "scatter": {
            "type": "scatter",
            "mode": "lines+markers",
            "line": {"shape": "spline", "width": 2},
            "marker": {"size": 0},
        },
        "spline": {
            "type": "scatter",
            "mode": "lines+markers",
            "line": {"shape": "spline", "width": 2},
            "marker": {"size": 0},
        },
        "bar": {
            "type": "scatter",
            "mode": "lines+markers",
            "line": {"shape": "spline", "width": 2},
            "marker": {"size": 0},
        },
        "heatmap": {
            "type": "heatmap",
            "colorscale": "Viridis",
        }
    }
}