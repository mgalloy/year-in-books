.PHONY: all clean

all: 2020 2021 2022 2023

2020: books-2020.pdf
2021: books-2021.pdf
2022: books-2022.pdf
2023: books-2023.pdf

clean:
	rm -f *.pdf

books-2020.pdf: books-2020.toml books.py
	./books.py -o books-2020.pdf books-2020.toml 

books-2021.pdf: books-2021.toml books.py
	./books.py -o books-2021.pdf books-2021.toml 

books-2022.pdf: books-2022.toml books.py
	./books.py -o books-2022.pdf books-2022.toml

books-2023.pdf: books-2023.toml books.py
	./books.py -o books-2023.pdf books-2023.toml
