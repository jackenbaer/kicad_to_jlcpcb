import csv
import argparse 





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





if __name__ == "__main__": 
	parser = argparse.ArgumentParser()
	parser.add_argument("--input-pos", required=True, help="Input position file created by kicad")
	parser.add_argument("--input-bom", required=True, help="Input bom file created by kicad")
	args = parser.parse_args()

	#Filenames, yeah should be in the same directory
	INPUT_POS = args.input_pos
	OUTPUT_POS = args.input_pos.split(".")[0] + "-output.csv"
	OUTPUT_POS_XLSX = args.input_pos.split(".")[0] + "-output.xlsx"

	INPUT_BOM = args.input_bom
	OUTPUT_BOM =  args.input_bom.split(".")[0] + "-output.csv"
	OUTPUT_BOM_XLSX = args.input_bom.split(".")[0] + "-output.xlsx"

	print("Reading input positions")
	input_lines = []
	with open(INPUT_POS, "r") as f: 
		reader =csv.reader(f)
		for row  in reader:
			input_lines.append(row)


	print("Writing output pos")
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





	des_to_footprint = { "diode": "D_SOD-123", 
											"r220ohm":"R_0603_1608Metric",
											"r10kohm":"R_0603_1608Metric",
											"transistor":"SOT-23",
											"pmosfet":"TO-252-2",
											"mosfet":"TO-252-2",
											"pinbarlong":"PinHeader_1x24_P2.54mm_Vertical", 
											"pinbar":"PinHeader_1x12_P2.54mm_Vertical",
											"pinbart":"PinHeader_1x04_P2.54mm_Vertical",
											"pinsingle":"PinHeader_1x01_P2.54mm_Vertical",
           
           }
	des_to_comment ={"diode": "C908230", 
											"r220ohm":"C176129",
											"r10kohm":"C15401",
											"transistor":"C2910145",
											"pmosfet":"C115991",
											"mosfet":"AP15N10K",
           						"pinbarlong":"PinHeader_1x24_P2.54mm_Vertical", 
											"pinbar":"PinHeader_1x12_P2.54mm_Vertical",
											"pinbart":"PinHeader_1x04_P2.54mm_Vertical",
											"pinsingle":"PinHeader_1x01_P2.54mm_Vertical",
	}




	print("Writing output bom")
	with open(OUTPUT_BOM, "w") as f : 
		writer = csv.writer(f, delimiter=",", quotechar='"')
		writer.writerow(["Comment", "Designator", "Footprint"])
		
		print(designators)
		for k in designators:
			fields = get_designator_field(designators[k])
			for field in fields: 
				writer.writerow([des_to_comment[k], field, des_to_footprint[k]])





print("Convert shit to xlsx")
# convert to xlsx
import pandas as pd 


df = pd.read_csv(OUTPUT_BOM)
df.to_excel(OUTPUT_BOM_XLSX, index=False, engine='openpyxl')

df = pd.read_csv(OUTPUT_POS)
df.to_excel(OUTPUT_POS_XLSX, index=False, engine='openpyxl')