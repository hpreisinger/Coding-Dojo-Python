from django.shortcuts import render, redirect, HttpResponse
from .models import Book, Author

# PRIMARY PAGES


def books(request):
    content = {
        "booklist": Book.objects.all()
    }
    return render(request, "books_authors_app/books.html", content)


def authors(request):
    content = {
        "authorlist": Author.objects.all()
    }
    return render(request, "books_authors_app/authors.html", content)


def book_profile(request, book_id):
    allAuthors = Author.objects.all()
    thisBook = Book.objects.get(id=book_id)
    authorlist = []
    for author in allAuthors:
        if thisBook not in author.books.all():
            authorlist.append(author)

    content = {
        "thisbook": thisBook,
        "authors": Book.objects.get(id=book_id).authors.all(),
        "authorlist": authorlist
    }
    return render(request, "books_authors_app/book_profile.html", content)


def author_profile(request, author_id):
    allBooks = Book.objects.all()
    thisAuthor = Author.objects.get(id=author_id)
    booklist = []
    for book in allBooks:
        if thisAuthor not in book.authors.all():
            booklist.append(book)

    content = {
        "thisauthor": thisAuthor,
        "books": Author.objects.get(id=author_id).books.all(),
        "booklist": booklist
    }
    return render(request, "books_authors_app/author_profile.html", content)

# FORM SUBMISSIONS


def book_form(request):
    if request.method == "POST":
        Book.objects.create(
            title=request.POST["title"], desc=request.POST["desc"])
    return redirect("/books")


def author_form(request):
    if request.method == "POST":
        Author.objects.create(
            first_name=request.POST["first_name"], last_name=request.POST["last_name"], notes=request.POST["notes"])
    return redirect("/authors")


def book_dropdown(request):
    if request.method == "POST":
        author_id = request.POST["author_id"]
        author = Author.objects.get(id=author_id)
        book = Book.objects.get(id=request.POST["book_id"])
        author.books.add(book)
    return redirect(f"/authors/{author_id}")


def author_dropdown(request):
    if request.method == "POST":
        book_id = request.POST["book_id"]
        book = Book.objects.get(id=book_id)
        author = Author.objects.get(id=request.POST["author_id"])
        book.authors.add(author)
    return redirect(f"/books/{book_id}")
