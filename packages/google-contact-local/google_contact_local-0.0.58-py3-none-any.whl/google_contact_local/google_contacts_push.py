from database_mysql_local.connector import Connector
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from .google_contacts import GoogleContacts, SCOPES, our_get_env
from .google_contacts_constants import GoogleContactConstants
from googleapiclient.errors import HttpError
import datetime


# TODO: the inheritance of GoogleContactsPush from GoogleContacts is temporary
# we want to inherit from GoogleAccount class
class GoogleContactsPush(GoogleContacts):
    def __init__(self):
        super().__init__()

    def initialize_service(self, email: str):
        # TODO: add call to api-management
        # Your existing authentication logic
        # TODO I think it is better to use the self.user_context.get_effective_profile_id() and make the effective_profile_id private
        main_profile_id = self.profile_local.get_profile_id_by_email_address(
            email_address=email
        )
        auth_details = self.user_externals_local.get_auth_details(
            username=email,
            system_id=GoogleContactConstants.GOOGLE_SYSTEM_ID,
            profile_id=main_profile_id
        )
        if not auth_details:
            self.logger.error(f"Auth details not found in DB; email: {email}, system_id: {GoogleContactConstants.GOOGLE_SYSTEM_ID}, profile_id: {main_profile_id}")  # noqa
            exception_message = f"Auth details not found in DB; email: {email}, system_id: {GoogleContactConstants.GOOGLE_SYSTEM_ID}, profile_id: {main_profile_id}"  # noqa
            raise Exception(exception_message)

        access_token = auth_details.get("access_token")
        refresh_token = auth_details.get("refresh_token")
        expiry = auth_details.get("expiry")
        is_refresh_token_valid = auth_details.get("is_refresh_token_valid")

        if isinstance(expiry, str):
            try:
                expiry_dt = datetime.datetime.fromisoformat(expiry)
            except ValueError:
                expiry_dt = datetime.datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S")
        else:
            expiry_dt = expiry  # already a datetime?

        if expiry_dt.tzinfo is not None:
            expiry_dt = expiry_dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)

        token_info = {
            "token": access_token,
            "refresh_token": refresh_token,
            "token_uri": self.google_token_uri,
            "client_id": self.google_client_id,
            "client_secret": self.google_client_secret,
            "scopes": SCOPES,
            "expiry": expiry_dt,
        }
        # self.creds = Credentials.from_authorized_user_info(token_info)  The old way that caused the premission denied error from the people api

        self.creds = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri=self.google_token_uri,
            client_id=self.google_client_id,
            client_secret=self.google_client_secret,
            scopes=SCOPES,
            expiry=expiry_dt,
        )

        # if not self.creds.valid: deprecated v2.24.0 Prefer checking :attr:token_state instead.
        # class TokenState(Enum):
        #     """
        #     Tracks the state of a token.
        #     FRESH: The token is valid. It is not expired or close to expired, or the token has no expiry.
        #     STALE: The token is close to expired, and should be refreshed. The token can be used normally.
        #     INVALID: The token is expired or invalid. The token cannot be used for a normal operation.
        #     """
        #     FRESH = 1
        #     STALE = 2
        #     INVALID = 3
        # ! this class could not be imported from the google library for some reason

        if self.creds.token_state == 2:
            self.logger.warning(
                f"Stored credentials are close to expiry. re-authenticates the email: {email}", object={"token_info": token_info}
            )

        if self.creds.token_state == 3:
            self.logger.error(
                "Stored credentials are not valid.", object={"token_info": token_info}
            )
            self.update_by_column_and_value(
                schema_name="user_external",
                table_name="user_external_table",
                column_name="refresh_token",
                column_value=refresh_token,
                data_dict={"is_refresh_token_valid": False},
            )
            if is_refresh_token_valid:
                self.authenticate(email=email)
            else:
                self.logger.error(
                    f"Stored credentials are not valid. Refresh token is not valid; emaoil: {email}, is_refresh_token_valid: {is_refresh_token_valid}, expiry: {expiry_dt}",  # noqa
                    object={"token_info": token_info},
                )
                raise Exception(f"Stored credentials are not valid. Refresh token is not valid; emaoil: {email}, is_refresh_token_valid: {is_refresh_token_valid}, expiry: {expiry_dt}")  # noqa

        self.service = build("people", "v1", credentials=self.creds)

    def create_and_push_contacts(
        self,
        *,
        user_external_username: str = None,
        data_source_types_ids_list: list = None,
        data_source_instances_ids_list: list = None,
        order_by: str = None,
        limit: int = 1,
    ) -> list[dict]:
        self.logger.start(
            "create_and_push_contacts",
            object={
                "username": user_external_username,
                "data_source_types_ids_list": data_source_types_ids_list,
                "data_source_instances_ids_list": data_source_instances_ids_list,
                "order_by": order_by,
                "limit": limit,
            },
        )
        user_external_username = user_external_username or our_get_env(
            "GOOGLE_USER_EXTERNAL_USERNAME", raise_if_empty=True
        )
        result_dicts_list = []
        try:
            contacts_ids_list = (
                self.get_contact_ids_with_no_google_people_api_resource_name(
                    limit=limit,
                    data_source_types_ids_list=data_source_types_ids_list,
                    data_source_instances_ids_list=data_source_instances_ids_list,
                    order_by=order_by,
                )
            )
            for contact_id in contacts_ids_list:
                result_dict = self.create_and_push_contact_by_contact_id(
                    username=user_external_username, contact_id=contact_id
                )
                result_dicts_list.append(result_dict)
        except Exception as exception:
            self.logger.exception(
                "Exception in create_and_push_contacts", object={"exception": exception}
            )
            raise exception
        self.logger.end(
            "create_and_push_contacts", object={"contacts_ids_list": contacts_ids_list}
        )
        return result_dicts_list

    def create_and_push_contact_by_contact_id(
        self, *, username: str, contact_id: int
    ) -> dict:
        self.logger.start(
            "create_and_push_contact_by_contact_id", object={"contact_id": contact_id}
        )
        result_dict = {}
        try:
            google_contact_dict = self.get_google_contact_dict_by_contact_id(
                contact_id=contact_id
            )
            google_contact = self.create_contact_by_google_contact_dict(
                username=username, google_contact_dict=google_contact_dict
            )
            groups_titles_to_resource_name = (
                self.create_non_existing_google_contact_groups(contact_id=contact_id)
            )
            self.link_contact_to_groups(
                contact_resource_name=google_contact["resourceName"],
                groups_titles_to_resource_name=groups_titles_to_resource_name,
            )
            result_dict["contact_resource_name"] = google_contact["resourceName"]
            result_dict["groups_titles_to_resource_name"] = (
                groups_titles_to_resource_name
            )
        except Exception as exception:
            self.logger.exception(
                "Exception in create_and_push_contact_by_contact_id",
                object={"exception": exception},
            )
            raise exception
        self.logger.end("create_and_push_contact_by_contact_id")
        return result_dict

    def create_contact_by_google_contact_dict(
        self, *, username: str, google_contact_dict: dict
    ) -> dict:
        self.initialize_service(email=username)
        google_contact = (
            self.service.people().createContact(body=google_contact_dict).execute()
        )
        return google_contact

    def get_contact_ids_with_no_google_people_api_resource_name(
        self,
        *,
        limit: int = 1,
        data_source_types_ids_list: list = None,
        data_source_instances_ids_list: list = None,
        order_by: str = None,
    ) -> list[int]:
        self.logger.start(
            "get_contact_ids_with_no_google_people_api_resource_name",
            object={"limit": limit},
        )
        contacts_ids_list: list = []
        connection = Connector.connect("contact")
        params = []
        select_query = ""
        select_query_part1 = (
            "SELECT DISTINCT cv.contact_id FROM contact.contact_view AS cv JOIN"
            " importer.importer_view AS iv JOIN contact_person.contact_person_view AS cpv"
            " JOIN data_source_instance.data_source_instance_table AS dsigv"
            " WHERE cv.contact_id = iv.entity_id AND cv.contact_id = cpv.contact_id AND"
            " iv.google_people_api_resource_name IS NULL AND iv.end_timestamp IS NULL"
        )
        select_query += select_query_part1
        if data_source_instances_ids_list:
            select_query += (
                " AND cv.data_source_instance_id = dsigv.data_source_instance_id AND ("
            )
            for data_source_instance_id in data_source_instances_ids_list:
                condition = "dsigv.data_source_instance_id = %s OR "
                select_query += condition
                params.append(data_source_instance_id)
            select_query = select_query[:-3]
            select_query += ")"
        elif data_source_types_ids_list:
            select_query += (
                " AND cv.data_source_instance_id = dsigv.data_source_instance_id AND ("
            )
            for data_source_type_id in data_source_types_ids_list:
                condition = "dsigv.data_source_type_id = %s OR "
                select_query += condition
                params.append(data_source_type_id)
            select_query = select_query[:-3]  # remove the last ' OR '
            select_query += ")"
        select_query_part2 = (
            " AND NOT EXISTS (SELECT 1 FROM importer.importer_view AS iv2 JOIN"
            " contact.contact_view AS cv2 JOIN contact_person.contact_person_view AS cpv2"
            " WHERE cpv2.contact_id = cv2.contact_id AND cpv.person_id = cpv2.person_id"
            " AND iv2.entity_id = cv2.contact_id AND iv2.google_people_api_resource_name IS NOT NULL)"
        )
        select_query += select_query_part2
        if order_by:
            select_query += " ORDER BY %s"
            params.append(order_by)
        select_query += " LIMIT %s"
        params.append(limit)
        self.logger.info(
            "select_query", object={"select_query": select_query, "params": params}
        )
        cursor = connection.cursor()
        cursor.execute(select_query, params)
        results = cursor.fetchall()
        for result in results:
            contacts_ids_list.append(result[0])
        self.logger.end(
            "get_contact_ids_with_no_google_people_api_resource_name",
            object={"contacts_ids_list": contacts_ids_list},
        )
        return contacts_ids_list

    def get_contact_ids_with_google_people_api_resource_name(
        self,
        *,
        limit: int = 1,
        data_source_types_ids_list: list = None,
        data_source_instances_ids_list: list = None,
        order_by: str = None,
    ) -> list[int]:
        self.logger.start(
            "get_contact_ids_with_google_people_api_resource_name",
            object={"limit": limit},
        )
        contacts_ids_list: list = []
        connection = Connector.connect("contact")
        params = []
        select_query = ""
        select_query_part1 = (
            "SELECT DISTINCT cv.contact_id FROM contact.contact_view AS cv JOIN"
            " importer.importer_view AS iv JOIN contact_person.contact_person_view AS cpv"
            " JOIN data_source_instance.data_source_instance_table AS dsigv"
            " WHERE cv.contact_id = iv.entity_id AND cv.contact_id = cpv.contact_id AND"
            " iv.google_people_api_resource_name IS NOT NULL AND iv.end_timestamp IS NULL"
        )
        select_query += select_query_part1
        if data_source_instances_ids_list:
            select_query += (
                " AND cv.data_source_instance_id = dsigv.data_source_instance_id AND ("
            )
            for data_source_instance_id in data_source_instances_ids_list:
                condition = "dsigv.data_source_instance_id = %s OR "
                select_query += condition
                params.append(data_source_instance_id)
            select_query = select_query[:-3]
            select_query += ")"
        elif data_source_types_ids_list:
            select_query += (
                " AND cv.data_source_instance_id = dsigv.data_source_instance_id AND ("
            )
            for data_source_type_id in data_source_types_ids_list:
                condition = "dsigv.data_source_type_id = %s OR "
                select_query += condition
                params.append(data_source_type_id)
            select_query = select_query[:-3]  # remove the last ' OR '
            select_query += ")"
        if order_by:
            select_query += " ORDER BY %s"
            params.append(order_by)
        select_query += " LIMIT %s"
        params.append(limit)
        self.logger.info(
            "select_query", object={"select_query": select_query, "params": params}
        )
        cursor = connection.cursor()
        cursor.execute(select_query, params)
        results = cursor.fetchall()
        for result in results:
            contacts_ids_list.append(result[0])
        self.logger.end(
            "get_contact_ids_with_google_people_api_resource_name",
            object={"contacts_ids_list": contacts_ids_list},
        )
        return contacts_ids_list

    # Get contact dict by contact id from the databse
    def get_google_contact_dict_by_contact_id(self, contact_id: int) -> dict:
        self.logger.start(
            "get_contact_dict_by_contact_id", object={"contact_id": contact_id}
        )
        google_contact_dict: dict = {}

        # Get the record from contact_view
        contact_view_select_result_dict: dict = (
            self.select_one_dict_by_column_and_value(
                schema_name="contact",
                view_table_name="contact_view",
                column_name="contact_id",
                column_value=contact_id,
            )
        )
        if contact_view_select_result_dict is None:
            self.logger.info(
                "No contact found with the given contact_id",
                object={"contact_id": contact_id},
            )
            self.logger.end(
                "get_contact_dict_by_contact_id",
                object={"contact_dict": google_contact_dict},
            )
            return google_contact_dict
        self.__create_google_contact_dict(
            contact_view_select_result_dict=contact_view_select_result_dict,
            google_contact_dict=google_contact_dict,
        )
        self.logger.end(
            "get_contact_dict_by_contact_id",
            object={"google_contact_dict": google_contact_dict},
        )
        return google_contact_dict

    def __create_google_contact_dict(
        self, *, contact_view_select_result_dict: dict, google_contact_dict: dict
    ):
        google_contact_dict["names"] = [
            {
                "givenName": contact_view_select_result_dict[
                    "original_first_name"
                ],  # TODO: Shall we use first_name?
                "familyName": contact_view_select_result_dict[
                    "original_last_name"
                ],  # TODO: Shall we use last_name?
                "displayName": contact_view_select_result_dict[
                    "display_as"
                ],  # TODO: Shall we use full_name?
            }
        ]
        google_contact_dict["phoneNumbers"] = [
            {
                "value": contact_view_select_result_dict["phone1"],
                # 'type': 'mobile',     # TODO: There is not phone type in the db, shall we add it?
            },
            {
                "value": contact_view_select_result_dict["phone2"],
                # 'type': 'mobile',     # TODO: There is not phone type in the db, shall we add it?
            },
            {
                "value": contact_view_select_result_dict["phone3"],
                # 'type': 'mobile',     # TODO: There is not phone type in the db, shall we add it?
            },
        ]
        google_contact_dict["emailAddresses"] = [
            {
                "value": contact_view_select_result_dict["email1"],
                # 'type': 'home',     # TODO: There is not email type in the db, shall we add it?
            },
            {
                "value": contact_view_select_result_dict["email2"],
                # 'type': 'home',     # TODO: There is not email type in the db, shall we add it?
            },
            {
                "value": contact_view_select_result_dict["email3"],
                # 'type': 'home',     # TODO: There is not email type in the db, shall we add it?
            },
        ]
        # TODO: use also organization_profile for this?
        google_contact_dict["organizations"] = [
            {
                "name": contact_view_select_result_dict["organization"],
                "title": contact_view_select_result_dict["job_title"],
            }
        ]
        google_contact_dict["occupations"] = [
            {
                "value": contact_view_select_result_dict["job_title"],
            }
        ]
        # TODO: use also contact_location for this?
        google_contact_dict["addresses"] = [
            {
                "streetAddress": contact_view_select_result_dict["address1_street"],
                "city": contact_view_select_result_dict["address1_city"],
                "region": contact_view_select_result_dict[
                    "address1_state"
                ],  # This is the state in Google Contact
                "postalCode": contact_view_select_result_dict["address1_postal_code"],
                "country": contact_view_select_result_dict["address1_country"],
            },
            {
                "streetAddress": contact_view_select_result_dict["address2_street"],
                "city": contact_view_select_result_dict["address2_city"],
                "region": contact_view_select_result_dict[
                    "address2_state"
                ],  # This is the state in Google Contact
                "postalCode": contact_view_select_result_dict["address2_postal_code"],
                "country": contact_view_select_result_dict["address2_country"],
            },
        ]
        google_contact_dict["birthdays"] = [
            {
                # 'date': contact_view_select_result_dict['birthday'], # TODO: we will have to convert it to date format
                "text": contact_view_select_result_dict["birthday"],
            }
        ]
        # TODO: if necessary get it also from url table
        google_contact_dict["urls"] = [
            {
                "value": contact_view_select_result_dict["website1"],
            },
            {
                "value": contact_view_select_result_dict["website2"],
            },
            {
                "value": contact_view_select_result_dict["website3"],
            },
        ]
        notes = self.select_one_value_by_column_and_value(
            schema_name="contact_note",
            view_table_name="contact_note_view",
            select_clause_value="note",
            column_name="contact_id",
            column_value=contact_view_select_result_dict["contact_id"],
        )
        google_contact_dict["biographies"] = [
            {
                "value": notes,
            }
        ]
        start_timestamp = self.select_one_value_by_where(
            schema_name="profile_profile",
            view_table_name="profile_profile_view",
            select_clause_value="start_timestamp",
            where="profile_id1 = %s AND profile_id2 = %s",
            params=(
                contact_view_select_result_dict["owner_profile_id"],
                contact_view_select_result_dict["main_profile_id"],
            ),
        )
        if start_timestamp:
            formatted_date = start_timestamp.strftime("%d %B %Y, %H:%M:%S")
            google_contact_dict["userDefined"] = [
                {"key": "Connected On", "value": formatted_date}
            ]

    # TODO: Shall we move the following method to a new class GoogleGroups?
    def list_contact_groups(self) -> list[dict]:
        results = self.service.contactGroups().list(pageSize=200).execute()
        return results.get("contactGroups", [])

    # TODO: Shall we move the following method to a new class GoogleGroups?
    def create_contact_group(self, *, group_title) -> str:
        contact_group = {"contactGroup": {"name": group_title}}
        group = self.service.contactGroups().create(body=contact_group).execute()
        return group["resourceName"]

    def create_non_existing_google_contact_groups(self, *, contact_id: int) -> dict:
        # Step 1: Retrieve local group information
        local_groups_dicts_lists: list[dict] = (
            self.contact_group.get_groups_of_contact_by_contact_id(
                contact_id=contact_id
            )
        )
        local_groups_titles_list: list[str] = []
        for local_groups_dict in local_groups_dicts_lists:
            local_groups_titles_list.append(local_groups_dict.get("title"))

        # Step 2: List existing Google contact groups
        google_groups_lists = self.list_contact_groups()
        groups_titles_to_resource_name = {}
        groups_titles_to_resource_name_to_link = {}

        # Step 3: Map existing Google contact groups to their resource names
        for group in google_groups_lists:
            groups_titles_to_resource_name[group.get("name")] = group.get(
                "resourceName"
            )

        # Step 4: Create groups in Google Contacts if they do not exist and prepare mapping to link
        for group_title in local_groups_titles_list:
            if group_title not in groups_titles_to_resource_name:
                resource_name = self.create_contact_group(group_title=group_title)
                groups_titles_to_resource_name[group_title] = resource_name
            groups_titles_to_resource_name_to_link[group_title] = (
                groups_titles_to_resource_name[group_title]
            )

        # Step 5: Return the mapping to link
        return groups_titles_to_resource_name_to_link

    def add_contact_to_group(
        self, *, contact_resource_name: str, group_resource_name: str
    ):
        member = {"resourceNamesToAdd": [contact_resource_name]}
        self.service.contactGroups().members().modify(
            resourceName=group_resource_name, body=member
        ).execute()

    def link_contact_to_groups(
        self, *, contact_resource_name: str, groups_titles_to_resource_name: dict
    ):
        for google_group_title, resource_name in groups_titles_to_resource_name.items():
            self.add_contact_to_group(
                contact_resource_name=contact_resource_name,
                group_resource_name=resource_name,
            )

    def delete_google_contact(self, contact_resource_name: str):
        try:
            # TODO: add call to api-management
            self.service.people().deleteContact(
                resourceName=contact_resource_name
            ).execute()
            self.logger.info(
                "Deleted contact",
                object={"contact_resource_name": contact_resource_name},
            )
        except Exception as exception:
            self.logger.exception(
                "Exception in delete_google_contact", object={"exception": exception}
            )

    def delete_google_contact_group(self, group_resource_name: str):
        try:
            self.service.contactGroups().delete(
                resourceName=group_resource_name
            ).execute()
            self.logger.info(
                "Deleted group", object={"group_resource_name": group_resource_name}
            )
        except Exception as exception:
            self.logger.exception(
                "Exception in delete_google_contact_group",
                object={"exception": exception},
            )

    def delete_multiple_google_contacts(self, contact_resource_names: list):
        for contact_resource_name in contact_resource_names:
            try:
                # TODO: add call to api-management
                self.service.people().deleteContact(
                    resourceName=contact_resource_name
                ).execute()
            except Exception as exception:
                self.logger.exception(
                    "Exception in delete_multiple_google_contacts",
                    object={"exception": exception},
                )

    def delete_multiple_google_contact_groups(
        self, groups_titles_to_resource_name: dict
    ):
        for group_resource_name in groups_titles_to_resource_name.values():
            try:
                self.service.contactGroups().delete(
                    resourceName=group_resource_name
                ).execute()
            except Exception as exception:
                self.logger.exception(
                    "Exception in delete_multiple_google_contact_groups",
                    object={"exception": exception},
                )

    def delete_multiple_google_contacts_and_groups(
        self, google_contacts_and_groups_titles_to_resource_name_dict: list[dict]
    ):
        # google_contacts_and_groups_titles_to_resource_name_dict is of the same structure
        # of create_and_push_contacts result_dicts_list
        contact_resource_names = []
        groups_titles_to_resource_name = {}
        for (
            google_contact_and_group_titles_to_resource_name_dict
        ) in google_contacts_and_groups_titles_to_resource_name_dict:
            contact_resource_names.append(
                google_contact_and_group_titles_to_resource_name_dict[
                    "contact_resource_name"
                ]
            )
            groups_titles_to_resource_name.update(
                google_contact_and_group_titles_to_resource_name_dict[
                    "groups_titles_to_resource_name"
                ]
            )
        self.delete_multiple_google_contacts(contact_resource_names)
        self.delete_multiple_google_contact_groups(groups_titles_to_resource_name)

    def update_contact_by_google_contact_dict(
        self, *, resource_name: str, google_contact_dict: dict, fields_to_update: list
    ) -> dict:
        self.logger.start(
            "update_contact_by_google_contact_dict",
            object={"resource_name": resource_name},
        )
        if not google_contact_dict:
            self.logger.end(
                "google_contact_dict is empty",
                object={"google_contact_dict": google_contact_dict},
            )
            updated_contact = {}
            return updated_contact
        update_fields = ",".join(fields_to_update)

        if not resource_name.startswith("people/"):
            resource_name = f"people/{resource_name}"

        try:
            # Retrieve the existing contact to get its etag
            existing_contact = (
                self.service.people()
                .get(
                    resourceName=resource_name,
                    personFields="names,phoneNumbers,emailAddresses,organizations,addresses,birthdays,urls,biographies,userDefined",
                )
                .execute()
            )

            # Add the etag to the google_contact_dict
            google_contact_dict["etag"] = existing_contact["etag"]

            updated_contact = (
                self.service.people()
                .updateContact(
                    resourceName=resource_name,
                    body=google_contact_dict,
                    updatePersonFields=update_fields,
                )
                .execute()
            )
            self.logger.info(
                "Contact updated successfully", object={"resource_name": resource_name}
            )
        except HttpError as exception:
            if exception.resp.status == 404:
                self.logger.error(
                    "Contact not found", object={"resource_name": resource_name}
                )
                updated_contact = {}
            else:
                self.logger.exception(
                    "HttpError in update_contact_by_google_contact_dict",
                    object={"exception": exception},
                )
                raise exception
        except Exception as exception:
            self.logger.exception(
                "Exception in update_contact_by_google_contact_dict",
                object={"exception": exception},
            )
            raise exception
        self.logger.end("update_contact_by_google_contact_dict")
        return updated_contact

    def update_google_contact_fields(
        self, *, username: str, contact_id: int, fields_to_update: list
    ) -> dict:
        self.logger.start("update_existing_contact", object={"contact_id": contact_id})
        self.initialize_service(email=username)
        result_dict = {}
        try:
            google_contact_dict = self.get_google_contact_dict_by_contact_id(
                contact_id=contact_id
            )
            resource_name = self.get_resource_name_by_contact_id(contact_id=contact_id)
            if not resource_name:
                raise Exception(f"No resource name found for contact_id: {contact_id}")
            updated_contact = self.update_contact_by_google_contact_dict(
                resource_name=resource_name,
                google_contact_dict=google_contact_dict,
                fields_to_update=fields_to_update,
            )
            resource_name = updated_contact.get("resourceName")
            final_resource_name = updated_contact.get("resourceName", resource_name)
            result_dict["contact_resource_name"] = final_resource_name
            # result_dict["contact_resource_name"] = updated_contact["resourceName"]

        except Exception as exception:
            self.logger.exception(
                "Exception in update_existing_contact", object={"exception": exception}
            )
            raise exception
        self.logger.end("update_existing_contact")
        return result_dict

    def get_resource_name_by_contact_id(self, contact_id: int) -> str:
        resource_name = self.select_one_value_by_column_and_value(
            schema_name="importer",
            view_table_name="importer_view",
            select_clause_value="google_people_api_resource_name",
            column_name="entity_id",
            column_value=contact_id,
        )
        return resource_name
