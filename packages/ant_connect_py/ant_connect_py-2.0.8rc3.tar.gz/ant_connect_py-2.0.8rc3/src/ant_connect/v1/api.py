import time
import codecs
import json
import base64
import warnings
from datetime import datetime, timedelta
import re
from typing import Any

import requests


# v1 will be depricated from Januari 1st 2025
warnings.warn(
    "This module (ANTConnect v1) of the API will be deprecated from Januari 1st 2025",
    DeprecationWarning,
    stacklevel=2,
)


class Response:
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code


class API:
    _host = ""
    _access_token = ""
    _api_version = "1.0"
    _authenticated = False
    _logger = None

    def __init__(self, host: str = "https://api.antcde.io/", logging: bool = False):
        # v1 will be depricated from Januari 1st 2025
        warnings.warn(
            "This class (ANTConnect v1) of the API will be deprecated from Januari 1st 2025",
            DeprecationWarning,
            stacklevel=2,
        )
        self._host = host
        self._logging = logging
        self._remainingRequests = 10

    def login(self, client_id: str, client_secret: str, username: str, password: str) -> Response:
        """Login into ANT"""
        warnings.warn(
            "This class (ANTConnect v1) of the API will be deprecated from Januari 1st 2025",
            DeprecationWarning,
            stacklevel=2,
        )
        self._authenticated = False
        self._client_id = client_id
        self._client_secret = client_secret
        response = self._make_request(
            "oauth/token",
            "POST",
            {
                "grant_type": "password",
                "username": username,
                "password": password,
                "client_id": client_id,
                "client_secret": client_secret,
            },
        )

        if self._logging:
            print("New login call at {}, returned with code {}".format(datetime.now(), response.status_code))
        if response.status_code != 200:
            print("The response was: {}".format(response.reason))
            return Response(response.reason, response.status_code)
        else:
            parsed_response = response.json()
            # print(parsed_response)
            if "access_token" not in parsed_response:
                raise SystemError("Please check credentials")
            now = datetime.now()
            self._access_token = parsed_response["access_token"]
            self._refresh_token = parsed_response["refresh_token"]
            self._expires_at = now + timedelta(seconds=parsed_response["expires_in"])
            self._authenticated = True

            user = self.getUserInfo()
            self._licenses = user["licenses"]
            if user["two_factor_enabled"]:
                two_fa_validated = False
                while not two_fa_validated:
                    code = input("Provide your 2FA code: ")
                    two_fa_validated = self.twoFactor(code)
            return Response("User authenticated", 200)

    def twoFactor(self, code: str):
        body = {"code": str(code)}
        response = self._make_api_request("2fa/verify", "POST", body)
        validated = False
        try:
            validated = response["status"] == "success"
        except ValueError:
            print("Your code was invalid, try it again")
        except:
            print("Your code was invalid, try it again")

        return validated

    def getUserInfo(self):
        return self._make_api_request("user", "GET")

    def _make_api_request(
        self,
        path: str,
        method: str,
        parameters: dict = None,
        delete_data: dict = None,
        isFile: bool = False,
    ) -> Any:
        parameters = parameters or {}

        if not self._authenticated:
            raise SystemError("You are not authenticated, please use login first.")

        if datetime.now() >= self._expires_at:
            print("Unauthorised, trying to refresh token...")
            self.refresh_token()
            if not self._authenticated:
                return Response("Access token expired", 401)

        data = parameters if method in ["GET", "DELETE"] else json.dumps(parameters)
        url = f"api/{self._api_version}/{path}"

        # If rate limit is not reached
        if self._remainingRequests == 0:
            remaining_seconds = (self._RateLimitRefreshAt - datetime.now()).total_seconds()
            if remaining_seconds > 0 and self._logging:
                print(f"Sleeping {remaining_seconds} seconds, API rate limit reached")
                time.sleep(remaining_seconds)

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self._access_token}",
        }

        retry_count = 0

        while retry_count < 3:
            response = self._make_request(url, method, data, headers, delete_data)

            if 500 <= response.status_code < 600:
                retry_count += 1
                if retry_count < 3:
                    print(
                        f"Encountered a {response.status_code} error. Retrying in 15 seconds... (Attempt {retry_count})"
                    )
                    time.sleep(15)
                    continue
                else:
                    print("Failed after 3 attempts")
                    return Response("Server failed after 3 retries", 500)
            else:
                break

        if response.status_code in [401, 404, 400]:
            try:
                print(f"An error occurred: {response.json()['message']}")
            except ValueError:
                print("An error occurred but couldn't parse the response.")
            if response.status_code == 401:
                self._authenticated = False
                self._access_token = ""
                self._refresh_token = ""
                self._expires_at = ""
            return Response(response.reason, response.status_code)

        ratelimit_remaining = int(response.headers.get("x-ratelimit-remaining", 40))  # default to 40 if not found
        if self._remainingRequests > ratelimit_remaining:
            self._RateLimitRefreshAt = datetime.now() + timedelta(seconds=60)
            print(f"Reset time to: {self._RateLimitRefreshAt}")

        self._remainingRequests = ratelimit_remaining

        if self._logging:
            print(f"New API call at {datetime.now()}, returned with code {response.status_code}")
            if int(ratelimit_remaining) < 10:
                print(f"Warning, you are reaching the API_rate_limit, {ratelimit_remaining} calls left this minute")

        if response.text == "":
            print("Response was empty")
            return Response("server returned in incorrect format, please contact support", 500)

        try:
            if isFile:
                return response.content.decode("utf-8")
            parsed_response = response.json()
            if "message" in parsed_response:
                if parsed_response["message"] == "Unauthenticated.":
                    raise PermissionError("Unauthenticated")
                if parsed_response["message"] == "Too Many Attempts.":
                    raise ProcessLookupError("Too many requests attempted")
            return parsed_response
        except ValueError:
            print("Couldn't parse the response.")
            return Response("server returned in incorrect format, please contact support", 500)

    def _make_request(
        self,
        path: str,
        method: str,
        parameters: dict = None,
        headers: dict = None,
        data: dict = None,
    ) -> requests.Response:
        parameters = {} if parameters is None else parameters
        headers = {} if headers is None else headers
        url = "{}{}".format(self._host, path)
        if method == "GET":
            return requests.get(url, params=parameters, headers=headers, verify=True)
        if method == "PUT":
            return requests.put(url, data=parameters, headers=headers, verify=True)
        if method == "DELETE":
            return requests.delete(
                url,
                data=json.dumps(data),
                params=parameters,
                headers=headers,
                verify=True,
            )
        if method == "POST":
            return requests.post(url, data=parameters, headers=headers, verify=True)
        raise NotImplementedError("http method not implemented")

    def refresh_token(self):
        body = {
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "scope": "",
        }
        url = "{}oauth/token".format(self._host)
        response = requests.post(url, data=body)
        if self._logging:
            print("New login call at {}, returned with code {}".format(datetime.now(), response.status_code))
        if response.status_code != 200:
            print("something went wrong with receiving new access_token")
            self._authenticated = False
        else:
            now = datetime.now()
            parsed_response = response.json()
            self._access_token = parsed_response["access_token"]
            self._refresh_token = parsed_response["refresh_token"]
            self._expires_at = now + timedelta(seconds=parsed_response["expires_in"])
            print("token successfully refreshed")

    def projects_read(self):
        """List all your projects"""
        path = "projects"
        return self._make_api_request(path, "GET")

    def project_create(
        self,
        licenseid: str,
        name: str,
        number: str = "",
        description: str = "",
        imageName: str = "",
        imageExtension: str = "",
        imageData: str = "",
    ) -> dict:
        """Create a new project"""
        path = "project"
        slug = slugify(name)
        if imageExtension == "":
            project = {
                "name": name,
                "number": number,
                "description": description,
                "license": licenseid,
                "slug": slug,
            }
        else:
            project = {
                "name": name,
                "number": number,
                "description": description,
                "license": licenseid,
                "image": {
                    "name": imageName,
                    "extension": imageExtension,
                    "data": imageData,
                },
                "slug": slug,
            }
        return self._make_api_request(path, "POST", project)

    def project_read(self, project_id: str) -> dict:
        """Get project details"""
        path = "project/{}".format(project_id)
        return self._make_api_request(path, "GET")

    def project_Update(self, project_id: str, name: str) -> dict:
        """Get project update"""
        path = "project/{}".format(project_id)
        return self._make_api_request(path, "PUT", {"name": name})

    def project_delete(self, project_id: str) -> dict:
        """Get project delete"""
        path = "project/{}".format(project_id)
        return self._make_api_request(path, "DELETE")

    def tables_read(self, project_id: str):
        """Get tables in a project"""
        path = "tables"
        return self._make_api_request(path, "GET", {"project[id]": project_id})

    def table_create(self, project_id: str, name: str) -> dict:
        """Create a table in a project"""
        path = "table"
        return self._make_api_request(path, "POST", {"project": {"id": project_id}, "name": name})

    def table_read(self, project_id: str, table_id: str) -> dict:
        """Get details of a table in a project"""
        path = "table/{}".format(table_id)
        return self._make_api_request(path, "GET", {"project[id]": project_id})

    def table_update(self, project_id: str, table_id: str, name: str) -> dict:
        """Update a table in a project"""
        path = "table/{}".format(table_id)
        return self._make_api_request(path, "PUT", {"project": {"id": project_id}, "name": name})

    def table_delete(self, project_id: str, table_id: str) -> dict:
        """Delete a table in a project"""
        path = "table/{}".format(table_id)
        return self._make_api_request(path, "DELETE", {"project[id]": project_id})

    def tables_query(self, project_id: str, queryBody):
        """executes query over multiple tables returns limited data"""
        path = "project/{}/tables/query".format(project_id)
        return self._make_api_request(path, "POST", queryBody)

    def tables_query_stream(self, project_id: str, queryBody):
        """executes query over single table and returns all data"""
        path = "project/{}/tables/query/stream".format(project_id)
        return self._make_api_request(path, "POST", queryBody, None, True)

    def columns_read(self, project_id: str, table_id: str):
        """Get all columns in a table"""
        path = "columns"
        return self._make_api_request(path, "GET", {"project[id]": project_id, "table[id]": table_id})

    def column_create(
        self,
        project_id: str,
        table_id: str,
        name: str,
        fieldType: str,
        defaultValue: str = "",
        options: list = None,
        required: bool = True,
        ordinal: int = "",
    ) -> dict:
        """Create a column in a table"""
        options = [] if options is None else options
        path = "column"
        return self._make_api_request(
            path,
            "POST",
            {
                "project": {"id": project_id},
                "table": {"id": table_id},
                "name": name,
                "type": fieldType,
                "options_value": options,
                "default": defaultValue,
                "required": required,
                "ordinal": ordinal,
            },
        )

    def column_read(self, project_id: str, table_id: str, column_id):
        """Get details for a specific column in a table"""
        path = "column/{}".format(column_id)
        return self._make_api_request(path, "GET", {"project[id]": project_id, "table[id]": table_id})

    def column_update(
        self,
        project_id: str,
        table_id: str,
        column_id: str,
        name: str,
        defaultValue: str = "",
        options: list = None,
        required: bool = True,
        ordinal: int = 0,
    ) -> dict:
        """Update details for a specific column in a table"""
        path = "column/{}".format(column_id)
        return self._make_api_request(
            path,
            "PUT",
            {
                "project": {"id": project_id},
                "table": {"id": table_id},
                "name": name,
                "required": required,
                "options": options,
                "default": defaultValue,
                "ordinal": ordinal,
            },
        )

    def column_delete(self, project_id: str, table_id: str, column_id: str) -> dict:
        """Delete column in a table"""
        path = "column/{}".format(column_id)
        return self._make_api_request(path, "DELETE", {"project[id]": project_id, "table[id]": table_id})

    def records_create_csv(self, project_id: str, table_id: str, records_csv: str, session: str = ""):
        """Import a csv file into a table"""
        path = "records/import"
        with codecs.open(records_csv, mode="r", encoding="utf-8") as csv_file:
            encoded_csv = base64.b64encode(str.encode(csv_file.read()))
        result = self._make_api_request(
            path,
            "POST",
            {
                "project": {"id": project_id},
                "table": {"id": table_id},
                "session": {"id": session},
                "records": encoded_csv.decode("utf-8"),
            },
        )
        return result

    def records_create(self, project_id: str, table_id: str, records: list, session: str = ""):
        """Create multiple records into a table"""
        path = "records/import"
        encoded_csv = base64.b64encode(self.create_virtual_csv(records).encode("utf-8"))
        result = self._make_api_request(
            path,
            "POST",
            {
                "project": {"id": project_id},
                "table": {"id": table_id},
                "session": {"id": session},
                "records": encoded_csv.decode("utf-8"),
            },
        )
        return result

    def records_import(self, project_id: str, table_id: str, records: list, session: str = ""):
        """Create multiple records into a table"""
        path = "records/import"
        encoded_csv = base64.b64encode(self.create_virtual_csv_Addid(records).encode("utf-8"))
        result = self._make_api_request(
            path,
            "POST",
            {
                "project": {"id": project_id},
                "table": {"id": table_id},
                "session": {"id": session},
                "records": encoded_csv.decode("utf-8"),
            },
        )
        return result

    def records_read_chunk(
        self,
        project_id: str,
        table_id: str,
        limit: int = 0,
        offset: int = 0,
        session: str = "",
    ) -> dict:
        """Get reords of table"""
        path = "records"
        record_data = self._make_api_request(
            path,
            "GET",
            {
                "project[id]": project_id,
                "table[id]": table_id,
                "filter[limit]": limit,
                "filter[offset]": offset,
                "filter[session]": session,
            },
        )
        return record_data

    def records_read(
        self,
        project_id: str,
        table_id: str,
        limit: int = 0,
        offset: int = 0,
        session: str = "",
        chunk_size: int = 10000,
    ) -> dict:
        """Get reords of table"""
        record_data = self.records_read_chunk(project_id, table_id, chunk_size, offset, session)
        if limit == 0 or limit > chunk_size:
            temp_limit = chunk_size
            if len(record_data["records"]) < temp_limit:
                return record_data["records"]
            else:
                if "metadata" in record_data:
                    chunks = (record_data["metadata"]["count"] - offset) // temp_limit
                    if self._logging:
                        print(
                            "Total table is bigger ({}) than chunksize({}), splitting up in: {} additional calls".format(
                                record_data["metadata"]["count"] - offset,
                                temp_limit,
                                chunks,
                            )
                        )
                    all_records = record_data["records"]
                    for i in range(1, chunks + 1):
                        temp_offset = offset + (i * temp_limit)
                        record_data = self.records_read_chunk(project_id, table_id, temp_limit, temp_offset, session)
                        if "message" in record_data.keys():
                            print(record_data["message"])
                        else:
                            all_records = all_records + record_data["records"]
                return all_records
        else:
            temp_limit = limit
            return record_data["records"]

    def records_search(
        self,
        projectId: str,
        tableId: str,
        searchFields: list,
        searchPrase: str = "",
        offset: int = 0,
        limit: int = 0,
        session: str = "",
        chunk_size: int = 10000,
    ):
        """Search in the records"""
        body = {
            "project": {"id": projectId},
            "table": {"id": tableId},
            "search": {"phrase": searchPrase},
            "searchfields": searchFields,
            "session": {"id": session},
        }
        record_data = self.search_chunk(body, chunk_size, offset)
        if limit == 0 or limit > chunk_size:
            temp_limit = chunk_size
            if len(record_data["records"]) < temp_limit:
                return record_data["records"]
            else:
                if "metadata" in record_data:
                    chunks = (record_data["metadata"]["count"] - offset) // temp_limit
                    if self._logging:
                        print(
                            "Total table is bigger ({}) than chunksize({}), splitting up in: {} additional calls".format(
                                record_data["metadata"]["count"] - offset,
                                temp_limit,
                                chunks,
                            )
                        )
                    all_records = record_data["records"]
                    for i in range(1, chunks + 1):
                        temp_offset = offset + (i * temp_limit)
                        record_data = self.search_chunk(body, chunk_size, temp_offset)
                        all_records = all_records + record_data["records"]
                return all_records
        else:
            temp_limit = limit
            return record_data["records"]

    def records_at_moment(
        self,
        projectId: str,
        tableId: str,
        timestamp: int,
        session: str = "",
        offset: int = 0,
        limit: int = 0,
        chunk_size: int = 10000,
    ):
        """Search in the records"""

        body = {
            "project": {"id": projectId},
            "table": {"id": tableId},
            "timestamp": timestamp,
            "session": {"id": session},
        }
        record_data = self.search_chunk(body, chunk_size, offset)
        if limit == 0 or limit > chunk_size:
            temp_limit = chunk_size
            if len(record_data["records"]) < temp_limit:
                return record_data["records"]
            else:
                if "metadata" in record_data:
                    chunks = (record_data["metadata"]["count"] - offset) // temp_limit
                    if self._logging:
                        print(
                            "Total table is bigger ({}) than chunksize({}), splitting up in: {} additional calls".format(
                                record_data["metadata"]["count"] - offset,
                                temp_limit,
                                chunks,
                            )
                        )
                    all_records = record_data["records"]
                    for i in range(1, chunks + 1):
                        temp_offset = offset + (i * temp_limit)
                        record_data = self.search_chunk(body, chunk_size, temp_offset)
                        all_records = all_records + record_data["records"]
                return all_records
        else:
            temp_limit = limit
            return record_data["records"]

    def records_search_exact(
        self,
        projectId: str,
        tableId: str,
        searchFields: list,
        searchExact: str = "",
        limit: int = 0,
        offset: int = 0,
        session: str = "",
        chunk_size: int = 10000,
    ):
        """Search in the records"""
        body = {
            "project": {"id": projectId},
            "table": {"id": tableId},
            "search": {"exact": searchExact},
            "searchfields": searchFields,
            "session": {"id": session},
        }
        record_data = self.search_chunk(body, chunk_size, offset)
        if limit == 0 or limit > chunk_size:
            temp_limit = chunk_size
            if len(record_data["records"]) < temp_limit:
                return record_data["records"]
            else:
                if "metadata" in record_data:
                    chunks = (record_data["metadata"]["count"] - offset) // temp_limit
                    if self._logging:
                        print(
                            "Total table is bigger ({}) than chunksize({}), splitting up in: {} additional calls".format(
                                record_data["metadata"]["count"] - offset,
                                temp_limit,
                                chunks,
                            )
                        )
                    all_records = record_data["records"]
                    for i in range(1, chunks + 1):
                        temp_offset = offset + (i * temp_limit)
                        record_data = self.search_chunk(body, chunk_size, temp_offset)
                        all_records = all_records + record_data["records"]
                return all_records
        else:
            temp_limit = limit
            return record_data["records"]

    def records_search_by_range(
        self,
        projectId: str,
        tableId: str,
        searchFields: list,
        min: int = None,
        max: int = None,
        limit: int = 0,
        offset: int = 0,
        session: str = "",
        chunk_size: int = 10000,
    ):
        """Search in the records"""
        search = {}
        if min is not None and max is not None:
            search = {"min": min, "max": max}
        if min is not None and max is None:
            search = {"min": min}
        if max is not None and min is None:
            search = {"max": max}
        body = {
            "project": {"id": projectId},
            "table": {"id": tableId},
            "search": search,
            "searchfields": searchFields,
            "session": {"id": session},
        }
        record_data = self.search_chunk(body, chunk_size, offset)
        if limit == 0 or limit > chunk_size:
            temp_limit = chunk_size
            if len(record_data["records"]) < temp_limit:
                return record_data["records"]
            else:
                if "metadata" in record_data:
                    chunks = (record_data["metadata"]["count"] - offset) // temp_limit
                    if self._logging:
                        print(
                            "Total table is bigger ({}) than chunksize({}), splitting up in: {} additional calls".format(
                                record_data["metadata"]["count"] - offset,
                                temp_limit,
                                chunks,
                            )
                        )
                    all_records = record_data["records"]
                    for i in range(1, chunks + 1):
                        temp_offset = offset + (i * temp_limit)
                        record_data = self.search_chunk(body, chunk_size, temp_offset)
                        all_records = all_records + record_data["records"]
                return all_records
        else:
            temp_limit = limit
            return record_data["records"]

    def search_chunk(self, body, chunk_size, offset):
        body["filter"] = object()
        body["filter"] = {"limit": chunk_size, "offset": offset}
        # print(body)
        return self._make_api_request("search", "POST", body)

    def records_by_revision(self, projectId: str, tableId: str, revisionId: str):
        """Get records of revision"""
        path = "search"
        package = {
            "project": {"id": projectId},
            "table": {"id": tableId},
            "revision": revisionId,
        }
        return self._make_api_request(path, "POST", package)

    def records_delete(self, project_id: str, table_id: str, records_ids: list) -> dict:
        """Delete records in table"""
        path = "records"
        data = {
            "project": {"id": project_id},
            "table": {"id": table_id},
            "records": records_ids,
        }
        return self._make_api_request(path, "DELETE", delete_data=data)

    def records_verify_csv(self, project_id: str, table_id: str, records_csv: str) -> dict:
        """Verify structure of CSV file against a table"""
        path = "records/verify"
        with codecs.open(records_csv, mode="r", encoding="utf-8") as csv_file:
            encoded_csv = base64.b64encode(str.encode(csv_file.read()))
        result = self._make_api_request(
            path,
            "POST",
            {
                "project": {"id": project_id},
                "table": {"id": table_id},
                "records": encoded_csv.decode("utf-8"),
            },
        )
        return result

    def records_verify(self, project_id: str, table_id: str, records: list) -> dict:
        """Verify structure of records against a table"""
        path = "records/verify"
        encoded_csv = base64.b64encode(self.create_virtual_csv(records).encode("utf-8"))
        result = self._make_api_request(
            path,
            "POST",
            {
                "project": {"id": project_id},
                "table": {"id": table_id},
                "records": encoded_csv.decode("utf-8"),
            },
        )
        return result

    def record_create(self, project_id: str, table_id: str, record_values: dict, session: str = "") -> dict:
        """Create a single record into a table"""
        path = "record"
        return self._make_api_request(
            path,
            "POST",
            {
                "project": {"id": project_id},
                "table": {"id": table_id},
                "session": {"id": session},
                "record": record_values,
            },
        )

    def record_read(self, project_id: str, table_id: str, record_id: str) -> dict:
        """Read a specific record of a table"""
        path = "record/{}".format(record_id)
        return self._make_api_request(path, "GET", {"project[id]": project_id, "table[id]": table_id})

    def record_update(
        self,
        project_id: str,
        table_id: str,
        record_id: str,
        updated_record_values: dict,
        session: str = "",
    ) -> dict:
        """Update a specific record of a table"""
        path = "record/{}".format(record_id)
        return self._make_api_request(
            path,
            "PUT",
            {
                "project": {"id": project_id},
                "table": {"id": table_id},
                "session": {"id": session},
                "record": updated_record_values,
            },
        )

    def record_delete(self, project_id: str, table_id: str, record_id: str) -> dict:
        """Delete a specific record of a table"""
        path = "record/{}".format(record_id)
        return self._make_api_request(path, "DELETE", {"project[id]": project_id, "table[id]": table_id})

    def record_history(self, project_id: str, table_id: str, record_id: str) -> dict:
        """Get change record history a specific record of a table"""
        path = "record/history/{}".format(record_id)
        return self._make_api_request(path, "GET", {"project[id]": project_id, "table[id]": table_id})

    def revisions_read(self, project_id: str, table_id: str) -> dict:
        """Get all revisions of a table"""
        path = "revisions"
        return self._make_api_request(path, "GET", {"project[id]": project_id, "table[id]": table_id})

    def revision_create(self, project_id: str, table_id: str, reason: str) -> dict:
        """Create a new revisions for a table"""
        path = "revision"
        return self._make_api_request(
            path,
            "POST",
            {
                "project": {"id": project_id},
                "table": {"id": table_id},
                "reason": reason,
                "timestamp": time.time(),
            },
        )

    def revision_read(self, project_id: str, table_id: str, revision_id: str) -> dict:
        """Get details of a revisions for a table"""
        path = "revision/{}".format(revision_id)
        return self._make_api_request(path, "GET", {"project[id]": project_id, "table[id]": table_id})

    def revision_update(self, project_id: str, table_id: str, revision_id: str, reason: str) -> dict:
        """Update a revision for a table"""
        path = "revision/{}".format(revision_id)
        return self._make_api_request(
            path,
            "PUT",
            {
                "project": {"id": project_id},
                "table": {"id": table_id},
                "reason": reason,
                "timestamp": time.time(),
            },
        )

    def revision_delete(self: str, project_id: str, table_id: str, revision_id: str) -> dict:
        """Delete a revision for a table"""
        path = "revision/{}".format(revision_id)
        return self._make_api_request(path, "DELETE", {"project[id]": project_id, "table[id]": table_id})

    def upload_document(
        self,
        project_id: str,
        table_id: str,
        column_name: str,
        document_location,
        document_title: str = None,
        session: str = "",
    ):
        """Upload a document to a table. Creates a new record"""
        if document_title is None:
            document_title = document_location.split("/")[-1]
        ext = document_title.split(".")[-1]
        path = "record"
        with open(document_location, "rb") as image_file:
            encoded_file = base64.b64encode(image_file.read())
        dataset = {
            "project": {"id": project_id},
            "table": {"id": table_id},
            "record": {
                column_name: {
                    "name": document_title,
                    "extension": ext,
                    "data": encoded_file.decode("utf-8"),
                }
            },
            "session": {"id": session},
        }
        res = self._make_api_request(path, "POST", dataset)
        if "id" in res:
            return res
        else:
            return "Error"

    def attach_document(
        self,
        project_id: str,
        table_id: str,
        column_name: str,
        record_id: str,
        document_location,
        document_title: str = None,
        session: str = "",
    ):
        """Upload a document to an existing record."""
        if document_title is None:
            document_title = document_location.split("/")[-1]
        ext = document_location.split(".")[-1]
        path = "record/{}".format(record_id)
        with open(document_location, "rb") as image_file:
            encoded_file = base64.b64encode(image_file.read())
        dataset = {
            "project": {"id": project_id},
            "table": {"id": table_id},
            "record": {
                column_name: {
                    "name": document_title,
                    "extension": ext,
                    "data": encoded_file.decode("utf-8"),
                }
            },
            "session": {"id": session},
        }
        # print(dataset)
        res = self._make_api_request(path, "PUT", dataset)
        # print(res)
        if "id" in res:
            return res
        elif "message" in res:
            return res["message"]
        else:
            return "Error"

    def download_document(
        self,
        project_id: str,
        table_id: str,
        document_id: str,
        file_location: str,
        file_name: str = None,
    ):
        """Download a document. Specify save location and filename"""
        path = "record/document/{}".format(document_id)
        response = self._make_api_request(path, "GET", {"project[id]": project_id, "table[id]": table_id}, "")
        if "file" in response:
            if file_name is None:
                file_name = "{}.{}".format(response["name"], response["extension"])
            content = base64.b64decode(response["file"])
            try:
                file = open("{}/{}".format(file_location, file_name), "wb+")
                file.write(content)
                file.close()
                return {"file": "{}/{}".format(file_location, file_name)}
            except Exception as ex:
                print("Error saving file: {}".format(ex))
                return False
        else:
            return False

    # tasks

    ## new -> license recommended
    def tasks_read(
        self,
        license: str = "",
        project_id: str = "",
        status: str = "",
        user: str = "",
        today: bool = False,
    ) -> list:
        """Get tasks"""
        depreciationMessage("param", "status", "01-02-2023", "taken")

        # license = selectLicense(license, self._licenses)
        path = "tasks?filter[license]={}&filter[today]={}".format(license, int(today))
        filters = []
        if project_id != "":
            filters.append({"column": "project", "operator": "=", "values": [project_id]})
        if status != "":
            filters.append({"column": "status", "operator": "=", "values": [status]})
        if user != "":
            filters.append({"column": "assigned_to", "operator": "=", "values": [user]})
        return self._make_api_request(path, "POST", {"advanced_filters": filters})

    def task_create(
        self,
        project_id: str,
        name: str,
        description: str,
        status: str,
        due_date: str,
        assigned_user: str,
        start_date: str = "",
        appendix: object = {},
        license: str = "",
        end_date: str = "",
    ) -> dict:
        """Create a task in a project"""
        path = "task-create"
        license = selectLicense(license, self._licenses)
        depreciationMessage("param", "status", "01-02-2023", "taken")
        body = {
            # required
            "license": license,
            "project": project_id,
            "title": name,
            "assigned_to": assigned_user,
            "due": due_date,
            # optional
            "description": description,
            "planned_start": start_date,
            "planned_end": end_date,
        }
        if appendix != {}:
            print("add appendix")
        return self._make_api_request(path, "POST", body)

    def task_read(self, task_id: str) -> dict:
        """Get details of a task"""
        path = "tasks/{}".format(task_id)
        return self._make_api_request(path, "GET", {})

    def task_update_name(self, task_id: str, name: str) -> dict:
        """Update a task name"""
        path = "tasks/{}".format(task_id)
        return self._make_api_request(path, "PUT", {"title": name})

    def task_respond(
        self,
        task_id: str,
        response: str,
        assigned_user: str = "",
        status: str = "",
        due_date: str = "",
        appendix: object = {},
    ) -> dict:
        """Respond to a task"""
        path = "tasks/{}/message".format(task_id)

        # Depreciation messages -> Moved to update_task
        if assigned_user != "":
            depreciationMessage("param", "assigned_user", "01-03-2023", "taken")
            self.update_task(assigned_to=assigned_user)
        if status != "":
            # Status = closed?
            depreciationMessage("param", "status", "01-02-2023", "taken")
            # self.update_task(assigned_user=assigned_user)
        if due_date != "":
            depreciationMessage("param", "due_date", "01-03-2023", "taken")
            self.update_task(due_date=due_date)
        if appendix != {}:
            depreciationMessage("param", "due_date", "01-03-2023", "taken")

        return self._make_api_request(path, "POST", {"message": response})

    def task_close(self, task_id: str):
        path = "tasks/{}/close".format(task_id)

        return self._make_api_request(path, "POST")

    def task_cancel(self, task_id: str):
        path = "tasks/{}/cancel".format(task_id)

        return self._make_api_request(path, "POST")

    def update_task(
        self,
        task_id: str,
        title: str = "",
        description: str = "",
        priority: str = "",
        planned_start: str = "",
        planned_end: str = "",
        assigned_to: str = "",
        due_date: str = "",
        sbs_code: str = "",
    ) -> dict:
        """update a task info"""
        path = "tasks/{}".format(task_id)
        body = {}
        if title != "":
            body["title"] = title
        if description != "":
            body["description"] = description
        if priority != "":
            body["priority"] = priority
        if planned_start != "":
            body["planned_start"] = planned_start
        if planned_end != "":
            body["planned_end"] = planned_end
        if assigned_to != "":
            body["assigned_to"] = assigned_to
        if due_date != "":
            body["due_date"] = due_date
        if sbs_code != "":
            body["sbs_code"] = sbs_code

        return self._make_api_request(path, "PUT", body)

    def task_upload_appendix(self, task_id: str, appendix: dict):
        path = "tasks/{}/appendixes".format(task_id)
        return self._make_api_request(path, "POST", appendix)

    def task_message_create(self, task_id: str, message: str):
        path = "tasks/{}/messages".format(task_id)
        return self._make_api_request(path, "POST", {"message": message})

    def task_delete(self, task_id: str) -> dict:
        """Delete a task"""
        path = "tasks/{}".format(task_id)
        return self._make_api_request(path, "DELETE", {})

    def task_getJob(self, project_id: str, task_id: str) -> dict:
        """Get the job associated to the given task"""
        path = "project/{}/task/{}/job".format(project_id, task_id)
        return self._make_api_request(path, "GET", {})

    ## CustomFunctions
    def record_update_withdocument(
        self,
        project_id: str,
        table_id: str,
        record_id: str,
        updated_record_values: dict,
        document_column_name: str,
        document_location,
        document_title: str = None,
    ) -> dict:
        """Update record with a document"""
        path = "record/{}".format(record_id)
        if document_title is None:
            document_title = document_location.split("/")[-1]
        ext = document_location.split(".")[-1]
        with open(document_location, "rb") as image_file:
            encoded_file = base64.b64encode(image_file.read())
            updated_record_values[document_column_name] = {
                "name": document_title,
                "extension": ext,
                "data": encoded_file.decode("utf-8"),
            }
        return self._make_api_request(
            path,
            "PUT",
            {
                "project": {"id": project_id},
                "table": {"id": table_id},
                "record": updated_record_values,
            },
        )

    def create_virtual_csv(self, records: list):
        """Not for use. Create a virtual CSV of records"""
        encoded_csv = ",".join(records[0].keys()) + "\n"
        for record in records:
            recs = []
            for key in record.keys():
                recs.append(record[key])
            encoded_csv += '"' + '","'.join(recs) + '"\n'
        return encoded_csv

    def create_virtual_csv_Addid(self, records: list):
        """Not for use. Create a virtual CSV of records"""
        encoded_csv = "id," + ",".join(records[0].keys()) + "\n"
        for record in records:
            recs = []
            for key in record.keys():
                recs.append(str(record[key]))
            encoded_csv += "," + ",".join(recs) + "\n"
        return encoded_csv

    def parse_document(self, documentLocation, documentTitle: str = None):
        """Parse a document to the ANT Format."""
        if documentTitle is None:
            documentTitle = documentLocation.split("/")[-1]
        ext = documentTitle.split(".")[-1]
        with open(documentLocation, "rb") as image_file:
            encoded_file = base64.b64encode(image_file.read())
        document = {
            "name": documentTitle.replace(f".{ext}", ""),
            "extension": ext,
            "data": encoded_file.decode("utf-8"),
        }
        return document

    def parse_date(self, year: int, month: int, day: int, hour: int, minute: int, seconds: int):
        """Parse a date to the ANT Format."""
        date = str(year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + seconds)
        return date

    def task_download(self, task_id: str, document_id: str, file_location: str, file_name: str = None):
        """Download a document. Specify save location and filename"""
        path = "task/document/{}".format(document_id)
        response = self._make_api_request(path, "GET", {"task[id]": task_id})
        if "file" in response[0]:
            if file_name is None:
                file_name = "{}.{}".format(response[0]["name"], response[0]["extension"])
            content = base64.b64decode(response[0]["file"])
            try:
                file = open("{}/{}".format(file_location, file_name), "wb+")
                file.write(content)
                file.close()
                return True
            except Exception as ex:
                print("Error saving file: {}".format(ex))
                return False

    def job_finish(self, project_id: str, job_id: str) -> dict:
        """Finish job (workflow task)"""
        path = "project/{}/job/{}/finish".format(project_id, job_id)
        return self._make_api_request(path, "POST", {})

    # SBS Codes
    def sbs_codes(self, project_id: str) -> dict:
        """Get all SBS codes"""
        path = "project/{}/sbs".format(project_id)
        return self._make_api_request(path, "GET", {})

    def sbs_getTree(self, project_id: str) -> dict:
        """Get SBS first objects in tree"""
        path = "project/{}/sbs-tree".format(project_id)
        return self._make_api_request(path, "GET", {})

    def sbs_search(self, project_id: str, value: str) -> dict:
        """Search sbs objects by code or label"""
        path = "project/{}/sbs-search?value={}".format(project_id, value)
        return self._make_api_request(path, "GET", {})

    def sbs_addCode(self, project_id: str, code: str, parentCode: str = "", label: str = "") -> dict:
        """Add SBS Code"""
        path = "project/{}/sbs".format(project_id)
        return self._make_api_request(path, "POST", {"code": code, "parent": parentCode, "label": label})

    def sbs_updateParent(self, project_id: str, sbsId: str, parent: str) -> dict:
        """Update the parent of the SBSCode"""
        path = "project/{}/sbs/{}".format(project_id, sbsId)
        return self._make_api_request(path, "PUT", {"parent": parent})

    def sbs_updateLabel(self, project_id: str, sbsId: str, label: str) -> dict:
        """Update the label of the SBS Code"""
        path = "project/{}/sbs/{}".format(project_id, sbsId)
        return self._make_api_request(path, "PUT", {"label": label})

    def sbs_removeCode(self, project_id: str, sbsId: str) -> dict:
        """Remove the SBSCode"""
        path = "project/{}/sbs/{}".format(project_id, sbsId)
        return self._make_api_request(path, "DELETE", {})

    def sbs_import(self, project_id: str, records: list) -> dict:
        """Create multiple sbs records into a table"""
        path = "project/{}/sbs-import".format(project_id)
        encoded_csv = base64.b64encode(self.create_virtual_csv_Addid(records).encode("utf-8"))
        result = self._make_api_request(path, "POST", {"records": encoded_csv.decode("utf-8")})
        return result

    def sbs_children(self, project_id: str, sbs_id: str) -> dict:
        """Get SBS Object children"""
        path = "project/{}/sbs/{}/children".format(project_id, sbs_id)
        return self._make_api_request(path, "GET", {})

    def sbs_multi_delete(self, project_id: str, records: list) -> dict:
        """Delete multiple sbs records from table"""
        path = "project/{}/sbs".format(project_id)
        body = {"records": records}
        result = self._make_api_request(path, "DELETE", delete_data=body)
        return result

    # WorkFlows
    def project_workflows(self, project_id: str) -> dict:
        """Get all workflows in  project"""
        path = "project/{}/workflows".format(project_id)
        return self._make_api_request(path, "GET", {})

    def project_workflows_inLicense(self, project_id: str) -> dict:
        """Returns the workflows which are in project license"""
        path = "project/{}/workflows/inLicense".format(project_id)
        return self._make_api_request(path, "GET", {})

    def project_workflow_details(self, project_id: str, projectWorkflowId: str) -> dict:
        """Returns the project workflow relation"""
        path = "project/{}/workflow/{}".format(project_id, projectWorkflowId)
        return self._make_api_request(path, "GET", {})

    def project_workflow_add(self, project_id: str, workflow_id: str, name: str) -> dict:
        """Adds a project workflow relation"""
        path = "project{}/wokrflow"
        body = {
            "project": {"id": project_id},
            "workflow": {"id": workflow_id},
            "name": "name",
        }
        return self._make_api_request(path, "POST", body)

    def project_workflow_delete(self, project_id: str, workflow_id: str) -> dict:
        """Delete a workflow from a project"""
        path = "project/{}/workflow/{}"
        return self._make_api_request(path, "DELETE", "")

    # Sessions
    def project_sessions(self, project_id: str, sbsId: str) -> dict:
        """Get Project Sessions"""
        path = "project/{}/sessions".format(project_id)
        return self._make_api_request(path, "GET", {})

    def workflow_sessions(self, project_id: str, session_id: str) -> dict:
        """Workflow sessions"""
        path = "project/{}/sessions/{}".format(project_id, session_id)
        return self._make_api_request(path, "GET", {})

    def workflow_createSession(self, project_id: str, workflow_id: str, name: str, sbs_code: str = "") -> dict:
        """Workflow sessions"""
        path = "project/{}/session".format(project_id)
        return self._make_api_request(path, "POST", {"name": name, "workflow": workflow_id, "sbs_code": sbs_code})

    def workflow_sessionUpdateName(self, project_id: str, session_id: str, name: str) -> dict:
        """Workflow sessions"""
        path = "project/{}/session/{}".format(project_id, session_id)
        return self._make_api_request(path, "PUT", {"name": name})

    def workflow_sessionUpdateSBS(self, project_id: str, session_id: str, sbs_code: str) -> dict:
        """Workflow sessions"""
        path = "project/{}/session/{}".format(project_id, session_id)
        return self._make_api_request(path, "PUT", {"sbs_code": sbs_code})

    def workflow_sessionDelete(self, project_id: str, session_id: str) -> dict:
        """Workflow sessions"""
        path = "project/{}/session/{}".format(project_id, session_id)
        return self._make_api_request(path, "DELETE", {})


# UTILS
class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def link(uri, label=None):
    """Private function"""
    if label is None:
        label = uri
    parameters = ""

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST
    escape_mask = "\033]8;{};{}\033\\{}\033]8;;\033\\"

    return escape_mask.format(parameters, uri, bcolors.OKBLUE + label + bcolors.ENDC)


def selectLicense(license, licenses):
    if license == "":
        selectedLicenseName = licenses[0]["name"]
        URL = link("https://docs.antcde.io/antconnect/python/#taken", "documentation")
        if len(licenses) > 1:
            print(
                bcolors.WARNING
                + "Warning"
                + bcolors.ENDC
                + ": No license provided. A random license ("
                + bcolors.OKGREEN
                + "{}".format(selectedLicenseName)
                + bcolors.ENDC
                + ") is selected to handle the tasks. Please specify which license you are using, see {}".format(URL)
            )
        else:
            print(
                bcolors.OKBLUE
                + "Info"
                + bcolors.ENDC
                + ": You didn't provided a license. Since you have only one license ("
                + bcolors.OKGREEN
                + "{}".format(selectedLicenseName)
                + bcolors.ENDC
                + "), this is automatically selected. Advised to add it, see {} ".format(URL)
            )
        return licenses[0]
    else:
        return license


def depreciationMessage(type, name, date, doc):
    URL = link("https://docs.antcde.io/antconnect/python/#{}".format(doc), "documentation")
    if type == "param":
        print(
            bcolors.WARNING
            + "Warning"
            + bcolors.ENDC
            + ': The parameter: "{}" will be been depreciated from {}. Please update according to {}'.format(
                name, date, URL
            )
        )
    if type == "def":
        print(
            bcolors.WARNING
            + "Warning"
            + bcolors.ENDC
            + ": The function {} will be been depreciated from {}. Please update according to {}".format(
                name, date, URL
            )
        )

    # Monitor the use of depreciated functions?
    # If depreciation date is soon, inform?


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    s = re.sub(r"^-+|-+$", "", s)
    return s
