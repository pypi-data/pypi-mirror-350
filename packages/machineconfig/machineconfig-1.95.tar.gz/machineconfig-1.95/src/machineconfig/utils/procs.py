"""Procs
"""
import psutil
import pandas as pd
from tqdm import tqdm
from pytz import timezone
from machineconfig.utils.utils import display_options
from typing import Optional
from rich.console import Console
from rich.panel import Panel

console = Console()

BOX_WIDTH = 78  # width for box drawing

pd.options.display.max_rows = 10000


def get_processes_accessing_file(path: str):
    # header for searching processes
    title = "🔍  SEARCHING FOR PROCESSES ACCESSING FILE"
    console.print(Panel(title, title="[bold blue]Process Info[/bold blue]", border_style="blue"))
    res: dict[int, list[str]] = {}
    for proc in tqdm(psutil.process_iter(), desc="🔎 Scanning processes"):
        try:
            files = proc.open_files()
        except psutil.AccessDenied:
            continue
        tmp = [file.path for file in files if path in file.path]
        if len(tmp) > 0:
            res[proc.pid] = tmp
    df = pd.DataFrame(res.items(), columns=['pid', 'files'])
    console.print(Panel(f"✅ Found {len(res)} processes accessing the specified file", title="[bold blue]Process Info[/bold blue]", border_style="blue"))
    return df


def kill_process(name: str):
    print(f"⚠️  Attempting to kill process: {name}...")
    killed = False
    for proc in psutil.process_iter():
        if proc.name() == name:
            proc.kill()
            print(f"💀 Process {name} (PID: {proc.pid}) terminated successfully")
            killed = True
    if not killed:
        print(f"❓ No process with name '{name}' was found")
    print(f"{'─'*80}\n")


class ProcessManager:
    def __init__(self):
        # header for initializing process manager
        title = "📊  INITIALIZING PROCESS MANAGER"
        console.print(Panel(title, title="[bold blue]Process Info[/bold blue]", border_style="blue"))
        process_info = []
        for proc in tqdm(psutil.process_iter(), desc="🔍 Reading system processes"):
            try:
                mem_usage_mb = proc.memory_info().rss / (1024 * 1024)
                process_info.append([proc.pid, proc.name(), proc.username(), proc.cpu_percent(), mem_usage_mb, proc.status(), proc.create_time(), " ".join(proc.cmdline())])
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): pass
        df = pd.DataFrame(process_info)
        df.columns = pd.Index(['pid', 'name', 'username', 'cpu_percent', 'memory_usage_mb', 'status', 'create_time', 'command'])
        df['create_time'] = pd.to_datetime(df['create_time'], unit='s', utc=True).apply(lambda x: x.tz_convert(timezone('Australia/Adelaide')))
        df = df.sort_values(by='memory_usage_mb', ascending=False).reset_index(drop=True)
        self.df = df
        console.print(Panel(f"✅ Process Manager initialized with {len(df)} processes", title="[bold blue]Process Info[/bold blue]", border_style="blue"))

    def choose_and_kill(self):
        # header for interactive process selection
        title = "🎯  INTERACTIVE PROCESS SELECTION AND TERMINATION"
        console.print(Panel(title, title="[bold blue]Process Info[/bold blue]", border_style="blue"))
        options = str(self.df).split("\n")[1:]
        res = display_options(options=str(self.df).split("\n"), msg="📋 Select processes to manage:", fzf=True, multi=True)
        indices = [options.index(val) for val in res]
        sub_df = self.df.iloc[indices]
        print("\n📊 All Processes:")
        print(self.df)
        print("\n🎯 Selected Processes:")
        print(sub_df)
        from crocodile.core import Struct
        for idx, (_, row) in enumerate(sub_df.iterrows()):
            Struct(row.to_dict()).print(as_config=True, title=f"📌 Process {idx}")
        kill_all = input("\n⚠️  Confirm killing ALL selected processes? y/[n] ").lower() == "y"
        if kill_all:
            self.kill(pids=sub_df.pid.to_list())
            return
        kill_by_index = input("\n🔫 Kill by index? (enter numbers separated by spaces, e.g. '1 4') or [n] to cancel: ")
        if kill_by_index != "" and kill_by_index != "n":
            indices = [int(val) for val in kill_by_index.split(" ")]
            sub_sub_df = sub_df.iloc[indices]
            for idx2, row in sub_sub_df.iterrows():
                Struct(row.to_dict()).print(as_config=True, title=f"🎯 Target Process {idx2}")
            _ = self.kill(pids=sub_sub_df.pid.to_list()) if input("\n⚠️  Confirm termination? y/[n] ").lower() == "y" else None
        console.print(Panel("🔔 No processes were terminated.", title="[bold blue]Process Info[/bold blue]", border_style="blue"))

    def filter_and_kill(self, name: Optional[str] = None):
        # header for filtering processes by name
        title = "🔍  FILTERING AND TERMINATING PROCESSES BY NAME"
        console.print(Panel(title, title="[bold blue]Process Info[/bold blue]", border_style="blue"))
        _ = 20
        df_sub = self.df.query(f"name == '{name}' ").sort_values(by='create_time', ascending=True)
        print(f"🎯 Found {len(df_sub)} processes matching name: '{name}'")
        self.kill(pids=df_sub.pid.to_list())
        console.print(Panel("", title="[bold blue]Process Info[/bold blue]", border_style="blue"))

    def kill(self, names: Optional[list[str]] = None, pids: Optional[list[int]] = None, commands: Optional[list[str]] = None):
        # header for process termination
        title = "💀  PROCESS TERMINATION"
        console.print(Panel(title, title="[bold blue]Process Info[/bold blue]", border_style="blue"))
        if names is None and pids is None and commands is None:
            print("❌ Error: No termination targets specified (names, pids, or commands)")
            raise ValueError('names, pids and commands cannot all be None')
        if names is None: names = []
        if pids is None: pids = []
        if commands is None: commands = []
        
        killed_count = 0
        
        for name in names:
            rows = self.df[self.df['name'] == name]
            if len(rows) > 0:
                for _idx, a_row in rows.iterrows():
                    psutil.Process(a_row.pid).kill()
                    print(f'💀 Killed process {name} with PID {a_row.pid}. It lived {get_age(a_row.create_time)}. RIP 🪦💐')
                    killed_count += 1
            else: 
                print(f'❓ No process named "{name}" found')
        
        for pid in pids:
            try:
                proc = psutil.Process(pid)
                proc_name = proc.name()
                proc_lifetime = get_age(proc.create_time())
                proc.kill()
                print(f'💀 Killed process with PID {pid} and name "{proc_name}". It lived {proc_lifetime}. RIP 🪦💐')
                killed_count += 1
            except psutil.NoSuchProcess: 
                print(f'❓ No process with PID {pid} found')
        
        for command in commands:
            rows = self.df[self.df['command'].to_str().contains(command)]
            if len(rows) > 0:
                for _idx, a_row in rows.iterrows():
                    psutil.Process(a_row.pid).kill()
                    print(f'💀 Killed process with "{command}" in its command & PID {a_row.pid}. It lived {get_age(a_row.create_time)}. RIP 🪦💐')
                    killed_count += 1
            else: 
                print(f'❓ No process has "{command}" in its command.')
        
        console.print(Panel(f"✅ Termination complete: {killed_count} processes terminated", title="[bold blue]Process Info[/bold blue]", border_style="blue"))


def get_age(create_time: float):
    try: age = pd.Timestamp.now(tz="Australia/Adelaide") - pd.to_datetime(create_time, unit="s", utc=True).tz_convert(timezone("Australia/Adelaide"))
    except Exception as e:
        try: age = pd.Timestamp.now() - pd.to_datetime(create_time, unit="s", utc=True).tz_localize(tz=None)
        except Exception as ee:  # type: ignore
            return f"unknown due to {ee} and {e}"
    return age


if __name__ == '__main__':
    pass
