import logging
from urllib.parse import urlparse

import requests

logger = logging.getLogger(__file__)


def create_zenodo_dataset(zenodo_url, zenodo_token, zenodo_dict, previous_version=None):
    """
    Create a dataset in Zenodo, using the personal token provided.
    If a Zenodo ID is provided as `previous_version`, a new version of this Zenodo record will be created.

    :param zenodo_url: URL to the Zenodo repository
    :param zenodo_token: Zenodo personal token
    :type zenodo_token: str
    :param zenodo_dict: Zenodo metadata dictionary, as returned by ZenodoMetadata.as_dict()
    :type zenodo_dict: dict
    :param previous_version: ID of the record to create a new version of, if applicable
    :type previous_version: str or None
    :return: Zenodo dataset ID
    :rtype: str
    """
    url = zenodo_url + '/api/records'
    if previous_version:
        url += f'/{previous_version}/versions'
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + zenodo_token
    }
    try:
        response = requests.post(url,
                                headers=headers,
                                json=zenodo_dict)
        response.raise_for_status()
        logger.debug('response = %s', response.json())
        return response.json()['id']
    except requests.exceptions.HTTPError as e:
        print(response.text)
        raise e


def prepare_zenodo_dataset(zenodo_url, dataset_id, zenodo_token):
    """"
    Prepare a dataset for review in ZENODO.

    :param zenodo_url: URL to the Zenodo repository
    :param dataset_id: Zenodo dataset ID
    :param zenodo_token: The Zenodo personal token to use for the upload
    :return: Zenodo response to the request
    """

    try:
        # Prereserve DOI
        headers = {"Authorization": "Bearer " + zenodo_token}
        reserve_doi_url = zenodo_url + f'/api/records/{dataset_id}/draft/pids/doi'
        response = requests.post(reserve_doi_url, headers=headers)
        response.raise_for_status()
        logger.debug('response = %s', response.json())
        # Get Zenodo dataset
        dataset_url = zenodo_url + f'/api/records/{dataset_id}/draft'
        response = requests.get(dataset_url, headers=headers)
        response.raise_for_status()
        logger.debug('response = %s', response.json())
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(response.text)
        raise e


def update_zenodo_dataset(zenodo_url, dataset_id, zenodo_token, zenodo_dict):
    """
    Update a dataset's metadata at the given Zenodo link.

    :param zenodo_url: URL to the Zenodo repository
    :param dataset_id: Zenodo dataset ID
    :param zenodo_token: Zenodo personal token
    :param zenodo_dict: Zenodo metadata dictionary, as returned by ZenodoMetadata.as_dict()
    :return: Zenodo dataset ID
    """
    url = zenodo_url + f'/api/records/{dataset_id}/draft'
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + zenodo_token
    }
    try:
        response = requests.put(url, headers=headers, json=zenodo_dict)
        response.raise_for_status()
        logger.debug('response = %s', response.json())
        return response.json()['id']
    except requests.exceptions.HTTPError as e:
        print(response.text)
        raise e


def upload_zenodo_assets(zenodo_url, dataset_id, zenodo_token, assets, path):
    """
    Upload assets to a Zenodo dataset.

    :param zenodo_url: URL to the Zenodo repository
    :param dataset_id: Zenodo dataset ID
    :param zenodo_token: Zenodo personal token
    :param assets: locations of assets to upload
    :type assets: list
    :param path: location where the assets are collected before upload
    """
    headers = {
        "Authorization": "Bearer " + zenodo_token
    }

    for location in assets:
        parsed_url = urlparse(location)
        filename = parsed_url.path.split('/')[-1]
        target = path / filename

        # Start file upload
        try:
            response = requests.post(zenodo_url + f'/api/records/{dataset_id}/draft/files',
                                    headers=headers,
                                    json=[{'key': filename}])
            response.raise_for_status()
            logger.debug('response = %s', response.json())
        except requests.exceptions.HTTPError as e:
            print(response.text)
            raise e

        # Upload file content
        with open(target, "rb") as fp:
            try:
                response = requests.put(zenodo_url + f'/api/records/{dataset_id}/draft/files/{filename}/content',
                                        headers=headers,
                                        data=fp)
                response.raise_for_status()
                logger.debug('response = %s', response.json())
            except requests.exceptions.HTTPError as e:
                print(response.json())
                raise e

        # Complete file upload
        try:
            response = requests.post(zenodo_url + f'/api/records/{dataset_id}/draft/files/{filename}/commit',
                                    headers=headers)
            response.raise_for_status()
            logger.debug('response = %s', response.json())
        except requests.exceptions.HTTPError as e:
            print(response.text)
            raise e


def delete_zenodo_dataset(zenodo_url, dataset_id, zenodo_token):
    """
    Delete a draft record from Zenodo.

    :param zenodo_url: URL to the Zenodo repository
    :param dataset_id: Zenodo record ID
    :param zenodo_token: Zenodo personal token
    """
    url = zenodo_url + f'/api/records/{dataset_id}/draft'
    headers = {
        "Authorization": "Bearer " + zenodo_token
    }
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(response.text)
        raise e


def get_zenodo_dataset(zenodo_url, dataset_id, zenodo_token):
    """
    Get a record from Zenodo.

    :param zenodo_url: URL to the Zenodo repository
    :param dataset_id: Zenodo record ID
    :param zenodo_token: Zenodo personal token
    """
    url = zenodo_url + f'/api/records/{dataset_id}/draft'
    headers = {
        "Authorization": "Bearer " + zenodo_token
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(response.text)
        raise e
