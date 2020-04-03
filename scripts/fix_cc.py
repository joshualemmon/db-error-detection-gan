import pandas as pd

def main():
	cc = pd.read_csv('../Data/csv/creditcard.csv')
	print(cc.dtypes)
	cc['is_dirty'] = 0
	for col in cc.columns:
		cc[col] = cc[col].astype(float)
	cc.to_csv('../Data/csv/cc.csv', index=False)
if __name__ == "__main__":
	main()