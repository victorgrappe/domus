
import pandas
import numpy_financial

def getProp():
    prop_df = pandas.read_csv(
        filepath_or_buffer='schema/properties.csv',
        dtype={
            'index':                'int64',
            'name':                 'object',
            'address':              'object',
            'provision':            'float64',
            'property':             'float64',
            'propertyRaw':          'float64',
            'propertyNotary':       'float64',
            'propertyWorks':        'float64',
            'propertyValuation':    'float64',
            'mortgageRate':         'float64',
            'mortgageYears':        'int64',
            'propertyArea':         'float64',
            'rent':                 'float64',
            'propertyTax':          'float64',
        },
        parse_dates=['operatingSart',]
    )
    prop_df['total']    = prop_df.apply(lambda prop : prop['propertyRaw'] + prop['propertyNotary'] + prop['propertyWorks'],                                                         axis=1)
    prop_df['mortgage'] = prop_df.apply(lambda prop : prop['total'] - prop['provision'],                                                                                            axis=1)
    prop_df['rent']     = prop_df.apply(lambda prop : numpy_financial.pmt(rate=prop['mortgageRate']/12, nper=prop['mortgageYears']*12, pv=-prop['mortgage'], fv=0, when='end'),     axis=1)
    prop_df['rent']     = prop_df.apply(lambda prop : 12 * prop['rent'] / prop['total'],                                                                                            axis=1)

    return prop_df




if __name__ == '__main__':
    # 1. Get Homes
    prop_df = getProp()
    print(prop_df)