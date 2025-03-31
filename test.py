import chardet

file_path = "Data_Categories.CSV"

with open(file_path, "rb") as f:
    rawdata = f.read()

result = chardet.detect(rawdata)
print(result)  # This will show the detected encoding