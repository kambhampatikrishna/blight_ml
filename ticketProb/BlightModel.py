import pandas as pd
import numpy as np
import sklearn
import seaborn as sns
from sklearn.model_selection import train_test_split
from .models import BlightModel
def getMappedTicketIdWithProbability():

        train=pd.read_csv(r"C:\Users\krisshnapraneeth\Downloads\ml\train.csv", encoding = 'ISO-8859-1')
        address = pd.read_csv(r'C:\Users\krisshnapraneeth\Downloads\ml\addresses.csv')
        latlons = pd.read_csv(r'C:\Users\krisshnapraneeth\Downloads\ml\latlons.csv')
        test = pd.read_csv(r'C:\Users\krisshnapraneeth\Downloads\ml\test.csv')
        address = address.merge(latlons, left_on='address', right_on='address')
        train = train.merge(address[['ticket_id', 'lat', 'lon']], left_on='ticket_id', right_on='ticket_id')
        test = test.merge(address[['ticket_id', 'lat', 'lon']], left_on='ticket_id', right_on='ticket_id')
        train = train[~train.compliance.isnull()]
        train.drop(['violation_zip_code', 'non_us_str_code', 'payment_date', 'collection_status', 'grafitti_status'], axis=1, inplace=True)
        # test.drop(['violation_zip_code', 'non_us_str_code', 'payment_date', 'collection_status', 'grafitti_status'], axis=1, inplace=True)
        train['ticket_issued_date'] = pd.to_datetime(train['ticket_issued_date'], format='%Y-%m-%d %H:%M:%S')
        train['hearing_date'] = pd.to_datetime(train['hearing_date'], format='%Y-%m-%d %H:%M:%S')
        train.drop(['state_fee', 'admin_fee', 'clean_up_cost'], axis=1, inplace=True)
        for var in ['ticket_issued_date', 'hearing_date']:
            train[var+'_year'] = train[var].apply(lambda x: x.year)
            train[var+'_month'] = train[var].apply(lambda x: x.month)
            train[var+'_dayofweek'] = train[var].apply(lambda x: x.dayofweek)

        train['date_diff'] = train['hearing_date'] - train['ticket_issued_date']
        train['date_diff'] = train['date_diff'].apply(lambda x: x.days)
        train.drop(['ticket_issued_date', 'hearing_date'], axis=1, inplace=True)
        train['date_diff'].describe()
        train.agency_name.value_counts()
        train = train[train['agency_name'] != 'Neighborhood City Halls']
        agency = train.groupby(['agency_name', 'compliance'])['compliance'].count().unstack().sort_values(0)
        agency['compliance_rate'] = agency[1]/(agency[1] + agency[0])*100
      #  print(agency)
        disposition = train.groupby(['disposition', 'compliance'])['compliance'].count().unstack().fillna(0).sort_values(0)
        disposition['disposition_rate'] = disposition[1]/(disposition[1] + disposition[0])*100
     #   print(disposition)
        train['violation_code'] = train['violation_code'].apply(lambda x: x[:2])
        train['violation_code'].value_counts()
        code = train.groupby(['violation_code', 'compliance'])['compliance'].count().unstack().fillna(0).sort_values(0)
        code['disposition_rate'] = code[1]/(code[1] + code[0])*100
       # print(code)
        train.drop(['violation_description'],axis=1, inplace=True)
        train['Michigan'] = train['state'].apply(lambda x: 1 if x == 'MI' else 0)
        train.drop(['mailing_address_str_number', 'mailing_address_str_name', 'city', 'state', 'zip_code', 'country'], axis=1, inplace=True)
        michigan = train.groupby(['Michigan', 'compliance'])['compliance'].count().unstack().fillna(0).sort_values(0)
        michigan['disposition_rate'] = michigan[1]/(michigan[1] + michigan[0])*100
        #print(michigan)
        train.drop(['payment_amount', 'balance_due','payment_status','compliance_detail'], axis=1, inplace=True)
        attributes = ['disposition', 'agency_name', 'violation_code']
        for col in attributes:
            dummies = pd.get_dummies(train[col], prefix=col)
            train = pd.concat([train, dummies], axis=1)
        train.drop(attributes, axis=1, inplace=True)

        features = train.drop(columns=['compliance','inspector_name','violator_name','violation_street_number','violation_street_name'])
        target = pd.DataFrame(train['compliance'])
        # print(features.columns)
        # print(target.shape)

        

        X, X_test, y, y_test = train_test_split(features, target, test_size =0.3, random_state=1)
        ticket_id_list=X_test['ticket_id']
        ticketList = []
        for ele in ticket_id_list:
            ticketList.append(ele)
        # print(ticketList)
       
        from sklearn.impute import SimpleImputer 

        imputer = SimpleImputer(strategy='median')
        imputer.fit(X)
        X = imputer.transform(X)
        X_test = imputer.transform(X_test)

        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import roc_auc_score
        lreg = LogisticRegression()
        lreg.fit(X, y)
    #    print(lreg.predict_proba(X_test))

        #print('AUC:', roc_auc_score(y_test, lreg.predict_proba(X_test)[:,1]))

        from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

        dtree = RandomForestClassifier()
        dtree.fit(X, y)
        l=dtree.predict_proba(X_test)[:,1]
        

        # l1=dtree.predict_proba(test)[:,1]
        # print(l)
        # print(l1)
       # print('AUC:', roc_auc_score(y_test, dtree.predict_proba(X_test)[:,1]))
        probability = []
        for ele in  dtree.predict_proba(X_test)[:,1]:
            probability.append(ele)

        mapped_dictionary = dict()
        for i in range(len(probability)):
            mapped_dictionary[ticketList[i]] = probability[i]
        # print(mapped_dictionary)
        return mapped_dictionary



# def getProbabilityForTicketId(ticket_id):
#     mapped_dictionary = getMappedTicketIdWithProbability()
#     for key,value in mapped_dictionary.items():
#         print(key,value)
#         obj = BlightModel(ticket_id=key,probability=value)
#         obj.save()
    
#     L = list(mapped_dictionary.keys())
#     print(L)
#     # print(ticket_id in L)
#     if(ticket_id in mapped_dictionary.keys()):
#         return mapped_dictionary[ticket_id]
#     else:
#         return None

# # print(dtree.predict_proba(X_test)[:,1])