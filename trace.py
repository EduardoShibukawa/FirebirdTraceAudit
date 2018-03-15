import fdb
import os
import datetime
import argparse


def trace(database, user, password, svc_host='service_mgr', config=None, output_file=None, verbose=False):
    svc = fdb.services.connect(host=svc_host, user=user, password=password)
    trace_start = datetime.datetime.now()
    if config:
        config = open(config).read() 
    else:
        config = r'''
            <database %[\\/]{}>
                enabled true

                include_filter %(INSERT|UPDATE|DELETE)%    
                exclude_filter %%RDB$%%    
                log_statement_finish true
                print_plan true            		
                time_threshold 0        
            </database>        
        '''.format(database)

    trace_id = svc.trace_start(
        config=config,
        name='trace_{}'.format(trace_start.strftime('%c'))
    )

    print("{}: Trace session {} started.".format(
        trace_start.strftime('%c'), trace_id))
    
    if not output_file:
        output_file = open('{date}_Audit_{id}_{database}.log'.format(
            date=trace_start.strftime("%Y.%m.%d"),
            id=trace_id,
            database=database
        ), 'a+')

    for line in svc:
        try:
            output_file.write(line)
            output_file.write('\n')
            if verbose:
                print(line)
        except:
            break

    output_file.close()

    print("Finished Trace")


def main():
    parser = argparse.ArgumentParser(
        description="Trace firebird database tool.")

    parser.add_argument('database',
                        help="Full path to database.")
    parser.add_argument('config',
                        help="Path to trace config file.")
    parser.add_argument('output', type=argparse.FileType('w'),
                        metavar='FILENAME',
                        help="File to store trace report.")
    parser.add_argument('-o', '--host',
                        help="Server host.")
    parser.add_argument('-u', '--user',
                        default=os.environ.get('ISC_USER', 'sysdba'),
                        help="User name")
    parser.add_argument('-p', '--password',
                        default=os.environ.get('ISC_PASSWORD', None),
                        help="User password")

    args = parser.parse_args()

    if not args.password:
        print("A password is required to use the Services Manager.")
        parser.print_help()
        return

    if not args.database:
        print("A database is required to use the Services Manager.")
        parser.print_help()
        return
    try:
        if args.host:
            svc_host = args.host + ':service_mgr'
        else:
            svc_host = 'service_mgr'

        trace(
            svc_host= svc_host, 
            database=args.database,
            user=args.user,
            password=args.password, 
            config=args.config,
            output_file=args.output_file
        )
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
