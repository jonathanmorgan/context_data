DROP TABLE context_data_datareference;
DROP TABLE context_data_datareference_related_data_sets;
DROP TABLE context_data_datareferencecontext;
DROP TABLE context_data_datareferencemention;
DROP TABLE context_data_datasetcitationdata;
DROP TABLE context_data_datasetidentifier;
DROP TABLE context_data_datasetmention;
DROP TABLE context_data_datasetnote;
DROP TABLE context_data_workdatasetcitationmention;
DROP TABLE context_data_workdatasetcitation;
DROP TABLE context_data_workdatasetmention;
DROP TABLE context_data_workresearchfield;
DROP TABLE context_data_workresearchmethod;
DROP TABLE context_data_datasetcitation;
DROP TABLE context_data_dataset;

-- remove migration log from django_migrations table so we can re-migrate.
DELETE FROM django_migrations WHERE app = 'context_data';
