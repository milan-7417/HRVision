# utils/charts.py

import plotly.express as px


# ==========================================================
# COMMON LAYOUT
# ==========================================================

def apply_layout(fig, title):

    fig.update_layout(

        title=title,

        template="plotly_white",

        height=420,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        title_x=0.03,

        font=dict(
            family="Segoe UI",
            size=14
        )
    )

    return fig


# ==========================================================
# DONUT CHART
# ==========================================================

def donut_chart(
    df,
    names,
    values,
    title,
    colors=None
):

    fig = px.pie(

        df,

        names=names,

        values=values,

        hole=.60,

        color=names,

        color_discrete_sequence=colors

    )

    fig.update_traces(

        textposition="inside",

        textinfo="percent+label"

    )

    return apply_layout(fig, title)


# ==========================================================
# PIE CHART
# ==========================================================

def pie_chart(
    df,
    names,
    values,
    title,
    colors=None
):

    fig = px.pie(

        df,

        names=names,

        values=values,

        color=names,

        color_discrete_sequence=colors

    )

    return apply_layout(fig, title)


# ==========================================================
# BAR CHART
# ==========================================================

def bar_chart(
    df,
    x,
    y,
    title,
    color=None,
    horizontal=False
):

    fig = px.bar(

        df,

        x=x if not horizontal else y,

        y=y if not horizontal else x,

        color=color,

        orientation="h" if horizontal else "v",

        text=y

    )

    fig.update_traces(textposition="outside")

    return apply_layout(fig, title)


# ==========================================================
# HISTOGRAM
# ==========================================================

def histogram_chart(
    df,
    x,
    title,
    bins=20,
    color="#2563EB"
):

    fig = px.histogram(

        df,

        x=x,

        nbins=bins,

        color_discrete_sequence=[color]

    )

    return apply_layout(fig, title)


# ==========================================================
# GROUPED BAR CHART
# ==========================================================

def grouped_bar_chart(
    df,
    x,
    y,
    color,
    title
):

    fig = px.bar(

        df,

        x=x,

        y=y,

        color=color,

        barmode="group",

        text=y

    )

    fig.update_traces(textposition="outside")

    return apply_layout(fig, title)


# ==========================================================
# SCATTER CHART
# ==========================================================

def scatter_chart(
    df,
    x,
    y,
    title,
    color=None
):

    fig = px.scatter(

        df,

        x=x,

        y=y,

        color=color,

        size_max=15

    )

    return apply_layout(fig, title)


# ==========================================================
# BOX PLOT
# ==========================================================

def box_plot(
    df,
    x,
    y,
    title,
    color=None
):

    fig = px.box(

        df,

        x=x,

        y=y,

        color=color

    )

    return apply_layout(fig, title)


# ==========================================================
# VIOLIN PLOT
# ==========================================================

def violin_plot(
    df,
    x,
    y,
    title,
    color=None
):

    fig = px.violin(

        df,

        x=x,

        y=y,

        color=color,

        box=True

    )

    return apply_layout(fig, title)


# ==========================================================
# LINE CHART
# ==========================================================

def line_chart(
    df,
    x,
    y,
    title,
    color=None
):

    fig = px.line(

        df,

        x=x,

        y=y,

        color=color,

        markers=True

    )

    return apply_layout(fig, title)