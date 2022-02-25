
## Regression Tests

Example: [https://www.boost.org/development/tests/develop/developer/summary.html](https://www.boost.org/development/tests/develop/developer/summary.html)  
Linked from: [https://www.boost.org/development/testing.html](https://www.boost.org/development/testing.html)  

### Summary of how tests are processed  

1. The matrix of test results is generated externally on 3rd party servers. Those results are uploaded to results.boost.org  

2. A cron job on the boost.org web server checks results.boost.org every hour to see if there is any new data. If new data is present it triggers a circleci run, https://github.com/boostorg/regression, ci/test-reports branch.  

3. The circleci job packages the results and uploads large zip files to the boost.org webserver: develop.zip and master.zip  

4. The boost.org server doesn't unzip the archives. Test results are served directly from the zip archives by "unzipping" individual files on-demand and displaying them to the web visitor.  

### More details about each steps  

1. The matrix of test results is generated externally on 3rd party servers. The results are uploaded to results.boost.org. The regression test code is available in the repo https://github.com/boostorg/regression . This process is already in place and running on those other systems (not the boost.org web server).  It may not need to be modified.

2. A cron job on the boost.org web server checks results.boost.org each hour, at the 30 minute mark, to see if there is any new data. The crontab file at /var/spool/cron/grafik:  

```
#0-59/30 * * * * $HOME/www.boost.org/testing/trigger_test_reports.sh
#BAJ - 4-Mar-2019 - asked to run once per hour
#BAJ - 16-Dec-2019 - commenting out for next line...
#30 * * * * $HOME/www.boost.org/testing/trigger_test_reports.sh
#BAJ - 16-Dec-2019 - switching to version that uses results.boost.og
30 * * * * $HOME/www.boost.org/testing/trigger_test_reports_new_server.sh
```

The script is $HOME/www.boost.org/testing/trigger_test_reports_new_server.sh, shown here:  

```
#!/bin/bash

CIRCLECI_TOKEN=_the_token_
RESULTS_URL=ftp://_the_url_

cd ${HOME}/www.boost.org/testing
curl -s ${RESULTS_URL}/develop/ > results.lst
curl -s ${RESULTS_URL}/master/ >> results.lst
cat results.lst | shasum -c results.sum 2>&1 > /dev/null
if [ $? -ne 0 ]; then
        cat results.lst | shasum > results.sum
        curl -s -X POST --header "Content-Type: application/json" -d '{ }' https://circleci.com/api/v1.1/project/github/boostorg/regression/tree/ci/test-reports?circle-token=${CIRCLECI_TOKEN} > /dev/null
fi
```

(RESULTS\_URL may be found in https://github.com/boostorg/regression , `reports/src/boost_wide_report.py` , notice "ftp_site =" and "site_path ="). The script contacts the RESULTS_URL and checks if any results have changed. If they have changed it triggers circleci, https://github.com/boostorg/regression repo, ci/test-reports branch.  

3. The circleci job calls the script `https://github.com/boostorg/regression/blob/ci/test-reports/ci_build_results_all.sh` . It packages all the results and uploads them to the boost.org web server. Uploads are done by the upload\_results() function of ci\_build\_results\_all.sh   

On the boost.org web server, the zip archives are found at `/home/grafik/www.boost.org/testing/live` :

```
[root@wowbagger cron]# ls -alh /home/grafik/www.boost.org/testing/live
total 2.0G
drwxr-xr-x 2 grafik boost 4.0K Feb 24 19:59 .
drwxr-xr-x 5 grafik boost 4.0K Oct 28 15:23 ..
-rw-r--r-- 1 grafik boost 1.1G Feb 24 19:59 develop.zip
-rw-r--r-- 1 grafik boost 972M Feb 24 19:55 master.zip
```

4. The boost.org apache web server hosts the files. Test results are served directly from the zip archives by "unzipping" individual files on-demand and displaying them to the web visitor. To review the flow of logic: firstly an important variable is RESULTS_DIR.  

The config file common/code/boost\_config.php includes the line   

```
define('BOOST_CONFIG_FILE','/home/www/shared/config.php');
```
  
The file /home/www/shared/config.php contains:  
```
<?php
define('BOOST_RSS_DIR', '/home/grafik/www.boost.org');
define('BOOST_WEBSITE_SHARED_DIR', __DIR__);
define('DATA_DIR', '/home/www/shared/data');
define('ARCHIVE_DIR', '/home/www/shared/archives/live');
define('STATIC_DIR', '/home/www/shared/archives/live');
define('RESULTS_DIR', '/home/grafik/www.boost.org/testing/live');
define('UNZIP', '/u/grafik/bin/unzip');
define('BOOST_TASKS_DIR', '/u/dnljms/boost-tasks');
define('BOOST_FIX_DIR', '/home/www/shared/repos/documentation-fixes');
define('BOOST_QUICKBOOK_EXECUTABLE', '/home/www/shared/bin/quickbook');
```
  
Notice `RESULTS_DIR=/home/grafik/www.boost.org/testing/live` which is where develop.zip and master.zip are.  
  
When a web visitor goes to https://www.boost.org/development/tests/master/developer/summary.html they encounter certain .htaccess rules:  
  
This is a rewrite rule in the development/.htaccess file  
  
```
RewriteRule ^tests/(.*)$ testing_results.php/$1 [L]
```
  
So all tests/ pages are processed by `testing_results.php`.  

`testing_results.php` calls BoostArchive. Although BoostArchive could be a general class, it's only used by testing_results.php.  BoostArchive serves the zip files directly as web pages.  For example, to display a file named summary.html, it calls a command "unzip -p develop.zip summary.html", which unzips the file on-the-fly.    

