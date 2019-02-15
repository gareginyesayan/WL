

from jira import JIRA
#import json
#from dateutil import parser
#import datetime
import ccilib as cci
#import getpass
#import sys
#import gspread
#from oauth2client.service_account import ServiceAccountCredentials
import re


class failed_content:
    
    def __init__(self, title, cci_file):
        self.title = title;
        self.cc = cci.cci(cci_file);
        self.items = self.cc.get_unique_cars_cgi_all()
        self.cla_number = self.cc.get_cla_count();
        self.failed_items = set();
        self.failed_cqc_items =set();
        self.failed_cqa_items = set();
        self.issues = set()
        self.activities = set(self.cc.get_cla_numbers(self.items));
        self.extra_failed_cla = set()

        
    def failed_cla(self):
        return set(self.cc.get_cla_numbers(self.failed_items));
    
    def all_failed_cla(self):
        return self.failed_cla() | self.extra_failed_cla
    
    def failed_cqc_cla(self):
        return set(self.cc.get_cla_numbers(self.failed_cqc_items));
    
    def failed_cqa_cla(self):
        return set(self.cc.get_cla_numbers(self.failed_cqa_items));
    
    def cqc_items_failure_rate(self):
        fr = 'N/A'
        if self.cla_number !=0:
            fr = len(self.failed_cqc_items)/self.cla_number
        return fr;
    
    def cqa_items_failure_rate(self):
        fr = 'N/A'
        if self.cla_number !=0:
            fr = len(self.failed_cqa_items)/self.cla_number
        return fr;
    
    def items_failure_rate(self):
        fr = 'N/A'
        if self.cla_number !=0:
            fr = len(self.failed_items)/self.cla_number
        return fr;
        
def issue_has_cgi(issue, item):
    des = issue.fields.description;
    ex = item + "[^>]*<"
    findings = re.findall(ex, des)
    return len(findings)


def item_failed(CGI):
    
    failed = 0;
    jac = JIRA('https://jira.cengage.com');
    query ='project = MTQA AND text ~ ' + CGI;
    issues = jac.search_issues(query);
    for issue in issues:
        if str(issue.fields.status) in ('Open','In Progress', 'Reopened') or str(issue.fields.resolution)=='Fixed' :
            failed = 1;
    return failed;

def find_all_issues(query):
#    query ='project = MTQA AND issuetype = Bug AND labels = back_half AND labels in (WLCQC)';
    jac = JIRA('https://jira.cengage.com');
    bunch = 50;
    issues = [];
    while bunch == 50:
        print('1')
        iss = jac.search_issues(query, startAt = len(issues) , maxResults = 50);
        bunch = len(list(iss))
        issues = issues + list(iss);
        print('2')
    return issues;

if __name__ == "__main__":
    
    
    titles = {'Conectados':[1]}
  
    query12 = 'project = MTQA AND issuetype = Bug AND labels = WL_2020 AND labels in (WLCQC, WLCQA) AND resolution in (Unresolved, Fixed) and component in (Content) and priority in ("High/Critical", "Blocker/Showstopper")  AND labels = Conectados and bucket = "Phase 3"'
    query34 = 'project = MTQA AND issuetype = Bug AND labels = WL_2020 AND labels in (WLCQC, WLCQA) AND resolution in (Unresolved) and component in (Content) and priority in ("Medium/Major", "Low/Minor")'
  
    issues = find_all_issues(query12)
    print('issues = ', len(issues), '\n');

    for key in titles:    
        title = key;
        cci_file ='C:\\Users\\gyesayan\\CARS\\CCI\\' + title + '_CCI.csv';
        rut = failed_content(title, cci_file)
 
        for item in rut.items:
            for issue in issues:

                if issue_has_cgi(issue, item) and title in issue.fields.labels:
#                    print(item, issue.key, issue_has_cgi(issue, item))
                    if "WLCQA" in issue.fields.labels:
                        rut.failed_cqa_items.add(item);
                    if "WLCQC" in issue.fields.labels:
                        rut.failed_cqc_items.add(item);
                    rut.failed_items.add(item);
                    rut.issues.add(issue.key);
                    
        for cla in rut.activities:
            for issue in issues:
                if (cla in issue.raw['fields']["description"] or cla in issue.fields.summary) and title in issue.fields.labels:
#                    print(cla, issue)
                    rut.extra_failed_cla.add(cla);
                    rut.issues.add(issue.key);

        print(title)

        items = len(set(rut.items))
        failed_items = len(set(rut.failed_items))
        print("Overall unique items: ",items)
        print("failed items: ",failed_items)
        print("item failure rate: ",failed_items/items)
        print("failed CLA: ",len(rut.all_failed_cla()))



    
