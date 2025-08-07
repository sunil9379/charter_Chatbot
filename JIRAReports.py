from jira import JIRA
import pandas as pd
import json


jira_server = 'https://jira.charter.com/'
jira_username = 'P3205066'
jira_password = 'RubeeTech@2512'
jql_query = "project = ITDACIT AND status = Retest  ORDER BY created DESC"


jira = JIRA(server=jira_server, basic_auth=(jira_username, jira_password))
tickets = jira.search_issues(jql_query)
tickets_1 = pd.DataFrame(tickets)
tickets_1['Status'] = "Retest"
tickets_1['Title'] = "Bug"
tickets_1.rename(columns={0: 'Ticket ID'}, inplace=True)
Tickets_dict = dict(tickets_1)
df = pd.DataFrame(Tickets_dict)
json_data = json.dumps(Tickets_dict)
print(json_data)


