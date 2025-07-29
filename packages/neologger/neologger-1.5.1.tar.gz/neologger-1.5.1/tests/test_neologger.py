from neologger import NeoLogger, Table, Alarm, SlackNotification
from neologger.core import Template
from neologger.core import FontColour, FontStyle, Condition
import time

slack = SlackNotification()
slack.set_hook("[SLACK_WEBHOOK_URL]")
alarm = Alarm(3, slack=slack)
neologger = NeoLogger("test_neolloger.py", alarm=alarm)

def main():
    print("\nBasic example:\n")
    neologger.log_this("Starting NeoLogger")
    print("\n")

    print("\nExample with OK label:\n")
    neologger.log_this_ok("Function completed Ok.")
    print("\n")

    print("\nExample with WARNING label:\n")
    neologger.log_this_warning("Data was sent uncompleted.")
    print("\n")

    print("\nExample with COMPLETED label:\n")
    neologger.log_this_completed("Data collection stage completed.")
    print("\n")

    print("\nExample with SUCCESS label:\n")
    neologger.log_this_success("Request has been completed successfuly")
    print("\n")
    
    print("\nExample with ERROR label:\n")
    neologger.log_this_error("Something went wrong!")
    print("\n")
    
    print("\nExample with BASE Template:\n")
    neologger.set_template(Template.BASE)
    neologger.log_this("NeoLogger has been set with BASE Template")
    print("\n")

    print("\nExample with NORMAL Template:\n")
    neologger.set_template(Template.NORMAL)
    neologger.log_this("NeoLogger has been set with NORMAL Template")
    print("\n")

    print("\nExample with DARK Template:\n")
    neologger.set_template(Template.DARK)
    neologger.log_this("NeoLogger has been set with DARK Template")
    print("\n")

    print("\nExample with FontStyle customisation\n")
    neologger.set_log_font_style(FontStyle.NORMAL, FontStyle.ITALIC, FontStyle.BOLD, FontStyle.UNDERLINE)
    neologger.log_this("Font style has been customised")
    print("\n")

    neologger.set_template(Template.BASE)
    print("\nExample with Elapsed Time display\n")
    time_track = neologger.get_time_mark()
    time.sleep(4) # Adding delay
    neologger.log_with_elapsed_time("Function completed.", time_track)
    print("\n")

    print("\nExample of Table")
    table = Table()
    table.set_title("Last month sales report.")
    header = ["No", "Depto", "Name", "Top Product", "Total Sales", "Rank"]
    table.set_header(header)
    row = table.new_row()
    row_content = ["1", "IT", "Pablo Martinez", "Servers", "£12,500", "1sr"]
    row.fill_row(row_content)
    table.push_row(row)
    row = table.new_row()
    row_content = ["2", "Marketing", "Beatriz Romero", "Campain", "£11,250", "2nd"]
    row.fill_row(row_content)
    table.push_row(row)
    row = table.new_row()
    row_content = ["3", "Automotive", "Gabriela Martinez", "Peugeot 3008", "£11,108", "3rd"]
    row.fill_row(row_content)
    table.push_row(row)
    row = table.new_row()
    row_content = ["4", "Robotics", "Aurora Martinez", "Robotic Arm", "£10,090", "4th"]
    row.fill_row(row_content)
    table.push_row(row)
    table.enable_total()
    table.enable_border()
    neologger.log_this(table.render(), save_json=False)

    print("\nExample of Table from JSON")
    table = Table()
    jdata = [
        {"Id": "1011", "Code": "Ab99s0r", "Expiration": "13-10-2024", "Status": "ACTIVE", "Base": "https://endpoint.com/api/action"},
        {"Id": "1012", "Code": "12dLLd0", "Expiration": "12-11-2024", "Status": "ACTIVE", "Base": "https://endpoint.com/api/action"},
        {"Id": "1013", "Code": "5540xxD", "Expiration": "10-08-2024", "Status": "ACTIVE", "Base": "https://endpoint.com/api/action"},
        {"Id": "1014", "Code": "0dd9AsX", "Expiration": "08-05-2024", "Status": "INACTIVE", "Base": "https://endpoint.com/api/action"}
    ]
    
    table.set_title("DATA FROM JSON")
    table.enable_total()
    table.enable_border()
    neologger.log_this(table.from_json(jdata), save_json=False)

    print("Testing embedded stopwatch in neologger")
    neologger.start_stopwatch("ABC function trace")
    neologger.lap("Function is starting")
    time.sleep(0.34)
    neologger.lap("First checkpoint reached")
    time.sleep(1.26)
    neologger.lap("Second checkpoint reached")
    time.sleep(0.45)
    neologger.lap("Last checkpoint reached")
    neologger.log_this_with_trace("Function ABC has completed execution.")


if __name__ == "__main__":
    main()