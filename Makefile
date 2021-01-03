.PHONY: all clean

all: 2020 20201

2020: books-2020.pdf
20201: books-2021.pdf

clean:
	rm -f *.pdf

books-2020.pdf: books-2020.toml books.py
	./books.py -o books-2020.pdf books-2020.toml 

books-2021.pdf: books-2021.toml books.py
	./books.py -o books-2021.pdf books-2021.toml 
