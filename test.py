@cash_receipts.route('/client_after_choice/<client_id>')
def client_after_choice(client_id):
    global form_data, operation_name
    client = Clients.query.filter(Clients.id == client_id).first()
    # print('client_after_choice()', 'client:', client, 'operation_name:', operation_name)
    date = form_data["date"]
    date = datetime.strptime(date, '%Y-%m-%d')
    sum = form_data["sum"]
    sum = float(sum)
    cash_desk_id = form_data["cash_desk_id"]
    cash_desk_name = form_data["cash_desk_name"]
    type_id = form_data["type_id"]
    type_name = form_data["type_name"]
    description = form_data["description"]
    form = CashReceiptsForm(id=form_data["id"], client_id=client_id, client_name=client.name,
                            date=date, sum=sum,
                            cash_desk_id=cash_desk_id, cash_desk_name=cash_desk_name,
                            type_id=type_id, type_name=type_name,
                            description=description)
    if operation_name == 'cash_receipt_create':
        # print('client_after_choice() - cash_receipt_create')
        return render_template('cash_receipts/cash_receipt_create.html', menu=menu, title="Створення надходження в касу", form=form)
    else:
        return 'client_after_choice ???'
