from pathlib import Path
db_path = "C:\Users\CHAK4624\pamidi\02_personal\02_learning\03_python\01_system_monitoring\data\systemMonitoring.db"
db_path = Path.resolve(db_path)

print(db_path)