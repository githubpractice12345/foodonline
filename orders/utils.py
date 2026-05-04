import datetime
import simplejson as json

def generate_order_number(pk):
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S') #20260421113340 + pk
    order_number = current_datetime + str(pk)
    return order_number


def total_order_by_vendor(order, vendor_id):
    total_data = json.loads(order.total_data)
    data = total_data.get(str(vendor_id))
    subtotal = 0
    tax = 0
    tax_dict = {}

    
    for key, val in data.items():
        # print(key, value)
        subtotal += float(key)
        val = val.replace("'", '"')
        val = json.loads(val)
        tax_dict.update(val)
            
        #calculate tax
        #{'CGST': {'9.00': '54.00'}, 'SGST': {'7.00': '42.00'}}
        for i in val:
            for j in val[i]:
                tax += float(val[i][j])
    grand_total = float(subtotal) + float(tax)
    # print('subtotal==>', subtotal)
    # print('tax==>', tax)
    # print('tax_dict==>', tax_dict)
    # print('grand_total==>', grand_total)

    context = {
        'subtotal': subtotal,
        'tax_dict': tax_dict,
        'grand_total': grand_total,
    }
    return context