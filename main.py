from app import app
import view
from cash_desks.cash_desks import cash_desks
from clients.clients import clients
from currency.currency import currency
from cash_receipts.cash_receipts import cash_receipts
from cash_expenses.cash_expenses import cash_expenses
from types_of_moves.types_of_moves import types_of_moves

app.register_blueprint(cash_desks, url_prefix='/cash_desks')
app.register_blueprint(clients, url_prefix='/clients')
app.register_blueprint(currency, url_prefix='/currency')
app.register_blueprint(cash_receipts, url_prefix='/cash_receipts')
app.register_blueprint(cash_expenses, url_prefix='/cash_expenses')
app.register_blueprint(types_of_moves, url_prefix='/types_of_moves')

if __name__ == '__main__':
    app.run()
