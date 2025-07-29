#!/usr/bin/env python3

import sys,time,traceback
import fandango as fn
from fandango import raw_input

__doc__ = """
tango_servers
-------------

This script uses fn.servers.ServersDict class to start/stop devices on any point of the control system using Tango Starters.

  tango_servers [host] start|stop|kill|restart|status|level [level] [server_name_expression_list] [-f/--force]
  
Examples:

  tango_servers status              # Will display status of devices in localhost
  tango_servers hostname.you.org stop "*hdb*"    # Will stop all *hdb* devices in hostname.you.org
  tango_servers restart "pyalarm/*"     # Will restart PyAlarm devices in ALL hosts
  tango_servers move new_host "pyalarm/*" "albaplc/*" # will restart servers on new_host
  
NOTE: ctds and tango_admin scripts provide similar functionality

"""

def main(args = []):
  actions = 'start stop kill restart status states level move'.split()
  args = [] or sys.argv[1:]
  opts = [a for a in args if a.startswith('-')]
  args = [a for a in args if a not in opts]
  
  try:
      assert 'help' not in str(opts+args)
      host = args[0] if args[0] not in actions else ''
      forced = '-f' in opts or '--force' in opts
      action = fn.first([a for a in args if a in actions] or [''])
      targets = args[bool(host)+bool(action):]
      level = [t for t in targets if fn.clmatch('[0-9]$',t)]
      if level: targets.remove(level[0])
      action = action or 'status' #order matters
  except:
      traceback.print_exc()
      print(__doc__)
      sys.exit(1)
      
  print('%s of %s at %s'%(action,targets,host or '*'))
  
  try:
      astor = fn.Astor()
      if targets:
          for exp in targets:
              print('Loading %s devices\n'%exp)
              astor.load_by_name(exp)
      else:
          h = host or fn.MyMachine().host
          print('Loading %s devices\n'%h)
          astor.load_by_host(h)
          
      sts = astor.states()
      if action in ('status','states','info','list'):
          if targets:
              for k,v in sorted(astor.items()):
                if host and v.host!=host:
                    continue
                print('%s (%s):\t%s'%(k,v.host,str(sts[k])))
                try:
                  for d,s in sorted(v.get_all_states().items()):
                    print('\t%s:\t%s'%(d,str(s)))
                except: pass
                print('')

          else:
            print('Note: Devices not controlled by Astor will not appear in this report\n\n')
            hosts = set(s.host for s in astor.values() if s.host)

            for h in hosts:
                ls = astor.get_host_overview(host)
                for l,ds in sorted(ls.items()):
                    print('%s:%s'%(h,l))
                    for s,devs in sorted(ds.items()):
                        print('\t'+s)
                        if not devs:
                            print('\t\tNo devices found')
                        else:
                            for d,st in sorted(devs.items()):
                                if d.split('/')[-3] == 'dserver':
                                    continue                                
                                print('\t\t%s:\t%s'%(d,st))
                print('')

      matched = [s for s in astor if not s.lower().startswith('starter/')] # if not targets or fn.clmatch(targets[0],s)]
      running = [s for s in matched if sts[s] is not None]
      
      if action in ('kill',):
          print('Killing : %s'%matched)
          if forced:
              conf = 'y'
          else:
              conf = raw_input(('%d servers will be killed:\n\t%s' % (
                len(matched),'\n\t'.join(matched)))
                + '\nIs it ok? (y/n)')

          if conf.lower().strip() in ('y','yes'):          
              astor.kill_servers(matched)
          else:
              sys.exit(1)              
          
      if action in ('restart',):
          nr = [_ for _ in matched if _ not in running]
          if nr:
              print('Some devices are not running and will NOT be restarted: ' + str(nr))
          matched = running          
          
      if action in ('stop','restart','move'):
          print('Stopping : %s'%running)
          if forced:
              conf = 'y'
          else:
              conf = raw_input(('%d servers will be stop:\n\t%s' % (
                len(running),'\n\t'.join(running)))
                + '\nIs it ok? (y/n)')

          if conf.lower().strip() in ('y','yes'):
              astor.stop_servers(running)
          else:
              sys.exit(1)

      if action in ('restart','move'):
          time.sleep(15.)
          
      if action in ('start','restart','move'):
          print('Starting : %s'%matched)
          not_match = [a for a in matched if not host and not astor[a].host]
          if not_match:
              conf = raw_input('Some servers (%s) will be started locally,'
                               ' is it ok? (y/n)' % not_match)
              if conf.lower().strip() not in ('y','yes'):
                  matched = [m for m in matched if m not in not_match]
              
          not_match = [s for s in matched if not astor[s].level]
          if not_match:
              if forced:
                  conf = 'y'
              else:
                  conf = raw_input('Some servers (%s) are not controlled,'
                               ' should start them? (y/n)' % not_match)
              if conf.lower().strip() not in ('y','yes'):
                  matched = [m for m in matched if m not in not_match]              

          astor.start_servers(matched,**(host and {'host':host} or {}))
              
      if action in ('start','restart','move','level') and level:
            for s in astor.keys():
                h = host or astor[s].host
                h and astor.set_server_level(s,h,int(level[0]))
      
      print('-'*80)
      print(' '.join(sys.argv)+': Done')  
  except:
      print(traceback.format_exc())
      print('-'*80)
      print(' '.join(sys.argv)+': Failed!')   
      
if __name__ == '__main__':
  main()
