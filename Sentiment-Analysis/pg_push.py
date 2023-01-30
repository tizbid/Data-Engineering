import psycopg2
import configparser
import csv


# Import credentials
config = configparser.ConfigParser()
#Read configuration
config.read('config.ini')
language_key = config['language']['key']
language_endpoint = config['language']['endpoint']



# Update connection string information
host = config['postgreSQL_DB']['host']
dbname = config['postgreSQL_DB']['dbname']
user = config['postgreSQL_DB']['user']
password = config['postgreSQL_DB']['password']
sslmode = config['postgreSQL_DB']['sslmode']

# Construct connection string

def db_connect():
    
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    conn = psycopg2.connect(conn_string)
    print("Connection established")

    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS opinion_Poll;")
    print("Finished dropping table (if existed)")

    # Create a table to store the data from the CSV file
    cursor.execute("CREATE TABLE opinion_Poll (tweet_no int, Location varchar(255), Tweet varchar(255), sentiment varchar(255));")
    print("Finished creating table")

    #cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
    #print (cursor.fetchall())



    # Import the CSV file into the new table
    with open(r'C:\Users\tizbi\Desktop\Projects\Week-1\Sentiment-Analysis\SA_df.csv', 'r') as f:
        #cursor.copy_from(f, 'Opinion_Poll', sep=',')
        reader = csv.reader(f)
        header = next(reader)
        query = "COPY opinion_Poll ({0}) FROM STDIN WITH CSV HEADER".format(','.join(header))
        cursor.copy_from(f, 'opinion_Poll', sep=',')

    # Close the connection
    conn.commit()
    cursor.close()
    conn.close()
    
    return
