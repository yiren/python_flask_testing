from marshmallow import Schema, fields


class BookSchema(Schema):
    title = fields.Str()
    author = fields.Str()
    description = fields.Str(required=False)


class Book:
    def __init__(self, title, author, description):
        self.title = title
        self.author = author
        self.description = description


incoming_data = {
    'title': 'Clean Code',
    'author': 'Bob Martin',
    'description': 'A book with recommendation for good coding practice.'
}

book_schema = BookSchema()
book_data = book_schema.load(incoming_data)

# print(book_data)

book = Book(**book_data)

print(book.title)
