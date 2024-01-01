.PHONY: all clean

LATEX=pdflatex

all: 2020 2021 2022 2023 2024

2020: books-2020.pdf books-list-2020.pdf
2021: books-2021.pdf books-list-2021.pdf
2022: books-2022.pdf books-list-2022.pdf
2023: books-2023.pdf books-list-2023.pdf
2024: books-2024.pdf books-list-2024.pdf

clean:
	rm -f *.pdf

books-2020.pdf: books-2020.toml books.py
	./books.py -o books-2020.pdf books-2020.toml 

books-list-2020.pdf: books-2020.toml books.py
	./books.py --list -o books-list-2020.tex books-2020.toml
	$(LATEX) -halt-on-error books-list-2020.tex

books-2021.pdf: books-2021.toml books.py
	./books.py -o books-2021.pdf books-2021.toml 

books-list-2021.pdf: books-2021.toml books.py
	./books.py --list -o books-list-2021.tex books-2021.toml
	$(LATEX) -halt-on-error books-list-2021.tex

books-2022.pdf: books-2022.toml books.py
	./books.py -o books-2022.pdf books-2022.toml

books-list-2022.pdf: books-2022.toml books.py
	./books.py --list -o books-list-2022.tex books-2022.toml
	$(LATEX) -halt-on-error books-list-2022.tex

books-2023.pdf: books-2023.toml books.py
	./books.py -o books-2023.pdf books-2023.toml

books-list-2023.pdf: books-2023.toml books.py
	./books.py --list -o books-list-2023.tex books-2023.toml
	$(LATEX) -halt-on-error books-list-2023.tex

books-2024.pdf: books-2024.toml books.py
	./books.py -o books-2024.pdf books-2024.toml

books-list-2024.pdf: books-2024.toml books.py
	./books.py --list -o books-list-2024.tex books-2024.toml
	$(LATEX) -halt-on-error books-list-2024.tex

