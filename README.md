# jetmon
Verizon MiFi Jetpack monitoring

## Installation

To drive Firefox, you have to download geckodriver and put it in the same folder as the Python executables or a folder that is on your system’s path.

Download it here:
https://github.com/mozilla/geckodriver/releases

On Linux or macOS, this means modifying the PATH environmental variable. You can see what directories, separated by a colon, make up your system’s path by executing the following command:

`$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin`

To include chromedriver on the path, if it is not already, make sure you include the chromedriver binary’s parent directory. The following line will set the PATH environmental variable its current content, plus an additional path added after the colon:

`$ export PATH="$PATH:/path/to/chromedriver"`

When chromedriver is available on your path, you should be able to execute the chromedriver executable from any directory.
