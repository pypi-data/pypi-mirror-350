from logger_local.LoggerComponentEnum import LoggerComponentEnum


class GoogleContactConstants:
    class LoggerSetupConstants:
        GOOGLE_CONTACT_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 188
        GOOGLE_CONTACT_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = (
            "google-contact-local-python-package/google-contacts.py"
        )
        DEVELOPER_EMAIL = "tal.g@circ.zone"
        GOOGLE_CONTACT_LOCAL_CODE_LOGGER_OBJECT = {
            "component_id": GOOGLE_CONTACT_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
            "component_name": GOOGLE_CONTACT_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
            "component_category": LoggerComponentEnum.ComponentCategory.Code.value,
            "developer_email": DEVELOPER_EMAIL,
        }
        GOOGLE_CONTACT_LOCAL_PYTHON_PACKAGE_TEST_LOGGER_OBJECT = {
            "component_id": GOOGLE_CONTACT_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
            "component_name": GOOGLE_CONTACT_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
            "component_category": LoggerComponentEnum.ComponentCategory.Unit_Test.value,
            "testing_framework": LoggerComponentEnum.testingFramework.pytest.value,
            "developer_email": DEVELOPER_EMAIL,
        }

    # TODO Use Sql2Code to bring those values
    GOOGLE_SYSTEM_ID = 6
    PEOPLE_API_TYPE_ID = 16
    DATA_SOURCE_TYPE_ID = 10
    CONTACT_ENTITY_TYPE_ID = 7
