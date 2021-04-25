
import pandas

def getHomes():
    home_df = pandas.read_csv(
        filepath_or_buffer='./schema/homes.csv',
        dtype={
            'I_index':      'int64',
            'I_name':       'object',
            'I_Address':    'object',
            'I_price':      'float64',
            'I_notary':     'float64',
            'I_ppd':        'float64',
            'I_works':      'float64',
            'I_initial':    'float64',
            'I_rate':       'float64',
            'I_years':      'int64',
            'I_area':       'float64',
            'I_rent':       'float64',
            'I_propertyTax':'float64',
        },
        parse_dates=['I_moveIn',]
    )
    return home_df


def addHomesProjections(home_df):
    home_df['P_total']          = home_df.apply(lambda home : home['I_price'] + home['I_notary'] + home['I_ppd'] + home['I_works'],                                             axis=1)
    home_df['P_total_fin']      = home_df.apply(lambda home : home['P_total'] - home['I_initial'],                                                                              axis=1)
    home_df['P_monthlyPayment'] = home_df.apply(lambda home : numpy_financial.pmt(rate=home['I_rate']/12, nper=home['I_years']*12, pv=-home['P_total_fin'], fv=0, when='end'),  axis=1)
    home_df['P_rentalYield']    = home_df.apply(lambda home : 12 * home['I_rent'] / home['P_total'],                                                                            axis=1)
    return home_df





if __name__ == '__main__':
    # 1. Get Homes
    home_df = getHomes()
    print(home_df)