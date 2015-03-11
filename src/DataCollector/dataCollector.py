__author__ = 'shashankm'

import datetime
import urllib
import zipfile
import os
import os.path

if __name__ == "__main__":
    current = datetime.datetime.now();
    delta = datetime.timedelta(days=-1)
    i = 0;
    while (i < 2):
        current += delta
        i += 1
        try:
            downloadURL = 'http://www.bseindia.com/bsedata/newbhavcopy/bhavcopy' + current.strftime("%d%m15") + '_CSV.ZIP'
            file_name = downloadURL.split('/')[-1]
            urllib.urlretrieve(downloadURL, file_name);

            if (os.path.isfile(file_name)):
                with zipfile.ZipFile(file_name, "r") as z:
                    z.extractall();

                os.remove(file_name);
        except:
            os.remove(file_name);
            pass