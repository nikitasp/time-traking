from hubstaff.models import DailyActivity, User, Project

def seconds_to_hms(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def agregate_activities(activities: list[DailyActivity]) -> dict:
    agregated_data = {}

    for activity in activities:
        user_id = activity.user_id
        project_id = activity.project_id

        if project_id not in agregated_data:
            agregated_data[project_id] = {}

        if user_id not in agregated_data[project_id]:
            agregated_data[project_id][user_id] = activity.billable
        else:
            agregated_data[project_id][user_id] += activity.billable        
    
    return agregated_data

def generate_html_table(agregated_data: dict, users: list[User], projects: list[Project], date: str) -> str:
    # I've been thinking to use some template engine but littery for one template is a bit to much and it will do exactly what you do in this function
    users = {u.id:u.name for u in users}
    projects = {p.id:p.name for p in projects}

    active_projects = {pid: name for pid, name in projects.items() if pid in agregated_data}
    active_employe_ids = set()
    for pid in agregated_data:
        for uid in agregated_data[pid]:
            active_employe_ids.add(uid)
    active_employees = {uid: name for uid, name in users.items() if uid in active_employe_ids}
    
    if not active_projects or not active_employees:
        return f"<p>No activity recorded for {date}.</p>"
    
    html = f"""
    <html>
    <head>
        <title>Hubstaff Time Report for {date}</title>
        <style>
            table {{ border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
            th {{ background-color: #f2f2f2; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            tr:hover {{ background-color: #f5f5f5; }}
        </style>
    </head>
    <body>
        <h2>Hubstaff Time Report for {date}</h2>
        <table>
            <tr>
                <th>Project</th>
                {''.join(f'<th>{name}</th>' for name in active_employees.values())}
                <th>Total Hours</th>
            </tr>
    """
    
    for pid, pname in sorted(active_projects.items(), key=lambda x: x[1]):
        html += f"            <tr>\n                <td>{pname}</td>\n"
        for uid in active_employees:
            if uid in agregated_data[pid]:
                time_spent = agregated_data[pid][uid]
                html += f"                <td>{seconds_to_hms(time_spent)}</td>\n"
            else:
                html += f"                <td>00:00:00</td>\n"    
        html += f"                <td>{seconds_to_hms(sum(agregated_data[pid].values()))}</td>\n" 
        html += "            </tr>\n"
    
    html += """
        </table>
    </body>
    </html>
    """
    return html