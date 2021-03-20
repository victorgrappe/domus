
import pandas

print("Hello domus")

def getFields():
    field_df = pandas.read_csv(filepath_or_buffer='./schema/fields.csv')
    return field_df

def getHomes():
    home_df = pandas.read_csv(filepath_or_buffer='./schema/homes.csv')
    return home_df

if __name__ == '__main__':
    field_df = getFields()
    home_df = getHomes()
    print(field_df)
    print(home_df)