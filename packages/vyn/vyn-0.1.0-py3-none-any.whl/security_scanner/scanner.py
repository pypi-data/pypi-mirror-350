import click
from .bandit_test import run_bandit_on_path
from .analyzer import get_ai_suggestion, save_scan_report
from prettytable import PrettyTable



# def save_scan_report(report_text, filename="scan_report.txt"):
#     try:
#         with open(filename, "w", encoding="utf-8") as f:
#             f.write(report_text)
#         print(f"\n✅ Scan report saved to {filename}")
#     except Exception as e:
#         print(f"\n❌ Error saving scan report: {e}")

@click.command()
@click.argument('target')
@click.option('--format', default='json')
def scan(target, format):
    click.echo(f"🔍 Scanning {target}...\n")
    issue_list = run_bandit_on_path(target)
    
    report_text = ""

    if format == 'table':
        table = PrettyTable()
        table.field_names = ["Name", "Issues Found"]

    for result in issue_list:
        issue = result.as_dict()
        issue_details = (
            "=" * 50 + "\n" +
            f"→ Issue      : {issue['issue_text']}\n" +
            f"→ File       : {issue['filename']}\n" +
            f"→ Line       : {issue['line_number']}\n" +
            f"→ Severity   : {issue['issue_severity']}\n" +
            f"→ Confidence : {issue['issue_confidence']}\n"
        )

        try:
            code_context = issue['code']
        except:
            code_context = "Code not available"

        ai_suggestion = get_ai_suggestion(issue['issue_text'], code_context)
        issue_details += f" AI Suggestion: {ai_suggestion}\n"

        print(issue_details)
        report_text += issue_details + "\n"

    # if format == 'table':
    #     print(table)

    # Ask once at the end
    save = input("\n💾 Would you like to save the scan report to a file? (y/n): ").strip().lower()
    if save == 'y':
        save_scan_report(results=report_text)

def main():
    scan()

if __name__ == '__main__':
    main()
