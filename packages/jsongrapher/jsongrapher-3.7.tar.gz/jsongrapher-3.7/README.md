# JSONGrapher (python)
This is the python version of JSONGrapher with JSONRecordCreator. This package is for plotting JSON records with drag and drop and has tools for creating the JSON records.

The software will automatically plot multiple records together, for comparison, and will automaticlaly converting units between records as needed to plot them for comparison (like kg/s and g/s).

To use python JSONGrapher, first install it using conda or pip:<br>
`pip install JSONGrapher[COMPLETE]` or `conda install conda-forge::jsongrapher` <br>
Alternatively, you can download the directory directly.<br> 

## **0\. Plotting a JSON Record**
It's as simple as one line! Then drag an [example](https://github.com/AdityaSavara/jsongrapher-py/tree/main/examples/example_1_drag_and_drop) JSONGrapher record into the window to plot!
Below shows several plot types for 2D and 3D plots, followed by a simple example of how to use python JSONGrapher to create your own records.
<pre>
import JSONGrapher 
JSONGrapher.launch()
</pre>

[![JSONGRapher window](https://raw.githubusercontent.com/AdityaSavara/JSONGrapher-py/main/JSONGrapher/JSONGrapherWindowShortened.png)](https://raw.githubusercontent.com/AdityaSavara/JSONGrapher-py/main/JSONGrapher/JSONGrapherWindowShortened.png) [![JSONGRapher plot](https://raw.githubusercontent.com/AdityaSavara/JSONGrapher-py/main/examples/example_1_drag_and_drop/UAN_DTA_image.png)](https://raw.githubusercontent.com/AdityaSavara/JSONGrapher-py/main/examples/example_1_drag_and_drop/UAN_DTA_image.png)

[![rainbow plot](https://raw.githubusercontent.com/AdityaSavara/JSONGrapher-py/main/examples/example_1_drag_and_drop/SrTiO3_rainbow_image.png)](https://raw.githubusercontent.com/AdityaSavara/JSONGrapher-py/main/examples/example_1_drag_and_drop/SrTiO3_rainbow_image.png)
[![mesh3d plot](https://raw.githubusercontent.com/AdityaSavara/JSONGrapher-py/main/examples/example_1_drag_and_drop/Rate_Constant_mesh3d.png)](https://raw.githubusercontent.com/AdityaSavara/JSONGrapher-py/main/examples/example_1_drag_and_drop/Rate_Constant_mesh3d.png)
[![scatter3d plot](https://raw.githubusercontent.com/AdityaSavara/JSONGrapher-py/main/examples/example_1_drag_and_drop/Rate_Constant_Scatter3d_example10.png)](https://raw.githubusercontent.com/AdityaSavara/JSONGrapher-py/main/examples/example_1_drag_and_drop/Rate_Constant_Scatter3d_example10.png)
[![bubble plot](https://raw.githubusercontent.com/AdityaSavara/JSONGrapher-py/main/examples/example_1_drag_and_drop/Rate_Constant_bubble.png)](https://raw.githubusercontent.com/AdityaSavara/JSONGrapher-py/main/examples/example_1_drag_and_drop/Rate_Constant_bubble.png)




## **1\. Preparing to Create a Record**

The remainder of this landing page follows a json record tutorial [example file](https://github.com/AdityaSavara/jsongrapher-py/blob/main/examples/example_2_creating_records_and_using_styles/example_2_json_record_tutorial.py) which shows how to create graphable .json records. The records can then be plotted with python JSONGrapher or with jsongrapher.com<br>

Let's create an example where we plot the height of a pear tree over several years. 
<pre>
x_label_including_units = "Time (years)"
y_label_including_units = "Height (m)"
time_in_years = [0, 1, 2, 3, 4]
tree_heights = [0, 0.42, 0.86, 1.19, 1.45]
</pre>

## **2\. Creating and Populating a New JSONGrapher Record**

<pre>
Record = JSONRecordCreator.create_new_JSONGrapherRecord()
Record.set_comments("Tree Growth Data collected from the US National Arboretum")
Record.set_datatype("Tree_Growth_Curve")
Record.set_x_axis_label_including_units(x_label_including_units)
Record.set_y_axis_label_including_units(y_label_including_units)
Record.add_data_series(series_name="pear tree growth", x_values=time_in_years, y_values=tree_heights, plot_type="scatter_spline")
Record.set_graph_title("Pear Tree Growth Versus Time")
</pre>

## **3\. Exporting to File**

We can export a record to a .json file, which can then be used with JSONGrapher. 
<pre>
Record.export_to_json_file("ExampleFromTutorial.json")
Record.print_to_inspect()
</pre>

<p><strong>Expected Output:</strong></p>
<pre>
JSONGrapher Record exported to, ./ExampleFromTutorial.json
{
    "comments": "Tree Growth Data collected from the US National Arboretum",
    "datatype": "Tree_Growth_Curve",
    "data": [
        {
            "name": "pear tree growth",
            "x": [0, 1, 2, 3, 4],
            "y": [0, 0.42, 0.86, 1.19, 1.45],
            "type": "scatter",
            "line": { "shape": "spline" }
        }
    ],
    "layout": {
        "title": "Pear Tree Growth Versus Time",
        "xaxis": { "title": "Time (year)" },
        "yaxis": { "title": "Height (m)" }
    }
}
</pre>

## **4\. Plotting to Inspect**

We can plot the data using Matplotlib and export the plot as a PNG file.
<pre>
Record.plot_with_matplotlib()
Record.export_to_matplotlib_png("image_from_tutorial_matplotlib_fig")
</pre>

We can create an interactive graph with python plotly:
<pre>
Record.plot_with_plotly() #Try hovering your mouse over points after this command!
</pre>

[![JSONGRapher record plotted using matplotlib](https://raw.githubusercontent.com/AdityaSavara/JSONGrapher-py/main/examples/example_2_creating_records_and_using_styles/image_from_tutorial_matplotlib_fig.png)](https://raw.githubusercontent.com/AdityaSavara/JSONGrapher-py/main/examples/example_2_creating_records_and_using_styles/image_from_tutorial_matplotlib_fig.png)

You can also see more examples: https://github.com/AdityaSavara/jsongrapher-py/tree/main/examples

Additionally, json records you send to others can be plotted by them at www.jsongrapher.com
This 'see the plot using a browser' capability is intended to facilitate including JSONGrapher records in supporting information of scientific publications.