import argparse
import pymysql
import pexpect

db = pymsql.connect("localhost","dbuser","passwd","MyDB")
cursor = db.cursor()

def add_filers(filer_name,model, disk_shelf_type,filer_sl_no):
    print("Adding new filer to the database MyDB..")
    sql = "INSERT INTO Hardware_info(Filer_name, \
   Model, Disk_shelf_type, Filer_sl_no, filer_status,user_id,reservation_start,reservation_end) \
   VALUES ('%s', '%s', '%s', '%s', '%s', '%d','%s','%s' )" % \
   (filer_name,model,disk_shelf_type,filer_sl_no,'Free', None, None,None)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
        table_info = cursor.fetchall()
        print("Available Hardwares in the table..")
        print(table_info)
    except:
        # Rollback in case there is any error
        db.rollback()

    # disconnect from server
    db.close()



def list_filers():
    print("List of available filers for reservation....")
    sql = "SELECT * from Hardware_info WHERE filer_status = 'Free'"
    try:
   # Execute the SQL command
        cursor.execute(sql)
        filer_list = cursor.fetchall()
        for filers in filer_list:
            print(filers)
     except:
   # Rollback in case there is any error
   db.rollback()

    # disconnect from server
    db.close()       


def reserve_hardware(userId,filer_name,days):
    print("Reserving filer {} for {} days" .format(filer_name,days))
    sql = "UPDATE Hardware_info SET user_id = '%d', Reservation_start = GETDATE(),Reservation_end = ADDDATE(GETDATE(),'%d'),\
    filer_status = 'RESERVE' WHERE filer_name = '%s'" % (userId,days,filer_name)
     try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    sql = "INSERT INTO History(User_id, Filer_name, Reservation_start = NOW(), Reserved_hours)\
    VALUES ('%d', '%s', '%d')" % (userId,filer_name,None)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()


def release_filer(filer_name):
    print("Released filer {}".format(filer_name))
    child = pexpect.spawn('Some command that requires password')
    child.expect('Enter password:')
    child.sendline('password')
    child.expect(pexpect.EOF, timeout=None)
    cmd_show_data = child.before
    cmd_output = cmd_show_data.split('\r\n')
    for data in cmd_output:
    print data
    status = 'GOOD'
    if status == 'GOOD':
        sql = "UPDATE Hardware_info SET User_id = 'None',Reservation_start = 'None',Reservation_end = 'None',\
    filer_status = 'Free' WHERE filer_name = '%s'" % (filer_name)
    else:
        sql = "UPDATE Hardware_info SET User_id = 'None', Reservation_start = 'None',Reservation_end = 'None',\
    filer_status = 'Bad' WHERE filer_name = '%s'" % (filer_name)
    try:

        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    sql = "UPDATE History SET Reserved_hours = HOUR(Reservation_start) WHERE Filer_name = '%s'"% filer_name
     try:

        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    
    # disconnect from server
    db.close()


def history(filer_name):
    print("History of filer {}".format(filer_name))
    sql = "SELECT * FROM HISTORY WHERE Filer_name = '%s'" % filer_name
     try:

        # Execute the SQL command
        cursor.execute(sql)
        filer_history = cursor.fetchall()
        for history in filer_history:
            print(history)

    except:
        # Rollback in case there is any error
        db.rollback()
    db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-A","add", nargs=4,help="Add hardwares/filers",action="store_true")
    parser.add_argument("-L","--list", help="List available hardwares/filers",action="store_true")
    parser.add_argument("-R","--reserve", nargs=3, help="Reserve hardware/filer")
    parser.add_argument("-REL","--release", nargs=1, help="Release reserved hardware/filer")
    parser.add_argument("-H","--history", nargs=1, help="History of the selected hardware/filer")
    args = parser.parse_args()
    if args.add:
        filer_name = args.add[0]
        model = args.add[1]
        disk_shelf_type = args.add[2]
        filer_sl_no = args.add[3]
        add_filers(filer_name,model,disk_shelf_type,filer_sl_no)
    elif args.list:
        list_filers()
    elif args.reserve:
         user_id = args.reserve[0]
         filer_name = args.reserve[1]
         days_to_reserve = args.reserve[2]
         reserve_hardware(user_id,filer_name,days_to_reserve)
    elif args.release:
        filer_name = args.release[0]
        release_filer(filer_name)
    elif args.history:
        filer_name = args.history[0]
        history(filer_name)
    else:
        pass
    
