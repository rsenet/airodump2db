import argparse
import sqlite3
import time  
import csv
import sys
import os

__author__  = 'Regis SENET'
__email__   = 'regis.senet@orhus.fr'
__git__     = 'https://github.com/rsenet/airodump2db'
__version__ = '0.1'
__license__ = 'GPLv3'
__pyver__   = '%d.%d.%d' % sys.version_info[0:3]
short_desc  = "Airodump to SQLite database"


arg_parser = argparse.ArgumentParser(description=short_desc)
arg_parser.add_argument('--input', help="Specify the CSV output from Airodump-ng (sudo airodump-ng wlan0mon -w FILENAME --output-format csv")
args = arg_parser.parse_args()

try:
    # Get variable
    timestamp = time.time()
    airodump_input = args.input

    if airodump_input:
        if os.path.exists(airodump_input):
            con = sqlite3.connect(f"airodump2db-{timestamp}.db")
            cur = con.cursor()

            # Create database
            cur.execute("CREATE TABLE airodump2db ('BSSID',\
                                                   'First time seen',\
                                                   'Last time seen',\
                                                   'Channel',\
                                                   'Speed',\
                                                   'Privacy',\
                                                   'Cipher',\
                                                   'Authentication',\
                                                   'Power',\
                                                   'Beacons',\
                                                   'IV',\
                                                   'LAN IP',\
                                                   'ID length',\
                                                   'ESSID',\
                                                   'Key');")

            with open(airodump_input,'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0

                try:
                    for row in csv_reader:
                        if line_count == 0:
                            line_count += 1

                        else:
                            sql = "INSERT INTO airodump2db ('BSSID', 'First time seen', 'Last time seen', 'Channel', 'Speed', 'Privacy', 'Cipher', \
                                                            'Authentication', 'Power', 'Beacons', 'IV', 'LAN IP', 'ID length', 'ESSID', 'Key') \
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                            value = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],\
                                     row[9], row[10], row[11], row[12], row[13], row[14])
                            cur.execute(sql, value)
                            con.commit()

                            line_count += 1

                except IndexError:
                    pass

                print(f'Processed {line_count} lines.')

        else:
             print(f"\n[x] Unable to find {main_file}. Leaving ...")

    else:
        arg_parser.print_help()

except KeyboardInterrupt:
    print("\n[x] Leaving ...")

