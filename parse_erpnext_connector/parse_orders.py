import datetime
from erpnext_amazon.vlog import vwrite
def timestamptodate(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')
def parse_order(connector_type,order):
    parsed_order = None
    if connector_type.lower() == 'shopclues':
        parsed_order = parse_shopclues_order(order)
    if connector_type.lower() == 'amazon':
        parsed_order = parse_amazon_order(order)
    return parsed_order

def parse_shopclues_order(order):
    parsed_shopclues_order = {}
    parsed_shopclues_order['order_details'] = {
        'order_id':order.get("order_id"),
        'order_date':timestamptodate(order.get("timestamp")),
        'parent_order_id':order.get("parent_order_id"),
        'payment_id':order.get("payment_id"),
    }
    buyer_full_name = order.get("firstname")
    if order.get("lastname"):
        buyer_full_name = buyer_full_name + order.get("lastname")
    parsed_shopclues_order['customer_details'] = {
        'buyer_id':order.get("user_id"),
        'buyer_name':buyer_full_name,
        'buyer_email':order.get("email"),
        'buyer_address_line1':order.get("s_address_2"),
        'buyer_city':order.get("s_city"),
        'buyer_state':order.get("s_state"),
        'buyer_zipcode':order.get("s_zipcode"),
        'buyer_phone':order.get("s_phone"),
    }
    for key, value in order.get("items").items():
        item_id = key
    parsed_shopclues_order['item_details'] = {
        'item_id': item_id,
        'all_items': [{'product_id':item_id,'product':order.get("items").get(item_id).get("product"),'selling_price':order.get("total"),'amount':order.get("items").get(item_id).get("amount")}] # for temporary purpose
    }
    return parsed_shopclues_order

def parse_amazon_order(order_item):
    parsed_amazon_order = {}
    order = order_item[0]
    item = order_item[1].ListOrderItemsResult.OrderItems.OrderItem
    parsing_successful = True
    if order.OrderStatus != 'Canceled' or order.OrderStatus !='Pending':
        try:
            payment_method = None
            if 'PaymentMethod' in order:
                payment_method = order.PaymentMethod
            parsed_amazon_order['order_details'] = {
                'order_id':order.AmazonOrderId,
                'order_date':order.PurchaseDate,
                'parent_order_id':None,
                'payment_id':None,
                'payment_method':payment_method,
                'amount':order.OrderTotal,
                'order_qty':order.NumberOfItemsUnshipped,
                'fulfillment_channel':order.FulfillmentChannel,
                'is_amazon_replacement':order.IsReplacementOrder
            }
            if order.FulfillmentChannel and order.FulfillmentChannel=='AFN':
                parsed_amazon_order['order_details']['fulfillment_channel'] = 'Amazon'
            elif order.FulfillmentChannel and order.FulfillmentChannel=='MFN':
                parsed_amazon_order['order_details']['fulfillment_channel'] = 'Seller'                
        except Exception, e:
            vwrite("Exception raised in parse_amazon_order - order information corrupted")
            vwrite(e)
            parsing_successful = False
        try:
            if 'BuyerEmail' in order:
                buyer_email = order.BuyerEmail
            else:
                buyer_email = "NA"
            parsed_amazon_order['customer_details'] = {
                'buyer_id':buyer_email,
                'buyer_name':order.BuyerName,
                'buyer_email':buyer_email,
                'buyer_address_line1':order.ShippingAddress.AddressLine1,
                'buyer_city':order.ShippingAddress.City,
                'buyer_state':order.ShippingAddress.StateOrRegion,
                'buyer_zipcode':order.ShippingAddress.PostalCode
            }
            if 'Phone' in order.ShippingAddress:
                parsed_amazon_order['customer_details']['buyer_phone'] = order.ShippingAddress.Phone
            else:
                parsed_amazon_order['customer_details']['buyer_phone'] = 'NA'
            if 'AddressLine2' in order.ShippingAddress:
                parsed_amazon_order['customer_details']['buyer_address_line2'] = order.ShippingAddress.AddressLine2
            else:
                parsed_amazon_order['customer_details']['buyer_address_line2'] = ""
                
        except Exception, e:
            vwrite("Exception raised in parse_amazon_order - buyer information corrupted")
            vwrite(e)
            parsing_successful = False
        try:
            parsed_amazon_order['item_details'] = {
                'item_id': item[0].ASIN,
                'all_items': item # for temporary purpose
            }
        except Exception, e:
            vwrite("Exception raised in parse_amazon_order - item information corrupted")
            vwrite(e)
            parsing_successful = False
    else:
        vwrite("Order %s %s" % (order.AmazonOrderId,order.OrderStatus))
    if not parsing_successful or len(parsed_amazon_order)==0:
        parsed_amazon_order = False
    return parsed_amazon_order
