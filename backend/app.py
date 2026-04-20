from flask import Flask, request, jsonify, send_file, Response, stream_with_context
from flask_cors import CORS
import requests
import csv
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure CORS for production
frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
CORS(app, resources={
    r"/api/*": {
        "origins": [frontend_url, "http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

BASE_URL = "https://test-management.browserstack.com/api/v2"

def get_projects(username, access_key):
    auth = (username, access_key)
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

def get_test_runs(project_id, username, access_key, include_closed='active', created_after='', created_before=''):
    auth = (username, access_key)
    all_test_runs = []
    page = 1
    
    while True:
        # Map frontend values to BrowserStack API parameters
        if include_closed == 'active':
            url = f"{BASE_URL}/projects/{project_id}/test-runs?include_closed=false&page={page}&page_size=300"
        elif include_closed == 'closed':
            url = f"{BASE_URL}/projects/{project_id}/test-runs?include_closed=true&run_state=closed&page={page}&page_size=300"
        else:  # 'all'
            url = f"{BASE_URL}/projects/{project_id}/test-runs?include_closed=true&page={page}&page_size=300"
        
        # Add date range filters if provided (format: YYYY-MM-DD)
        if created_after:
            url += f"&created_after={created_after}"
        if created_before:
            url += f"&created_before={created_before}"
        
        if page == 1:
            print(f"DEBUG: Fetching test runs - URL: {url}")
        
        response = requests.get(url, auth=auth)
        response.raise_for_status()
        data = response.json()
        
        test_runs = data.get("test_runs", [])
        print(f"DEBUG: Project {project_id}, Page {page}: Got {len(test_runs)} test runs")
        
        if not test_runs:
            break
        
        all_test_runs.extend(test_runs)
        
        # Check if there are more pages (BrowserStack API returns max 30 per page)
        if len(test_runs) < 30:
            print(f"DEBUG: Last page for project {project_id} (got {len(test_runs)} < 30)")
            break
        
        page += 1
        
        # Safety limit to prevent infinite loops
        if page > 100:
            print(f"WARNING: Reached page limit for project {project_id}")
            break
    
    print(f"DEBUG: Total test runs fetched for project {project_id}: {len(all_test_runs)}")
    
    return {"test_runs": all_test_runs}

def get_test_run_details(project_id, test_run_id, username, access_key):
    auth = (username, access_key)
    url = f"{BASE_URL}/projects/{project_id}/test-runs/{test_run_id}"
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return response.json()

@app.route('/api/generate-report-stream', methods=['POST'])
def generate_report_stream():
    """Generate report with real-time progress updates via Server-Sent Events"""
    def generate():
        try:
            data = request.json
            username = data.get('username')
            access_key = data.get('accessKey')
            test_run_filter = data.get('testRunFilter', '')
            include_closed = data.get('includeClosed', 'active')
            created_after = data.get('createdAfter', '')
            created_before = data.get('createdBefore', '')
            
            if not username or not access_key:
                yield f"data: {json.dumps({'error': 'Username and access key are required'})}\n\n"
                return
            
            # Send initial progress
            initial_data = {'progress': 0, 'message': 'Connecting to BrowserStack...'}
            yield f"data: {json.dumps(initial_data)}\n\n"
            
            try:
                projects_response = get_projects(username, access_key)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 401:
                    error_data = {'error': 'Invalid BrowserStack credentials. Please check your username and access key.'}
                    yield f"data: {json.dumps(error_data)}\n\n"
                elif e.response.status_code == 403:
                    error_data = {'error': 'Access forbidden. Please verify your BrowserStack account permissions.'}
                    yield f"data: {json.dumps(error_data)}\n\n"
                else:
                    error_data = {'error': f'BrowserStack API error: {str(e)}'}
                    yield f"data: {json.dumps(error_data)}\n\n"
                return
            
            projects = projects_response.get("projects", [])
            total_projects = len(projects)
            
            projects_data = {'progress': 10, 'message': f'Found {total_projects} projects. Fetching test runs...'}
            yield f"data: {json.dumps(projects_data)}\n\n"
            
            report_data = []
            processed_projects = 0
            
            for project in projects:
                project_id = project.get("identifier")
                project_name = project.get("name")
                
                try:
                    test_runs_response = get_test_runs(project_id, username, access_key, include_closed, created_after, created_before)
                    test_runs = test_runs_response.get("test_runs", [])
                    
                    matching_runs = [run for run in test_runs if not test_run_filter or test_run_filter.lower() in run.get("name", "").lower()]
                    
                    for idx, run in enumerate(matching_runs):
                        run_id = run.get("identifier")
                        run_name = run.get("name", "")
                        run_state = run.get("run_state")
                        active_state = run.get("active_state")
                        
                        # Calculate progress
                        processed_projects += 1
                        progress = 10 + int((processed_projects / max(total_projects, 1)) * 80)
                        message = f'Processing {project_name}: {run_name[:50]}...'
                        progress_data = {
                            'progress': min(progress, 90),
                            'message': message
                        }
                        yield f"data: {json.dumps(progress_data)}\n\n"
                        
                        try:
                            run_details_response = get_test_run_details(project_id, run_id, username, access_key)
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
                            
                            pass_percentage = round((passed / total_tests * 100), 2) if total_tests > 0 else 0
                            fail_percentage = round((failed / total_tests * 100), 2) if total_tests > 0 else 0
                            
                            report_data.append({
                                "project": project_name,
                                "testRun": run_details.get("name", run_id),
                                "activeState": active_state,
                                "runState": run_state,
                                "totalTests": total_tests,
                                "passed": passed,
                                "failed": failed,
                                "blocked": blocked,
                                "untested": untested,
                                "skipped": skipped,
                                "passPercentage": pass_percentage,
                                "failPercentage": fail_percentage
                            })
                        except Exception as e:
                            print(f"Error fetching details for run {run_id}: {e}")
                            
                except Exception as e:
                    print(f"Error fetching project {project_name}: {e}")
            
            # Send completion
            completion_data = {
                'progress': 100,
                'message': 'Report generated successfully!',
                'data': report_data,
                'totalRuns': len(report_data),
                'complete': True
            }
            yield f"data: {json.dumps(completion_data)}\n\n"
            
        except Exception as e:
            error_data = {'error': str(e)}
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    try:
        data = request.json
        username = data.get('username')
        access_key = data.get('accessKey')
        test_run_filter = data.get('testRunFilter', '')
        
        if not username or not access_key:
            return jsonify({'error': 'Username and access key are required'}), 400
        
        try:
            projects_response = get_projects(username, access_key)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                return jsonify({'error': 'Invalid BrowserStack credentials. Please check your username and access key.'}), 401
            elif e.response.status_code == 403:
                return jsonify({'error': 'Access forbidden. Please verify your BrowserStack account permissions.'}), 403
            else:
                return jsonify({'error': f'BrowserStack API error: {str(e)}'}), e.response.status_code
        projects = projects_response.get("projects", [])
        report_data = []
        
        for project in projects:
            project_id = project.get("identifier")
            project_name = project.get("name")
            
            try:
                test_runs_response = get_test_runs(project_id, username, access_key)
                test_runs = test_runs_response.get("test_runs", [])
                
                for run in test_runs:
                    run_id = run.get("identifier")
                    run_name = run.get("name", "")
                    run_state = run.get("run_state")
                    active_state = run.get("active_state")
                    
                    if test_run_filter and test_run_filter.lower() not in run_name.lower():
                        continue
                    
                    try:
                        run_details_response = get_test_run_details(project_id, run_id, username, access_key)
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
                        
                        pass_percentage = round((passed / total_tests * 100), 2) if total_tests > 0 else 0
                        fail_percentage = round((failed / total_tests * 100), 2) if total_tests > 0 else 0
                        
                        report_data.append({
                            "project": project_name,
                            "testRun": run_details.get("name", run_id),
                            "activeState": active_state,
                            "runState": run_state,
                            "totalTests": total_tests,
                            "passed": passed,
                            "failed": failed,
                            "blocked": blocked,
                            "untested": untested,
                            "skipped": skipped,
                            "passPercentage": pass_percentage,
                            "failPercentage": fail_percentage
                        })
                    except Exception as e:
                        print(f"Error fetching details for run {run_id}: {e}")
                        
            except Exception as e:
                print(f"Error fetching project {project_name}: {e}")
        
        return jsonify({
            'success': True,
            'data': report_data,
            'totalRuns': len(report_data)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-report', methods=['POST'])
def download_report():
    try:
        data = request.json
        report_data = data.get('reportData', [])
        
        if not report_data:
            return jsonify({'error': 'No data to download'}), 400
        
        # Create CSV using Python's built-in csv module
        output = io.StringIO()
        
        # Define CSV headers
        headers = ['Project', 'Test Run', 'Total Tests', 'Passed', 'Failed', 
                   'Blocked', 'Untested', 'Skipped', 'Execution %', 'Pass %', 'Fail %']
        
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        
        # Write data rows
        for item in report_data:
            execution_percentage = 0
            if item.get('totalTests', 0) > 0:
                executed = item.get('passed', 0) + item.get('failed', 0) + item.get('blocked', 0)
                execution_percentage = round((executed / item['totalTests']) * 100, 2)
            
            writer.writerow({
                'Project': item.get('project', ''),
                'Test Run': item.get('testRun', ''),
                'Total Tests': item.get('totalTests', 0),
                'Passed': item.get('passed', 0),
                'Failed': item.get('failed', 0),
                'Blocked': item.get('blocked', 0),
                'Untested': item.get('untested', 0),
                'Skipped': item.get('skipped', 0),
                'Execution %': execution_percentage,
                'Pass %': item.get('passPercentage', 0),
                'Fail %': item.get('failPercentage', 0)
            })
        
        # Convert StringIO to BytesIO for send_file
        output.seek(0)
        byte_output = io.BytesIO(output.getvalue().encode('utf-8'))
        byte_output.seek(0)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'browserstack_report_{timestamp}.csv'
        
        return send_file(
            byte_output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/send-email', methods=['POST'])
def send_email():
    try:
        data = request.json
        recipient_email = data.get('email')
        report_data = data.get('reportData', [])
        smtp_config = data.get('smtpConfig', {})
        
        if not recipient_email or not report_data:
            return jsonify({'error': 'Email and report data are required'}), 400
        
        df = pd.DataFrame(report_data)
        df.columns = ['Project', 'Test Run', 'Active State', 'Run State', 'Total Tests', 
                      'Passed', 'Failed', 'Blocked', 'Untested', 'Skipped', 'Pass %', 'Fail %']
        
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_content = csv_buffer.getvalue()
        
        msg = MIMEMultipart()
        msg['From'] = smtp_config.get('from_email', 'noreply@browserstack.com')
        msg['To'] = recipient_email
        msg['Subject'] = f'BrowserStack Test Report - {datetime.now().strftime("%Y-%m-%d %H:%M")}'
        
        total_tests = df['Total Tests'].sum()
        total_passed = df['Passed'].sum()
        total_failed = df['Failed'].sum()
        overall_pass_rate = round((total_passed / total_tests * 100), 2) if total_tests > 0 else 0
        
        body = f"""
        <html>
        <body>
            <h2>BrowserStack Test Execution Report</h2>
            <p>Please find the attached test execution report.</p>
            
            <h3>Summary:</h3>
            <ul>
                <li><strong>Total Test Runs:</strong> {len(df)}</li>
                <li><strong>Total Tests:</strong> {total_tests}</li>
                <li><strong>Passed:</strong> {total_passed}</li>
                <li><strong>Failed:</strong> {total_failed}</li>
                <li><strong>Overall Pass Rate:</strong> {overall_pass_rate}%</li>
            </ul>
            
            <p>Best regards,<br>BrowserStack Reporting System</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'browserstack_report_{timestamp}.csv'
        
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(csv_content.encode())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(attachment)
        
        smtp_server = smtp_config.get('smtp_server') or os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(smtp_config.get('smtp_port') or os.getenv('SMTP_PORT', 587))
        smtp_username = smtp_config.get('smtp_username') or os.getenv('SMTP_USERNAME')
        smtp_password = smtp_config.get('smtp_password') or os.getenv('SMTP_PASSWORD')
        
        if smtp_username and smtp_password:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            server.quit()
            
            return jsonify({'success': True, 'message': 'Email sent successfully'})
        else:
            return jsonify({
                'success': False, 
                'message': 'SMTP configuration required. Please set up SMTP credentials in environment variables.'
            }), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'BrowserStack Report Generator API',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'generate_report': '/api/generate-report (POST)',
            'download_report': '/api/download-report (POST)',
            'send_email': '/api/send-email (POST)'
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'API is running'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
