.PHONY: book clean

all: books

books: books-2020.pdf

clean:
	rm -f *.pdf

books-2020.pdf: books-2020.toml
	./books.py -o books-2020.pdf books-2020.toml 

