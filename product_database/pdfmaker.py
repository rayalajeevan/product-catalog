from fpdf import FPDF
import xlwt

title="Products List"
class PdfMaker(FPDF):
    def __init__(self,*args,**kwrgs):
        super().__init__(*args,**kwrgs)  
          
    def header(self):
        self.set_font('Arial', '', 7)
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        self.set_draw_color(0,0,250)
        self.set_fill_color(0,0,250)
        self.set_text_color(255,255,255)
        self.set_line_width(1)
        self.cell(w, 9, title, 1, 1, 'C', 1)
        self.ln(10)
        
    def makeData(self,data):
        epw=self.w - 2*self.l_margin
        col_width =epw/10
        dataList=("Prodcut ID","Product Name","Price","Category","Quantity","Description","Created By","Updated By","Created On","Updated On")
        for x in dataList:
            if dataList.index(x) in [5,8,9]:
                self.cell(col_width+5, 15, str(x), border=1)
            else:
                self.cell(col_width-1, 15, str(x), border=1)
        self.ln(15)
        for x in data:
            for key,value in x.items():
                if key in ["description","created_on","updated_on"]:
                    self.cell(col_width+5, 15,str(value)[0:18]+"..." if len(str(value))>18 else str(value) , border=1)
                else:
                    self.cell(col_width-1, 15, str(value), border=1)
            self.ln(15)

class ExcelMaker():
    
    def makeExcelSheet(self,objs):
        dataList=("Prodcut ID","Product Name","Price","Category","Quantity","Description","Created By","Updated By","Created On","Updated On")
        wb=xlwt.Workbook()
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        style.font = font
        sheet1 = wb.add_sheet('PRODUCTS')
        for x in range(len(dataList)):
            sheet1.write(0,x,dataList[x],style=style)
        for y in range(len(objs)):
            z=0
            for value in objs[y].values():
                sheet1.write(y+1,z,value) 
                z+=1
        wb.save("productslist.xls")
            