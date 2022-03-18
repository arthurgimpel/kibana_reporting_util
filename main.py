import requests
import time
import json


def download_pdf(pdf_url, es_user, es_password):
    try:
        payload = requests.get(pdf_url, auth=requests.auth.HTTPBasicAuth(es_user, es_password))
    except requests.exceptions.RequestException as err:
        print('Error in downloading PDF')
        raise SystemExit(err)
    return payload


def get_report_pdf(report_url, es_user, es_password):
    req_headers = {'kbn-xsrf': 'true'}
    try:
        payload = requests.post(report_url, headers=req_headers, auth=requests.auth.HTTPBasicAuth(es_user, es_password))
        response_json = payload.json()
        pdf_path = response_json['path']
        pdf_path = kibana_url + pdf_path

    except requests.exceptions.RequestException as err:
        print('Error in generating report')
        raise SystemExit(err)
    print('Got PDF URL, waiting for report generation')
    time.sleep(120)
    print('Downloading PDF report')
    pdf_report = download_pdf(pdf_path, es_user, es_password)
    print('PDF report downloaded successfully')
    return pdf_report


def save_report(file_name, file_obj):
    with open(file_name + '.pdf', 'wb') as f:
        f.write(file_obj)


if __name__ == '__main__':
    print('Loading settings file')
    try:
        settings_file = open('report_settings.json')
        settings = json.load(settings_file)
    except Exception as err:
        print('Error in loading settings file')
        raise SystemExit(err)
    print('Settings file loaded')
    for setting in settings['kibana_reports']:
        kibana_report_url = setting['report_url']
        user = setting['es_user']
        password = setting['es_password']
        report_name = setting['report_name']
        print('Starting report generation for ' + report_name)
        kibana_url = kibana_report_url[0:kibana_report_url.rfind(':9243/')+5]
        response = get_report_pdf(kibana_report_url, user, password)
        print('Report generation complete, saving file on disk')
        pdf_file = response.content
        save_report(report_name, pdf_file)
        print('Report ' + report_name + ' was saved successfully')




