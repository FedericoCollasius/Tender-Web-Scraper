import re
import requests
import xlsxwriter
from datetime import  datetime, timedelta 



# We will use the requests module to get the json file detailing the tenders from the Acumar website. 
url = 'https://www.acumar.gob.ar/wp-admin/admin-ajax.php?action=wp_ajax_ninja_tables_public_action&table_id=22559&target_action=get-all-data&default_sorting=new_first'
response = requests.get(url=url, verify=False)
licitaciones = response.json()


# We are only interested in tenders that are not older than two weeks old. We will also define the keywords we will be searching for. 
delta = datetime.now() - timedelta(weeks=2)
keywords = ["remediacion", "agua subterranea", "estudio", "caracterizacion", "suelo", "riesgo", "RBCA", "contaminacion"]
interes = []

for l in licitaciones:
    # The date is given as a string in the format YYYY-MM-DDTHoursMinutesSecondsMiliseconds. This standard is a annoying so we will 
    # parse it into YYYY/MM/DD and then into a datetime object.
    try:
        opening_date = datetime.strptime(l['value']['fechadeapertura'], '%Y/%m/%d')

        # Check if the date is not older than delta weeks old. 
        if opening_date >= delta:  
            name_lower = l['value']['nombreproceso'].lower()  
            if any(keyword in l['value']['nombreproceso'] for keyword in keywords):
                link = re.search(r'href=[\'"]?([^\'" >]+)', l['value']['nmerodeproceso']).group(1) 
                interes.append((l['value']['nombreproceso'], link))

    except ValueError:

        # It should be no surprise that a public entity cant even format a date correctly. So we will have to correct it...
        # If the date is not in a valid format, we will correct it and parse it again.

        # Split the date into its parts.
        year =  opening_date.year
        month = opening_date.month
        day = opening_date.day

        # Correct the day and month if they are out of range.
        if int(day) > 31:
            day = str(int(day) % 31)
            if int(month) > 12: 
                month = str(int(month) % 12)
                year = str(int(year) + 1)
            else:
                month = str(int(month) + 1)

        if int(day) == 0: 
            day = str(1)
        
        # Re-assemble the date in the correct format.
        opening_date = f"{year}/{month:02d}/{day:02d}"

        # Parse the date using the datetime module.
        opening_date = datetime.strptime(opening_date, '%Y/%m/%d')

        # Check if the date is not older than a delta weeks old. 
        if opening_date >= delta:    
            name_lower = l['value']['nombreproceso'].lower()  
            if any(keyword in l['value']['nombreproceso'] for keyword in keywords):
                link = re.search(r'href=[\'"]?([^\'" >]+)', l['value']['nmerodeproceso']).group(1) 
                interes.append((l['value']['nombreproceso'], link))
            

# Create a workbook and add a worksheet to add the tenders we are interested in.
workbook = xlsxwriter.Workbook('Acumar.xlsx') 
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': True})

worksheet.write("A1", "Nombre de la licitacion", bold)
worksheet.write("B1", "Link a la licitacion", bold)

row = 1 
col = 0 
for nombre, link in interes:
    worksheet.write(row, col, nombre)
    worksheet.write_url(row, col + 1, link)
    row += 1

workbook.close()