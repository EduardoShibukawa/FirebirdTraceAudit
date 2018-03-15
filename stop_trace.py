import fdb
import os
import argparse

def stop_trace(user, password, id, svc_host='service_mgr'):    
    svc = fdb.services.connect(host=svc_host, user=user, password=password)
    svc.trace_stop(id)

def main():
    parser = argparse.ArgumentParser(description="Stop firebird trace tool.")

    parser.add_argument('database',
                        help="Full path to database.")    
    parser.add_argument('-o', '--host',
                        help="Server host.")
    parser.add_argument('-u', '--user',
                        default=os.environ.get('ISC_USER', 'sysdba'),
                        help="User name")
    parser.add_argument('-p', '--password',
                        default=os.environ.get('ISC_PASSWORD', None),
                        help="User password")
    parser.add_argument('-i', '--id',
                        help="Trace id")

    args = parser.parse_args()

    if not args.password:
        print("A password is required to use the Services Manager.")
        parser.print_help()
        return

    if not args.id:
        print("The trace id is required to use the Services Manager.")
        parser.print_help()
        return        
    try:
        if args.host:
            svc_host = args.host + ':service_mgr'
        else:
            svc_host = 'service_mgr'

        stop_trace(svc_host=svc_host, user=args.user, password=args.password, id=int(args.id))
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()