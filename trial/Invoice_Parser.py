def bil_by_parser(data):
    names_map={"Bil_by_name":"Business_Name","Bil_by_street":"Street","Bil_by_city":"City","Bil_by_country":"Country",
               "Bil_by_pincode":"Pincode","Bil_by_email":"Email","Bil_by_phone":"Phone"}
    keys=list(data.keys()).copy()
    data["Billed_By"]={}
    for key in keys:
        if "Bil_by" in key:
            new_val=data[key]
            new_key=names_map[key]
            data.pop(key)
            data["Billed_By"][new_key]=new_val
    data["Billed_By"]['Address']=data["Billed_By"]['Street']+','+data["Billed_By"]['City']+','+data["Billed_By"]['Country']+','+data["Billed_By"]['Pincode']
    return data

def bil_to_parser(data):
    names_map={"Bil_to_name":"Business_Name","Bil_to_street":"Street","Bil_to_city":"City","Bil_to_country":"Country",
               "Bil_to_pincode":"Pincode","Bil_to_email":"Email","Bil_to_phone":"Phone"}
    keys=list(data.keys()).copy()
    data["Billed_To"]={}
    for key in keys:
        if "Bil_to" in key:
            new_val=data[key]
            new_key=names_map[key]
            data.pop(key)
            data["Billed_To"][new_key]=new_val
    data["Billed_To"]['Address']=data["Billed_To"]['Street']+','+data["Billed_To"]['City']+','+data["Billed_To"]['Country']+','+data["Billed_To"]['Pincode']
    return data

def item_parser(data):
    names_map={"item_name":"item_name","Rate":"Rate","Quantity":"Quantity","GST_Rate":"GST Rate","CGST":"CGST",
               "SGST":"SGST","Total":"Total"}
    keys=list(data.keys()).copy()
    data["Item"]=[]
    for key in keys:
        rev_key_name=key[::-1]
        ind=rev_key_name.find("_")
        if ind>0:
            ind=-ind
            if key[:ind-1] in names_map:
                try:
                    item_no=int(key[ind:])
                except ValueError:
                    #print("Not a key")
                    continue
                new_key=names_map[key[:ind-1]]
                new_val=data[key]
                if len(data["Item"])==0:
                    data["Item"].append({})
                else:
                    if len(data["Item"])<item_no:
                        data["Item"].append({})
                data["Item"][item_no-1][new_key]=new_val
                data.pop(key)
    return data

def info_parser(data):
    #data={'csrfmiddlewaretoken': '5EPeeIWqkknl0bldNjh4QlJb2erqfivsgWMiEaOBCrfMC4uRQLJuaIVO0McmGz4f', 'invoice_title': 'hi', 'invoice_subtitle': 'hi2', 'Invoice_Date': '2022-07-14', 'Due_Date': '2022-07-14', 'Bil_by_name': 'dsa', 'Bil_by_street': 'lalithanagar near lalitha temple', 'Bil_by_city': 'Visakhapatnam, Andhra Pradesh, India', 'Bil_by_country': 'India', 'Bil_by_pincode': '530016', 'Bil_by_email': 'abhiramganesh98@gmail.com', 'Bil_by_phone': '09573571256', 'Bil_to_name': 'dsa', 'Bil_to_street': 'lalithanagar near lalitha temple', 'Bil_to_city': 'Visakhapatnam, Andhra Pradesh, India', 'Bil_to_country': 'India', 'Bil_to_pincode': '530016', 'Bil_to_email': 'abhiramganesh98@gmail.com', 'Bil_to_phone': '09573571256', 'item_name_1': 'Rajabattula Abhiram', 'Quantity_1': '12', 'Rate_1': '10', 'GST_Rate_1': '12', 'CGST_1': '7.199999999999999', 'SGST_1': '7.199999999999999', 'Total_1': '134.4', 'item_name_2': 'ascx', 'Quantity_2': '10', 'Rate_2': '15', 'GST_Rate_2': '25', 'CGST_2': '18.75', 'SGST_2': '18.75', 'Total_2': '187.5', 'Sub_Total_sum': '321.9', 'Shipping_sum': '', 'Discount_sum': '', 'Total_sum': '321.9'}
    data=bil_by_parser(data)
    data=bil_to_parser(data)
    data=item_parser(data)
    # data.pop("csrfmiddlewaretoken")
    return data


def Html_parser(data):
    line=''
    for i in range(1,len(data)+1):
        item=data[i-1]
        line+="<div class='row item' id='row_"+str(i)+"'><div class='col-xs-2 desc'><input type='text' id='name_"+str(i)+"' name='item_name_"+str(i)+"'placeholder='Name' onkeyup='updateTotal(this.id)' value='"+item['item_title']+"' required><br></div><div class='col-xs-1 desc'><input type='number' id='Q_"+str(i)+"' name='Quantity_"+str(i)+"'placeholder='Quantity' onkeyup='updateTotal(this.id)' value='"+str(item['Quantity'])+"' required><br></div><div class='col-xs-2 desc'><input type='number' id='R_"+str(i)+"' name='Rate_"+str(i)+"'placeholder='Price' onkeyup='updateTotal(this.id)' value='"+str(item['Rate'])+"' required><br></div><div class='col-xs-2 desc'><input type='number' id='G_"+str(i)+"' name='GST_Rate_"+str(i)+"'placeholder='GST_Rate' onkeyup='updateTotal(this.id)' value='"+str(item['item_GST_Rate'])+"' required><br></div><div class='col-xs-2 desc'><input type='number' id='C_"+str(i)+"' name='CGST_"+str(i)+"'placeholder='CGST' onkeyup='updateTotal(this.id)' value='"+str(item['CGST'])+"' readonly><br></div><div class='col-xs-2 qty'><input type='number' id='S_"+str(i)+"' name='SGST_"+str(i)+"' placeholder='SGST'onkeyup='updateTotal(this.id)' value='"+str(item['SGST'])+"' readonly><br></div><div class='col-xs-1 amount text-right'><input type='number' id='T_"+str(i)+"' name='Total_"+str(i)+"'placeholder='Total Amount' value='"+str(item['Total'])+"' readonly><br></div></div>"
    return line