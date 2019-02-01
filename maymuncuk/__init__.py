#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import csv
import sys
from datetime import datetime

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from googleapiclient import sample_tools


from .models import Entry


class Maymuncuk(object):
    date_format = '%Y-%m-%d'
    property_uri = None
    engine = None
    entries = []

    def __init__(self, property_uri):
        self.property_uri = property_uri

    def create_engine(self, filename):
        self.engine = create_engine('sqlite:///{}'.format(filename))

        if (os.path.isfile(filename)):
            print('Datebase is ready.')
            return

        Base.metadata.create_all(self.engine)
        print('Datebase is created.')
    
    def create_session(self):
        if not self.engine:
            print('No engine initialized.')
            return

        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()
    
    def get_entry_count_by_date(self, date):
        return self.session.query(Entry).filter_by(date=date).count()

    def save(self):
        if not self.entries:
            print('No entry to commit.')
            return

        for entry in self.entries:
            self.session.add(entry)
        
        self.session.commit()
        print('Committed {} entries.'.format(len(self.entries)))
        self.entries = []


    def query(self, payload):
        service, flags = sample_tools.init(
            sys.argv, 'webmasters', 'v3', __doc__, __file__, parents=[],
            scope='https://www.googleapis.com/auth/webmasters.readonly')

        response = service.searchanalytics().query(siteUrl=self.property_uri, body=payload).execute()

        for row in response['rows']:
            entry = Entry(
                query=row['keys'][0],
                date=datetime.strptime(payload['startDate'], self.date_format),
                clicks=row['clicks'],
                impressions=row['impressions'],
                ctr=row['ctr'],
                position=row['position'],
            )
            self.entries.append(entry)

        return len(self.entries)