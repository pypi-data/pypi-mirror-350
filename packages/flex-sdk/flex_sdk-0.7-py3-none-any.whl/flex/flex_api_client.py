import requests
import base64
import datetime
from datetime import datetime, timedelta
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from flex.flex_objects import Action, WorkflowDefinition, User, Collection, Item, Asset, Workflow, Job, UserDefinedObject, Keyframe, JobConfiguration, Annotation, Taxonomy, Taxon
import concurrent.futures
from functools import partial
import time 
import urllib.parse
import re

# Increase default recursion limit (from 999 to 1500)
# See : https://stackoverflow.com/questions/14222416/recursion-in-python-runtimeerror-maximum-recursion-depth-exceeded-while-callin
# max_number_of_objects_to_retrieve = limit * recursion_limit
sys.setrecursionlimit(1500)

class FlexApiClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        
        # Prepare basic authentication header
        credentials = f"{username}:{password}"
        base64_encoded_credentials = base64.b64encode(credentials.encode())
        auth_header = {'Authorization': f'Basic {base64_encoded_credentials.decode()}'}

        # Set Content-Type header and combine with additional headers
        self.headers = {
            'Content-Type': 'application/vnd.nativ.mio.v1+json',
            **auth_header,
        }
    
    def get_actions(self, filters = None):
        """Get Actions."""
        endpoint = f"/actions"
        if filters:
            endpoint += f";{filters}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            action_list = [Action(action) for action in response.json().get('actions', [])]
            return action_list
        except requests.RequestException as e:
            raise Exception(e)
    
    def get_action(self, actionId):
        """Get Action."""
        endpoint = f"/actions/{actionId}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            action = Action(response.json())
            return action
        except requests.RequestException as e:
            raise Exception(e)
        
    def get_workflow_definition(self, workflowDefinitionId):
        """Get Workflow Definition."""
        endpoint = f"/workflowDefinitions/{workflowDefinitionId}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            workflow_definition = WorkflowDefinition(response.json())
            return workflow_definition
        except requests.RequestException as e:
            raise Exception(e)
        
    def get_workflow_definitions(self, filters = None):
        """Get Workflow Definitions."""
        endpoint = f"/workflowDefinitions"
        if filters:
            endpoint += f";{filters}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            workflow_definition_list = [WorkflowDefinition(action) for action in response.json().get('workflowDefinitions', [])]
            return workflow_definition_list
        except requests.RequestException as e:
            raise Exception(e)
        
    def get_user(self, userId):
        """Get User."""
        endpoint = f"/users/{userId}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            user = User(response.json())
            return user
        except requests.RequestException as e:
            raise Exception(e)
        
    def get_users(self, filters = None):
        """Get Users."""
        endpoint = f"/users"
        if filters:
            endpoint += f";{filters}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            user_list = [User(action) for action in response.json().get('users', [])]
            return user_list
        except requests.RequestException as e:
            raise Exception(e)
        
    def create_action(self, name, type, pluginClass, pluginUuid, visibilityIds, additional_param):
        """Create a new action."""
        # Mandatory fields : name, type, pluginClass, visibilityIds
        endpoint = "/actions"
        try:
            payload = {
                        'name': name,
                        'type': type,
                        'pluginClass': pluginClass,
                        'pluginUuid': pluginUuid,
                        'visibilityIds': visibilityIds
                      }
            
            for param_name, param_value in additional_param.items():
                payload[param_name] = param_value
            
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            action = Action(response.json())
            return action
        except requests.RequestException as e:
            raise Exception(e)
        
    def create_workflow(self, payload):
        endpoint = f"/workflows"
        try:
            response = requests.post(self.base_url + endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            return Workflow(response.json())
        except requests.RequestException as e:
            raise Exception(e)
    
    def get_collections(self, filters = None) -> list[Collection]:
        """Get Collections."""
        endpoint = f"/collections"
        if filters:
            endpoint += f";{filters}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            collection_list = [Collection(collection) for collection in response.json().get('collections', [])]
            return collection_list
        except requests.RequestException as e:
            raise Exception(e)
        
    def get_collection(self, collection_uuid) -> Collection:
        """Get Collections."""
        endpoint = f"/collections/{collection_uuid}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            collection = Collection(response.json())
            return collection
        except requests.RequestException as e:
            raise Exception(e)
        
    def get_collection_items(self, collection_uuid, offset=0) -> list[Item]:
        """Get Collections Items."""
        limit = 100
        endpoint = f"/collections/{collection_uuid}/items?limit={limit}&offset={offset}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            item_list = [Item(item) for item in response.json()["items"]]
            total_results = response.json()['totalResults']
            if (total_results > limit + offset):
                item_list.extend(self.get_collection_items(collection_uuid, offset + limit))

            return item_list
        except requests.RequestException as e:
            raise Exception(e)
        
    def update_collection_items(self, collection_uuid, item_list):
        """Update Collections Items."""
        endpoint = f"/collections/{collection_uuid}/items"
        try:
            items = []
            for item in item_list:
                item_json = {"id": item.id, "type": item.type}
                if (item.in_timecode):
                    item_json["in"] = item.in_timecode
                if (item.out_timecode):
                    item_json["out"] = item.out_timecode
                if (item.item_name):
                    item_json["itemName"] = item.item_name
                items.append(item_json)
            payload = {"items": items}
            print(payload)
            response = requests.put(self.base_url + endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(e)
        
    def delete_items_from_collection(self, collection_uuid, item_list):
        """Delete Items from Collection."""
        endpoint = f"/collections/{collection_uuid}/items"
        try:
            items_to_delete = []
            for item in item_list:
                items_to_delete.append(str(item.item_key))
            payload = {"itemKeys": items_to_delete}
            response = requests.delete(self.base_url + endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(e)
        
    def get_collection_metadata(self, collection_uuid, ):
        """Get Collection Metadata."""
        endpoint = f"/collections/{collection_uuid}/metadata"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(e)
        
    def update_collection_metadata(self, collection_uuid, metadata, metadata_definition_entity_id):
        """Update Collection Metadata."""
        endpoint = f"/collections/{collection_uuid}/metadata/{metadata_definition_entity_id}"
        try:
            response = requests.put(self.base_url + endpoint, json=metadata, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(e)
        
    def get_asset(self, asset_id, include_metadata = False):
        endpoint = f"/assets/{asset_id};includeMetadata={include_metadata}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            asset = Asset(response.json())
            return asset
        except requests.RequestException as e:
            raise Exception(e)

    def update_asset(self, asset_id, payload):
        endpoint = f"/assets/{asset_id}"
        try:
            response = requests.put(self.base_url + endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            asset = Asset(response.json())
            return asset
        except requests.RequestException as e:
            raise Exception(e)
        
    def get_asset_workflows(self, asset_id):
        endpoint = f"/assets/{asset_id}/workflows"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            asset = [Workflow(workflow) for workflow in response.json()["workflows"]]
            return asset
        except requests.RequestException as e:
            raise Exception(e)
        
    def get_asset_metadata(self, asset_id):
        endpoint = f"/assets/{asset_id}/metadata"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()["instance"]
        except requests.RequestException as e:
            raise Exception(e)
        
    def set_asset_metadata(self, asset_id, metadata):
        endpoint = f"/assets/{asset_id}/metadata"
        try:
            response = requests.put(self.base_url + endpoint, json=metadata, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(e)
        
    def get_assets(self, filters, offset = 0):
        limit = 100
        endpoint = f"/assets;offset={offset};limit={100}"
        if filters:
            endpoint += f";{filters}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            asset_list = [Asset(asset) for asset in response_json["assets"]]
            total_results = response_json["totalCount"]
            if (total_results > offset + limit):
                asset_list.extend(self.get_assets(filters, offset + limit))
            return asset_list
        except requests.RequestException as e:
            raise Exception(e)
        
    def get_annotations(self, asset_id, offset = 0):
        limit = 100
        endpoint = f"/assets/{asset_id}/annotations;offset={offset};limit={100}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            annotation_list = [Annotation(asset) for asset in response_json["annotations"]]
            total_results = response_json["totalCount"]
            if (total_results > offset + limit):
                annotation_list.extend(self.get_annotations(asset_id, offset + limit))
            return annotation_list
        except requests.RequestException as e:
            raise Exception(e)

    def get_annotations_by_filters(self, asset_id, filters, offset = 0):
        limit = 100
        endpoint = f"/assets/{asset_id}/annotations;{filters};offset={offset};limit={100}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            annotation_list = [Annotation(asset) for asset in response_json["annotations"]]
            total_results = response_json["totalCount"]
            if (total_results > offset + limit):
                annotation_list.extend(self.get_annotations_by_filters(asset_id, filters, offset + limit))
            return annotation_list
        except requests.RequestException as e:
            raise Exception(e)
        
    def set_annotation_metadata(self, asset_id, annotation_id, metadata):
        endpoint = f"/assets/{asset_id}/annotations/{annotation_id}"
        try:
            payload = {
                "metadataAnnotation": {
                    "metadata": metadata
                }
            }
            response = requests.put(self.base_url + endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            return response_json
        except requests.RequestException as e:
            raise Exception(e)
        
    def delete_annotations(self, asset_id, originator_context, originator_correlation_id):
        endpoint = f"/assets/{asset_id}/annotations"
        try:
            payload = {
                        'originatorContext': originator_context,
                        'originatorCorrelationId': originator_correlation_id
                      }
            response = requests.delete(self.base_url + endpoint, json=payload,headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(e)
        
    def get_workflow_instance(self, workflow_id, include_variables = "false"):
        endpoint = f"/workflows/{workflow_id};includeVariables={include_variables}"
        try:
            response = requests.get(self.base_url + endpoint,headers=self.headers)
            response.raise_for_status()
            workflow = Workflow(response.json())
            return workflow
        except requests.RequestException as e:
            raise Exception(e)
        
    def delete_annotation(self, annotation_id):
        endpoint = f"/assets/annotations/{annotation_id}"
        try:
            response = requests.delete(self.base_url + endpoint,headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(e)
        
    def get_workflow_instance(self, workflow_id, include_variables = "false"):
        endpoint = f"/workflows/{workflow_id};includeVariables={include_variables}"
        try:
            response = requests.get(self.base_url + endpoint,headers=self.headers)
            response.raise_for_status()
            workflow = Workflow(response.json())
            return workflow
        except requests.RequestException as e:
            raise Exception(e)

    def get_job(self, job_id):
        endpoint = f"/jobs/{job_id}"
        try:
            response = requests.get(self.base_url + endpoint,headers=self.headers)
            response.raise_for_status()
            job = Job(response.json())
            return job
        except requests.RequestException as e:
            raise Exception(e)

    def fetch_job_page(self, filters, offset):
        limit = 100
        endpoint = f"/jobs;offset={offset};limit={limit}"
        if filters:
            endpoint += f";{filters}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Error fetching assets at offset {offset}: {e}")

    def get_jobs(self, filters):
        print("Fetching first page of jobs...")
        first_page = self.fetch_job_page(filters, 0)
        total_results = first_page["totalCount"]
        jobs = [Job(job) for job in first_page["jobs"]]
        print(f"Total jobs to fetch: {total_results}")
        print(f"Fetched first 100 jobs. Fetching remaining {total_results - 100} jobs in parallel...")

        start_time = time.time()
        fetched_count = 100

        with concurrent.futures.ThreadPoolExecutor() as executor:
            offsets = range(100, total_results, 100)
            fetch_func = partial(self.fetch_job_page, filters)
            future_to_offset = {executor.submit(fetch_func, offset): offset for offset in offsets}
            
            for future in concurrent.futures.as_completed(future_to_offset):
                offset = future_to_offset[future]
                try:
                    data = future.result()
                    new_jobs = [Job(job) for job in data["jobs"]]
                    jobs.extend(new_jobs)
                    fetched_count += len(new_jobs)
                    
                    # Print progress
                    progress = fetched_count / total_results
                    elapsed_time = time.time() - start_time
                    estimated_total_time = elapsed_time / progress if progress > 0 else 0
                    remaining_time = estimated_total_time - elapsed_time
                    print(f"Fetched jobs: {fetched_count}/{total_results} ({progress:.2%}) - "
                          f"Elapsed: {elapsed_time:.2f}s - Estimated remaining: {remaining_time:.2f}s")
                except Exception as e:
                    print(f"Error fetching jobs at offset {offset}: {e}")

        total_time = time.time() - start_time
        print(f"Finished fetching all jobs in {total_time:.2f} seconds")
        print(f"Total jobs fetched: {len(jobs)}")

        return jobs
        
    def get_job_configuration(self, job_id):
        endpoint = f"/jobs/{job_id}/configuration"
        try:
            response = requests.get(self.base_url + endpoint,headers=self.headers)
            response.raise_for_status()
            job_configuration = response.json()["instance"]
            return job_configuration
        except requests.RequestException as e:
            raise Exception(e)
        
    def get_job_history(self, job_id):
        endpoint = f"/jobs/{job_id}/history"
        try:
            response = requests.get(self.base_url + endpoint,headers=self.headers)
            response.raise_for_status()
            job_history = response.json()
            return job_history
        except requests.RequestException as e:
            raise Exception(e)
        
    def set_job_configuration(self, job_id, job_configuration):
        endpoint = f"/jobs/{job_id}/configuration"
        try:
            response = requests.put(self.base_url + endpoint, json=job_configuration, headers=self.headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise Exception(e)
        
    def retry_job(self, jobId):
        """Retry a job."""
        endpoint = f"/jobs/{jobId}/actions"
        try:
            jobStatus = self.get_job(jobId).status

            if jobStatus != "Failed":
                raise Exception(f"Couldn't retry the job as it is not Failed, its status is : {jobStatus}")

            payload = {
                        'action': 'retry'
                    }
            
            print(f"Retrying job ID {jobId}")
            response = requests.post(self.base_url + endpoint, json=payload, headers=self.headers)
            response.raise_for_status()

            return response.json()
        except requests.RequestException as e:
            print(f"Couldn't retry job ID {jobId} :", e)
            pass

    def cancel_job(self, job_id):
        """Cancel a job."""
        endpoint = f"/jobs/{job_id}/actions"
        try:
            job = self.get_job(job_id)
            job_status = job.status

            if job_status != "Failed":
                print(f"Couldn't cancel the job as it is not Failed, its status is : {job_status}")
                return job
            else:
                payload = {
                        'action': 'cancel'
                    }
                response = requests.post(self.base_url + endpoint, json=payload, headers=self.headers)
                response.raise_for_status()
                print(f'Job ID {job_id} has been cancelled!')
                return job
        except requests.RequestException as e:
            print(f"POST request error: {e}")
            return None
        
    def get_workflow(self, workflow_id):
        """Get a workflow."""
        endpoint = f"/workflows/{workflow_id}"
        try:
                
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            workflow = Workflow(response.json())
            return workflow
        except requests.RequestException as e:
            raise Exception(e)

    def get_workflow_variables(self, workflow_id):
        """Get workflow variables."""
        endpoint = f"/workflows/{workflow_id}/variables"
        try:
                
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(e)

    def cancel_workflow(self, workflow_id):
        """Cancel a workflow."""
        endpoint = f"/workflows/{workflow_id}/actions"
        try:
            workflow = self.get_workflow(workflow_id)
            status = workflow.status

            if status != "Failed":
                print(f"Couldn't cancel the workflow ID {workflow_id} as it is not Failed, its status is : {status}")
                return workflow
            else:
                payload = {
                            'action': 'cancel'
                        }
                    
                response = requests.post(self.base_url + endpoint, json=payload, headers=self.headers)
                response.raise_for_status()
                workflow = Workflow(response.json())
                print(f'Workflow ID {workflow_id} has been cancelled!')
                return workflow
        except requests.RequestException as e:
            print(f"POST request error: {e}")
            return None

    def get_object(self, plural_name, object_id):
        endpoint = f"/{plural_name}/{object_id}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            user_defined_object = UserDefinedObject(response.json())
            return user_defined_object
        except requests.RequestException as e:
            raise Exception(e)
        
    def get_objects(self, plural_name, filters, offset = 0):
        limit = 100
        endpoint = f"/assets;offset={offset};limit={100}"
        if filters:
            endpoint += f";{filters}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            object_list = [Asset(asset) for asset in response_json["objects"]]
            total_results = response_json["totalCount"]
            if (total_results > offset + limit):
                object_list.extend(self.get_objects(plural_name, filters, offset + limit))
            return object_list
        except requests.RequestException as e:
            raise Exception(e)
        
    def get_object_data(self, plural_name, object_id):
        endpoint = f"/{plural_name}/{object_id}/data"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()["instance"]
        except requests.RequestException as e:
            raise Exception(e)
        
    def set_object_data(self, plural_name, object_id, metadata):
        endpoint = f"/plural_name/{object_id}/data"
        try:
            response = requests.put(self.base_url + endpoint, json=metadata, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(e)

    def get_asset_keyframes(self, asset_id, offset = 0):
        limit = 100
        endpoint = f'/assets/{asset_id}/keyframes;offset={offset};limit={limit}'
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            keyframe_list = [Keyframe(keyframe) for keyframe in response.json()["keyframes"]]
            total_results = response_json["totalCount"]
            if (total_results > offset + limit):
                keyframe_list.extend(self.get_asset_keyframes(asset_id, offset + limit))
            return keyframe_list
        except requests.RequestException as e:
            raise Exception(e)

    def get_asset_children(self, asset_id, filters = None, offset = 0):
        limit = 100
        endpoint = f'/assets/{asset_id}/children;offset={offset};limit={limit}'
        if filters:
            endpoint += ';' + filters
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            asset_list = [Asset(child) for child in response.json()["assets"]]
            total_results = response_json["totalCount"]
            if (total_results > offset + limit):
                asset_list.extend(self.get_asset_children(asset_id, filters, offset + limit))
            return asset_list
        except requests.RequestException as e:
            raise Exception(e)

    def delete_asset_keyframe(self, asset_id, keyframe_id):
        endpoint = f'/assets/{asset_id}/keyframes/{keyframe_id}'
        try:
            response = requests.delete(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            return
        except requests.RequestException as e:
            raise Exception(e)
        
    def get_asset_keyframes_number(self, asset_id):
        endpoint = f'/assets/{asset_id}/keyframes;limit=1'
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            total_results = response_json["totalCount"]
            return total_results
        except requests.RequestException as e:
            raise Exception(e)
        
    def create_asset(self, payload):
        """Create a new asset."""
        endpoint = "/assets"
        try:
            response = requests.post(self.base_url + endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            asset = Asset(response.json())
            return asset
        except requests.RequestException as e:
            raise Exception(e)
        
    def create_job(self, payload):
        """Create a new job."""
        endpoint = "/jobs"
        try:
            response = requests.post(self.base_url + endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            job = Job(response.json())
            return job
        except requests.RequestException as e:
            raise Exception(e)


    def get_assets_by_filters(self, filters, offset = 0, pagination=False, createdFrom=None, createdTo=None, pagination_delta_in_days=None):
        """Get assets."""
        """Supports the offset until 10000 results, and pagination on created dates if it is required (metadata filters)."""
        # Set variables
        limit = 100
        if not pagination_delta_in_days:
            pagination_delta_in_days = 10

        # End condition
        if createdFrom and datetime.now() < datetime.strptime(createdFrom, '%d %b %Y'):
            # if current_datetime < createdFromAsDate
            # createdFrom date cannot be a future date : return an empy list.
            parsed_current_date = datetime.now().strftime('%d %b %Y')
            print(f"createdFrom is later that the current date : createdFrom={createdFrom}, current_date={parsed_current_date}")
            # No asset can be found
            return []
        
        # Set up creation date filters for pagination in the endpoint
        if createdFrom and createdTo:
            endpoint = f"/assets;{filters};offset={offset};createdFrom={createdFrom};createdTo={createdTo}"
        else:
            endpoint = f"/assets;{filters};offset={offset}"

        # Retrieve assets
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            response_assets = response_json["assets"]
            total_results = response_json["totalCount"]

            # print(f"Found {total_results} assets with filters {filters}, offset {offset}, createdFrom {createdFrom}, createdTo {createdTo}")

            asset_list = []
            for asset in response_assets:
                if (asset["fileInformation"]["originalFileName"]):
                    flex_asset = Asset(asset)
                else:
                    flex_asset = Asset(asset)
                asset_list.append(flex_asset)

            if (total_results > 10000 and "metadata" in filters):
                # Activate pagination
                if "created" not in filters:
                    # if not createdTo is equivalent to if not pagination
                    if not pagination:
                        # Init created - 1st of Sept. 2023
                        from_date = datetime(2023, 9, 1)
                        createdFrom = from_date.strftime('%d %b %Y')
                        new_createdTo = from_date + timedelta(days=pagination_delta_in_days)
                        createdTo = new_createdTo.strftime('%d %b %Y')
                        asset_list.extend(self.get_assets_by_filters(filters, 0, True, createdFrom, createdTo))
                    else:
                        # if pagination and total_results > 10000, divide the pagination delta by 2
                        pagination_delta_in_days //= 2
                        print(f"Reducing the pagination delta to {pagination_delta_in_days}")
                        parsed_createdTo = datetime.strptime(createdTo, '%d %b %Y')
                        # Add days for the pagination
                        new_createdTo = parsed_createdTo - timedelta(days=pagination_delta_in_days)
                        createdTo = new_createdTo.strftime('%d %b %Y')
                        asset_list.extend(self.get_assets_by_filters(filters, 0, True, createdFrom, createdTo))
                else:
                    raise Exception("Unable to paginate on the creation date filters as there query already contains a creation date filter.")

            elif (total_results > offset + limit):
                # Set new offset
                asset_list.extend(self.get_assets_by_filters(filters, offset + limit, pagination, createdFrom, createdTo))
            elif pagination:
                # Set new pagination creation date filters
                createdFrom = createdTo
                parsed_date = datetime.strptime(createdTo, '%d %b %Y')
                # Add days for the pagination
                new_date = parsed_date + timedelta(days=pagination_delta_in_days)
                createdTo = new_date.strftime('%d %b %Y')
                asset_list.extend(self.get_assets_by_filters(filters, 0, True, createdFrom, createdTo))

            return asset_list
        except requests.RequestException as e:
            raise Exception(e)
        
    def get_metadata_definition_fields(self, metadata_definition_id):
        endpoint = f'/metadataDefinitions/{metadata_definition_id}/definition'
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            return response_json
        except requests.RequestException as e:
            raise Exception(e)

    def fetch_assets_page(self, filters, offset):
        limit = 100
        endpoint = f"/assets;offset={offset};limit={limit}"
        if filters:
            endpoint += f";{filters}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Error fetching assets at offset {offset}: {e}")

    def get_assets_parallel(self, filters):
        print("Fetching first page of assets...")
        first_page = self.fetch_assets_page(filters, 0)
        total_results = first_page["totalCount"]
        assets = [Asset(asset) for asset in first_page["assets"]]
        print(f"Total assets to fetch: {total_results}")
        print(f"Fetched first 100 assets. Fetching remaining {total_results - 100} assets in parallel...")

        start_time = time.time()
        fetched_count = 100

        with concurrent.futures.ThreadPoolExecutor() as executor:
            offsets = range(100, total_results, 100)
            fetch_func = partial(self.fetch_assets_page, filters)
            future_to_offset = {executor.submit(fetch_func, offset): offset for offset in offsets}
            
            for future in concurrent.futures.as_completed(future_to_offset):
                offset = future_to_offset[future]
                try:
                    data = future.result()
                    new_assets = [Asset(asset) for asset in data["assets"]]
                    assets.extend(new_assets)
                    fetched_count += len(new_assets)
                    
                    # Print progress
                    progress = fetched_count / total_results
                    elapsed_time = time.time() - start_time
                    estimated_total_time = elapsed_time / progress if progress > 0 else 0
                    remaining_time = estimated_total_time - elapsed_time
                    print(f"Fetched assets: {fetched_count}/{total_results} ({progress:.2%}) - "
                          f"Elapsed: {elapsed_time:.2f}s - Estimated remaining: {remaining_time:.2f}s")
                except Exception as e:
                    print(f"Error fetching assets at offset {offset}: {e}")

        total_time = time.time() - start_time
        print(f"Finished fetching all assets in {total_time:.2f} seconds")
        print(f"Total assets fetched: {len(assets)}")

        return assets
    
    def get_taxonomies_by_filter(self, filters):
        endpoint = f"/taxonomies;{filters}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            taxonomy_list = [Taxonomy(taxonomy) for taxonomy in response.json()]
            return taxonomy_list
        except requests.RequestException as e:
            raise Exception(e)
        
    def get_taxonomy(self, taxonomy_id):
        endpoint = f"/taxonomies/{taxonomy_id}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            taxonomy = Taxonomy(response.json())
            return taxonomy
        except requests.RequestException as e:
            raise Exception(e)
        
    def create_root_taxon(self, taxonomy_id, payload):
        endpoint = f"/taxonomies/{taxonomy_id}/taxons"
        try:
            response = requests.post(self.base_url + endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            return Taxon(response.json())
        except requests.RequestException as e:
            print(f'Request failed with status code {response.status_code}: {response.text}')
            taxon = self.get_root_taxons_by_name(taxonomy_id, payload['name'])
            if (taxon):
                return taxon
            # raise Exception(e)
        
    def create_taxon(self, taxonomy_id, parent_taxon_id, payload):
        endpoint = f"/taxonomies/{taxonomy_id}/taxons/{parent_taxon_id}/taxons"
        try:
            response = requests.post(self.base_url + endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            return Taxon(response.json())
        except requests.RequestException as e:
            print(f'Request failed with status code {response.status_code}: {response.text}')
            taxon = self.get_taxons_by_name(taxonomy_id, parent_taxon_id, payload['name'])
            if (taxon):
                return taxon

            # raise Exception(e)
        
    def get_root_taxons_by_filters(self, taxonomy_id, filters):
        pattern = r"name=([^;]*)"
        match = re.search(pattern, filters)
        if match:
            name = match.group(1)
            # URL encode the name
            encoded_name = urllib.parse.quote(name)
            encoded_filter = f"name={encoded_name}"
            encoded_filters = filters.replace(f"name={name}", encoded_filter)
        else:
            encoded_filters = filters
        endpoint = f"/taxonomies/{taxonomy_id}/taxons;{encoded_filters}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            taxon_list = [Taxon(taxonomy) for taxonomy in response.json()]
            return taxon_list
        except requests.RequestException as e:
            print(f'Request failed with status code {response.status_code}: {response.text}')
            # raise Exception(e)

    def get_root_taxons_by_name(self, taxonomy_id, name):
        endpoint = f"/taxonomies/{taxonomy_id}/taxons"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            taxon_list = [Taxon(taxonomy) for taxonomy in response.json()]
            # Find the taxon where name matches taxon_name
            matching_taxon = next((taxon for taxon in taxon_list if taxon.name == name), None)

            if matching_taxon:
                return matching_taxon
            else:
                print(f"No root taxon found with name: {name}")
        except requests.RequestException as e:
            print(f'Request failed with status code {response.status_code}: {response.text}')
            # raise Exception(e)
        
    def get_taxons_by_filters(self, taxonomy_id, parent_taxon_id, filters):
        pattern = r"name=([^;]*)"
        match = re.search(pattern, filters)
        if match:
            name = match.group(1)
            # URL encode the name
            encoded_name = urllib.parse.quote(name)
            encoded_filter = f"name={encoded_name}"
            encoded_filters = filters.replace(f"name={name}", encoded_filter)
        else:
            encoded_filters = filters
        endpoint = f"/taxonomies/{taxonomy_id}/taxons/{parent_taxon_id}/taxons;{encoded_filters}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            taxon_list = [Taxon(taxonomy) for taxonomy in response.json()['taxons']]
            return taxon_list
        except requests.RequestException as e:
            print(f'Request failed with status code {response.status_code}: {response.text}')
            # raise Exception(e)

    def get_taxons_by_name(self, taxonomy_id, parent_taxon_id, name):
        endpoint = f"/taxonomies/{taxonomy_id}/taxons/{parent_taxon_id}/taxons"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            taxon_list = [Taxon(taxonomy) for taxonomy in response.json()['taxons']]

            # Find the taxon where name matches taxon_name
            matching_taxon = next((taxon for taxon in taxon_list if taxon.name == name), None)

            if matching_taxon:
                return matching_taxon
            else:
                print(f"No taxon found with name: {name}")
        except requests.RequestException as e:
            print(f'Request failed with status code {response.status_code}: {response.text}')
            # raise Exception(e)

    def get_objects_by_filters(self, type, filters, limit = 100, offset = 0, pagination=False, createdFrom=None, createdTo=None, pagination_delta_in_days=None, plural_name=None, pagination_delta_in_hours = 24):
        """Get objects."""
        """Supports the offset until 10000 results, and pagination on created dates if it is required (metadata filters)."""
        # Set variables
        if not pagination_delta_in_days:
            pagination_delta_in_days = 10

        if pagination_delta_in_hours != 24 and createdTo.hours < 24:
            time_change = datetime.timedelta(hours=pagination_delta_in_hours)
            createdFrom += time_change
            createdTo += time_change

        # End condition
        if createdFrom and datetime.now() < datetime.strptime(createdFrom, '%d %b %Y'):
            # if current_datetime < createdFromAsDate
            # createdFrom date cannot be a future date : return an empy list.
            parsed_current_date = datetime.now().strftime('%d %b %Y')
            print(f"createdFrom is later that the current date : createdFrom={createdFrom}, current_date={parsed_current_date}")
            # No asset can be found
            return []
        
        if (plural_name):
            if createdFrom and createdTo:
                endpoint = f"/{plural_name};{filters};offset={offset};createdFrom={createdFrom};createdTo={createdTo}"
            else:
                endpoint = f"/{plural_name};{filters};offset={offset}"

        else:
            # Set up creation date filters for pagination in the endpoint
            if createdFrom and createdTo:
                if ('fql' in filters):
                    # AND created > "2019-08-22" AND created < "2024-03-22"
                    parsed_created_from = datetime.strptime(createdFrom, '%d %b %Y')
                    fql_formatted_created_from = datetime.strftime(parsed_created_from, '%Y-%m-%d')
                    parsed_created_to = datetime.strptime(createdTo, '%d %b %Y')
                    fql_formatted_created_to = datetime.strftime(parsed_created_to, '%Y-%m-%d')
                    date_filters_fql = f" AND created > \"{fql_formatted_created_from}\" AND created < \"{fql_formatted_created_to}\""
                    encoded_date_filters_fql = urllib.parse.quote(date_filters_fql)
                    # Add encoded date filters for fql
                    endpoint = f"/{type};{filters}{encoded_date_filters_fql};offset={offset}"
                else:
                    endpoint = f"/{type};{filters};offset={offset};createdFrom={createdFrom};createdTo={createdTo}"
            else:
                endpoint = f"/{type};{filters};offset={offset}"

        # Retrieve assets
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            object_list = response_json["objects"]
            total_results = response_json["totalCount"]

            print(f"Found {total_results} {type} with filters {filters}, offset {offset}, createdFrom {createdFrom}, createdTo {createdTo}")

            if (total_results > 10000 and "metadata" in filters):
                # Activate pagination
                if "created" not in filters:
                    # if not createdTo is equivalent to if not pagination
                    if not pagination:
                        # Init created - 1st of Sept. 2023
                        from_date = datetime(2023, 9, 1)
                        createdFrom = from_date.strftime('%d %b %Y')
                        new_createdTo = from_date + timedelta(days=pagination_delta_in_days)
                        createdTo = new_createdTo.strftime('%d %b %Y')
                        object_list.extend(self.get_objects_by_filters(type, filters, limit, 0, True, createdFrom, createdTo, None, plural_name))
                    else:
                        if pagination_delta_in_days == 1:
                            pagination_delta_in_hours //= 2
                            print(f"Reducing the pagination delta to {pagination_delta_in_hours} hours")
                            parsed_createdTo = datetime.strptime(createdTo, '%d %b %Y')
                            # Add days for the pagination
                            new_createdTo = parsed_createdTo - timedelta(days=pagination_delta_in_days)
                            createdTo = new_createdTo.strftime('%d %b %Y')
                            object_list.extend(self.get_objects_by_filters(type, filters, limit, 0, True, createdFrom, createdTo, pagination_delta_in_days, plural_name, pagination_delta_in_hours))
                        else:
                            # if pagination and total_results > 10000, divide the pagination delta by 2
                            pagination_delta_in_days //= 2
                            print(f"Reducing the pagination delta to {pagination_delta_in_days} days")
                            parsed_createdTo = datetime.strptime(createdTo, '%d %b %Y')
                            # Add days for the pagination
                            new_createdTo = parsed_createdTo - timedelta(days=pagination_delta_in_days)
                            createdTo = new_createdTo.strftime('%d %b %Y')
                            object_list.extend(self.get_objects_by_filters(type, filters, limit, 0, True, createdFrom, createdTo, pagination_delta_in_days, plural_name))
                else:
                    raise Exception("Unable to paginate on the creation date filters as there query already contains a creation date filter.")

            elif (total_results > offset + limit):
                # Set new offset
                object_list.extend(self.get_objects_by_filters(type, filters, limit, offset + limit, pagination, createdFrom, createdTo, None, plural_name))
            elif pagination:
                # Set new pagination creation date filters
                createdFrom = createdTo
                parsed_date = datetime.strptime(createdTo, '%d %b %Y')
                # Add days for the pagination
                new_date = parsed_date + timedelta(days=pagination_delta_in_days)
                createdTo = new_date.strftime('%d %b %Y')
                object_list.extend(self.get_objects_by_filters(type, filters, limit, 0, True, createdFrom, createdTo, None, plural_name))

            return object_list
        except requests.RequestException as e:
            raise Exception(e)