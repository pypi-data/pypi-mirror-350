from logger_local.LoggerComponentEnum import LoggerComponentEnum

ORGANIZATIONS_LOCAL_PYTHON_COMPONENT_ID = 286
ORGANIZATIONS_LOCAL_PYTHON_COMPONENT_NAME = "organization-local-python-package"
DEVELOPER_EMAIL = "tal.g@circ.zone"
ORGANIZATIONS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT = {
    'component_id': ORGANIZATIONS_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': ORGANIZATIONS_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}

ORGANIZATIONS_PYTHON_PACKAGE_TEST_LOGGER_OBJECT = {
    'component_id': ORGANIZATIONS_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': ORGANIZATIONS_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
    'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
    'developer_email': DEVELOPER_EMAIL
}
