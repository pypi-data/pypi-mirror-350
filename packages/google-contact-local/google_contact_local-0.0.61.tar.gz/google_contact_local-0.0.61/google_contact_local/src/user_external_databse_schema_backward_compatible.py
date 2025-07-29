# from data_store_local import DataStore

# Class UserExternalDatabaseSchemaBackwardCompatible:
#   def before_start():
#     smart_datastore.execute("ALTER TABLE `user_external`.`user_external_table`
# 		CHANGE COLUMN `access_token_old` `access_token` VARCHAR(255) NULL DEFAULT NULL COMMENT 'Token to access the external system (i.e. LinkedIn)\\\\\\\\ncode \\\\nShould rename to access_token_old  as moved to token__user_external' ;")  # noqa
#   def after_finish():
#     pass
