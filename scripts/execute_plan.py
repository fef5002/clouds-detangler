"""Execute an actions plan using rclone (scaffold).

Planned behaviour:

- Read actions_plan.csv
- For each row:
    - Build an rclone command (e.g. moveto/copyto/delete)
    - If --dry-run: print the command
    - If --apply: run the command

For now, this is a placeholder that simply explains its intended role.
"""

def main():
    print("execute_plan.py is a placeholder for now.")
    print("In the future, this script will read actions_plan.csv and")
    print("translate each row into a safe rclone command (dry-run first).")

if __name__ == "__main__":
    main()
