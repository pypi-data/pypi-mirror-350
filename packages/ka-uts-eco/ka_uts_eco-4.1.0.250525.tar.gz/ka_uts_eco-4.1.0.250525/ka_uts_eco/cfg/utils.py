"""
This module provides utility classes for the management of OmniTracker
EcoVadis NHRR (Nachhaltigkeits Risiko Rating) processing for Department UMH
"""
from typing import Any

TyArr = list[Any]
TyDic = dict[Any, Any]
TyAoD = list[TyDic]
TyDoAoD = dict[Any, TyAoD]


class CfgUtils:

    d_ecv_iq2umh_iq = {
        'Sehr niedrig': '1',
        'Niedrig': '2',
        'Mittelniedrig': '3',
        'Mittelhoch': '4',
        'Hoch': '4',
        'Sehr hoch': '4',
        'Undefiniert': '4',
    }

    otex_key_objectid = 'Eindeutige ID'
    otex_key_duns = 'DUNS-Nummer'
    otex_key_coco = 'Landesvorwahl'
    otex_key_poco = 'Postleitzahl'
    otex_key_town = 'Stadt'

    otex_key_cc = 'Landesvorwahl'

    evex_key_cc = 'Land'

    a_otex_key: TyArr = [
        'DUNS-Nummer',
        'Steuer-ID',
        'Umsatzsteuer-ID',
        'Handelsregister-Nr',
        'Offizieller Name des Unternehmens',
        'LEI'
    ]

    d_otex2evex_keys: TyDic = {
        'DUNS-Nummer': 'DUNS-Nummer',
        'Steuer-ID': 'Steuer-ID oder andere Identifikationsnummer',
        'Umsatzsteuer-ID': 'Steuer-ID oder andere Identifikationsnummer',
        'Handelsregister-Nr': 'Steuer-ID oder andere Identifikationsnummer',
        'Offizieller Name des Unternehmens': 'Name des Unternehmens',
        'LEI': 'Steuer-ID oder andere Identifikationsnummer',
        'Eindeutige ID': 'Eindeutige ID'
    }

    d_evex2otex_keys: TyDic = {
        'Eindeutige ID': 'Eindeutige ID',
        'IQ-ID': 'IQ-ID'
    }

    d_evup_en2de: TyDic = {
        "UniqueId": "Eindeutige ID",
        "CompanyName": "Offizieller Name des Unternehmens",
        "CriticalityScale": "ScaleAbc",
        "CriticalityLevel": "Kritikalitätsstufe",
        "SpendScale": "ScaleAbc",
        "SpendLevel": "Spend Level",
        "DunsNumber": "DUNS-Nummer",
        "RegistrationNumber": "Steuer-ID oder andere Identifikationsnummer",
        "CountryCode": "Landesvorwahl",
        "Tags": "Tags",
        "contactFirstName": "Vorname des Ansprechpartners beim Unternehmen",
        "contactLastName": "Nachname des Ansprechpartners beim Unternehmen",
        "contactEmail": "Kontakt-Telefonnummer für das Unternehmen",
    }

    d_evup2const: TyDic = {

        'Anzeigename des Unternehmens (Ihr Name)': None,
        'DUNS-Nummer': '',
        'Steuer-ID oder andere Identifikationsnummer': '',
        'Offizieller Name des Unternehmens': '',

        'Landesvorwahl': '',
        'Postleitzahl': '',
        'Stadt': '',
        'Adresse': '',
        'Eindeutige ID': '',
        'IQ-ID': '',
        'Kritikalitätsstufe': '',
        'Spend Level': '',

        'Vorname des Ansprechpartners beim Unternehmen': '',
        'Nachname des Ansprechpartners beim Unternehmen': '',
        'E-Mail-Adresse des Ansprechpartners beim Unternehmen': '',
        'Kontakt-Telefonnummer für das Unternehmen': '',
        'E-Mail der anfordernden Kontaktperson': '',

        'Tags': 'Union Investment 2024; KRG'
    }

    doaod_evup2otex_keys: TyDoAoD = {
        'id1': [
            {
                'DUNS-Nummer': 'DUNS-Nummer'
            }
        ],
        'id2': [
            {
                'Steuer-ID oder andere Identifikationsnummer': 'Steuer-ID',
                'Landesvorwahl': 'Landesvorwahl'
            },
            {
                'Steuer-ID oder andere Identifikationsnummer': 'Umsatzsteuer-ID',
                'Landesvorwahl': 'Landesvorwahl',
                'Postleitzahl': 'Postleitzahl',
                'Stadt': 'Stadt',
                'Adresse': 'Adresse',
            },
            {
                'Steuer-ID oder andere Identifikationsnummer': 'Handelsregister-Nr',
                'Landesvorwahl': 'Landesvorwahl',
                'Postleitzahl': 'Postleitzahl',
                'Stadt': 'Stadt',
                'Adresse': 'Adresse',
            },
            {
                'Steuer-ID oder andere Identifikationsnummer': 'LEI',
                'Landesvorwahl': 'Landesvorwahl',
                'Postleitzahl': 'Postleitzahl',
                'Stadt': 'Stadt',
                'Adresse': 'Adresse',
            }
        ],
        'id3': [
            {
                'Offizieller Name des Unternehmens': 'Offizieller Name des Unternehmens',
                'Landesvorwahl': 'Land',
                'Postleitzahl': 'Postleitzahl',
                'Stadt': 'Stadt',
                'Adresse': 'Adresse',
            }
        ]
    }

    d_evup2otex_nonkeys: TyDic = {
        'Landesvorwahl': 'Landesvorwahl',
        'Postleitzahl': 'Postleitzahl',
        'Stadt': 'Stadt',
        'Adresse': 'Adresse',
        'Eindeutige ID': 'Eindeutige ID',
        'Anzeigename des Unternehmens': 'Anzeigename des Unternehmens',
        'Offizieller Name des Unternehmens': 'Offizieller Name des Unternehmens'
    }

    d_evup2otex_plz_ort_strasse: TyDic = {
        'Postleitzahl': 'Postleitzahl',
        'Stadt': 'Stadt',
        'Adresse': 'Adresse',
    }

    a_evup_key: TyArr = [
        'DUNS-Nummer',
        'Steuer-ID oder andere Identifikationsnummer',
        'Offizieller Name des Unternehmens'
    ]

    d_del_evup2evex: TyDic = {
        'Eindeutige ID': 'Eindeutige ID',
        'IQ-ID': 'IQ-ID',
    }

    d_evup2evex: TyDic = {
        'IQ-ID': 'IQ-ID',
        'Kritikalitätsstufe': 'Kritikalitätsstufe',
        'Spend Level': 'Spend Level',

        'Vorname des Ansprechpartners beim Unternehmen': 'Vorname des Ansprechpartners beim Unternehmen',
        'Nachname des Ansprechpartners beim Unternehmen': 'Nachname des Ansprechpartners beim Unternehmen',
        'E-Mail-Adresse des Ansprechpartners beim Unternehmen': 'E-Mail-Adresse des Ansprechpartners beim Unternehmen',
        'Kontakt-Telefonnummer für das Unternehmen': 'Kontakt-Telefonnummer für das Unternehmen',
        'E-Mail der anfordernden Kontaktperson': 'E-Mail der anfordernden Kontaktperson',
        'Tags': 'Tags'
    }

    d_evup2otex: TyDic = {
        'Anzeigename des Unternehmens (Ihr Name)': 'Anzeigename des Unternehmens (Ihr Name)',
        'DUNS-Nummer': 'DUNS-Nummer',
        'Offizieller Name des Unternehmens': 'Offizieller Name des Unternehmens',

        'Landesvorwahl': 'Landesvorwahl',
        'Postleitzahl': 'Postleitzahl',
        'Stadt': 'Stadt',
        'Adresse': 'Adresse',
        'Eindeutige ID': 'Eindeutige ID',
    }

    d_otex2evex: TyDic = {
        'IQ-ID': 'IQ-ID',
        'Kritikalitätsstufe': 'Kritikalitätsstufe',
        'Spend Level': 'Spend Level',

        'Vorname des Ansprechpartners beim Unternehmen': 'Vorname des Ansprechpartners beim Unternehmen',
        'Nachname des Ansprechpartners beim Unternehmen': 'Nachname des Ansprechpartners beim Unternehmen',
        'E-Mail-Adresse des Ansprechpartners beim Unternehmen': 'E-Mail-Adresse des Ansprechpartners beim Unternehmen',
        'Kontakt-Telefonnummer für das Unternehmen': 'Kontakt-Telefonnummer für das Unternehmen',
        'E-Mail der anfordernden Kontaktperson': 'E-Mail der anfordernden Kontaktperson',
        'Tags': 'Tags'
    }

    d_evex2otex: TyDic = {
        'IQ-ID': 'IQ-ID',
        'Kritikalitätsstufe': 'Kritikalitätsstufe',
        'Spend Level': 'Spend Level',

        'Vorname des Ansprechpartners beim Unternehmen': 'Vorname des Ansprechpartners beim Unternehmen',
        'Nachname des Ansprechpartners beim Unternehmen': 'Nachname des Ansprechpartners beim Unternehmen',
        'E-Mail-Adresse des Ansprechpartners beim Unternehmen': 'E-Mail-Adresse des Ansprechpartners beim Unternehmen',
        'Kontakt-Telefonnummer für das Unternehmen': 'Kontakt-Telefonnummer für das Unternehmen',
        'E-Mail der anfordernden Kontaktperson': 'E-Mail der anfordernden Kontaktperson',
        'Tags': 'Tags'
    }

    d_otex2evup: TyDic = {
        'Offizieller Name des Unternehmens': 'Offizieller Name des Unternehmens',
        'DUNS-Nummer': 'DUNS-Nummer',
        'Steuer-ID': 'Steuer-ID oder andere Identifikationsnummer',
        'Landesvorwahl': 'Landesvorwahl',
        'Eindeutige ID': 'Eindeutige ID'
    }
