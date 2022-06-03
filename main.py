import indexCollector
import emailServer
import pandas as pd


# TODO Find better way of writing and handling html
intro = """<html>
                   <head>
                   <p>Here is your weekly report for the market Indexes...</p>
                   </head>
        """
conclusion = """
        <body>
            <p style='color:red;'>Have a good day </p>
        </body>
    </html>"""


if __name__ == "__main__":
    print('Generating Index Report... ')

    # TODO make mongo db for clients and there tickers
    # List of all indexes to be gathered
    tickers = ['^DJI', '^GSPC', '^IXIC', 'CL=F', 'GC=F', 'SI=F', '^TNX']

    # Credentials for email service
    smtp_server = ""
    sender_email = ""
    email_list = []
    email_from = ""
    email_to = ""
    password = ""

    # Initialize web scrapper and email server
    indexes = indexCollector.IndexCollector(tickers)
    emailServer = emailServer.EmailServer(smtp_server,465,sender_email,password,email_list)

    try:
        # Collect index/stock information and return as dictionary
        print('Gathering the bodies this may take a minute.')
        collated_data = indexes.collect_data()

        # Convert the data stored as Dict to a pandas dataframe in html
        print('Putting them into coffins')
        data_table = pd.DataFrame(collated_data).to_html()

    except Exception as e:
        # If there is an error when scrapping data print error and close email server
        error = "Something went wrong collecting data... \n " + str(e)
        print(error)

        # Close connection to server and delete instances
        emailServer.server.quit()
        del emailServer
        del indexes


    try:
        for email in email_list:
            # Combine each part of the message into the email and send it
            emailServer.mail_composition("Weekly Index Report",  email_from, email_to, intro, data_table, conclusion)
            emailServer.send_message(email)

        emailServer.server.quit() # Close server connection
        print("Everything worked properly have a nice day...")
        del emailServer
        del indexes

    except Exception as e:
        error = "Something when wrong sending the email... \n " + str(e) + "\n"
        print(error)
        emailServer.server.quit() # Close server connection
        del emailServer
        del indexes


