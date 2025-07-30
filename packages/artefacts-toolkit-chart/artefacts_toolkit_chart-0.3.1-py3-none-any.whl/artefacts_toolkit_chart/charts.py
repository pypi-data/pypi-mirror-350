import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import csv

from pathlib import Path

from rosbags.rosbag2 import Reader
from rosbags.typesys import Stores, get_typestore

from artefacts_toolkit_utilities.utils import _extract_attribute_data


def _split_topic_name_and_attributes(topic):
    """Split a topic string into name and attributes parts.

    For 'time' special case, returns ('time', '').
    For regular topics like 'topic.attribute1.attribute2',
    returns ('topic', 'attribute1.attribute2').
    """
    if topic.lower() == "time":
        return "time", ""
    else:
        return topic.split(".", 1)


def _plot_data(x_data, y_data, x_title, y_title, output_filepath):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode="lines+markers", name=y_title))

    fig.update_layout(
        title=f"{y_title} vs {x_title}",
        xaxis_title=x_title,
        yaxis_title=y_title,
    )

    pio.write_html(fig, file=output_filepath, auto_open=False)


def _save_as_csv(x_data, y_data, x_title, y_title, output_filepath):
    with open(output_filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Write header row
        writer.writerow([x_title, y_title])
        # Write data rows
        for x, y in zip(x_data, y_data):
            writer.writerow([x, y])


"""
Makes a chart based on provided topics (x, y) where each topic is a string with the format
"topic.attribute1.attribute2...". Attributes are split by "." Any depth of attributes can be used.
If the attribute is a list, the index can be specified in square brackets (e.g., "topic.attribute[0]").
If one of the topics is time, the other topic will be plotted against its timestamps.
"""


def _make_rosbag_chart(
    filepath, topic_x, topic_y, field_unit, output_dir, chart_name, output_format="html"
):
    try:
        typestore = get_typestore(Stores.LATEST)
        x_data = []
        y_data = []
        initial_timestamp = None
        x_plot_name = f"{topic_x} ({field_unit})" if field_unit else topic_x
        y_plot_name = f"{topic_y} ({field_unit})" if field_unit else topic_y

        # Override plot names if one of the topics is time
        topic_x_name, topic_x_attributes = _split_topic_name_and_attributes(topic_x)
        topic_y_name, topic_y_attributes = _split_topic_name_and_attributes(topic_y)

        # If the topic is time, set the plot name to "Time (s)"
        if topic_x_name == "time":
            x_plot_name = "Time (s)"
        if topic_y_name == "time":
            y_plot_name = "Time (s)"

        with Reader(filepath) as reader:
            for connection, timestamp, rawdata in reader.messages():
                msg = typestore.deserialize_cdr(rawdata, connection.msgtype)

                # Use the rosbag2 timestamp (epoch) if no header
                if not hasattr(msg, "header"):
                    msg_timestamp = timestamp / 1e9  # nanoseconds to seconds
                    if initial_timestamp is None:
                        initial_timestamp = msg_timestamp
                    normalized_timestamp = msg_timestamp - initial_timestamp
                else:
                    normalized_timestamp = (
                        msg.header.stamp.sec + msg.header.stamp.nanosec / 1e9
                    )

                # If only one actual topic is provided, use that topic's timestamps or rosbag time
                if topic_x_name == "time" and connection.topic == topic_y_name:
                    x_data.append(normalized_timestamp)
                elif connection.topic == topic_x_name:
                    x_data.append(_extract_attribute_data(msg, topic_x_attributes))
                if topic_y_name == "time" and connection.topic == topic_x_name:
                    y_data.append(normalized_timestamp)
                elif connection.topic == topic_y_name:
                    y_data.append(_extract_attribute_data(msg, topic_y_attributes))

        x_data = np.array(x_data)
        y_data = np.array(y_data)

        if output_format.lower() == "html":
            output_filepath = f"{output_dir}/{chart_name}.html"
            _plot_data(x_data, y_data, x_plot_name, y_plot_name, output_filepath)
        elif output_format.lower() == "csv":
            output_filepath = f"{output_dir}/{chart_name}.csv"
            _save_as_csv(x_data, y_data, x_plot_name, y_plot_name, output_filepath)
    except Exception as e:
        print(f"ERROR: Unable to create chart for {chart_name}. {e}")


def make_chart(
    filepath,
    topic_x,
    topic_y,
    field_unit=None,
    output_dir="output",
    chart_name="chart",
    file_type="rosbag",
    output_format="html",
):
    supported_formats = ["html", "csv"]
    supported_file_types = ["rosbag"]

    if output_format.lower() not in supported_formats:
        raise ValueError(
            f"Unsupported output format '{output_format}'. Supported formats are: {supported_formats}"
        )
    if file_type not in supported_file_types:
        raise NotImplementedError(
            "At present, charts can only be created from rosbags."
        )

    try:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        # Clean up
        extensions = [".html", ".csv"]
        for ext in extensions:
            for p in Path(output_dir).glob(f"{chart_name}{ext}"):
                p.unlink()
    except Exception as e:
        print(e)

    if file_type == "rosbag":
        _make_rosbag_chart(
            filepath,
            topic_x,
            topic_y,
            field_unit,
            output_dir,
            chart_name,
            output_format,
        )
