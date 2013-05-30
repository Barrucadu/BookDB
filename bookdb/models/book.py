"""Book model: data structure and associated operations on books.

Book:   ORM class for dealing with books in the database
lookup: Look up a book by ISBN.
"""

from models import Base, DBSession
from sqlalchemy import Boolean, Column, Date, Integer, String, Text
from datetime import date


class Book(Base):
    """A class to represent a book. A book has an ISBN, title, list of
    authors, read flag, last read date, location, borrower, quote,
    notes, and image.

    Unfortunately sqlalchemy has no list column type, and so the
    authors stored as an ampersand-separated string.
    """

    __tablename__ = 'books'

    # PEP8 doesn't like having multiple spaces after the operator, but
    # I don't care. It is so much more readible when aligned like
    # this.
    id       = Column(Integer, primary_key=True)
    isbn     = Column(String, unique=True)
    title    = Column(String)
    subtitle = Column(Text)
    volume   = Column(Text)
    fascicle = Column(Text)
    voltitle = Column(Text)
    author   = Column(String)
    read     = Column(Boolean)
    lastread = Column(Date)
    location = Column(String)
    borrower = Column(String)
    quote    = Column(Text)
    notes    = Column(Text)
    image    = Column(Text)

    def __init__(self):
        """Create a new book, which contains no data.
        """

        self.mutate()

    def mutate(self, isbn='', title='', subtitle='', volume=-1,
               fascicle=-1, voltitle='', author='', read=False,
               lastread=date.min, location='', borrower='', quote='',
               notes='', image=''):
        """Modify this book to contain the new data

        :param isbn: The ISBN number of the book, this cannot already
            be in the database.
        :param title: The title of the book.
        :param subtitle: Subtitle of the book (if any).
        :param volume: Volume number of the book (if any).
        :param fascicle: Fascicle number o the book (if any).
        :param voltitle: Title of the volume (if any).
        :param author: List of authors of the book, in the format
            "Surname, Forename Initials", with ampersands separating
            different authors.
        :param read: Whether the book has been read or not
        :param lastread: The date on which the book was last read
            (invalid if read = False)
        :param location: Location of the book.
        :param borrower: Borrower of the book.
        :param quote:    A quote from the book.
        :param notes:    Any notes on the book.
        :param image:    The filename of the cover image.
        """

        self.isbn     = isbn
        self.title    = title
        self.subtitle = subtitle
        self.volume   = volume
        self.fascicle = fascicle
        self.voltitle = voltitle
        self.author   = author
        self.read     = read
        self.lastread = lastread
        self.location = location
        self.borrower = borrower
        self.quote    = quote
        self.notes    = notes
        self.image    = image

    def authors(self):
        """Get the authors of a book in list form.
        """

        return [author.strip()
                for author in self.author.split('&')]

    @staticmethod
    def unstring(field):
        """Take the name of a field and return the field. Return None
        if the name is bad.

        :param field: The name of the field.
        """

        try:
            return {'isbn':     Book.isbn,
                    'title':    Book.title,
                    'subtitle': Book.subtitle,
                    'volume':   Book.volume,
                    'fascicle': Book.fascicle,
                    'voltitle': Book.voltitle,
                    'author':   Book.author,
                    'read':     Book.read,
                    'lastread': Book.lastread,
                    'location': Book.location,
                    'borrower': Book.borrower,
                    'quote':    Book.quote,
                    'notes':    Book.notes,
                    'image':    Book.image}[field]
        except:
            return None

def lookup(isbn):
    """Look up a book by ISBN. Throws an exception if there is no
    such book

    :param isbn: The ISBN of the book.
    """

    return DBSession.query(Book).filter(Book.isbn == isbn).one()
