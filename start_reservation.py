import argparse


def list_filers():
    print("Available filers are....")
    pass

def reserve_hardware(filer_name,days):
    print("Reserving filer {} for {} days" .format(filer_name,days))
    pass

def release_filer(filer_name):
    print("Released filer {}".format(filer_name))
    pass

def history(filer_name):
    print("History of filer {}".format(filer_name))
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-L","--list", help="List available harwares/filers",action="store_true")
    parser.add_argument("-R","--reserve", nargs=2, help="Reserve hardware/filer")
    parser.add_argument("-REL","--release", nargs=1, help="Release reserved hardware/filer")
    parser.add_argument("-H","--history", nargs=1, help="History of the selected hardware/filer")
    args = parser.parse_args()
    if args.list:
        list_filers()
    elif args.reserve:
         filer_name = args.reserve[0]
         days_to_reserve = args.reserve[1]
         reserve_hardware(filer_name,days_to_reserve)
    elif args.release:
        filer_name = args.release[0]
        release_filer(filer_name)
    elif args.history:
        filer_name = args.history[0]
        history(filer_name)
    else:
        pass
    
