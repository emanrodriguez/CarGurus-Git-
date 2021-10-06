import sys
import subprocess


def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    return


if __name__ == '__main__':
    packages = ['BeautifulSoup', 'requests', 'mysql.connector', 'twilio.rest', 'flask', 'twilio.twiml.messaging_response', 'twilio.rest']
    for i in packages:
        install(i)


