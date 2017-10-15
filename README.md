# Gluster Log Tools

## Colorize the log files
Colored output for Gluster logs.

    cat /var/log/glusterfs/glusterd.log | gluster-log colorize

## JSON output
Log messages can be converted to `json` for better integration with external
tools/applications.
    
    cat /var/log/glusterfs/glusterd.log | gluster-log json

Output can be redirected to file for post processing

    cat /var/log/glusterfs/glusterd.log | gluster-log json > ~/glusterd_log.json

## Future plans
- Support for filters for each field(Example, filter based on given time range,
  filter based on an event etc..)
- Support for multiple log files processing
- Support for file input(`gluster-log colorize <LOGFILE>`)
