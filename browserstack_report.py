"""
BrowserStack Test Management Reporting Script

This script fetches test run data from BrowserStack Test Management API
and generates a CSV report with test statistics.

Configuration:
- Update TEST_RUN_NAME_FILTER to change which test runs to include in the report
- The filter is case-insensitive and matches test runs containing the specified text
"""

import requests
import pandas as pd

# 🔐 Credentials
USERNAME = "abhyudayapathak_WTr9zi"
ACCESS_KEY = "ALysQQQwMwyiyJkKwouR"

BASE_URL = "https://test-management.browserstack.com/api/v2"
auth = (USERNAME, ACCESS_KEY)

# 🔧 Configuration - Update this value to change the test run filter
TEST_RUN_NAME_FILTER = "regression cycle 1"  # Filter test runs by this name (case-insensitive)

# � Get all projects
def get_projects():
    all_projects = []
    page = 1
    
    while True:
        url = f"{BASE_URL}/projects?p={page}"
        response = requests.get(url, auth=auth)
        response.raise_for_status()
        data = response.json()
        
        projects = data.get("projects", [])
        all_projects.extend(projects)
        
        info = data.get("info", {})
        next_page = info.get("next")
        
        if not next_page:
            break
        
        page += 1
    
    return {"projects": all_projects}

# 📌 Get test runs for a project
def get_test_runs(project_id):
    url = f"{BASE_URL}/projects/{project_id}/test-runs"
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return response.json()

def get_test_run_details(project_id, test_run_id):
    url = f"{BASE_URL}/projects/{project_id}/test-runs/{test_run_id}"
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return response.json()

# 📊 Build report (with filtering + aggregation)
def build_report():
    projects_response = get_projects()
    projects = projects_response.get("projects", [])
    report_data = []

    print(f"\n📋 Total projects found: {len(projects)}\n")
    
    for project in projects:
        project_id = project.get("identifier")
        project_name = project.get("name")

        print(f"Fetching runs for project: {project_name} ({project_id})")

        try:
            test_runs_response = get_test_runs(project_id)
            test_runs = test_runs_response.get("test_runs", [])

            for run in test_runs:
                run_id = run.get("identifier")
                run_name = run.get("name", "")
                run_state = run.get("run_state")
                active_state = run.get("active_state")
                
                if TEST_RUN_NAME_FILTER.lower() not in run_name.lower():
                    continue
                
                print(f"  ✓ Found: {run_name} ({run_id}) - {active_state}/{run_state}")

                try:
                    run_details_response = get_test_run_details(project_id, run_id)
                    run_details = run_details_response.get("test_run", {})
                    overall_progress = run_details.get("overall_progress", {})
                    
                    total_tests = run_details.get("test_cases_count", 0)
                    passed = overall_progress.get("Passed", overall_progress.get("passed", 0))
                    failed = overall_progress.get("Failed", overall_progress.get("failed", 0))
                    blocked = overall_progress.get("Blocked", overall_progress.get("blocked", 0))
                    untested = overall_progress.get("Untested", overall_progress.get("untested", 0))
                    skipped = overall_progress.get("Skipped", overall_progress.get("skipped", 0))
                    
                    if total_tests == 0:
                        total_tests = passed + failed + blocked + untested + skipped
                    
                    report_data.append({
                        "Project": project_name,
                        "Test Run": run_details.get("name", run_id),
                        "Active State": active_state,
                        "Run State": run_state,
                        "Total Tests": total_tests,
                        "Passed": passed,
                        "Failed": failed,
                        "Blocked": blocked,
                        "Untested": untested,
                        "Skipped": skipped
                    })
                except Exception as e:
                    print(f"Error fetching details for run {run_id}: {e}")

        except Exception as e:
            print(f"Error fetching project {project_name}: {e}")

    df = pd.DataFrame(report_data)

    if df.empty:
        print(f"\n⚠️  No '{TEST_RUN_NAME_FILTER}' test runs found.")
        return df
    
    print(f"\n✅ Found {len(df)} '{TEST_RUN_NAME_FILTER}' test runs")

    df["Pass %"] = df.apply(lambda row: round((row["Passed"] / row["Total Tests"] * 100), 2) if row["Total Tests"] > 0 else 0, axis=1)
    df["Fail %"] = df.apply(lambda row: round((row["Failed"] / row["Total Tests"] * 100), 2) if row["Total Tests"] > 0 else 0, axis=1)

    return df

# 📤 Save report
def save_report(df):
    if df.empty:
        print("\n⚠️  No data to save.")
        return
    
    file_name = "browserstack_regression_cycle1_report.csv"
    df.to_csv(file_name, index=False)
    print(f"✅ Report saved as {file_name}")

# 🚀 Execute
if __name__ == "__main__":
    df = build_report()
    print(df)
    save_report(df)