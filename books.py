#!/usr/bin/env python

import argparse
import collections

import matplotlib.pyplot as plt
import toml


def get_styles():
    return({"title_color": "#a68",
            "heading_color": "grey",
            "font": {"fontname": "DejaVu Sans Mono"}})


def parse_catalog(input_filename):
    return(toml.load(input_filename))


def print_catalog(catalog):
    for book_idid, book in catalog["books"].items():
        title = book["title"]
        author = book["author"] if type(book["author"]) == str else ', '.join(book["author"])
        print(f"*{title}* by {author}")


def display_title(ax, catalog, styles, right=0.9, top=0.9):
    gap = 0.025
    ax.text(right, top, "Year in Books 2020",
            fontsize=28, fontweight="bold", color=styles["title_color"],
            horizontalalignment="right", **styles["font"])
    ax.text(right, top - gap, "Michael Galloy",
            fontsize=20, color=styles["heading_color"],
            horizontalalignment="right", **styles["font"])


def display_number(ax, catalog, styles, left=0.125, top=0.8):
    n_books = len(catalog["books"])
    gap = 0.025
    ax.text(left, top, f"{n_books}",
            fontsize=100, fontweight="bold", color=styles["heading_color"],
            horizontalalignment="center", **styles["font"])
    ax.text(left, top - gap, "books",
            fontsize=18, color=styles["heading_color"],
            horizontalalignment="center", **styles["font"])


def display_authors(ax, catalog, styles, n_authors=5, left=0.6, width=0.30, top=0.5):
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
            "\n".join([a[0] for a in most_common_authors]),
            verticalalignment="top", **styles["font"])
    ax.text(left + width, top - gap,
            "\n".join([f"{a[1]}" for a in most_common_authors]),
            verticalalignment="top", horizontalalignment="right", **styles["font"])


def render_infographic(catalog, output_filename):
    styles = get_styles()

    xsize = 8.5   # inches
    ysize = 11.0  # inches
    fig = plt.figure(frameon=False)
    fig.set_size_inches(xsize, ysize)

    ax = plt.Axes(fig, [0.0, 0.0, 1.0, 1.0])
    ax.set_axis_off()
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())
    fig.add_axes(ax)

    display_title(ax, catalog, styles)
    display_number(ax, catalog, styles)
    display_authors(ax, catalog, styles)

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
