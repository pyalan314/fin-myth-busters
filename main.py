from datetime import datetime, timedelta

import scipy.stats as stats
from icecream import ic

import common


def january_effect(symbol, years=None):
    """
    The "January Effect" is a phenomenon observed in financial markets
    where stock prices tend to experience a rise during the month of January.
    This effect is often attributed to various factors and theories,
    although its exact cause remains debated among experts.
    """
    df = common.generate_daily_ret_df(symbol, years=years)
    # df = df[df['Year'] > 2010]
    jan_ret = df[df['Month'] == 1]['Ret']
    non_jan_ret = df[df['Month'] != 1]['Ret']
    t_statistic, p_value = stats.ttest_ind(
        jan_ret,
        non_jan_ret,
        alternative='greater',
        equal_var=False
    )

    ic(jan_ret.mean())
    ic(non_jan_ret.mean())
    ic(t_statistic)
    ic(p_value)


def may_july_effect(symbol, years=None):
    """
    From wiki
    五窮六絕七翻身 「May is poor, June is bleak, and July will turn around」是香港股市在1980年代至今的一個都市傳說，是當時的經濟分析員在參考過歷年香港股市的升跌而得出的結論。
    結論指：股市在每逢5月時都會開始跌市，到了6月更會大跌，但到了7月，股市卻會起死回生。[1]
    出現此現象是因為香港大多數公司在3月公佈年結業績，之後派息除淨。所以到了5月時，由於大多數公司都已經派息除淨，股價自然會下跌，直到暑假後股民期待中期業績為止。
    美國股市同類理論叫sell in May and go away。
    根據1992年至2011年的恒生指數走勢，20個5月升市跌市各佔一半，6月也是差不多情況，即使5月和6月是跌市，7月也不一定是升市，「五窮六絕七翻身」之說法被認為不準確
    """
    df = common.generate_daily_ret_df(symbol, years=years)
    may_ret = df[df['Month'] == 5]['Ret']
    july_ret = df[df['Month'] == 7]['Ret']
    t_statistic, p_value = stats.ttest_ind(
        may_ret,
        july_ret,
        alternative='less',
        equal_var=False
    )
    ic(may_ret.mean())
    ic(july_ret.mean())
    ic(t_statistic)
    ic(p_value)


def june_july_effect(symbol, years=None):
    """
    Same as may_july_effect
    """
    df = common.generate_daily_ret_df(symbol, years=years)
    df = df[df.index > datetime.today() - timedelta(days=365*years)]
    june_ret = df[df['Month'] == 6]['Ret']
    july_ret = df[df['Month'] == 7]['Ret']
    t_statistic, p_value = stats.ttest_ind(
        june_ret,
        july_ret,
        alternative='less',
        equal_var=False
    )
    ic(june_ret.mean())
    ic(july_ret.mean())
    ic(t_statistic)
    ic(p_value)


def main():
    example1 = common.generate_daily_ret_df('SPY', provider='yahoo', years=10)
    common.explore_ret(example1)
    example2 = common.generate_daily_ret_df('SPY', provider='alpha', years=10)
    common.explore_ret(example2)

    january_effect('^HSI', 10)
    january_effect('^GSPC', 10)

    january_effect('^HSI', 5)
    january_effect('^GSPC', 5)

    may_july_effect('^HSI', 5)
    may_july_effect('^HSI', 10)

    june_july_effect('^HSI', 5)
    june_july_effect('^HSI', 10)


if __name__ == '__main__':
    main()


