.PHONY: all clean

all: 2020

2020: books-2020.pdf

clean:
	rm -f *.pdf

books-2020.pdf: books-2020.toml books.py
	./books.py -o books-2020.pdf books-2020.toml 

