from processor_regex import classify_with_regex
from processor_bert import classify_with_bert
from processor_llm import classify_with_llm
import webbrowser
import threading
import time
import os

def classify(logs):
    labels = []
    for source, log_msg in logs:
        label = classify_log(source, log_msg)
        labels.append(label)
    return labels


def classify_log(source, log_msg):
    if source == "LegacyCRM":
        label = classify_with_llm(log_msg)
    else:
        label = classify_with_regex(log_msg)
        if not label:
            label = classify_with_bert(log_msg)
    return label

def classify_csv(input_file):
    import pandas as pd
    df = pd.read_csv(input_file)

    # Perform classification
    df["target_label"] = classify(list(zip(df["source"], df["log_message"])))

    # Save the modified file
    output_file = "output.csv"
    df.to_csv(output_file, index=False)

    return output_file

def open_browser():
    """Open browser after a short delay to ensure Flask app is running"""
    time.sleep(2)  # Wait 2 seconds for Flask to start
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    # First run the classification on the test data
    classify_csv("resources/test.csv")
    print("Classification completed! Opening web interface...")
    
    # Start browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Import and run the Flask app
    from app import app
    PORT = int(os.environ.get("PORT", "5000"))
    app.run(host='0.0.0.0', port=PORT, debug=False)
    
    # logs = [
    #     ("ModernCRM", "IP 192.168.133.114 blocked due to potential attack"),
    #     ("BillingSystem", "User 12345 logged in."),
    #     ("AnalyticsEngine", "File data_6957.csv uploaded successfully by user User265."),
    #     ("AnalyticsEngine", "Backup completed successfully."),
    #     ("ModernHR", "GET /v2/54fadb412c4e40cdbaed9335e4c35a9e/servers/detail HTTP/1.1 RCODE  200 len: 1583 time: 0.1878400"),
    #     ("ModernHR", "Admin access escalation detected for user 9429"),
    #     ("LegacyCRM", "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."),
    #     ("LegacyCRM", "Invoice generation process aborted for order ID 8910 due to invalid tax calculation module."),
    #     ("LegacyCRM", "The 'BulkEmailSender' feature is no longer supported. Use 'EmailCampaignManager' for improved functionality."),
    #     ("LegacyCRM", " The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025")
    # ]
    # labels = classify(logs)
    #
    # for log, label in zip(logs, labels):
    #     print(log[0], "->", label)


