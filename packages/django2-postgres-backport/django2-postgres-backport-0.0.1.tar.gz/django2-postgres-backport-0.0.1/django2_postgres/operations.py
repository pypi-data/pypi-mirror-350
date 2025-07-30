from django.db import NotSupportedError
from django.db.migrations import AddIndex, RemoveIndex
from django.db.migrations.operations.base import Operation

import django
if django.VERSION >= (3, 0):
    from django.contrib.postgres.operations import *
else:
    class NotInTransactionMixin:
        def _ensure_not_in_transaction(self, schema_editor):
            if schema_editor.connection.in_atomic_block:
                raise NotSupportedError(
                    'The %s operation cannot be executed inside a transaction '
                    '(set atomic = False on the migration).'
                    % self.__class__.__name__
                )


    class AddIndexConcurrently(NotInTransactionMixin, AddIndex):
        """Create an index using PostgreSQL's CREATE INDEX CONCURRENTLY syntax."""
        atomic = False

        def describe(self):
            return 'Concurrently create index %s on field(s) %s of model %s' % (
                self.index.name,
                ', '.join(self.index.fields),
                self.model_name,
            )

        def database_forwards(self, app_label, schema_editor, from_state, to_state):
            self._ensure_not_in_transaction(schema_editor)
            model = to_state.apps.get_model(app_label, self.model_name)
            if self.allow_migrate_model(schema_editor.connection.alias, model):
                orig = str(self.index.create_sql(model, schema_editor))
                concurrently = orig.replace('CREATE INDEX', 'CREATE INDEX CONCURRENTLY')
                schema_editor.execute(concurrently, params=None)

        def database_backwards(self, app_label, schema_editor, from_state, to_state):
            self._ensure_not_in_transaction(schema_editor)
            model = from_state.apps.get_model(app_label, self.model_name)
            if self.allow_migrate_model(schema_editor.connection.alias, model):
                orig = str(self.index.remove_sql(model, schema_editor))
                concurrently = orig.replace('DROP INDEX', 'DROP INDEX CONCURRENTLY')
                schema_editor.execute(concurrently, params=None)


    class RemoveIndexConcurrently(NotInTransactionMixin, RemoveIndex):
        """Remove an index using PostgreSQL's DROP INDEX CONCURRENTLY syntax."""
        atomic = False

        def describe(self):
            return 'Concurrently remove index %s from %s' % (self.name, self.model_name)

        def database_forwards(self, app_label, schema_editor, from_state, to_state):
            self._ensure_not_in_transaction(schema_editor)
            model = from_state.apps.get_model(app_label, self.model_name)
            if self.allow_migrate_model(schema_editor.connection.alias, model):
                from_model_state = from_state.models[app_label, self.model_name_lower]
                index = from_model_state.get_index_by_name(self.name)
                orig = str(index.remove_sql(model, schema_editor))
                concurrently = orig.replace('DROP INDEX', 'DROP INDEX CONCURRENTLY')
                schema_editor.execute(concurrently, params=None)

        def database_backwards(self, app_label, schema_editor, from_state, to_state):
            self._ensure_not_in_transaction(schema_editor)
            model = to_state.apps.get_model(app_label, self.model_name)
            if self.allow_migrate_model(schema_editor.connection.alias, model):
                to_model_state = to_state.models[app_label, self.model_name_lower]
                index = to_model_state.get_index_by_name(self.name)
                orig = str(index.create_sql(model, schema_editor))
                concurrently = orig.replace('CREATE INDEX', 'CREATE INDEX CONCURRENTLY')
                schema_editor.execute(concurrently, params=None)
