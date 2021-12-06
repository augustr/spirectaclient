#!/usr/bin/env python3

import configparser
import json

from lib.spirecta_client import SpirectaClient

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("spirecta.conf")

    spirecta_client = SpirectaClient(config["spirecta"]["username"],
                                     config["spirecta"]["password"],
                                     config["spirecta"]["client-id"],
                                     config["spirecta"]["client-secret"])
    spirecta_client.touch()
    report = spirecta_client.monthly_result_report()
    # Uncomment to debug full response
    #print(json.dumps(report, indent=4, sort_keys=True))

    income_current = report['data']['total']['income']['current']
    income_budget = report['data']['total']['income']['budget']
    expense_current = report['data']['total']['expense']['current']
    expense_budget = report['data']['total']['expense']['budget']
    result_current = income_current - expense_current
    result_budget = income_budget - expense_budget

    print('Current Income [Budget]: {} [{}]'.format(int(income_current), int(income_budget)))
    print('Current Expense [Budget]: {} [{}]'.format(int(expense_current), int(expense_budget)))
    print('Result [Budget]: {} [{}]'.format(int(result_current), int(result_budget)))

    # Try out some visualization
    import altair as alt
    import pandas as pd
    
    data = pd.DataFrame([[income_current, 'Utfall', 'Inkomst'],
                         [income_budget, 'Budget', 'Inkomst'],
                         [expense_current, 'Utfall', 'Utgifter'],
                         [expense_budget, 'Budget', 'Utgifter'],
                         [result_current, 'Utfall', 'Resultat'],
                         [result_budget, 'Budget', 'Resultat']],
                          columns=['Kronor', 'Typ', 'Nov 2021'])

    alt.Chart(data).mark_bar().encode(alt.Column('Nov 2021'), 
                                      alt.X('Typ'),
                                      alt.Y('Kronor', axis=alt.Axis(grid=False)),
                                      alt.Color('Typ')).show()
