"""
models.py
Xinxu Chen (chenxin@bu.edu)

Defines the Voter model and loads voter data from CSV.
"""

import csv
import os
from datetime import datetime

from django.conf import settings
from django.db import models


class Voter(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)

    street_number = models.CharField(max_length=20, blank=True)
    street_name = models.CharField(max_length=200, blank=True)
    apartment_number = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)
    date_of_registration = models.DateField(null=True, blank=True)

    party_affiliation = models.CharField(max_length=2, blank=True)
    precinct_number = models.CharField(max_length=20, blank=True)

    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    voter_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def street_address(self):
        parts = [self.street_number, self.street_name]
        address = " ".join([part for part in parts if part]).strip()

        if self.apartment_number:
            address += f", Apt {self.apartment_number}"

        return address

    def full_address(self):
        address = self.street_address()

        if self.zip_code:
            address += f", Newton, MA {self.zip_code}"
        else:
            address += ", Newton, MA"

        return address

    @staticmethod
    def parse_date(date_string):
        if not date_string:
            return None

        date_string = date_string.strip()
        if not date_string:
            return None

        for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y']:
            try:
                return datetime.strptime(date_string, fmt).date()
            except ValueError:
                continue

        return None

    @staticmethod
    def parse_bool(value):
        if value is None:
            return False
        return str(value).strip().upper() == 'TRUE'

    @classmethod
    def load_data(cls):
        csv_path = os.path.join(settings.BASE_DIR, 'newton_voters.csv')

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Could not find CSV file: {csv_path}")

        if cls.objects.exists():
            print("Data already loaded.")
            return

        with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                cls.objects.create(
                    last_name=row['Last Name'].strip(),
                    first_name=row['First Name'].strip(),
                    street_number=row['Residential Address - Street Number'].strip(),
                    street_name=row['Residential Address - Street Name'].strip(),
                    apartment_number=row['Residential Address - Apartment Number'].strip(),
                    zip_code=row['Residential Address - Zip Code'].strip(),
                    date_of_birth=cls.parse_date(row['Date of Birth']),
                    date_of_registration=cls.parse_date(row['Date of Registration']),
                    party_affiliation=row['Party Affiliation'].strip(),
                    precinct_number=row['Precinct Number'].strip(),
                    v20state=cls.parse_bool(row['v20state']),
                    v21town=cls.parse_bool(row['v21town']),
                    v21primary=cls.parse_bool(row['v21primary']),
                    v22general=cls.parse_bool(row['v22general']),
                    v23town=cls.parse_bool(row['v23town']),
                    voter_score=int(row['voter_score'].strip()),
                )

        print(f"Loaded {cls.objects.count()} voters.")