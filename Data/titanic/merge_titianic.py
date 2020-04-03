import pandas as pd
def main():
	train = pd.read_csv('train.csv', quotechar='"')
	lived = train['Survived']
	train.drop('Survived', axis=1, inplace=True)
	train = pd.concat([train, lived], axis=1)
	test = pd.read_csv('test.csv', quotechar='"')
	testy = pd.read_csv('gender_submission.csv')
	testy.drop('PassengerId', axis=1, inplace=True)
	test = pd.concat([test, testy], axis=1)

	final = pd.concat([train,test], ignore_index=True)

	temp = final['Name'].str.replace('"','').str.split(',', n=1, expand=True)
	final['Name'] = temp[1] + ' ' +  temp[0]
	final.fillna(value={'Age': 0, 'Cabin':' ', 'Fare':0, 'Embarked' : ' '}, inplace=True)
	final['is_dirty'] = 0
	final.to_csv('titanic.csv', index=False)

if __name__ == "__main__":
	main()