
import numpy_financial
import pandas
#pandas.options.display.float_format = "{:.2f} €".format
from operator import attrgetter
import warnings
warnings.filterwarnings('ignore')


def getFields():
    field_df = pandas.read_csv(filepath_or_buffer='./schema/fields.csv')
    return field_df


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


def getHomesStyled(home_df, html=False):
    format_dict = {
        'P_total':          '${0:,.0f}',
        'P_total_fin':      '${0:,.2f}',
        'P_monthlyPayment': '{:.2%}',
        'P_rentalYield':    '{:.2%}',
    }
    home_style = home_df.style.format(format_dict).background_gradient(subset=['P_total_fin'], cmap='BuGn')
    #home_style = home_style.render().split('\n')[:1000] if html else home_style
    return home_style


def getHomeSteps(home_d, months=30):
    step_ds_date = pandas.date_range(
        start=home_d['I_moveIn'],
        periods=12 * months,
        freq='MS',
        tz='UTC',
        normalize=True,
        name='date',
        closed=None
    )
    step_df = pandas.DataFrame(data=step_ds_date)
    step_df['home']             = home_d['I_index']
    step_df['month']            = step_df.apply(lambda step : step['date'].to_period('M')  - step_ds_date[0].to_period('M') ,               axis=1).apply(attrgetter('n'))
    step_df['year']             = step_df.apply(lambda step : step['month'] / 12,                                                           axis=1)
    step_df['value']            = step_df.apply(lambda step : home_d['I_price'] * (1 + step['year'] * home_d['I_priceValuationPerYear']),   axis=1)
    step_df['finalBalance']     = step_df.apply(lambda step : numpy_financial.pv(rate=home_d['I_rate']/12, nper=12*(home_d['I_years'] - step['year']), pmt=-home_d['P_monthlyPayment']),   axis=1)
    step_df['rentalIncome']     = step_df.apply(lambda step : home_d['I_rent'],                                                             axis=1)


    return step_df


def getHomesSteps(home_df):
    step_dfl = []
    for index, home_d in home_df.iterrows():
        step_df = getHomeSteps(home_d)
        step_dfl.append(step_df)
    step_df = pandas.concat(step_dfl, axis=0)
    return step_df


def getHomesStepsStyled(step_df, html=False):
    format_dict = {
        'P_total':          '${0:,.0f}',
        'P_total_fin':      '${0:,.2f}',
        'P_monthlyPayment': '{:.2%}',
        'P_rentalYield':    '{:.2%}',
    }
    step_style = step_df.style.format(format_dict).background_gradient(subset=['P_total_fin'], cmap='BuGn')
    #step_style = step_style.render().split('\n')[:1000] if html else step_style
    return home_style


if __name__ == '__main__':
    # 1. Get Homes
    home_df = getHomes()
    home_df = addHomesProjections(home_df=home_df)
    home_style = getHomesStyled(home_df=home_df, html=False)
    print(home_df)

    # 2. Get Homes Steps
    step_df = getHomesSteps(home_df)
    print(step_df[step_df['home'] == 1].head(n=15))
    print(step_df[step_df['home'] == 1].tail(n=15))



