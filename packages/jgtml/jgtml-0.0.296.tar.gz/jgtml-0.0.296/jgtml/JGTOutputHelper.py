import json
import os

def create_entry_signal_summary(data):
    out = f"""
# Entry Signal Details
## Trade Information
- **Entry Rate:** {data['entry']}
- **Stop Rate:** {data['stop']}
- **Buy/Sell:** {data['bs']}
- **Lots:** {data['lots']}
- **Tlid ID:** {data['tlid_id']}
- **Instrument:** {data['i']}
- **Timeframe:** {data['t']}
- **Risk(pips):** {data['pips_risk']}
"""

    return out

TEMPLATE_CHART_N_LINKS="""
![](charts/signal.png)
[M1](charts/M1.png)-[W1](charts/W1.png)-[D1](charts/D1.png)-[H4](charts/H4.png)-[H1](charts/H1.png)-[m15](charts/m15.png)-[m5](charts/m5.png)
"""
 


TEMPLATE_UTILITES = """
----
## Utilities


* [entry.sh](.jgt/entry.sh)
* [cancel.sh](.jgt/cancel.sh)
* [watch.sh](.jgt/watch.sh)
* [status.sh](.jgt/status.sh)
* [update.sh](.jgt/update.sh)
* [env.sh](.jgt/env.sh)
* Other scripts might include: .jgt/mv.sh, .jgt/rmtrade.sh, .jgt/xtrail.sh, .jgt/xfdb.sh

### CLI Commands

```sh
#.jgt/env.sh
#fxtr -id $OrderID $demo_arg
#fxrmorder -id $OrderID $demo_arg
#fxclosetrade -tid $trade_id $demo_arg
#fxtr -id $OrderID $demo_arg
#jgtapp fxwatchorder -id $OrderID  -d $bs \$demo_arg
#jgtapp fxmvstop -tid $trade_id -x $1 $demo_arg
#jgtapp fxrmtrade -tid $trade_id  $demo_arg
#jgtapp fxmvstopgator -tid $trade_id -i $instrument -t $timeframe --lips $demo_arg
#jgtapp fxmvstopfdb -tid $trade_id -i $instrument -t $timeframe  $demo_arg
#jgtapp fxstatusorder -id $OrderID  $demo_arg
```

#### More

* run 

```sh
#mkdir -p helps
#jgtapp --help > helps/jgtapp.txt
#fxtr --help > helps/fxtr.txt
```
### --@STCIssue Future Enhancements
* CLI Commands to run, not hard coded scripts
* Example : _fxtrupdate, _jgtsession_mksg, _jgtsession_vswsopen, _jgtsession_mkads_ctx_timeframe, _jgtsession_mkads_all_timeframes

"""

def create_bar_to_markdown(bar,title):
    mddata=f"""

## {title}
| Metric           | Value         |
|------------------|---------------|
"""
    for key, value in bar.items():
        mddata+=f"| {key} | {value} |\n"
    return mddata
        
def get_chart_n_links():
    if 'TEMPLATE_CHART_N_LINKS' in os.environ:
        return os.getenv('TEMPLATE_CHART_N_LINKS')
    return TEMPLATE_CHART_N_LINKS

def get_utilities():
    if 'TEMPLATE_UTILITES' in os.environ:
        return os.getenv('TEMPLATE_UTILITES')
    return TEMPLATE_UTILITES

def generate_markdown_from_json_file(json_filepath):
    with open(json_filepath, 'r') as file:
        data = json.load(file)
    
    signalbar = data['signalbar']
    currentbar = data['currentbar']
    
    markdown_output = create_entry_signal_summary(data)

    markdown_output += get_chart_n_links()


    markdown_output += TEMPLATE_UTILITES

    markdown_output += create_bar_to_markdown(signalbar,"Signal Bar Data")
    
    markdown_output += create_bar_to_markdown(currentbar,"Current Bar Data")


    return markdown_output

def serialize_signal_to_markdown_file_from_json_file(json_filepath,quiet=True):
    markdown_output = generate_markdown_from_json_file(json_filepath)
    markdown_filepath = json_filepath.replace('.json', '.md')
    try:  
      with open(markdown_filepath, 'w') as file:
          file.write(markdown_output)
          if not quiet:print(f">Markdown file saved to: {markdown_filepath}")
      return markdown_filepath
    except Exception as e:
      print(f"Error saving markdown file to {markdown_filepath} {e}")
      return None
  
FDBSCAN_DIR_DEFAULT="data/signals"

def get_fdbscan_dir():
    if 'FDBSCAN_DIR' in os.environ:
        return os.getenv('FDBSCAN_DIR')
    return FDBSCAN_DIR_DEFAULT
    
def serialize_signal_to_json_file(i,t,o,signal_bar,current_bar,quiet=True,signal_dir=None,ext="json",indent=2):
      if signal_dir is None:
          signal_dir=get_fdbscan_dir()
      tlid_id=o["tlid_id"]
      o["i"]=i
      o["t"]=t
      o["signalbar"]=signal_bar
      o["currentbar"]=current_bar
      
      signal_fn = create_signal_filename(i,t, tlid_id, ext)
      signal_savepath =os.path.join(signal_dir,signal_fn)
      try:      
        os.makedirs(signal_dir,exist_ok=True)
        json.dump(o,open(signal_savepath,"w"),indent=indent)
        if not quiet:print(f">Signal saved to :{signal_savepath}")
        return signal_savepath
      except Exception as e:
        print(f"Error saving signal to {signal_savepath} {e}")
        return None

def create_signal_savepath(i,t, tlid_id, ext, signal_dir=None):
    if signal_dir is None:
        signal_dir=get_fdbscan_dir()
    signal_fn = create_signal_filename(i,t, tlid_id, ext)
    signal_savepath =os.path.join(signal_dir,signal_fn)
    return signal_savepath

def create_signal_filename(i,t, tlid_id, ext):
    ifn=i.replace("/","-")
    filename = f"{ifn}_{t}_{tlid_id}.{ext}"
    return filename
