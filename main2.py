from models import Customer, Order, Product
from repositories.customer_repository import CustomerRepository
from repositories.product_repository import ProductRepository
from repositories.order_repository import OrderRepository
from datetime import date

def run_integration_test():
    # 0. Instanciando os repositórios
    customer_repo = CustomerRepository()
    product_repo = ProductRepository()
    order_repo = OrderRepository()

    print("--- 1. CUSTOMER REGISTRATION ---")
    # Criamos o objeto Customer primeiro
    new_customer = Customer(name="Tony Stark", city="MALIBU")
    
    # O repository salva e o banco gera o ID
    customer_id = customer_repo.save(new_customer)
    
    if customer_id:
        new_customer.customer_id = customer_id # Atualizamos o objeto com o ID real
        print(f"Customer {new_customer.name} saved with ID: {customer_id}\n")
    else:
        print("Failed to save customer. Aborting.")
        return

    print("--- 2. FETCHING AVAILABLE PRODUCTS ---")
    active_products = product_repo.get_all_active()
    for p in active_products:
        print(f"ID: {p.product_id} | Product: {p.name} | Price: ${p.price}")
    print("")

    print("--- 3. CREATING A COMPLETE ORDER (Transaction Test) ---")
    # Criamos o objeto Order usando os dados do cliente salvo
    today = date.today().strftime('%Y-%m-%d')
    order = Order(customer_id=new_customer.customer_id, order_date=today)
    
    # Adicionamos os itens usando o método interno da classe Order
    # Notebook (ID 4) e Mouse (ID 2)
    order.add_item(product_id=4, quantity=1)
    order.add_item(product_id=2, quantity=2)
    
    # O repositório agora recebe o OBJETO completo e cuida da transação
    order_id = order_repo.save(order)

    if order_id:
        print(f"Order #{order_id} successfully created for {new_customer.name}!")
    else:
        print("Failed to create order.")
        return

    print("\n--- 4. FINAL SALES REPORT (Viewing the Result) ---")
    # Usamos a Procedure ou View via Repositório para validar os cálculos do banco
    report = order_repo.get_sales_report()
    
    grand_total = 0
    found = False
    if report:
        for line in report:
            # Filtramos apenas as linhas do pedido que acabamos de criar
            if line['order_id'] == order_id:
                found = True
                print(f"Product: {line['product']} | Qty: {line['quantity']} | Line Total: {line['total_price_formatted']}")
                grand_total += float(line['total_price_raw'])
        
        if found:
            print("-" * 30)
            print(f"ORDER GRAND TOTAL (Calculated by DB): ${grand_total:.2f}")
        else:
            print(f"Order #{order_id} was saved, but no lines were found in the view.")
    else:
        print("No report data available.")

if __name__ == "__main__":
    run_integration_test()