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
            order_total = order.OrderTotal
            try:
                promotion_discount = item[0].PromotionDiscount
                order_total = float(order_total) + (float(promotion_discount)+ (float(promotion_discount)*0.18))
            except Exception, e:
                dummy=0
            parsed_amazon_order['order_details'] = {
                'order_id':order.AmazonOrderId,
                'order_date':order.PurchaseDate,
                'parent_order_id':None,
                'payment_id':None,
                'payment_method':payment_method,
                'amount':order_total,
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
            vwrite(order_item)
            parsing_successful = False
        try:
            if order.OrderStatus == "Pending":
                buyer_email="dummyemail@gmail.com"
                try:
                    buyer_email = buyer_email
                except Exception, e:
                    vwrite("buyer_email exception for %s" % order.AmazonOrderId)
                    vwrite(e.message)
                    if order.AmazonOrderId!='406-3467514-8935543':
                        parsing_successful = False
                    #parsing_successful = False
                parsed_amazon_order['customer_details'] = {
                    'buyer_id':buyer_email,
                    'buyer_name':"ToBeUpdated",
                    'buyer_email':buyer_email,
                    #'buyer_address_line1':order.ShippingAddress.AddressLine1,
                    'buyer_city':"NA",
                    'buyer_state':"NA",
                    'buyer_zipcode':"NA",
                    'buyer_phone':"NA",
                    'buyer_address_line1':"NA",
                    'buyer_address_line2':"NA"
                }
            else:
                if order.AmazonOrderId=='406-4876683-9312302':
                    buyer_email='mukeshdadhichemailnotfound@marketplace.amazon.in'
                else:
                    buyer_email=order.BuyerEmail
                try:
                    buyer_email = buyer_email
                except Exception, e:
                    vwrite("buyer_email exception for %s" % order.AmazonOrderId)
                    vwrite(e.message)
                    if order.AmazonOrderId!='406-3467514-8935543':
                        parsing_successful = False
                    #parsing_successful = False
                parsed_amazon_order['customer_details'] = {
                    'buyer_id':buyer_email,
                    'buyer_name':order.BuyerName,
                    'buyer_email':buyer_email,
                    #'buyer_address_line1':order.ShippingAddress.AddressLine1,
                    'buyer_city':order.ShippingAddress.City,
                    'buyer_state':order.ShippingAddress.StateOrRegion,
                    'buyer_zipcode':order.ShippingAddress.PostalCode
                }
                #if order.AmazonOrderId=='403-4661462-2381149':
                #    parsed_amazon_order['customer_details']['buyer_phone'] = 'NA'
                #else:
                #    parsed_amazon_order['customer_details']['buyer_phone'] = order.ShippingAddress.Phone
                try:
                    parsed_amazon_order['customer_details']['buyer_phone'] = order.ShippingAddress.Phone
                except Exception, e:
                    parsed_amazon_order['customer_details']['buyer_phone'] = 'NA'
                try:
                    parsed_amazon_order['customer_details']['buyer_address_line1'] = order.ShippingAddress.AddressLine1
                except Exception, e:
                    parsed_amazon_order['customer_details']['buyer_address_line1'] = 'NA'
                try:
                    parsed_amazon_order['customer_details']['buyer_address_line2'] = order.ShippingAddress.AddressLine2
                except Exception, e:
                    parsed_amazon_order['customer_details']['buyer_address_line2'] = 'NA'
            #if 'AddressLine2' in order.ShippingAddress:
	    #if order.AmazonOrderId=='404-0144366-4954730':
            #    parsed_amazon_order['customer_details']['buyer_address_line2'] = ""
            #else:
            #    parsed_amazon_order['customer_details']['buyer_address_line2'] = order.ShippingAddress.AddressLine2
        except Exception, e:
            vwrite("Exception raised in parse_amazon_order - buyer information corrupted")
            vwrite(e)
            vwrite(order_item)
            parsing_successful = False
        try:
            parsed_amazon_order['item_details'] = {
                'item_id': item[0].ASIN,
                'all_items': item # for temporary purpose
            }
        except Exception, e:
            vwrite("Exception raised in parse_amazon_order - item information corrupted")
            vwrite(e)
            vwrite(order_item)
            parsing_successful = False
    else:
        vwrite("Order %s %s" % (order.AmazonOrderId,order.OrderStatus))
    if not parsing_successful or len(parsed_amazon_order)==0:
        parsed_amazon_order = False
    return parsed_amazon_order

