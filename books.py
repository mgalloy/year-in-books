#!/usr/bin/env python

import argparse
import datetime
import collections
import math

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
from matplotlib import ticker
import numpy as np
import toml


def get_styles():
    return({"title_color": "#a86",
            "heading_color": "grey",
            "font": {"fontname": "DejaVu Sans Mono"}})


def parse_catalog(input_filename):
    return(toml.load(input_filename))


def print_catalog(catalog):
    for i, b in enumerate(catalog["books"].items()):
        book_id, book = b
        title = book["title"]
        author = book["author"] if type(book["author"]) == str else ', '.join(book["author"])
        print(f"{i+1}. *{title}* by {author}")


def display_background(fig, ax, catalog, styles):
    text = []
    for i, b in enumerate(catalog["books"].items()):
        book_id, book = b
        title = book["title"]
        author = book["author"] if type(book["author"]) == str else ', '.join(book["author"])
        text.append(f"{title} by {author}")

    text = " • ".join(text)
    lines = []
    width = 70
    for i in range(math.ceil(len(text) / width)):
        lines.append(text[i*width:(i+1)*width])
    text = "\n".join(lines)

    # TODO: should adjust fontsize that the text fills the background
    t = ax.text(0.0, 0.0, text, fontsize=17, color="#f4f4f4")
    # r = fig.canvas.get_renderer()
    # bb = t.get_window_extent(renderer=r)
    # height = bb.y1 / r.dpi


def display_title(ax, catalog, styles, year, right=0.9, top=0.9):
    gap = 0.025
    ax.text(right, top, f"Year in Books {year}",
            fontsize=28, fontweight="bold", color=styles["title_color"],
            horizontalalignment="right", **styles["font"])
    ax.text(right, top - gap, "Michael Galloy",
            fontsize=20, color=styles["heading_color"],
            horizontalalignment="right", **styles["font"])


def display_number(ax, catalog, styles, left=0.15, top=0.85):
    n_books = len(catalog["books"])
    gap = 0.025
    ax.text(left, top, f"{n_books}",
            fontsize=100, fontweight="bold", color=styles["heading_color"],
            horizontalalignment="center", **styles["font"])
    ax.text(left, top - gap, "total books",
            fontsize=18, color=styles["heading_color"],
            horizontalalignment="center", **styles["font"])


def display_authors(ax, catalog, styles, n_authors=10, left=0.575, width=0.325, top=0.5):
    authors = collections.Counter()
    for book_id, book in catalog["books"].items():
        if type(book["author"]) == str:
            authors.update([book["author"]])
        else:
            authors.update(book["author"])
    most_common_authors = authors.most_common(n_authors)

    gap = 0.0125
    ax.text(left, top, f"Top {n_authors} authors",
            fontsize=24, fontweight="bold",
            color=styles["heading_color"], **styles["font"])
    ax.text(left, top - gap,
            "\n".join([f"{i+1:02d}. {a[0]}" for i, a in enumerate(most_common_authors)]),
            verticalalignment="top", **styles["font"])
    ax.text(left + width, top - gap,
            "\n".join([f"{a[1]}" for a in most_common_authors]),
            verticalalignment="top", horizontalalignment="right", **styles["font"])


def get_finished(catalog):
    finished = [book[1]["finished"] for book in catalog["books"].items()]
    finished = sorted(finished)

    year = int(finished[0].strftime("%Y"))
    return(year, finished)


def display_weeks_histogram(fig, catalog, styles, left=0.1, width=0.8, bottom=0.175, height=0.025):
    year, finished = get_finished(catalog)

    ax = plt.Axes(fig, [left, bottom, width, height])
    ax.set_facecolor("#ffffff00")
    n, bins, patches = ax.hist(finished, bins=52,
                               range=(datetime.date(year, 1, 1),
                                      datetime.date(year, 12, 31)))

    for i, b in zip(n, bins):
        if i > 0:
            ax.text(b + 3.5, i + 0.5, f"{i:.0f}",
                    horizontalalignment="center",
                    verticalalignment="bottom",
                    color="grey",
                    fontsize=6)

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%U"))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=4))
    ax.set_xlabel("By week")

    ax.yaxis.set_major_locator(ticker.MultipleLocator(2))

    fig.add_axes(ax)

    for a in ["left", "right", "top"]:
        ax.spines[a].set_visible(False)


def display_months_histogram(fig, catalog, styles, left=0.1, width=0.8, bottom=0.1, height=0.025):
    finished = [book[1]["finished"] for book in catalog["books"].items()]
    finished = sorted(finished)

    year = int(finished[0].strftime("%Y"))

    ax = plt.Axes(fig, [left, bottom, width, height])
    ax.set_facecolor("#ffffff00")
    n, bins, patches = ax.hist(finished, bins=12,
                               range=(datetime.date(year, 1, 1),
                                      datetime.date(year, 12, 31)))
    for i, b in zip(n, bins):
        if i > 0:
            ax.text(b + 14.0, i + 0.5, f"{i:.0f}",
                    horizontalalignment="center",
                    verticalalignment="bottom",
                    color="grey",
                    fontsize=6)

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.set_xlabel("By month")

    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))

    fig.add_axes(ax)

    for a in ["left", "right", "top"]:
        ax.spines[a].set_visible(False)


def display_timeline(fig, catalog, styles, left=0.1, width=0.8, bottom=0.25, height=0.025):
    finished = [book[1]["finished"] for book in catalog["books"].items()]
    finished = sorted(finished)

    year = int(finished[0].strftime("%Y"))

    ax = plt.Axes(fig, [left, bottom, width, height])
    ax.set_facecolor("#ffffff00")
    ax.hist(finished, bins=365,
            range=(datetime.date(year, 1, 1), datetime.date(year, 12, 31)))

    months = mdates.MonthLocator()  # every month
    days = mdates.WeekdayLocator(byweekday=mdates.MO)   # every Monday
    months_fmt = mdates.DateFormatter("%b")
    days_fmt = mdates.DateFormatter("%d")

    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(months_fmt)
    ax.xaxis.set_minor_locator(days)
    #ax.xaxis.set_minor_formatter(days_fmt)
    ax.set_xlabel("Reading timeline")

    fig.add_axes(ax)

    for a in ["left", "right", "top"]:
        ax.spines[a].set_visible(False)


def grade_key(grade_pair):
    grade = grade_pair[0]
    value = ord(grade[0].lower()) - ord("a")
    value *= 10
    if len(grade) > 1:
        if grade[1] == "-":
            value += 2
        if grade[1] == "+":
            value -= 2
    return(value)


def display_barplot(fig, catalog, styles, attribute, left=0.1, width=0.30, bottom=0.6, height=0.075):
    attrs = collections.Counter()
    for book_id, book in catalog["books"].items():
        if type(book[attribute]) == str:
            attrs.update([book[attribute]])
        else:
            attrs.update(book[attribute])

    ax = plt.Axes(fig, [left, bottom, width, height])

    ax.set_facecolor("#ffffff00")
    if attribute == "grade":
        attrs = {k: v for k, v in sorted(attrs.items(), key=grade_key, reverse=True)}
    cmap = plt.get_cmap("Dark2")#Pastel1")
    n = len(attrs)
    colors = cmap(np.arange(n) / n)
    ax.bar(attrs.keys(), attrs.values(), color=colors)
    for i, a in enumerate(attrs.values()):
        ax.text(i, a, f"{a}",
                horizontalalignment="center",
                verticalalignment="bottom",
                color="grey",
                fontsize=6)

    for tick in ax.get_xticklabels():
        tick.set_horizontalalignment("right")
        tick.set_rotation(45)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))

    fig.add_axes(ax)

    for a in ["left", "right", "top"]:
        ax.spines[a].set_visible(False)


def display_genres(fig, catalog, styles, left=0.075, width=0.25, bottom=0.675, height=0.075):
    display_barplot(fig, catalog, styles, "genres", left=left, width=width, bottom=bottom, height=height)


def display_via(fig, catalog, styles, left=0.375, width=0.25, bottom=0.675, height=0.075):
    display_barplot(fig, catalog, styles, "via", left=left, width=width, bottom=bottom, height=height)


def display_grades(fig, catalog, styles, left=0.675, width=0.25, bottom=0.675, height=0.075):
    display_barplot(fig, catalog, styles, "grade", left=left, width=width, bottom=bottom, height=height)


def display_media(fig, catalog, styles, left=0.1, width=0.15, bottom=0.40, height=0.125):
    display_barplot(fig, catalog, styles, "media", left=left, width=width, bottom=bottom, height=height)


def display_format(fig, catalog, styles, left=0.325, width=0.15, bottom=0.40, height=0.125):
    display_barplot(fig, catalog, styles, "format", left=left, width=width, bottom=bottom, height=height)


def render_infographic(catalog, output_filename):
    styles = get_styles()

    xsize = 8.5   # inches
    ysize = 11.0  # inches
    fig = plt.figure(frameon=False)
    fig.set_size_inches(xsize, ysize)

    main_ax = plt.Axes(fig, [0.0, 0.0, 1.0, 1.0])
    main_ax.set_axis_off()
    main_ax.xaxis.set_major_locator(plt.NullLocator())
    main_ax.yaxis.set_major_locator(plt.NullLocator())
    fig.add_axes(main_ax)

    year, finished = get_finished(catalog)
    display_background(fig, main_ax, catalog, styles)
    display_title(main_ax, catalog, styles, year)
    display_number(main_ax, catalog, styles)
    display_authors(main_ax, catalog, styles)

    display_genres(fig, catalog, styles)
    display_via(fig, catalog, styles)
    display_grades(fig, catalog, styles)
    display_media(fig, catalog, styles)
    display_format(fig, catalog, styles)

    display_weeks_histogram(fig, catalog, styles)
    display_months_histogram(fig, catalog, styles)
    display_timeline(fig, catalog, styles)

    plt.savefig(output_filename)


def create_infographic(input_filename, output_filename):
    catalog = parse_catalog(input_filename)
    print_catalog(catalog)
    render_infographic(catalog, output_filename)


def main():
    parser = argparse.ArgumentParser(description="Year in Books infographic")
    parser.add_argument("input_filename", help="input yaml filename")
    parser.add_argument("-o", "--output", help="output filename",
                        default="output.pdf")
    args = parser.parse_args()

    create_infographic(args.input_filename, args.output)


if __name__ == "__main__":
    main()
