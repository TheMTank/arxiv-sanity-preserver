import pickle

with open('db.p', 'rb') as f:
	new_db = pickle.load(f)
with open('db_jan_13th.p', 'rb') as f: 
        old_db = pickle.load(f)

print(len(new_db), len(old_db))
merged_db = {**new_db, **old_db}
print(len(merged_db))

with open('db.p', 'wb') as f:
	pickle.dump(merged_db, f)
