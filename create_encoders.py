"""
Create label encoder pickle files for the fertilizer recommendation system
"""
import pickle
from sklearn.preprocessing import LabelEncoder
from pathlib import Path

# Get the project directory
PROJECT_DIR = Path(__file__).parent

# Create label encoders with realistic values
# CYCLE - 3 classes (indices 0, 1, 2)
le_cycle = LabelEncoder()
le_cycle.fit(['Kharif', 'Rabi', 'Summer'])

# DESCRIPTION - 10 classes (indices 0-9)
le_desc = LabelEncoder()
le_desc.fit([
    'Early Monsoon',
    'Mid Monsoon', 
    'Late Monsoon',
    'Early Winter',
    'Mid Winter',
    'Late Winter',
    'Early Summer',
    'Mid Summer',
    'Late Summer',
    'Transition Period'
])

# FERTILIZER - 7 classes (indices 0-6)
le_fert = LabelEncoder()
le_fert.fit([
    'Urea (46% N)',
    'DAP (18:46:0)',
    'NPK 10:26:26',
    'Potassium Chloride (MOP)',
    'Single Super Phosphate (SSP)',
    'NPK 20:20:0',
    'Ammonium Sulfate (AS)'
])

# Save encoders
pickle.dump(le_cycle, open(PROJECT_DIR / "le_actual_cycle (1).pkl", 'wb'))
pickle.dump(le_desc, open(PROJECT_DIR / "le_actual_desc (1).pkl", 'wb'))
pickle.dump(le_fert, open(PROJECT_DIR / "le_actual_fert (1).pkl", 'wb'))

print("✅ Created label encoders:")
print(f"   - Cycle classes: {list(le_cycle.classes_)}")
print(f"   - Description classes: {list(le_desc.classes_)}")
print(f"   - Fertilizer classes: {list(le_fert.classes_)}")
print("\n✅ Encoder files saved successfully!")
