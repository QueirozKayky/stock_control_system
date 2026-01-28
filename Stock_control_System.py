import sqlite3

def start_db():
    connection = sqlite3.connect('stock_almox.db')
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_almox(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    """)
    
    connection.commit()
    connection.close()
    print('Database Ready!')


#menu do estoque.
def menu():
    while True:
        print('-'*30)
        print('>>>Control Stock<<<')
        print('-'*30)
        print('[1] Register New Item')
        print('[2] List Items of Stock')
        print('[3] Remove Item from stock')
        print('[4] Update')
        print('[5] Search Item')
        print('[6] Check Low Stock Items')
        print('[7]Exit')

        try:
            option = int(input('Select One Option: '))
        except ValueError:
            print('Ops, select one option between 1 and 8')
            continue
        if 1 <= option <=8:
            if option == 1:
                register_item()
            elif option == 2:
                list_items()
            elif option == 3:
                remove_item()
            elif option == 4:
                update()
            elif option == 5:
                search_item()
            elif option == 6:
                check_low_stock()
            elif option == 7:
                withdraw_item()
            elif option == 8:
                print('-'*20)
                print('See you soon! BYE')
                print('-'*20)
                break
        else:
            print('Invalid Option! Please type a number between 1 and 4 of menu.')

#registro de item. 
def register_item():
    print('-'*25)
    print('>>>Register new item<<<')
    print('-'*25)
    name_of_item = str(input('Enter Item Name: '))
    while True:
        try:
            quantity_of_item = int(input('Type the quantity of item: '))
            if quantity_of_item <0:
                print('Quantity must be positive')
            else:
                break
        except ValueError:
            print('Please, Enter a Int Number!')

    price_of_item = float(input('Enter the Value of the item: '))

    connection = sqlite3.connect('stock_almox.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO stock_almox (description,quantity,price)VALUES (?,?,?)",
                   (name_of_item,quantity_of_item,price_of_item))
    connection.commit()
    connection.close()
    
    print('--------------------')
    print('>>>Add successfully<<<')
    print('--------------------')

#listagem dos itens.
def list_items(pause_on_exit=True):

    print('-'*50)
    print('>>>>>>>>>>>>>>>>List of Stock<<<<<<<<<<<<<<<')
    print('-'*50)

    connection = sqlite3.connect('stock_almox.db')
    cursor = connection.cursor()
    #fazendo seleção de todas as colunas da tabela.
    cursor.execute("SELECT id, description, quantity, price, created_at FROM stock_almox")
    rows = cursor.fetchall()

    
    if len(rows) == 0:
        print('Stock is currently empty')
    else:
        print(f"{'ID':<4} | {'Description':<20} | {'Qty':>8} | {'Price':>10} |{'Date':>10}")
        print("-" * 65)
        for row in rows:
            date_br = row[4] #pega a data crua do banco de dados.
            if date_br:
                #pega apenas os primeiros 10 caracteres (yyyy/mm/dd) e inverte.
                year, month, day = date_br[:10].split('-') 
                hour = date_br[11:16]
                date_formated = f"{day}/{month}/{year} {hour}"
            else:
                date_formated = "None Date"
            output_line = f"{str(row[0]):<4} | {str(row[1]):<20} | {str(row[2]):>8} | {row[3]:>10.2f} | {date_formated:<20}"
            print(output_line)

    if pause_on_exit:
        input("Press Enter to return to the Main Menu...")
    connection.close()

#remoção dos itens do estoque
def remove_item():
    print('-----------------')
    print('>>>Remove item<<<')
    print('-----------------')

    connection = sqlite3.connect('stock_almox.db')
    cursor = connection.cursor()

    #precisa do SELECT para o fetchall funcionar!!!
    cursor.execute("SELECT * FROM stock_almox")
    rows = cursor.fetchall()

    #lendo as linhas.
    if len(rows) == 0:
        print('Stock is currently empty')
    else:
        #trazendo a lista para o usuario verificar qual ID quer remover.
        list_items(pause_on_exit= False)

        while True:
            try:
                id_to_remove = int(input('Type the ID: '))
                if id_to_remove <0:
                    print('ID must be 0 or greater.')
                    continue

                #deletando Item 
                cursor.execute("DELETE FROM stock_almox WHERE id = ?", (id_to_remove,))
        
                #verificando se algo foi deletado de verdade
                if cursor.rowcount >0:
                    connection.commit() #salva
                    print(f"Success! Removed item ID {id_to_remove}") 
                else:
                    print('ID not found...')  
                break
            except ValueError:
                print('Please type a Number ID')

    connection.close()            

    input('\n Press ENTER to return to the main menu...')

# Atualização de itens
def update():
    #abrindo conexão com o Banco!
    connection = sqlite3.connect('stock_almox.db')
    cursor = connection.cursor()
    #Executando a lista de itens do banco para verificar se existe algo ou não.
    cursor.execute("SELECT * FROM stock_almox")
    rows = cursor.fetchall()
    #verificando se esta vazio.
    if len(rows) == 0:
        print('Stock is currently empty')
    else:
        list_items(pause_on_exit=False)
    
    
    id_to_update = int(input('Enter te ID: '))
    cursor.execute("SELECT * FROM stock_almox WHERE id = ?",(id_to_update,))

    #checando se o ID existe
    first_row = cursor.fetchone()
    if first_row:
        #first_row[1] mostra o nome do item
        print(f"Item: {first_row[1]}")
    else:
        print("No matching row found...")
        connection.close()
        return

    #Dando opção para o usuario escolher qual atualizar.
    choice_to_update = str(input('What do you want do update? [Item, Quantity or Price [I/Q/P]]: ')).upper()
    #Decisão de Atualização do nome do item.
    if choice_to_update == 'I' or choice_to_update == 'ITEM':
        new_name = str(input('Enter the NEW name of ITEM: '))
        cursor.execute("UPDATE stock_almox SET description = ? WHERE id = ?", (new_name,id_to_update))
        print('-' * 55)
        print('>>>>Sucess!! You update the description!!!<<<<')
        print('-' * 55)
    #Decisão de Atualização da quantidade do item.
    elif choice_to_update == 'Q' or choice_to_update == 'QUANTITY':
        while True:
            try:
                new_quantity = int(input('What is the NEW quantity: '))
                if new_quantity <0:
                    print('Quantity must be positive')
                else:
                    cursor.execute("UPDATE stock_almox SET quantity = ? WHERE id = ?", (new_quantity,id_to_update))
                    print('-' * 45)
                    print('>>>> | Sucess You update the quantity | <<<<')
                    print('-' * 45)
                    break
            except ValueError:
                print('Please, Enter a Int Number!')
                break
    #Decisão de Atualização do Preço do item.
    elif choice_to_update == 'P' or choice_to_update == 'PRICE':
        while True:
            try:
                new_price = float(input('New PRICE: '))
                if new_price <0:
                    print('The price must be posite')
                else:
                    cursor.execute("UPDATE stock_almox SET price = ? WHERE id = ?", (new_price, id_to_update))
                    print('-'*45)
                    print('>>>> | Sucess You update the PRICE | <<<<')
                    print('-'*45)
                    break
            except ValueError:
                print('Please, Enter a Float Number!')
                break
            
    #salvando o banco e fechando.
    connection.commit()            
    connection.close()

# Procura de Itens no Estoque
def search_item():
    #abrindo conexão com o Banco!
    connection = sqlite3.connect('stock_almox.db')
    cursor = connection.cursor()
    #Usuario digita o nome do item a ser buscado.
    search_item = str(input('Enter the name of the item to search: '))
    #fazendo a busca no banco de dados usando LIKE para encontrar correspondências parciais.
    cursor.execute("SELECT id, description, quantity, price, created_at FROM stock_almox WHERE description LIKE ?", ('%' + search_item + '%',))
    rows = cursor.fetchall()
    if len(rows) == 0:
        print('No items found matching your search.')
    else:
        #exibindo o cabeçalho dos resultados.
        print(f"\nResults for '{search_item}':")
        print('-' * 85)
        print(f"{'ID':<4} | {'Description':<20} | {'Qty':>8} | {'Price':>10} | {'Date':<20}")
        print("-" * 85)
        #exibindo os resultados da busca.
        for row in rows:
            print(f"{row[0]:<4} | {row[1]:<20} | {row[2]:>8} | {row[3]:>10.2f} | {row[4]}")
            
    connection.close()
    input("\nPress Enter to return to the Main Menu...")

# Verificação de Itens com Baixo Estoque
def check_low_stock():#
    #abrindo conexão com o Banco
    connection = sqlite3.connect('stock_almox.db')
    cursor = connection.cursor()
    # Definindo o limite para baixo estoque
    low_stock_limit = 5
    cursor.execute("SELECT id, description, quantity FROM stock_almox WHERE quantity <= ?", (low_stock_limit,))
    #buscando itens com quantidade menor ou igual ao limite definido.
    rows = cursor.fetchall()
    if len(rows) == 0:
        print('No items are low in stock.')
    else:
        #exibindo os itens com baixo estoque.
        print('Items low in stock:')
        print(f"{'ID':<4} | {'Description':<20} | {'Qty':>8}")
        print("-" * 40)
        for row in rows:
            print(f"{row[0]:<4} | {row[1]:<20} | {row[2]:>8}")
    connection.close()
    input("\nPress Enter to return to the Main Menu...")

def withdraw_item():
    connection = sqlite3.connect('stock_almox.db')
    cursor = connection.cursor()
    search_item = str(input('Enter the ID of the item to withdraw: '))
    cursor.execute("SELECT id, description, quantity FROM stock_almox WHERE id = ?", (search_item,))
    row = cursor.fetchone()
    if row is None:
        print('Item not found.')
    else:
        print(f"Item found: ID: {row[0]}, Description: {row[1]}, Quantity: {row[2]}")
        while True:
            try:
                withdraw_quantity = int(input('Enter the quantity to withdraw: '))
                if withdraw_quantity < 0:
                    print('Quantity must be positive.')
                elif withdraw_quantity > row[2]:
                    print('Insufficient stock to withdraw that quantity.')
                else:
                    new_quantity = row[2] - withdraw_quantity
                    cursor.execute("UPDATE stock_almox SET quantity = ? WHERE id = ?", (new_quantity, search_item))
                    connection.commit()
                    print(f'Successfully withdrew {withdraw_quantity} of item ID {search_item}. New quantity is {new_quantity}.')
                    break
            except ValueError:
                print('Please enter a valid integer for quantity.')
    connection.close()
    

start_db()        
menu()