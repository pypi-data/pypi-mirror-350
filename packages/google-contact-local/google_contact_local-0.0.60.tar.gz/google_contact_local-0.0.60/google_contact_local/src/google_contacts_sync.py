from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo

from importer_local.importer_sync_conflict_resolution import (
    ImporterSyncConflictResolution,
)
from importer_local.importer_sync_conflict_resolution import (
    UpdateStatus as ImporterUpdateStatus,
)
from database_mysql_local.sync_conflict_resolution import UpdateStatus

from .google_contacts_push import GoogleContactsPush  # , SCOPES, our_get_env
from .google_contacts import DEFAULT_LOCATION_ID
from .google_contacts_constants import GoogleContactConstants


# TODO: complete to develpp this class
class GoogleContactsSync(GoogleContactsPush):
    def __init__(self):
        super().__init__()
        self.contact_to_push_dict = {}

    # TODO Please add comment why this code is commented.
    def _insert_contact_details_to_db(
        self, contact_dict: dict, user_external_id: int, data_source_instance_id: int
    ) -> int:
        # TODO: complete to develpp this method
        contact_dict["location_id"] = DEFAULT_LOCATION_ID
        try:
            # Get update status
            # This is only the importer's sync conflict resolution.
            update_status = self.__conflict_resolution(
                last_modified_timestamp=contact_dict.get("last_modified_timestamp"),
                contact_id=contact_dict.get("contact_id"),
            )
            update_status = update_status
            # insert organization
            self._sync_organization(contact_dict=contact_dict)

            # insert link contact_location
            # The location is in contact_dict
            location_results = self._insert_link_contact_location(
                # TODO Why do we need both?  contact_dict=contact_dict, contact_id=contact_id
                contact_dict=contact_dict
            ) or [{}]
            # TODO Same comments as in contact-csv, Why location_results[0]? What if we have multiple locations? - Please add such test.
            # TODO Can we have one copy of this code used both by google-contact and contact-csv?
            contact_dict["location_id"] = location_results[0].get("location_id")
            contact_dict["country_id"] = location_results[0].get("country_id")

            # insert link contact_group
            # TODO I expected to have only contact_id and group_list as parameters
            self._insert_link_contact_groups(
                # TODO Why do we need both? contact_dict=contact_dict and contact_id=contact_id
                contact_dict=contact_dict
            )

            # insert link contact_persons
            # TODO I expected to have only contact_id and person_list as parameters
            contact_person_result_dict = (
                self._insert_link_contact_persons(contact_dict=contact_dict) or {}
            )
            contact_dict["person_id"] = contact_person_result_dict.get("person_id")

            # insert link contact_profiles
            # TODO I expected to have only contact_id and profile_list as parameters
            # TODO contact_profiles_dict =
            contact_profile_info = (
                self._insert_contact_profiles(contact_dict=contact_dict) or {}
            )
            contact_dict["profiles_ids_list"] = contact_profile_info.get(
                "profiles_ids_list"
            )

            # insert organization-profile
            # TODO I'm not sure I understand, contact can have multiple profiles, and contact can have multiple organizations, are we linking one organization of the contact with all his profiles?  # noqa
            self._sync_organization_profile(contact_dict=contact_dict)

            # insert link contact_email_addresses
            # TODO I expected to have only contact_id and email_address_list as parameters
            self._insert_link_contact_email_addresses(contact_dict=contact_dict)

            # insert link contact_notes
            GoogleContactsSync._insert_link_contact_notes_and_text_blocks(
                contact_dict=contact_dict
            )

            # insert link contact_phones
            self._insert_link_contact_phones(contact_dict=contact_dict)

            # inset link contact_user_externals
            self._insert_link_contact_user_external(contact_dict=contact_dict)

            # insert link contact_internet_domains
            self._insert_link_contact_domains(contact_dict=contact_dict)

        except Exception as exception:
            self.logger.exception(
                log_message="Error while inserting to contact connection tables",
                object={"exception": exception},
            )
            raise exception
        finally:
            # Update contact on google contacts
            self.update_contact_by_google_contact_dict(
                resource_name=contact_dict.get("resource_name"),
                google_contact_dict=self.contact_to_push_dict,
                fields_to_update=self.contact_to_push_dict.keys(),
            )
            importer_id = self._insert_importer(
                # TODO As contact can have multiple locations, I think we should location_id=contact_dict.get("main_location_id")
                contact_id=contact_dict.get("contact_id"),
                location_id=contact_dict.get("location_id") or DEFAULT_LOCATION_ID,
                user_external_id=user_external_id,
                data_source_instance_id=data_source_instance_id,
                google_people_api_resource_name=contact_dict.get("resource_name"),
            )
            self.logger.info(object={"importer_id": importer_id})

        return importer_id

    # TODO: Test this method
    def _sync_organization(self, contact_dict: dict):
        update_status_and_information_list = (
            self.organizations_local.get_update_status_and_information_list(
                last_modified_timestamp=contact_dict.get("last_modified_timestamp"),
                main_profile_id=contact_dict.get("main_profile_id"),
            )
        )
        if not update_status_and_information_list:
            self._insert_organization(contact_dict=contact_dict)
        else:
            is_update_data_source_found = False
            for update_status_and_information in update_status_and_information_list:
                update_status = update_status_and_information.get("update_status")
                organization_name = update_status_and_information.get(
                    "organization_name"
                )
                job_title_ml_id = update_status_and_information.get("job_title_ml_id")
                # TODO: move the following select to get_update_status_and_information_list
                job_title_str = self.select_one_value_by_column_and_value(
                    schema_name="job_title",
                    view_table_name="job_title_ml_with_deleted_and_test_data_view",
                    select_clause_value="job_title_ml.title",
                    column_name="job_title_ml_id",
                    column_value=job_title_ml_id,
                )
                if update_status == UpdateStatus.UPDATE_DATA_SOURCE:
                    is_update_data_source_found = True
                    organization_name = update_status_and_information.get(
                        "organization_name"
                    )
                # Add organization_name and job_title from the db to contact_to_push_dict
                update_status_and_information["name"] = organization_name
                update_status_and_information["title"] = job_title_str
                organizations_job_titles_dicts_list: list[dict] = contact_dict.get(
                    "organizations_job_titles_dicts_list"
                )
                # Check if the organization name is already found in the organizations_job_titles_dicts_list
                is_organization_name_found = False
                for (
                    organizations_job_titles_dict
                ) in organizations_job_titles_dicts_list:
                    if (
                        organizations_job_titles_dict.get("name") == organization_name
                        and organizations_job_titles_dict.get("title") == job_title_str
                    ):
                        # Update contact_dict["organizations_job_titles_dicts_list"]
                        organizations_job_titles_dict["organization_id"] = (
                            update_status_and_information.get("organization_id")
                        )
                        organizations_job_titles_dict["organization_ml_id"] = (
                            update_status_and_information.get("organization_ml_id")
                        )
                        organizations_job_titles_dict["job_title_id"] = (
                            update_status_and_information.get("job_title_id")
                        )
                        organizations_job_titles_dict["job_title_ml_id"] = (
                            update_status_and_information.get("job_title_ml_id")
                        )
                        is_organization_name_found = True
                if not is_organization_name_found:
                    contact_dict["organizations_job_titles_dicts_list"].append(
                        update_status_and_information
                    )
            self._insert_organization(contact_dict=contact_dict)
            if is_update_data_source_found:
                self.contact_to_push_dict["organizations"] = []
                for organization_job_title_dict in contact_dict.get(
                    "organizations_job_titles_dicts_list"
                ):
                    self.contact_to_push_dict["organizations"].append(
                        {
                            "name": organization_job_title_dict.get("name"),
                            "title": organization_job_title_dict.get("title"),
                        }
                    )

    def _sync_organization_profile(
        self,
        contact_dict: dict,
    ) -> list:
        organizations_job_titles_dicts_list: list[dict] = contact_dict.get(
            "organizations_job_titles_dicts_list"
        )
        main_profile_id = contact_dict.get("main_profile_id")
        if main_profile_id is None:
            self._insert_organization_profile(contact_dict=contact_dict)
        else:
            organization_profiles_ids_list: list[dict] = []
            for organization_job_title_dict in organizations_job_titles_dicts_list:
                organization_id = organization_job_title_dict.get("organization_id")
                organization_ml_id = organization_job_title_dict.get(
                    "organization_ml_id"
                )
                job_title_id = organization_job_title_dict.get("job_title_id")
                job_title_ml_id = organization_job_title_dict.get("job_title_ml_id")
                data_dict = {
                    "organization_ml_id": organization_ml_id,
                    "job_title_id": job_title_id,
                    "job_title_ml_id": job_title_ml_id,
                }
                organization_profile_id = self.organization_profile.upsert_mapping(
                    organization_id=organization_id,
                    profile_id=main_profile_id,
                    data_dict=data_dict,
                )
                organization_profiles_ids_list.append(organization_profile_id)
            contact_dict["organization_profiles_ids_list"] = (
                organization_profiles_ids_list
            )

    def __conflict_resolution(
        self, last_modified_timestamp: str, contact_id: int
    ) -> ImporterUpdateStatus:
        """
        Conflict resolution for Google contact
        :return: contact_dict
        """

        if not contact_id:
            return ImporterUpdateStatus.DONT_UPDATE
        sync_conflict_resolution = ImporterSyncConflictResolution()
        update_status: ImporterUpdateStatus = (
            sync_conflict_resolution.get_update_status(
                last_modified_timestamp=last_modified_timestamp,
                data_source_instance_id=GoogleContactConstants.DATA_SOURCE_TYPE_ID,
                entity_type_id=GoogleContactConstants.CONTACT_ENTITY_TYPE_ID,
                entity_id=contact_id,
            )
        )

        return update_status

    @staticmethod
    # TODO Let's use existing function from python-sdk, or move this function to python-sdk
    def __get_formatted_timestamp(last_modified_timestamp_str: str) -> Optional[str]:
        if not last_modified_timestamp_str:
            return
        timestamp = datetime.strptime(
            last_modified_timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        timestamp = timestamp.replace(tzinfo=ZoneInfo("UTC"))
        formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_timestamp
