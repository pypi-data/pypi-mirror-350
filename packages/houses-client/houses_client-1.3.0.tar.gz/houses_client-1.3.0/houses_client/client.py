import sys, getopt
import oidc_client
from datetime import datetime, timedelta
import requests
import logging
import json
import time


class HousesClient(object):
    """
    A Single step (job) in the HOUSES pipeline
    """

    def __init__(self, api_endpoint, client_id, client_secret, self_hosted, log_level="INFO"):
        """
        Create a new HOUSES SDK Client
        :param api_endpoint: houses endpoint
        :param client_id: OIDC Client ID
        :param client_secret:  OIC Client Secret
        :param log_level: Log level, default = INFO
        """
        self.logger = self.__init_logger(log_level)
        self.api_endpoint = api_endpoint
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.access_token_expiration = None
        self.task_status = None
        self.self_hosted = self_hosted
        if self.api_endpoint is None:
            self.logger.fatal("API endpoint is required")
        if not self.self_hosted:
            self.__init_provider_config()
            if self.client_id is None:
                self.logger.fatal("OIDC Client ID is required")
            if self.client_secret is None:
                self.logger.fatal("OIDC Client Secret is required")

    def __init_logger(self, levelName):
        """
        Initialize logger
        :param levelName:
        :return:
        """
        level = logging.INFO
        if levelName.upper() == 'DEBUG':
            level = logging.DEBUG
        elif levelName.upper() == 'ERROR':
            level = logging.error
        elif levelName.upper() == 'WARNING':
            level = logging.warning
        log_format = '%(process)d %(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s'

        logger = logging.getLogger("houses-sdk")
        logger.setLevel(level)
        print(f"Setting log level to {level}")
        if logger.hasHandlers() == False:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(level)
            stream_formatter = logging.Formatter(log_format)
            stream_handler.setFormatter(stream_formatter)
            logger.addHandler(stream_handler)
        return logger

    def __init_provider_config(self):
        """
        Initialize OIDC ProviderConfig
        :return:
        """
        baseUrl = f"{self.api_endpoint}/auth/realms/houses"
        self.providerConfig = oidc_client.ProviderConfig(issuer=baseUrl,
                                                         authorization_endpoint=f"{baseUrl}/protocol/openid-connect/auth",
                                                         token_endpoint=f"{baseUrl}/protocol/openid-connect/token")
        self.logger.debug(f"Using auth provider config :{self.providerConfig}")

    def __get_access_token(self):
        """
        Get current or new OIDC Access Token
        :return:
        """
        if self.self_hosted:
            return "anonymous"
        else:
            if self.access_token is None:
                self.logger.debug(f"Fetching new access token")
                tokenResponse: oidc_client.TokenResponse = oidc_client.lib.login(self.providerConfig,
                                                                                 client_id=self.client_id,
                                                                                 client_secret=self.client_secret)
                self.access_token = tokenResponse.access_token
                self.logger.debug(f"{self.access_token}")

            return self.access_token

    def __get_api_endpoint(self):
        path = "/api"
        if self.self_hosted:
            path = ""
        return f"{self.api_endpoint}{path}"

    def __submit_get_metrics_batch(self, files, year, delimiter):
        for i in range(0, 2):
            response = requests.post(f"{self.__get_api_endpoint()}/index/getMetricsBatch",
                                     files=files,
                                     data={"year": year, "delimiter": delimiter},
                                     headers=self.__get_headers())
            if not self.is_expired_access_token(response):
                return response
            else:
                self.access_token = None

    def __submit_get_status_request(self):
        url = f"{self.__get_api_endpoint()}/index/task_status?task_id={self.task_id}"
        for i in range(0, 2):
            response = requests.get(url, headers=self.__get_headers())
            if not self.is_expired_access_token(response):
                return response
            else:
                self.access_token = None

    def __delete_task_request(self):
        url = f"{self.__get_api_endpoint()}/index/task?task_id={self.task_id}"
        for i in range(0, 2):
            response = requests.delete(url, headers=self.__get_headers())
            if not self.is_expired_access_token(response):
                return response
            else:
                self.access_token = None

    def __submit_get_results_request(self):
        url = f"{self.__get_api_endpoint()}/index/task_results_file?task_id={self.task_id}"
        for i in range(0, 2):
            response = requests.get(url, headers=self.__get_headers())
            if not self.is_expired_access_token(response):
                return response
            else:
                self.access_token = None

    def __get_headers(self):
        return {"Authorization": f"Bearer {self.__get_access_token()}"}

    def is_expired_access_token(self, response):
        return response.status_code == 401 and "Signature has expired" in response.content.decode()

    def batch(self, input_path, output_path, year=None, delimiter=","):
        """
        Submit HOUSES batch request
        :param input_path: Input CSV File Path
        :param output_path: Output CSV File Path
        :param year: Optional year for index
        :param delimiter: Optional file delimiter, default = ,
        :return:
        """
        if not isinstance(year, int):
            year = int(year)
        self.task_status = None
        self.logger.info(f"Batch input: {input_path} and write to {output_path} for year={year}")
        files = {'data_file': open(input_path, 'rb')}
        r = self.__submit_get_metrics_batch(files, year, delimiter)
        if r.status_code != 200:
            self.logger.fatal(f"Error processing request, unexpected status = {r.status_code}, {r.content}")
            self.access_token = None

        self.task_id = json.loads(r.text)['task_id']
        self.logger.info(f"Request submitted: {self.task_id}")
        waitSeconds = 1
        maxWaitSeconds = 30
        while self.task_status is None or self.task_status != 'SUCCESS':
            # get status
            time.sleep(waitSeconds)
            self.logger.info(f"Checking request status {self.task_id}")
            sr = self.__submit_get_status_request()
            if sr.status_code != 200:
                self.logger.fatal(f"Error checking status of task, unexpected status = {sr.status_code}, {sr.content}")
            self.task_status = json.loads(sr.text)['status']
            if self.task_status == 'ERROR':
                raise Exception("Request Error reported")
            waitSeconds = min(maxWaitSeconds, waitSeconds * 2)
            self.logger.info(f"Request status = {self.task_status}")

        self.logger.info("Downloading results")
        dr = self.__submit_get_results_request()
        if dr.status_code != 200:
            self.logger.fatal(f"Error downloading results, unexpected status = {dr.status_code}, {dr.content}")
        open(output_path, 'wb').write(dr.content)
        # delete task data
        self.__delete_task_request()
        self.logger.info(f"Results downloaded to {output_path}")


def main(argv):
    """
    Example CLI Usage of the client
    :param argv:
    :return:
    """
    opts, args = getopt.getopt(argv, "he:i:o:u:s:e,y:d:l", ["ifile=", "ofile=", "clientid=",
                                                            "clientsecret=", "endpoint=", "year=", "delimiter=",
                                                            "selfhosted"])
    inputfile = None
    outputfile = None
    apiendpoint = None
    clientid = None
    clientsecret = None
    year = None
    delimiter = ","
    self_hosted = False
    for opt, arg in opts:
        if opt == '-h':
            print(
                'client.py -i <inputfile> -o <outputfile> -u <oidc client id> -s <oidc secret> -e <api endpoint> -y <year optional> -d <delimiter>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-u", "--clientid"):
            clientid = arg
        elif opt in ("-s", "--clientsecret"):
            clientsecret = arg
        elif opt in ("-e", "--endpoint"):
            apiendpoint = arg
        elif opt in ("-y", "--year"):
            year = arg
        elif opt in ("-d", "--delimiter"):
            delimiter = arg
        elif opt in ("-l", "--selfhosted"):
            self_hosted = True
    client = HousesClient(api_endpoint=apiendpoint, client_id=clientid, client_secret=clientsecret,
                          self_hosted=self_hosted)
    client.batch(input_path=inputfile, output_path=outputfile, year=year, delimiter=delimiter)


if __name__ == '__main__':
    main(sys.argv[1:])
