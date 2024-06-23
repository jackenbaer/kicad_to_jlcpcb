import csv


INPUT_POS = "Untitled-all-pos.csv"
OUTPUT_POS = "output-pos.csv"
OUTPUT_POS_XLSX = "output-pos.xlsx"

INPUT_BOM = "bom.csv"
OUTPUT_BOM = "output-bom.csv"
OUTPUT_BOM_XLSX = "output-bom.xlsx"


input_lines = []
with open(INPUT_POS, "r") as f: 
  reader =csv.reader(f)
  for row  in reader:
    input_lines.append(row)



designators = {}
with open(OUTPUT_POS, "w") as o: 
  writer = csv.writer(o, delimiter=",", quotechar='"')
  
  writer.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])
  
  for i, row in enumerate(input_lines[1:]): 
    designator = row[0] + str(i) 
    
    if row[0].lower() in designators:
      designators[row[0].lower()].append(designator.lower())
    else:
      designators[row[0].lower()] = [designator.lower()]
    
    midx = row[3][:-2] + "mm"
    midy = row[4][:-2] + "mm"
    layer = "Top"
    rotation = int(float(row[5])) % 360 
    
    writer.writerow([designator.lower(), midx, midy, layer, rotation])






def get_designator_field(liste): 
  res  = []
  cntr = 0 
  s =""
  for key in liste:
    if cntr > 150: 
      s += key
      res.append(s)
      s = ""
      cntr = 0
    else: 
      s += key + ","
    cntr +=1
  res.append(s)
  return res

des_to_footprint = { "diode": "D_SOD-123", 
                    "r220ohm":"R_0603_1608Metric",
                    "r10kohm":"R_0603_1608Metric",
                    "transistor":"SOT-23",
                    "pmosfet":"TO-252-2",
                    "mosfet":"TO-252-2",
}
des_to_comment ={"diode": "C908230", 
                    "r220ohm":"C176129",
                    "r10kohm":"C15401",
                    "transistor":"C2910145",
                    "pmosfet":"C115991",
                    "mosfet":"AP15N10K",
	
}

with open(OUTPUT_BOM, "w") as f : 
  writer = csv.writer(f, delimiter=",", quotechar='"')
  writer.writerow(["Comment", "Designator", "Footprint"])
  
  print(designators)
  for k in designators:
    fields = get_designator_field(designators[k])
    for field in fields: 
      writer.writerow([des_to_comment[k], field, des_to_footprint[k]])

    
    




# convert to xlsx
import pandas as pd 


df = pd.read_csv(OUTPUT_BOM)
df.to_excel(OUTPUT_BOM_XLSX, index=False, engine='openpyxl')

df = pd.read_csv(OUTPUT_POS)
df.to_excel(OUTPUT_POS_XLSX, index=False, engine='openpyxl')