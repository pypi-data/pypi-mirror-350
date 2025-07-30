from batch_pipeline_classes.BaseProcessor import BaseProcessor
from google.cloud.bigquery import Client, WriteDisposition, QueryJobConfig


class GCPProcessor(BaseProcessor):

    def __init__(self, project_id, region, dataset_id):
        self.project_id = project_id
        self.region = region
        self.dataset_id = dataset_id
        self.bq_client = Client(
            project = self.project_id,
            location = self.region
        )


    def prepare_auto_increment_data(self, data):
        pass

    def write_to_db(self, data:dict, table_name, mode=""):

        mode = mode.strip().lower()
        wd = WriteDisposition.WRITE_APPEND

        if mode == "overwrite":
            wd = WriteDisposition.WRITE_TRUNCATE

        query = '''
        INSERT INTO {self.dataset_id}.{table_name}
        ({",".join(data.keys()})
        VALUES ({",".join(data.values()})
        '''

        query_job = self.bq_client.query(
            query,
            job_config=QueryJobConfig(
                 write_disposition = wd
            )
        )

        job_done = False
        while not job_done:
            job_done = query_job.done()

        return job_done


    def read_from_db(self, query):

        query_job = self.bq_client.query(query)
        query_result = query_job.result()

        rows_list = []

        for row in query_result:
            row_dict = {}
            for key, val in row.items():
                row_dict[key] = val

            rows_list.append(row_dict)

        return rows_list

    def execute_sql(self, sql_statement: str):

        query_job = self.bq_client.query(sql_statement)
        job_done = False
        while not job_done:
            job_done = query_job.done()

        return job_done

    # def execute_stored_procedure(self, name:str):
    #     stored_procedure_query = f"CALL {self.dataset_id}.{name}()"
    #     query_job = self.bq_client.query(stored_procedure_query)
    #
    #     job_done = False
    #     while not job_done:
    #         job_done = query_job.done()
    #
    #     return job_done
    @staticmethod
    def process_contest(
            contest,
            from_date = None,
            to_date = None,
            amount_of_contests = 40
    ):

        min_id = contest["max_index"] - amount_of_contests

        # Initial Run
        # if initial and contest["id"] > min_id \
        #     and contest["phase"] == "FINISHED" \
        #     and self.translate_unix_to_timestamp(contest["startTimeSeconds"] + contest["durationSeconds"]).date() < to_date:
        if from_date is None:
            contest_start_time = BaseProcessor.translate_unix_to_timestamp(contest["startTimeSeconds"])
            contest_end_time = BaseProcessor.translate_unix_to_timestamp(contest["startTimeSeconds"] + contest["durationSeconds"])

            if contest["id"] > min_id \
                and contest["phase"] == "FINISHED" \
                and contest_end_time.date() < to_date:
                    return {
                        "id": contest["id"],
                        "name": contest["name"],
                        "start": contest_start_time,
                        "end": contest_end_time,
                        "duration": contest["durationSeconds"],
                        "type": contest["type"]
                    }

        # Manual Parameters provided
        elif from_date is not None and to_date is not None:
            contest_start_time = BaseProcessor.translate_unix_to_timestamp(contest["startTimeSeconds"])
            contest_end_time = BaseProcessor.translate_unix_to_timestamp(contest["startTimeSeconds"] + contest["durationSeconds"])
            if (
                    from_date <= contest_end_time.date() < to_date
                    and contest["phase"] == "FINISHED"
                    and contest["id"] > min_id
            ):

                return {
                    "id": contest["id"],
                    "name": contest["name"],
                    "start": contest_start_time,
                    "end": contest_end_time,
                    "duration": contest["durationSeconds"],
                    "type": contest["type"]
                }
        # else:
        #     raise Exception("Incorrect combination of attributes for loading contests!")

        # self.write_to_db(data=lst_of_rows, mode="overwrite", table_name = "contest_stg")
        #
        # return [row[0] for row in lst_of_rows]
        return {}

    @staticmethod
    def extract_submissions(contest_id):
        sumbissions = BaseProcessor.establish_connection("https://codeforces.com/api/contest.status", contestId=str(contest_id))
        contest_sumbissions = [
            {
                "id": subm["id"],
                "timestamp": BaseProcessor.translate_unix_to_timestamp(subm["creationTimeSeconds"]),
                "id_contest": subm["contestId"],
                "id_problem": str(subm["problem"]["contestId"]) + "/" + str(subm["problem"]["index"]),
                "problem_name": subm["problem"]["name"],
                "tags": ",".join(subm["problem"]["tags"]),
                "author": subm["author"]["members"][0].get("handle", "unknown") if subm["author"]["members"] else "unknown",
                "programming_language": subm["programmingLanguage"],
                "verdict": subm["verdict"],
                "time_consumed": subm["timeConsumedMillis"],
                "memory_usage": subm["memoryConsumedBytes"]
            }

            for subm in sumbissions
        ]

        print("Submissions Extracted!")
        return contest_sumbissions

    @staticmethod
    def extract_users(rows):
        unique_names_string = ";".join(rows)

        raw_rows = BaseProcessor.establish_connection("https://codeforces.com/api/user.info", handles=unique_names_string)

        unpacked_rows = [
            {
                "country": raw_row.get("country", "unknown"),
                "rating": raw_row.get("rating", 0),
                "nickname": raw_row["handle"],
                "title": raw_row.get("rank", "none"),
                "registration_date": BaseProcessor.translate_unix_to_timestamp(raw_row["registrationTimeSeconds"])
            }
            for raw_row in raw_rows
        ]

        return unpacked_rows
