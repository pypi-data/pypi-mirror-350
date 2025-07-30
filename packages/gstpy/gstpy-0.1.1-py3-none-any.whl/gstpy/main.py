from tabulate import tabulate
#class
class GST:
    def __init__(self,items=0,rate=18,mode="exclusive"):
        self.items = items
        self.rate = rate
        self.type = "exclusive"
        self.data = []
        self.exclusive_data = []
        self.inclusive_data = []
        self.exclusive_data_qty = []
        self.inclusive_data_qty = []
        if isinstance(self.items,list) or isinstance(self.items,dict):
            if mode.lower() =="exclusive":
                    self.exclusive(items=self.items,rate=self.rate,out="table")
            elif mode.lower() == "inclusive":
                self.inclusive(items=self.items,rate=self.rate,out="table")

        if isinstance(self.items,int):
            if self.items >=1:
                if mode.lower() =="exclusive":
                    self.exclusive(items=self.items,rate=self.rate,out="table")
                elif mode.lower() == "inclusive":
                    self.inclusive(items=self.items,rate=self.rate,out="table")

            
    #display function for both exclusive and inclusive   
    def display_data(self,data,qty=False,mode="exclusive",rate=18):
        raw_data = data.copy()
        HEADER_EX = ["S.No.","Item","Price (₹)",f"Tax {rate}%","Total (₹)"]
        #name,amount,qty,tax,total_tax,total_amount
        HEADER_EX_QTY = ["S.No.","Item","Price (₹)","Qty",f"Tax {rate}%",f"Total Tax {rate}%","Total (₹)"]

        HEADER_IN = ["S.No.","Item","Actual Price (₹)",f"Tax {rate}%","Total (₹)"]
        #name,amount,qty,tax,total_tax,total_amount
        HEADER_IN_QTY = ["S.No.","Item","Actual Price (₹)","Qty","Total AP (₹)",f"Tax {rate}%",f"Total Tax {rate}%","Total (₹)"]



        last_index = len(raw_data)
        total_price = 0
        total_tax = 0
        total_amount = 0
        total_qty = 0
        total_tax_qty = 0
        actual_price =0
        total_actual_price=0
        if mode == "exclusive":
            if qty == True:
                #name,amount,qty,tax,total_tax,total_amount
                for i in range(0,last_index):
                    total_price = total_price + raw_data[i][1]
                    total_qty = total_qty + raw_data[i][2]
                    total_tax = total_tax + raw_data[i][3]
                    total_tax_qty = total_tax_qty + raw_data[i][4]
                    total_amount = total_amount + raw_data[i][5]
                raw_data.insert(last_index,["Grand Total = ",total_price,total_qty,total_tax,total_tax_qty,total_amount])
            else:
                for i in range(0,last_index):
                    total_price = total_price + raw_data[i][1]
                    total_tax = total_tax + raw_data[i][2]
                    total_amount = total_amount + raw_data[i][3]
                raw_data.insert(last_index,["Grand Total = ",total_price,total_tax,total_amount])


        elif mode == "inclusive":
            actual_price =0
            total_qty = 0
            total_actual_price = 0
            total_tax = 0
            total_tax_qty = 0
            total_amount = 0
            if qty == True:
                #name,amount,qty,tax,total_tax,total_amount
                for i in range(0,last_index):
                    actual_price = actual_price + raw_data[i][1]
                    total_qty = total_qty + raw_data[i][2]
                    total_actual_price = total_actual_price + raw_data[i][3]
                    total_tax = total_tax + raw_data[i][4]
                    total_tax_qty = total_tax_qty + raw_data[i][5]
                    total_amount = total_amount + raw_data[i][6]
                
                raw_data.insert(last_index,["Grand Total = ",total_price,total_qty,total_actual_price,total_tax,total_tax_qty,total_amount])
            else:
                for i in range(0,last_index):
                    total_price = total_price + raw_data[i][1]
                    total_tax = total_tax + raw_data[i][2]
                    total_amount = total_amount + raw_data[i][3]
                raw_data.insert(last_index,["Grand Total = ",total_price,total_tax,total_amount])

            for num in range(0,len(raw_data)-1):
                raw_data[num].insert(0,num+1)
            raw_data[len(raw_data)-1].insert(0,"##>")

        if qty == False:
            if mode=="exclusive":
                print(tabulate(raw_data, HEADER_EX, tablefmt="rounded_grid"))
            elif mode=="inclusive":
                print(tabulate(raw_data, HEADER_IN, tablefmt="rounded_grid"))
        elif qty == True:
            if mode=="exclusive":
                print(tabulate(raw_data, HEADER_EX_QTY, tablefmt="rounded_grid"))
            elif mode=="inclusive":
                print(tabulate(raw_data, HEADER_IN_QTY, tablefmt="rounded_grid"))

        

                

    #exclusive() method solve exclusive gst
    def exclusive(self,items,rate=18,out="list"):
        qty = False
        self.exclusive_data = []
        self.exclusive_data_qty = []
        if isinstance(items,list):
            if isinstance(items[0],int):
                for amount in items:
                    item_name = ""
                    tax = (amount*rate)/100 
                    total_amount= round(tax+amount,2)
                    #name, amount, tax, total_amount
                    self.exclusive_data.append([item_name,round(amount,2),round(tax,2),total_amount])
                self.data = self.exclusive_data.copy()
            
            elif len(items[0])>2:
                qty = True
                for data in items:
                    item_name = data[0]
                    amount=round(data[1],2)
                    qty_number = data[2]
                    tax = (amount*rate)/100
                    total_tax = round(tax*qty_number,2)
                    total_amount = round(amount+total_tax,2)
                    #name,amount,qty,tax,total_tax,total_amount
                    self.exclusive_data_qty.append([item_name,amount,qty_number,round(tax,2),total_tax,total_amount])
                self.data = self.exclusive_data_qty.copy()

            else:
                for data in items:
                    item_name = data[0]
                    amount = round(data[1],2)
                    tax = (data[1]*rate)/100 
                    total_amount = round(tax+amount,2)
                    #name, amount, tax, total_amount
                    self.exclusive_data.append([item_name,amount,round(tax,2),total_amount])
                self.data = self.exclusive_data.copy()
        elif isinstance(items,dict):
            if isinstance(list(items.values())[0],int):
                for item_name,amount in items.items():
                    tax = (amount*rate)/100 
                    self.exclusive_data.append([item_name,round(amount,2),round(tax,2),round(amount+tax,2)])
                self.data = self.exclusive_data.copy()
            elif isinstance(list(items.values())[0],list):
                qty = True
                for item_name,amount_and_qty in items.items():
                    amount = round(amount_and_qty[0],2)
                    qty_number = amount_and_qty[1]
                    tax = (amount*rate)/100
                    total_tax = round(tax*qty_number,2)
                    total_amount = round(amount+total_tax,2)
                    self.exclusive_data_qty.append([item_name,amount,qty_number,round(tax,2),total_tax,total_amount])
                self.data = self.exclusive_data_qty.copy()

        elif isinstance(items,int):
            tax = (items*rate)/100
            self.exclusive_data.append(["",items,round(tax,2),round(items+tax,2)])
            self.data = self.exclusive_data.copy()
        else:
            print("pass correct data")
        
        if out.lower() == "list":
            if qty == False:
                return self.exclusive_data
            elif qty == True:
                return self.exclusive_data_qty

        elif out.lower() == "dict":
            dict_data = {}
            if qty == False:
                for data in self.exclusive_data:
                    dict_data[data[0]]=data[1:]
                return dict_data
            else:
                for data in self.exclusive_data_qty:
                    dict_data[data[0]]=data[1:]
                return dict_data

        elif out.lower() =="table":
            if qty == True:
                self.display_data(data=self.exclusive_data_qty, rate=rate,qty=True)
            else:
                self.display_data(data=self.exclusive_data, rate=rate)
    '''
        inclusive method
    '''            

    #inclusive() method solve inclusive gst
    def inclusive(self,items,rate=18,out="list"):
        qty = False
        self.inclusive_data = []
        self.inclusive_data_qty = []
        if isinstance(items,list):
            if isinstance(items[0],int):
                for amount in items:
                    item_name = ""
                    tax = (amount*rate)/(100+rate) 
                    total_amount= round(amount,2)
                    #name, amount, tax, total_amount
                    self.inclusive_data.append([item_name,round(amount-tax,2),round(tax,2),total_amount])
                self.data = self.inclusive_data.copy()
            
            elif len(items[0])>2:
                self.inclusive_data_qty = []
                qty = True
                for data in items:
                    item_name = data[0]
                    amount=round(data[1],2)
                    qty_number = data[2]
                    tax = (amount*rate)/(100+rate) 
                    total_tax = round(tax*qty_number,2)
                    total_amount = round(amount*qty_number,2)
                    actual_amount = amount - tax
                    total_actual_amount = actual_amount * qty_number
                    #name,amount,qty,tax,total_tax,total_amount
                    self.inclusive_data_qty.append([item_name,actual_amount,qty_number,total_actual_amount,round(tax,2),total_tax,total_amount])
                self.data = self.inclusive_data_qty.copy()

            else:
                for data in items:
                    item_name = data[0]
                    amount = round(data[1],2)
                    tax = (data[1]*rate)/(100+rate)  
                    total_amount = round(amount,2)
                    #name, amount, tax, total_amount
                    self.inclusive_data.append([item_name,amount-tax,round(tax,2),total_amount])
                self.data = self.inclusive_data.copy()
        elif isinstance(items,dict):
            if isinstance(list(items.values())[0],int):
                for item_name,amount in items.items():
                    tax = (amount*rate)/(100+rate)  
                    self.inclusive_data.append([item_name,round(amount-tax,2),round(tax,2),round(amount,2)])
                self.data = self.inclusive_data.copy()
            elif isinstance(list(items.values())[0],list):
                self.inclusive_data_qty = []
                qty = True
                for item_name,amount_and_qty in items.items():
                    amount = round(amount_and_qty[0],2)
                    qty_number = amount_and_qty[1]
                    tax = (amount*rate)/(100+rate) 
                    total_tax = round(tax*qty_number,2)
                    total_amount = round(amount*qty_number,2)
                    actual_amount = amount - tax
                    total_actual_amount = actual_amount * qty_number
                    self.inclusive_data_qty.append([item_name, actual_amount, qty_number, total_actual_amount,round(tax,2),total_tax,total_amount])
                self.data = self.inclusive_data_qty.copy()

        elif isinstance(items,int):
            tax = (items*rate)/(100+rate) 
            self.inclusive_data.append(["",items-tax,round(tax,2),round(items,2)])
            self.data = self.inclusive_data.copy()
        else:
            print("pass correct data")
        
        if out.lower() == "list":
            if qty == False:
                return self.inclusive_data
            elif qty == True:
                return self.inclusive_data_qty

        elif out.lower() == "dict":
            dict_data = {}
            if qty == False:
                for data in self.inclusive_data:
                    dict_data[data[0]]=data[1:]
                return dict_data
            else:
                for data in self.inclusive_data_qty:
                    dict_data[data[0]]=data[1:]
                return dict_data

        elif out.lower() =="table":
            if qty == True:
                self.display_data(data=self.inclusive_data_qty, rate=rate,qty=True,mode="inclusive")
            else:
                self.display_data(data=self.inclusive_data, rate=rate,mode="inclusive")
    
    #gst() is super funtion that handle the all type of GSTs like exclusive and inclusive       
    def gst(self,items,rate=18,out="list",mode = "exclusice"):
        if mode.lower() == "exclusive":
            self.exclusive(items=items,rate=rate,out=out)
        elif mode.lower() == "inclusive":
            self.inclusive(items=items,rate=rate,out=out)

 #exgst function return a exclusive gst rate single value   
def exgst(price, rate = 18):
    return (price*rate) / 100
 #ingst function return a inclusive gst rate single value
def ingst(price,rate = 18):
    return (price*rate) / (100 + rate)
