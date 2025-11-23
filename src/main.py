import argparse
from . import task_manager as tm
from rich.console import Console
from rich.table import Table
console = Console()

STATUS_ICONS = {
    'todo': '❌',      
    'in-progress': '⏳', 
    'done': '✅'    
}

def add_t(args):
    tm.add_task(args.title, args.due_to)

def list_t(args):
    tasks = tm.list_tasks(args.status_filter)  

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", width=6)
    table.add_column("Title", min_width=20)
    table.add_column("Due In")
    table.add_column("Status")
    table.add_column("Ramaining")   

    for task in tasks:
        obj = tm.Task(**task)
        remaining = obj.remaining_time
        
        # Determine remaining_time
        if not remaining: 
            display_time = ''
        elif remaining.total_seconds() < 0:
            display_time = '[red]Overdue[/red]'
        else:
            if obj.status == 'todo':
                display_time = f'[white]{remaining.days} days[/white]'
            else:
                display_time = f'[yellow]{remaining.days} days[/yellow]' if obj.status == 'in-progress' else f'[red]{abs(remaining.days)} days[/red]'

        # Add row to table    
        table.add_row (
            # id
            str(obj.id),
            # title
            obj.title,
            # due_to
            obj.due_to if obj.due_to else ' ',
            # status
            STATUS_ICONS.get(obj.status, obj.status),
            # remaining
            f'[green]Done[/green]' if obj.status == 'done' else display_time
        )
    console.print(table)

    total = len(tasks)
    if total > 0:
        done_count = sum(1 for t in tasks if t['status'] == 'done')
        percent = (done_count / total) * 100
        
        filled_length = int(10 * done_count // total)
        bar = "█" * filled_length + "░" * (10 - filled_length)
        
        color = "green" if percent >= 50 else "blue" if percent > 25 else "yellow"
        
        console.print(f"\n[bold]Progress:[/bold] [{color}]{bar}[/{color}] {percent:.1f}% ({done_count}/{total} done)")
    else:
        console.print("\n[italic]No tasks found.[/italic]")

def update_t(args):
    success_ids = []
    fail_ids = []

    for task_id in args.id:
        if tm.update_task(task_id, args.status, args.title):
            success_ids.append(str(task_id))
        else:
            fail_ids.append(str(task_id))

    if success_ids:
        ids_str = ", ".join(success_ids)
        console.print(f"[green]✅ Updated tasks: {ids_str}[/green]")
    
    if fail_ids:
        ids_str = ", ".join(fail_ids)
        console.print(f"[red]❌ Not found IDs: {ids_str}[/red]")

def delete_t(args):
    success_ids = []
    fail_ids = []

    for task_id in args.id:
        if tm.delete_task(task_id):
            success_ids.append(str(task_id))
        else:
            fail_ids.append(str(task_id))
    
    if success_ids:
        ids_str = ", ".join(success_ids)
        console.print(f"[green]✅ Deleted tasks: {ids_str}[/green]")
    if fail_ids:
        ids_str = ", ".join(fail_ids)
        console.print(f"[red]❌ Not found IDs: {ids_str}[/red]")

# Main Parser
parser = argparse.ArgumentParser (
    description = 'Todo CLI - Application',
)
# Sub-Parsers
subparsers = parser.add_subparsers(dest='command', help = 'List of commands')

add_parser = subparsers.add_parser('add', help='Add a new task')
add_parser.set_defaults(func=add_t)

list_parser = subparsers.add_parser('ls', help='List all tasks')
list_parser.set_defaults(func=list_t)

update_parser = subparsers.add_parser('upd', help='Update task status')
update_parser.set_defaults(func=update_t)

delete_parser = subparsers.add_parser('del', help='Delete a task')
delete_parser.set_defaults(func=delete_t)

# Add arguments
add_parser.add_argument('title', type=str, help = 'Title of the task')
add_parser.add_argument('--due', dest = 'due_to', type=str, help = 'YYYY-MM-DD', default=None)

# List arguments
list_parser.add_argument('--status', dest='status_filter', type=str, choices=['todo', 'in-progress', 'done'], help='Filter tasks by status', default=None)

# Update arguments
update_parser.add_argument('id', type=int, nargs='+', help='ID of the task to update')
update_parser.add_argument('--status', type=str, choices=['todo', 'in-progress', 'done'], help='New status of the task')
update_parser.add_argument('--title', type=str, help='New title of the task')

# Delete arguments
delete_parser.add_argument('id', type=int, nargs='+', help='ID of the task to delete')


#=============== ANALYZE ARGS ===============#
def main():
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help() 

#=============== RUN ===============#
if __name__ == '__main__':
    main()